"""Named domain errors for a drama root path (`ai_videos/{drama}` or a series member).

Shared by the Downloads import and the media archive/rename writers. They used to
live in the Casting aggregate's error module; casting was removed with the old
pipeline (follow-up 233) and these two are all that remained in use.
"""
from __future__ import annotations


class DramaDomainError(Exception):
    """Base for drama-path domain errors."""


class InvalidDramaPathError(DramaDomainError):
    """rel_drama_path is not a drama root under ai_videos/ (or escapes the sandbox)."""


class DramaNotFoundError(DramaDomainError):
    """The drama folder is not on disk."""
