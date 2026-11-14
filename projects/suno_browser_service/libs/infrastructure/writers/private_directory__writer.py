import csv
import io
import os
import re
import subprocess
from pathlib import Path

from projects.suno_browser_service.libs.common.errors import ServiceError


class PrivateDirectoryWriter:
    @staticmethod
    def ensure(path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)
        if os.name != "nt":
            path.chmod(0o700)
            return
        result = subprocess.run(["whoami", "/user", "/fo", "csv", "/nh"], capture_output=True, text=True, check=True)
        row = next(csv.reader(io.StringIO(result.stdout.strip())))
        sid = row[-1]
        if not re.fullmatch(r"S-1-[0-9-]+", sid):
            raise ServiceError("private_directory", "无法确定当前用户 SID；停止写入登录凭据")
        result = subprocess.run(
            ["icacls", str(path), "/inheritance:r", "/grant:r", f"*{sid}:(OI)(CI)F", "*S-1-5-18:(OI)(CI)F",
             "*S-1-5-32-544:(OI)(CI)F", "/remove:g", "*S-1-1-0", "*S-1-5-11", "*S-1-5-32-545"],
            capture_output=True, text=True)
        if result.returncode:
            raise ServiceError("private_directory", "无法限制服务数据目录的 Windows ACL；停止写入登录凭据")
