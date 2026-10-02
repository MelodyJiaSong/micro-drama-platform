"""The routing key a scenes-tree entry carries (follow-up 173).

One grammar, read by the tree labels and by the downloads import, so the key
the sidebar shows is the key a download is routed by:

| name                          | key           | what it is                      |
|-------------------------------|---------------|---------------------------------|
| `bg4_闪金镇`                   | `bg4`         | scene subject (anchor `{dir}.png`) |
| `bg1-1_谷心_北望修道院`         | `bg1-1`       | view of subject 1               |

Objects are not scene keys: every object is a prop (`libs.common.prop_key`,
follow-up 174), and a scene only links to it.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_KEY = r"bg(\d+)(?:-(\d+))?"
_LEADING_RE = re.compile(rf"^({_KEY})_(.+)$")
# Anywhere in a download stem: generators wrap the prompt head in their own
# prefix (`ElevenLabs_image_gpt-image-2_bg1-1_…`), so a key is matched at an
# ASCII-alphanumeric boundary rather than at position 0.
_ANYWHERE_RE = re.compile(rf"(?<![A-Za-z0-9]){_KEY}(?![A-Za-z0-9-])")


@dataclass(frozen=True)
class SceneKey:
    subject: int
    view: int | None
    text: str           # the key exactly as it appeared (`bg1-1`)
    rest: str           # what follows the key in the stem, `_` stripped
    start: int          # where the key starts in the searched text


def _build(subject: str, view: str | None, text: str, rest: str, start: int) -> SceneKey:
    return SceneKey(
        subject=int(subject),
        view=int(view) if view is not None else None,
        text=text,
        rest=rest,
        start=start,
    )


def split_name(name: str) -> tuple[str, str] | None:
    """`("bg1-1", "谷心_北望修道院")` out of `bg1-1_谷心_北望修道院`, or None when
    the name does not open with a key followed by `_`."""
    m = _LEADING_RE.match(name)
    return (m.group(1), m.group(4)) if m else None


def label(name: str) -> str | None:
    """The sidebar label `{key} {rest}` for a keyed name, else None."""
    parts = split_name(name)
    return f"{parts[0]} {parts[1]}" if parts else None


def prefixed(key: str, text: str) -> str:
    return f"{key} {text}"


def parse_name(name: str) -> SceneKey | None:
    """The key a folder / file name opens with (`bg1-1_谷心_北望修道院`)."""
    m = _LEADING_RE.match(name)
    if m is None:
        return None
    return _build(m.group(2), m.group(3), m.group(1), m.group(4), 0)


def first_key(stem: str) -> SceneKey | None:
    """The LEFTMOST scene key in a download stem.

    Leftmost is correct by construction: the routing key is the prompt's first
    line, so it precedes anything the generator inlined from the `参考:` line
    below it (`bg2-1_主街正向 参考 bg1-1_广场正向.png` is view bg2-1)."""
    m = _ANYWHERE_RE.search(stem)
    if m is None:
        return None
    return _build(m.group(1), m.group(2), m.group(0), stem[m.end():].lstrip("_"), m.start())


__all__ = [
    "SceneKey",
    "first_key",
    "label",
    "parse_name",
    "prefixed",
    "split_name",
]
