"""The `{L}{N}` / `{L}{N}-{M}` routing-key grammar, one letter per asset kind.

Props (`p`, follow-up 174) and equipment (`e`) name their folders and view files
with the same grammar and find it in a download stem under the same boundary
rules, so both are built here from their letter (`prop_key`, `equipment_key`):

| name                  | key         | what it is                   |
|-----------------------|-------------|------------------------------|
| `{L}{N}_{rest}`        | `{L}{N}`     | the asset folder / its card  |
| `{L}{N}-{M}_{view}.png` | `{L}{N}-{M}` | view M of that asset         |
"""
from __future__ import annotations

import re
from dataclasses import dataclass

# `{key}-{i}` of an asset is its i-th view. The card's own ```text first line is
# the authority for the view name; this is the convention the asset generators
# write, and the fallback when a card does not list the view.
VIEW_NAMES: dict[int, str] = {1: "正面", 2: "侧面", 3: "背面"}


@dataclass(frozen=True)
class NumberedKey:
    number: int
    view: int | None
    base: str    # the asset part as written (`p15`, `e12`)
    text: str    # the whole key as written (`p15-1`)
    rest: str    # what follows the key in the stem, `_` stripped
    start: int   # where the key starts in the searched text


class KeyGrammar:
    def __init__(self, letter: str) -> None:
        key = rf"(?P<key>{re.escape(letter)}(?P<n>\d+)(?:-(?P<v>\d+))?)"
        self._letter = letter
        self._leading = re.compile(rf"^{key}_(?P<rest>.+)$")
        # Anywhere in a download stem, at an ASCII-alphanumeric boundary:
        # generators wrap the prompt head in their own prefix
        # (`ElevenLabs_image_gpt-image-2_p15-1_…`), and `mp4` / `_pbr` / `ep01`
        # must not read as a key. A trailing `-{digit}` is refused so a cut-off
        # view number never passes for the bare key.
        self._anywhere = re.compile(rf"(?<![A-Za-z0-9]){key}(?![A-Za-z0-9]|-\d)")

    def _build(self, m: re.Match[str], rest: str) -> NumberedKey:
        number, view = m.group("n"), m.group("v")
        return NumberedKey(
            number=int(number),
            view=int(view) if view is not None else None,
            base=f"{self._letter}{number}",
            text=m.group("key"),
            rest=rest,
            start=m.start(),
        )

    def split_name(self, name: str) -> tuple[str, str] | None:
        """`("p15-1", "正面.png")` out of `p15-1_正面.png`, or None when the name
        does not open with a key followed by `_`."""
        m = self._leading.match(name)
        return (m.group("key"), m.group("rest")) if m else None

    def label(self, name: str) -> str | None:
        """The sidebar label `{key} {rest}` for a keyed name, else None."""
        parts = self.split_name(name)
        return f"{parts[0]} {parts[1]}" if parts else None

    def parse_name(self, name: str) -> NumberedKey | None:
        """The key a folder / file name opens with (`p15_两层石木旅店`)."""
        m = self._leading.match(name)
        return self._build(m, m.group("rest")) if m else None

    def first_key(self, stem: str) -> NumberedKey | None:
        """The LEFTMOST key in a download stem — the prompt's first line, so it
        precedes anything inlined from the `参考:` line below it
        (`p15-2_侧面 参考 p15-1_正面.png` is view 2)."""
        m = self._anywhere.search(stem)
        return self._build(m, stem[m.end():].lstrip("_")) if m else None


__all__ = ["VIEW_NAMES", "KeyGrammar", "NumberedKey"]
