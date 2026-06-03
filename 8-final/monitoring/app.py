from textual.app import App
from textual.binding import Binding

from config.config import AppSettings
from screens import MainScreen


class MonitorApp(App):
    TITLE = "URL Monitor"
    SUB_TITLE = "v1.0.0"
    BINDINGS = [Binding("q", "quit", "Quit", priority=True)]

    def __init__(self, settings: AppSettings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settings

    def on_mount(self) -> None:
        self.push_screen(MainScreen())
