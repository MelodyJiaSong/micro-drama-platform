"""Named domain errors for character turntable view + audio extraction.

Each error class is a distinct named subclass of the base, mapped to an HTTP
`detail.kind` string in `apps/api/app_factory.py`. (The truncate and per-shot
character-reel errors went with those features in follow-up 233.)
"""
from __future__ import annotations


class CharacterVideoDomainError(Exception):
    """Base for character-video extraction errors."""


class InvalidCharacterVideoPathError(CharacterVideoDomainError):
    """Path is empty, outside sandbox, or otherwise malformed."""


class NotCharacterVideoError(CharacterVideoDomainError):
    """Extension is not a video type, or path is not under
    `ai_videos/{drama}/…/characters/{cN_xxx}/`."""


class CharacterVideoNotFoundError(CharacterVideoDomainError):
    """Source mp4 file does not exist."""


class FfmpegMissingForCharacterVideoError(CharacterVideoDomainError):
    """ffmpeg binary unavailable on this host."""


# --- View + audio extraction (per follow-up 093) -----------------------------


class ViewExtractFailedError(CharacterVideoDomainError):
    """ffmpeg ran but at least one of the 3 angle PNGs (front/side/back) could
    not be produced. Raised only when ALL outputs fail (3 views + audio + trim) —
    partial-failure runs return a 200 with a non-empty `failures` list."""


class AudioExtractFailedError(CharacterVideoDomainError):
    """ffmpeg ran but the .mp3 audio track could not be produced. Raised only
    when ALL outputs fail (3 views + audio + trim) — partial-failure runs return
    a 200 with a non-empty `failures` list."""


class InvalidCharactersDirError(CharacterVideoDomainError):
    """Path is empty, outside sandbox, or not an `ai_videos/{drama}/.../
    characters/` directory — used by the batch extract-all run."""
