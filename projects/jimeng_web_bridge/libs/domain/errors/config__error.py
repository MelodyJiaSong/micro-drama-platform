class ConfigError(Exception):
    error_code: str = "config_invalid"

    def __init__(self, field_path: str, message: str) -> None:
        super().__init__(f"{field_path}: {message}")
        self.field_path: str = field_path
        self.message: str = message


class UnknownModelError(ConfigError):
    error_code = "unknown_model"


class MissingAbbrevError(ConfigError):
    error_code = "drama_abbrev_missing"
