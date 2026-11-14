import os
from pathlib import Path
from typing import BinaryIO

from projects.suno_browser_service.libs.common.errors import ServiceError


class LockClient:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.handle: BinaryIO | None = None

    def acquire(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = self.path.open("a+b")
        self.handle.write(b"0")
        self.handle.flush()
        self.handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            self.handle.close()
            self.handle = None
            raise ServiceError("browser_busy", "本服务或登录窗口正在使用浏览器配置") from exc

    def release(self) -> None:
        if self.handle is not None:
            self.handle.close()
            self.handle = None
