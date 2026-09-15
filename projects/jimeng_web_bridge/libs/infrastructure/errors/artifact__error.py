from __future__ import annotations


class InvalidArtifactNameError(Exception):
    pass


class ArtifactTooLargeError(Exception):
    pass


class UnsupportedThumbnailSourceError(Exception):
    pass
