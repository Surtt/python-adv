from dataclasses import dataclass


@dataclass
class AppSettings:
    app_name: str = "URL Monitor"
    app_version: str = "1.0.0"
    default_interval: int = 30

    @classmethod
    def from_defaults(cls) -> "AppSettings":
        return cls()
