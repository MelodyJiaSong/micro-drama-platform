from __future__ import annotations

import io
import re
import time
from pathlib import Path

from PIL import Image

from libs.infrastructure.daos.artifact__dao import ArtifactDao
from libs.infrastructure.errors.artifact__error import ArtifactTooLargeError, InvalidArtifactNameError

_SAFE_SEGMENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_\-]{0,63}$")
_QUALITIES: tuple[int, ...] = (85, 75, 65, 55, 45)
_MIN_EDGE: int = 320
PREVIEW_PREFIX: str = "preview_"


class ArtifactWriter:
    """Job artifacts under `.data/artifacts/{job_id}/` — never under `ai_videos/` (FR-45).

    Previews are re-encoded as JPEG and shrunk until they fit the byte budget (FR-32).
    """

    def __init__(self, root: Path) -> None:
        self._root = root

    def save_preview(self, job_id: str, name: str, png_bytes: bytes, max_bytes: int) -> ArtifactDao:
        target = self._job_dir(job_id) / f"{PREVIEW_PREFIX}{_segment(name)}.jpg"
        with Image.open(io.BytesIO(png_bytes)) as original:
            image = original.convert("RGB")
        while True:
            for quality in _QUALITIES:
                buffer = io.BytesIO()
                image.save(buffer, format="JPEG", quality=quality, optimize=True)
                if buffer.tell() <= max_bytes:
                    return self._write(target, buffer.getvalue(), image.size)
            if min(image.size) <= _MIN_EDGE:
                raise ArtifactTooLargeError(f"preview cannot fit {max_bytes} bytes")
            image = image.resize((int(image.width * 0.8), int(image.height * 0.8)))

    def save_failure_screenshot(self, job_id: str, name: str, png_bytes: bytes) -> ArtifactDao:
        target = self._job_dir(job_id) / f"failure_{_segment(name)}.png"
        with Image.open(io.BytesIO(png_bytes)) as image:
            size = image.size
        return self._write(target, png_bytes, size)

    def save_failure_dom(self, job_id: str, name: str, html: str) -> Path:
        target = self._job_dir(job_id) / "private" / f"dom_{_segment(name)}.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        return target

    def prune_previews(self, older_than_days: int, now_epoch_s: float | None = None) -> int:
        cutoff = (time.time() if now_epoch_s is None else now_epoch_s) - older_than_days * 86400
        removed = 0
        if not self._root.is_dir():
            return 0
        for preview in self._root.glob(f"*/{PREVIEW_PREFIX}*.jpg"):
            if preview.stat().st_mtime < cutoff:
                preview.unlink()
                removed += 1
        return removed

    def _job_dir(self, job_id: str) -> Path:
        directory = self._root / _segment(job_id)
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    def _write(self, target: Path, data: bytes, size: tuple[int, int]) -> ArtifactDao:
        temp = target.with_suffix(target.suffix + ".tmp")
        temp.write_bytes(data)
        temp.replace(target)
        return ArtifactDao(path=target, size_bytes=len(data), width=size[0], height=size[1])


def _segment(value: str) -> str:
    if not _SAFE_SEGMENT.fullmatch(value):
        raise InvalidArtifactNameError(value)
    return value
