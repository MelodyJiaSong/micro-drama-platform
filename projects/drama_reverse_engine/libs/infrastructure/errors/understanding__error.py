from __future__ import annotations


class UnderstandingError(Exception):
    pass


class UnderstandingBackendUnavailableError(UnderstandingError):
    """No video-understanding backend configured — the pipeline halts loudly
    rather than fabricating an analysis (no silent fallback)."""
