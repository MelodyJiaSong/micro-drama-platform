from __future__ import annotations


class UnknownExportSelectionError(Exception):
    """The requested artifact key or format is not an exportable option."""


class ExportArtifactMissingError(Exception):
    """A selected artifact has not been generated yet for this episode."""
