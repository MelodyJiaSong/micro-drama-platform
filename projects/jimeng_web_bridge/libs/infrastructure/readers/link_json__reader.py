from __future__ import annotations

import json
import os

from libs.common import drama_ref
from libs.common.paths import AI_VIDEOS_DIR_NAME, RepoSandbox
from libs.infrastructure.daos.drama_tree__dao import LinkTargetDao
from libs.infrastructure.errors.sandbox__error import LinkRejectedError

LINK_SUFFIX: str = ".link.json"
MAX_LINK_BYTES: int = 64 * 1024
IMAGE_EXTS: tuple[str, ...] = (".png", ".jpg", ".jpeg", ".webp")
VIDEO_EXTS: tuple[str, ...] = (".mp4", ".mov")
AUDIO_EXTS: tuple[str, ...] = (".mp3", ".wav", ".m4a")
_MEDIA_CLASSES: tuple[tuple[str, ...], ...] = (IMAGE_EXTS, VIDEO_EXTS, AUDIO_EXTS)


class LinkJsonReader:
    """Resolves a cross-episode `*.link.json` one hop.

    Rejected: chains, escapes, reparse points, targets inside a hard-excluded folder (any case), and a
    target whose media class differs from the link's own inner suffix, so a `.png.link.json` can never
    surface a config file, an md file, a render, a candidate or an archived file as a reference.
    """

    def __init__(self, sandbox: RepoSandbox) -> None:
        self._sandbox: RepoSandbox = sandbox

    def read(self, link_rel: str) -> LinkTargetDao:
        link = self._sandbox.check_read(link_rel)
        if link.path is None or link.rel is None or not link.rel.endswith(LINK_SUFFIX):
            raise LinkRejectedError(link.violation or "not_a_link", link.rel)
        try:
            if not link.path.is_file():
                raise LinkRejectedError("not_a_file", link.rel)
            if link.path.stat().st_size > MAX_LINK_BYTES:
                raise LinkRejectedError("too_large", link.rel)
            data = json.loads(link.path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError) as error:
            raise LinkRejectedError("malformed", link.rel) from error
        target = data.get("target") if isinstance(data, dict) else None
        if not isinstance(target, str) or not target:
            raise LinkRejectedError("malformed", link.rel)
        normalized = target.replace("\\", "/")
        if normalized.split("/", 1)[0] != AI_VIDEOS_DIR_NAME:
            raise LinkRejectedError("outside_ai_videos", link.rel)
        if normalized.casefold().endswith(LINK_SUFFIX):
            raise LinkRejectedError("chained_link", link.rel)
        resolved = self._sandbox.check_read(normalized)
        if resolved.path is None or resolved.rel is None:
            raise LinkRejectedError(resolved.violation or "rejected", link.rel)
        # Resolution expands case variants and 8.3 short names (`C1-2PN~1.JSO`), so re-check the real name.
        if resolved.rel.casefold().endswith(LINK_SUFFIX) or resolved.path.name.casefold().endswith(LINK_SUFFIX):
            raise LinkRejectedError("chained_link", link.rel)
        if drama_ref.inside_hard_excluded(resolved.rel):
            raise LinkRejectedError("target_excluded", link.rel)
        if not resolved.path.is_file():
            raise LinkRejectedError("target_missing", link.rel)
        expected = media_class(link.rel[: -len(LINK_SUFFIX)])
        if expected is None or media_class(resolved.rel) != expected:
            raise LinkRejectedError("target_type_mismatch", link.rel)
        note = data.get("note")
        return LinkTargetDao(
            link_rel=link.rel,
            target_rel=resolved.rel,
            note=note if isinstance(note, str) and note else None,
        )


def media_class(name: str) -> tuple[str, ...] | None:
    ext = os.path.splitext(name)[1].casefold()
    return next((extensions for extensions in _MEDIA_CLASSES if ext in extensions), None)
