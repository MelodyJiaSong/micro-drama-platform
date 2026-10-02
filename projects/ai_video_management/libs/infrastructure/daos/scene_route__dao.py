"""Where a scene-keyed download lands (follow-up 173)."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

KIND_SUBJECT: str = "scene_subject"          # `bg{N}_{主体}/` — anchor or bare-key view
KIND_VIEW: str = "scene_view"                # `bg{N}_{主体}/bg{N}-{M}_{…}/`


@dataclass(frozen=True)
class SceneRouteDao:
    folder: Path
    kind: str
    name: str   # destination file name, extension included
