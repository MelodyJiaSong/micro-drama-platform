from __future__ import annotations


class ClaudeCliError(Exception):
    """Raised when the local `claude` CLI is missing, times out, exits nonzero, or
    returns an unparseable result envelope."""
