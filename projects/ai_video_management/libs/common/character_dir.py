"""Which folder under a drama's `characters/` is a character card.

`c{N}_…` is the named cast; `m{N}_…` is monsters and crowd NPCs (kobolds,
wolves, guards). Both get a portrait + turntable video (ai_video.md rule
22.2: "every character, crowds and non-humans included"), so every
character-folder feature — the gallery, 3-view extraction, truncation — must
accept both. The UI twin is `apps/ui/src/lib/characterDir.ts`.
"""
from __future__ import annotations

import re

CHARACTER_DIR_RE: re.Pattern[str] = re.compile(r"^[cm]\d+(_.*)?$")
