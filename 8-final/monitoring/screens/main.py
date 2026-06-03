from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Label
from textual.containers import Vertical

from widgets import UrlFormWidget

SAMPLE_DATA = [
    ("https://example.com", "30", "OK", "200", "12:00:00"),
    ("https://google.com", "10", "OK", "200", "12:00:05"),
    ("https://broken-site.io", "60", "ERROR", "503", "11:59:41"),
]


class MainScreen(Screen):
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

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield UrlFormWidget()
        yield Label("", id="status-label")
        with Vertical(id="table-container"):
            yield DataTable(id="monitors-table", cursor_type="row")
        yield Footer()

    def on_mount(self) -> None:
        self._setup_table()
        self.query_one(DataTable).focus()

    def _setup_table(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("URL", "Interval (s)", "Status", "HTTP", "Last Checked")
        for row in SAMPLE_DATA:
            table.add_row(*row)
