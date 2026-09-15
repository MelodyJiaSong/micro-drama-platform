from __future__ import annotations


class ConfigIoError(Exception):
    pass


class ConfigConflictError(ConfigIoError):
    def __init__(self, location: str, expected_sha256: str | None, current_sha256: str | None) -> None:
        super().__init__(f"config changed since it was read: {location}")
        self.location: str = location
        self.expected_sha256: str | None = expected_sha256
        self.current_sha256: str | None = current_sha256


class ConfigParseError(ConfigIoError):
    def __init__(self, location: str, detail: str) -> None:
        super().__init__(f"invalid TOML in {location}: {detail}")
        self.location: str = location
        self.detail: str = detail


class ConfigWriteError(ConfigIoError):
    """An OS-level failure during the atomic save (e.g. the file is held open); `detail` never carries a path."""

    def __init__(self, location: str, detail: str) -> None:
        super().__init__(f"could not save {location}: {detail}")
        self.location: str = location
        self.detail: str = detail


class DramaRootNotFoundError(ConfigIoError):
    def __init__(self, drama_rel: str) -> None:
        super().__init__(f"not a drama root: {drama_rel}")
        self.drama_rel: str = drama_rel
