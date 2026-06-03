from textual.app import ComposeResult
from textual.widgets import Button, Input
from textual.widget import Widget


class UrlFormWidget(Widget):
    DEFAULT_CSS = """
    UrlFormWidget {
        height: auto;
        padding: 1 2;
        layout: horizontal;
        background: #161b22;
        border: solid #21262d;
        margin: 1 2 0 2;
    }

    UrlFormWidget #url-input {
        width: 1fr;
        background: #0d1117;
        border: tall #30363d;
        color: #e6edf3;
        padding: 0 1;
    }

    UrlFormWidget #url-input:focus {
        border: tall #58a6ff;
    }

    UrlFormWidget #interval-input {
        width: 16;
        margin: 0 1;
        background: #0d1117;
        border: tall #30363d;
        color: #e6edf3;
        padding: 0 1;
    }

    UrlFormWidget #interval-input:focus {
        border: tall #58a6ff;
    }

    UrlFormWidget #add-button {
        width: 12;
        background: #238636;
        color: #ffffff;
        border: none;
        height: 3;
    }

    UrlFormWidget #add-button:hover {
        background: #2ea043;
    }

    UrlFormWidget #add-button:focus {
        background: #2ea043;
        border: none;
    }
    """

    def compose(self) -> ComposeResult:
        yield Input(placeholder="https://example.com", id="url-input")
        yield Input(placeholder="Interval (s)", id="interval-input")
        yield Button("Add", id="add-button", variant="success")
