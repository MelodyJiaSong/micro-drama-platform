"""Route a download by the scene routing key it carries (follow-up 173).

The key the sidebar shows (`libs.common.scene_key`) is the key a download is
routed by, at any depth of the scenes tree:

| leftmost key in the name | lands in                                   | as                  |
|--------------------------|--------------------------------------------|---------------------|
| `bg{N}_{主体}`            | subject `bg{N}_{主体}/`                     | `{subject dir}.png` |
| `bg{N}-{M}`              | view dir `bg{N}_…/bg{N}-{M}_…/` if present | `{view dir}.png`    |
|                          | else the subject dir                       | `bg{N}-{M}.png`     |

Objects are not routed here: every object is a prop and a scene only links to
it (`prop_route__reader`, follow-up 174) — so a model file never takes a scene
route. Every lookup refuses to guess: a number owned by two folders routes nowhere.
"""
from __future__ import annotations

from pathlib import Path

from libs.common import scene_key, series_shared
from libs.common.scene_key import SceneKey
from libs.infrastructure.daos.scene_route__dao import KIND_SUBJECT, KIND_VIEW, SceneRouteDao
from libs.infrastructure.readers.prop_route__reader import MODEL_EXTS


class SceneKeyRouter:
    def route(self, filename: str, drama_dir: Path) -> SceneRouteDao | None:
        src = Path(filename)
        ext = src.suffix.lower()
        key = scene_key.first_key(src.stem)
        if key is None or ext in MODEL_EXTS:
            return None
        subject = self.subject(key.subject, drama_dir)
        if subject is None:
            return None
        if key.view is not None:
            view = self._view_dir(subject, key)
            if view is not None:
                return SceneRouteDao(view, KIND_VIEW, f"{view.name}{ext}")
            return SceneRouteDao(subject, KIND_SUBJECT, f"{key.text}{ext}")
        own = scene_key.parse_name(subject.name)
        if own is not None and _names_subject(key.rest, own.rest):
            return SceneRouteDao(subject, KIND_SUBJECT, f"{subject.name}{ext}")
        return None

    @staticmethod
    def subject(number: int, drama_dir: Path) -> Path | None:
        """The one subject folder numbered `number`, or None when none / several."""
        hits = [
            d for d in series_shared.scene_subject_dirs(drama_dir)
            if (k := scene_key.parse_name(d.name)) is not None and k.subject == number
        ]
        return hits[0] if len({p.resolve() for p in hits}) == 1 else None

    @staticmethod
    def _view_dir(subject: Path, key: SceneKey) -> Path | None:
        hits = [
            d for d in series_shared.child_dirs(subject)
            if (k := scene_key.parse_name(d.name)) is not None
            and k.subject == key.subject and k.view == key.view
        ]
        return hits[0] if len(hits) == 1 else None


def _names_subject(rest: str, subject_name: str) -> bool:
    """Does the text after `bg{N}_` in a download name name this subject?

    An anchor prompt's first line is the subject folder name (`bg4_闪金镇`); the
    generator may truncate it (`bg172_艾尔文森`) or run text on after it. A bare
    `bg{N}_` is not enough — legacy plate ids reuse small numbers per scene."""
    token = rest.split()[0] if rest.split() else ""
    if not token or not subject_name:
        return False
    return token.startswith(subject_name) or (len(token) >= 2 and subject_name.startswith(token))


__all__ = ["SceneKeyRouter"]
