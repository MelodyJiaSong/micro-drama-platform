"""Cross-episode asset shortcuts — `*.link.json`.

A series reuses assets across episodes: `hy2` shoots with the same character
entity, the same knife and the same kit as `hy1`. Copying the bytes would
violate the repo's single-source rule (`ai_video.md` rule 4i ①: 一份东西只有一个
出处，副本必漂), and an OS symlink is invisible to the webapp on purpose — every
reader skips symlinks as a traversal guard.

So a reuse is recorded as a tiny tracked JSON sidecar next to where the asset
*would* have lived:

    ai_videos/{series}/hy2/2_世界观人设/props/p1_砍刀/p1_砍刀.png.link.json
    {"target": "ai_videos/{series}/hy1/2_世界观人设/props/p1_砍刀/p1_砍刀.png",
     "note": "跨片复用 · 同一把刀，不重出图"}

The tree reader renders that as a leaf sitting in hy2's folder whose `path` is
the **target**, so `/api/media` serves it and preview works with no media-layer
change at all; the node just carries `is_link` so the UI can mark it.

Only the manifest is tracked — the bytes stay in exactly one episode.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

LINK_SUFFIX: str = ".link.json"
AI_VIDEOS_DIR_NAME: str = "ai_videos"


@dataclass(frozen=True)
class AssetLink:
    """A resolved shortcut. `target_rel` is repo-relative and known to exist."""
    target_rel: str
    display_name: str
    note: str | None


def is_link_file(path: Path) -> bool:
    return path.name.endswith(LINK_SUFFIX)


def read(root: Path, link_file: Path) -> AssetLink | None:
    """Resolve a `*.link.json`, or None when it is malformed, escapes the
    `ai_videos/` sandbox, or points at something that is not a real file.

    Never raises: a broken link is simply not rendered, the same way a missing
    file is. Callers show the raw json instead so the user can see and fix it.
    """
    try:
        data = json.loads(link_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    target = data.get("target")
    if not isinstance(target, str) or not target:
        return None

    normalized = target.replace("\\", "/").strip("/")
    parts = normalized.split("/")
    if parts[0] != AI_VIDEOS_DIR_NAME or any(p in ("", ".", "..") for p in parts):
        return None

    resolved = (root / normalized).resolve(strict=False)
    root_resolved = root.resolve(strict=False)
    if root_resolved not in resolved.parents:
        return None
    if resolved.is_symlink() or not resolved.is_file():
        return None

    note = data.get("note")
    return AssetLink(
        target_rel=normalized,
        display_name=parts[-1],
        note=note if isinstance(note, str) and note else None,
    )
