from __future__ import annotations


class FfmpegError(Exception):
    def __init__(self, args_summary: str, returncode: int, tail: str) -> None:
        super().__init__(f"ffmpeg failed (rc={returncode}) for {args_summary}: {tail}")
        self.returncode = returncode
