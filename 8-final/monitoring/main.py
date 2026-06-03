from app import MonitorApp
from config.config import AppSettings


def run():
    settings = AppSettings.from_defaults()
    MonitorApp(settings).run()


if __name__ == "__main__":
    run()
