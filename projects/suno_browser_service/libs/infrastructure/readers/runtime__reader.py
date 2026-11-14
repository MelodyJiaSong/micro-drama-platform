from pathlib import Path

from projects.suno_browser_service.libs.common.settings import AUTOMATION_PAUSE_FILENAME


class RuntimeReader:
    def __init__(self, directory: Path) -> None:
        self.directory = directory

    def shutdown_requested(self) -> bool:
        return (self.directory / "shutdown.request").exists()

    def automation_paused(self) -> bool:
        return (self.directory / AUTOMATION_PAUSE_FILENAME).exists()
