from __future__ import annotations

import re
from pathlib import Path

from libs.application.dtos.artifact__dto import ArtifactQdto
from libs.common.paths import is_reparse_point, is_within
from libs.infrastructure.errors.artifact__error import InvalidArtifactNameError

_JOB_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_\-]{0,63}")
_SCREENSHOT = re.compile(r"(?:preview_[A-Za-z0-9][A-Za-z0-9_\-]{0,63}\.jpg|failure_[A-Za-z0-9][A-Za-z0-9_\-]{0,63}\.png)")
_CONTENT_TYPES: dict[str, str] = {".jpg": "image/jpeg", ".png": "image/png"}


class ArtifactQuery:
    """FR-36: only screenshots are reachable. DOM snapshots and traces live under `private/` and never match."""

    def __init__(self, artifacts_dir: Path) -> None:
        self._root = artifacts_dir

    def get_screenshot(self, job_id: str, name: str) -> ArtifactQdto:
        if _JOB_ID.fullmatch(job_id) is None:
            raise InvalidArtifactNameError("job id rejected")
        if _SCREENSHOT.fullmatch(name) is None:
            raise InvalidArtifactNameError("screenshot name rejected")
        job_dir = self._root / job_id
        target = job_dir / name
        if any(is_reparse_point(path) for path in (self._root, job_dir, target)):
            raise InvalidArtifactNameError("reparse point rejected")
        if not target.is_file() or not is_within(target.resolve(), job_dir.resolve()):
            raise FileNotFoundError(f"{job_id}/{name}")
        return ArtifactQdto(file_path=target, content_type=_CONTENT_TYPES[target.suffix])
