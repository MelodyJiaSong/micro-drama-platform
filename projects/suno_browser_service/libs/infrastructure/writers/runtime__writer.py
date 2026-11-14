import json
import os
from pathlib import Path
from datetime import datetime, timezone

from projects.suno_browser_service.libs.common.settings import AUTOMATION_PAUSE_FILENAME


class RuntimeWriter:
    def __init__(self, directory: Path) -> None:
        self.directory = directory

    def begin(self, port: int) -> None:
        (self.directory / "shutdown.request").unlink(missing_ok=True)
        record = self.directory / "server.json"
        temporary = record.with_suffix(".json.tmp")
        temporary.write_text(json.dumps({"pid": os.getpid(), "port": port}), encoding="utf-8")
        os.replace(temporary, record)

    def pause_automation(self, job_id: str, reason: str) -> None:
        path = self.directory / AUTOMATION_PAUSE_FILENAME
        path.write_text(json.dumps({"job_id": job_id, "reason": reason,
                                    "at": datetime.now(timezone.utc).isoformat()}), encoding="utf-8")

    def clear_automation_pause(self) -> None:
        (self.directory / AUTOMATION_PAUSE_FILENAME).unlink(missing_ok=True)
