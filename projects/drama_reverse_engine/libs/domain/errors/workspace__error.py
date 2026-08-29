from __future__ import annotations


class WorkspaceError(Exception):
    pass


class PathEscapeError(WorkspaceError):
    """A relative path attempted to escape the workspace sandbox (SEC-05)."""
