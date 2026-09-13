"""The `{prefix}{N}-{M}` routing key of a reference-image asset.

`ai_video.md` rule 4b-A / CLAUDE.md § 参考图资产的命名与路由 give every
pasteable image prompt a **routing key** as its first characters —
`bg1-2`, `p3-1`, `c2-1` — precisely because the out-of-image tool names the
download after the prompt's opening text and mangles everything around it:

    prompt first line : p3-2_黏土壁炉锚点
    download          : ElevenLabs_image_gpt-image-2_p3-2_黏土壁炉锚点 一座手_2026-09-13T07_26_16.png
                                                    ^^^^

The key is short, pure ASCII+digits, and survives that mangling — so the
**only** reliable way to name an imported asset is to find the key *anywhere*
in the stem and use it alone. Matching on "does the stem start with a folder
token" fails the moment the generator prepends its own name, and collapsing to
`{folder}{N}` loses the view identity outright (the numbering is
order-dependent, so which view is which changes on every import).

Scene subjects already worked this way (`bg(\\d+)-(\\d+)` searched anywhere);
props and characters did not, so `p3-1` and `p3-2` both landed on
`p3_抹泥板与黏土壁炉.png` and silently overwrote each other. This module is
that logic, shared by `DownloadsImporter` (naming on import) and
`MediaRenamer` (the normalise-names pass) so the two ends cannot drift.

The expected prefix is taken from the **asset folder's own name**, never
guessed from the filename — that makes false positives impossible
(`gpt-image-2` cannot be mistaken for a key when the folder says `p3`).
"""
from __future__ import annotations

import re

# `p3_抹泥板与黏土壁炉` -> `p3`; `bg10_崖下砾石滩` -> `bg10`; `c1_砌炉的老人` -> `c1`.
# A bare `p3` (no trailing `_名字`) is accepted too.
_FOLDER_KEY_RE = re.compile(r"^((?:bg|[cp])\d+)(?:_|$)", re.IGNORECASE)


def folder_key(folder_name: str) -> str | None:
    """The routing prefix an asset folder owns (`p3`), or None if it owns none.

    None for scene roots (`caoya`), prop view folders (`v1_车外全景`), scene
    plates (`bg1_朝北_城门` — that is a single-image folder keyed by its own
    name, not by `{N}-{M}`) and anything else outside the convention.
    """
    m = _FOLDER_KEY_RE.match(folder_name.strip())
    if m is None:
        return None
    # `bg1_朝北_城门` matches `bg1` too, but a plate folder is single-image and
    # must keep the rename-to-folder-name contract — its own name IS the key.
    # Plates have a 方位 segment after the number; subjects do not.
    if folder_name.lower().startswith("bg") and folder_name.count("_") >= 2:
        return None
    return m.group(1)


def view_key_in(stem: str, folder_name: str) -> str | None:
    """`p3-2` out of a mangled download stem, or None when the stem carries no
    key for this folder.

    Looks for `{folder's prefix}-{digits}` anywhere in `stem`, requiring a
    non-alphanumeric boundary in front so `sdxl-p2-1` style noise inside a
    model name cannot masquerade as a key. Returns the canonical lowercase
    key (`p3-2`) — the filename is the key and nothing else; the Chinese view
    name stays in the card (same contract as scene subjects).
    """
    prefix = folder_key(folder_name)
    if prefix is None:
        return None
    hit = re.search(
        rf"(?<![A-Za-z0-9]){re.escape(prefix)}-(\d+)", stem, re.IGNORECASE
    )
    return f"{prefix.lower()}-{hit.group(1)}" if hit else None
