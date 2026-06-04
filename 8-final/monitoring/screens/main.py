from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import httpx
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Button, DataTable, Footer, Header, Input, Label
from textual.containers import Vertical

from widgets import UrlFormWidget


@dataclass
class MonitorEntry:
    url: str
    interval: int
    timer: Optional[Timer] = field(default=None, repr=False)


class MainScreen(Screen):
    BINDINGS = [Binding("d", "delete_row", "Delete")]

    DEFAULT_CSS = """
    Screen {
        background: #0d1117;
    }

    Header {
        background: #161b22;
        color: #58a6ff;
        border-bottom: solid #21262d;
    }

    Footer {
        background: #161b22;
        color: #8b949e;
        border-top: solid #21262d;
    }

    #status-label {
        margin: 0 2;
        padding: 0 1;
        height: 1;
        color: #3fb950;
    }

    #status-label.error {
        color: #f85149;
    }

    #table-container {
        margin: 0 2 1 2;
        padding: 1;
        background: #161b22;
        border: solid #21262d;
        height: 1fr;
    }

    DataTable {
        background: #161b22;
        color: #e6edf3;
    }

    DataTable > .datatable--header {
        background: #21262d;
        color: #8b949e;
        text-style: bold;
    }

    DataTable > .datatable--cursor {
        background: #1f4068;
        color: #e6edf3;
    }

    DataTable > .datatable--hover {
        background: #1c2128;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self._monitors: dict[str, MonitorEntry] = {}

    @property
    def _data_file(self) -> Path:
        return self.app.settings.data_file

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield UrlFormWidget()
        yield Label("", id="status-label")
        with Vertical(id="table-container"):
            yield DataTable(id="monitors-table", cursor_type="row")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_column("URL", key="url")
        table.add_column("Interval (s)", key="interval")
        table.add_column("Status", key="status")
        table.add_column("HTTP", key="http")
        table.add_column("Last Checked", key="last_checked")
        table.focus()
        self._load_from_file()

    # ── persistence ──────────────────────────────────────────────────────

    def _load_from_file(self) -> None:
        if not self._data_file.exists():
            return
        for line in self._data_file.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t", 1)
            if len(parts) != 2:
                continue
            url, interval_str = parts
            try:
                self._add_monitor(url, int(interval_str))
            except ValueError:
                pass

    def _save_to_file(self) -> None:
        self._data_file.parent.mkdir(parents=True, exist_ok=True)
        lines = [f"{e.url}\t{e.interval}" for e in self._monitors.values()]
        self._data_file.write_text("\n".join(lines) + ("\n" if lines else ""))

    # ── monitor management ───────────────────────────────────────────────

    def _add_monitor(self, url: str, interval: int) -> None:
        table = self.query_one(DataTable)
        table.add_row(url, str(interval), "Pending", "-", "-", key=url)

        timer = self.set_interval(interval, self._make_checker(url))
        self._monitors[url] = MonitorEntry(url=url, interval=interval, timer=timer)

        # Immediate first check
        self.set_timer(0.3, self._make_checker(url))

    def _make_checker(self, url: str):
        async def checker() -> None:
            await self._check_url(url)
        return checker

    async def _check_url(self, url: str) -> None:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0, follow_redirects=True)
            status = "OK" if response.status_code < 400 else "ERROR"
            http_code = str(response.status_code)
        except Exception:
            status = "ERROR"
            http_code = "---"

        last_checked = datetime.now().strftime("%H:%M:%S")
        table = self.query_one(DataTable)
        table.update_cell(url, "status", status)
        table.update_cell(url, "http", http_code)
        table.update_cell(url, "last_checked", last_checked)

    # ── event handlers ───────────────────────────────────────────────────

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "add-button":
            return

        url_input = self.query_one("#url-input", Input)
        interval_input = self.query_one("#interval-input", Input)

        url = url_input.value.strip()
        interval_str = interval_input.value.strip()

        if not url:
            self._set_status("URL is required.", error=True)
            return

        if not url.startswith(("http://", "https://")):
            self._set_status("URL must start with http:// or https://", error=True)
            return

        try:
            interval = int(interval_str) if interval_str else self.app.settings.default_interval
            if interval <= 0:
                raise ValueError
        except ValueError:
            self._set_status("Interval must be a positive integer.", error=True)
            return

        if url in self._monitors:
            self._set_status(f"Already monitoring {url}.", error=True)
            return

        self._add_monitor(url, interval)
        self._save_to_file()
        url_input.clear()
        interval_input.clear()
        self._set_status(f"Added monitor for {url}.")
        self.query_one(DataTable).focus()

    def action_delete_row(self) -> None:
        table = self.query_one(DataTable)
        if not self._monitors or table.cursor_row < 0:
            return

        url_list = list(self._monitors.keys())
        if table.cursor_row >= len(url_list):
            return

        url = url_list[table.cursor_row]
        entry = self._monitors.pop(url)
        if entry.timer:
            entry.timer.stop()

        table.remove_row(url)
        self._save_to_file()
        self._set_status(f"Removed monitor for {url}.")

    def _set_status(self, message: str, error: bool = False) -> None:
        label = self.query_one("#status-label", Label)
        label.update(message)
        if error:
            label.add_class("error")
        else:
            label.remove_class("error")
