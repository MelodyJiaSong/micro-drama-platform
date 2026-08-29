from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

_BODY_RE = re.compile(r"## 视频 prompt\n\n```text\n(.*?)\n```", re.DOTALL)


@dataclass(frozen=True)
class ShotMdDao:
    shot: int
    duration_s: float
    link: str
    tail_locked: bool
    body: str
    body_sha256: str


class ShotMdReader:
    @staticmethod
    def parse(md: str) -> ShotMdDao:
        def _grab(key: str) -> str:
            m = re.search(rf"^{key}: (.+)$", md, re.MULTILINE)
            return m.group(1).strip() if m else ""

        body = _BODY_RE.search(md).group(1)
        # hash covers body AND the generation-relevant envelope fields, so re-timing
        # or re-linking a shot also invalidates stale done-segments state
        fingerprint = f"{body}\n@{_grab('duration_s')}|{_grab('link')}|{_grab('tail_locked')}"
        return ShotMdDao(
            shot=int(_grab("shot")),
            duration_s=float(_grab("duration_s")),
            link=_grab("link"),
            tail_locked=_grab("tail_locked") == "true",
            body=body,
            body_sha256=hashlib.sha256(fingerprint.encode("utf-8")).hexdigest(),
        )
