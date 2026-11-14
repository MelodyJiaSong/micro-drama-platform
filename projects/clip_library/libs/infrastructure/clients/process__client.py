from collections import deque
from pathlib import Path
import subprocess
from typing import Callable

from libs.infrastructure.errors.library__error import ToolFailedError

_TAIL_LINES = 8


class ProcessClient:
    def capture(self, tool: str, arguments: list[str], cwd: Path | None = None) -> str:
        result = subprocess.run(arguments, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                                errors="replace", stdin=subprocess.DEVNULL)
        if result.returncode != 0:
            tail = "\n".join(result.stderr.strip().splitlines()[-_TAIL_LINES:])
            raise ToolFailedError(tool, result.returncode, tail)
        return result.stdout

    def stream(self, tool: str, arguments: list[str], notify: Callable[[str], None]) -> None:
        tail: deque[str] = deque(maxlen=_TAIL_LINES)
        with subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              stdin=subprocess.DEVNULL, text=True, encoding="utf-8",
                              errors="replace") as process:
            assert process.stdout is not None
            for line in process.stdout:
                line = line.rstrip("\r\n")
                tail.append(line)
                notify(line)
        if process.returncode != 0:
            raise ToolFailedError(tool, process.returncode, "\n".join(tail))
