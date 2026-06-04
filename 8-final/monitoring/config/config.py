from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AppSettings:
    app_name: str = "URL Monitor"
    app_version: str = "1.0.0"
    default_interval: int = 30
    data_file: Path = field(
        default_factory=lambda: Path(__file__).parent.parent / "data" / "monitors.txt"
    )

    @classmethod
    def from_defaults(cls) -> "AppSettings":
        return cls()
