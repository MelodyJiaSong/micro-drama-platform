"""The name a keyed view download lands as, read off its asset's card.

A keyed asset — a prop `props/p{N}_{名}/`, an equipment item
`equipment/…/e{N}_{品质}_{名}/` — keeps one card `{folder}/{folder}.md` whose
```text blocks are its image prompts, each opening with its routing key
(`p15-1_正面`, `e12-2_侧面`). The generator names the download after that first
line, so it is also the name the imported view keeps: the card is the
authority, `key_grammar.VIEW_NAMES` the convention when the card is silent.
"""
from __future__ import annotations

import re
from pathlib import Path

from libs.common.key_grammar import VIEW_NAMES

VIEW_IMAGE_EXTS: frozenset[str] = frozenset({".png", ".webp", ".jpg", ".jpeg"})
_TEXT_FENCE_RE = re.compile(r"```text\n(.*?)\n```", re.S)
_UNSAFE_NAME_RE = re.compile(r"[\x00-\x1f/\\:*?\"<>|]")


def view_stem(folder: Path, own: str, view: int) -> str:
    """The first line of the card's ```text block for view `view` of the asset
    keyed `own` (`p15-1_正面`) — also the prompt's first line — else the asset
    generator's convention."""
    prefix = f"{own}-{view}_"
    try:
        text = (folder / f"{folder.name}.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError):
        text = ""
    for block in _TEXT_FENCE_RE.findall(text):
        first = block.split("\n", 1)[0].strip()
        if first.startswith(prefix) and len(first) > len(prefix) and not _UNSAFE_NAME_RE.search(first):
            return first
    name = VIEW_NAMES.get(view)
    return f"{prefix}{name}" if name else f"{own}-{view}"


__all__ = ["VIEW_IMAGE_EXTS", "view_stem"]
