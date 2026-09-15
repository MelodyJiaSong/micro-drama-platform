import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import TypeVar

from libs.domain.errors.config__error import ConfigError

E = TypeVar("E", bound=StrEnum)

_BARE_KEY = re.compile(r"^[A-Za-z0-9_-]+$")


def key_path(parent: str, key: str) -> str:
    segment: str = key if _BARE_KEY.match(key) else f'"{key}"'
    return segment if not parent else f"{parent}.{segment}"


@dataclass(frozen=True)
class ConfigTable:
    data: Mapping[str, object]
    path: str = ""

    @classmethod
    def of(cls, data: object, path: str = "") -> "ConfigTable":
        if not isinstance(data, Mapping):
            raise ConfigError(path or "<root>", "必须是表（table）")
        return cls(data, path)

    def at(self, key: str) -> str:
        return key_path(self.path, key)

    def has(self, key: str) -> bool:
        return key in self.data

    def keys(self) -> tuple[str, ...]:
        return tuple(str(k) for k in self.data.keys())

    def require(self, key: str) -> object:
        if key not in self.data:
            raise ConfigError(self.at(key), "缺少必填键")
        return self.data[key]

    def only_keys(self, allowed: Iterable[str], hints: Mapping[str, str] | None = None) -> None:
        allowed_set: frozenset[str] = frozenset(allowed)
        for key in self.keys():
            if key not in allowed_set:
                hint: str = (hints or {}).get(key, "未知键")
                raise ConfigError(self.at(key), hint)

    def table(self, key: str) -> "ConfigTable":
        return ConfigTable.of(self.require(key), self.at(key))

    def string(self, key: str, allow_empty: bool = False, pattern: re.Pattern[str] | None = None) -> str:
        value: object = self.require(key)
        if not isinstance(value, str):
            raise ConfigError(self.at(key), "必须是字符串")
        if not allow_empty and value == "":
            raise ConfigError(self.at(key), "不能为空字符串")
        if pattern is not None and value != "" and not pattern.match(value):
            raise ConfigError(self.at(key), f"格式不合法：{value!r}")
        return value

    def enum(self, key: str, enum_type: type[E]) -> E:
        value: str = self.string(key)
        options: list[str] = [member.value for member in enum_type]
        if value not in options:
            raise ConfigError(self.at(key), f"取值必须是 {' | '.join(options)} 之一，实际 {value!r}")
        return enum_type(value)

    def one_of(self, key: str, options: Sequence[str]) -> str:
        value: str = self.string(key)
        if value not in options:
            raise ConfigError(self.at(key), f"取值必须是 {' | '.join(options)} 之一，实际 {value!r}")
        return value

    def integer(self, key: str, lo: int | None = None, hi: int | None = None) -> int:
        value: object = self.require(key)
        if isinstance(value, bool) or not isinstance(value, int):
            raise ConfigError(self.at(key), "必须是整数")
        self._check_bounds(key, value, lo, hi)
        return int(value)

    def number(self, key: str, lo: float | None = None, hi: float | None = None) -> float:
        value: object = self.require(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ConfigError(self.at(key), "必须是数字")
        self._check_bounds(key, value, lo, hi)
        return float(value)

    def boolean(self, key: str) -> bool:
        value: object = self.require(key)
        if not isinstance(value, bool):
            raise ConfigError(self.at(key), "必须是 true 或 false")
        return value

    def string_list(self, key: str, allow_empty: bool = False) -> tuple[str, ...]:
        value: object = self.require(key)
        if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
            raise ConfigError(self.at(key), "必须是字符串数组")
        if not allow_empty and len(value) == 0:
            raise ConfigError(self.at(key), "不能为空数组")
        items: list[str] = []
        for index, item in enumerate(value):
            if not isinstance(item, str) or item == "":
                raise ConfigError(f"{self.at(key)}[{index}]", "必须是非空字符串")
            items.append(item)
        return tuple(items)

    def string_map(self, key: str) -> dict[str, str]:
        child: ConfigTable = self.table(key)
        result: dict[str, str] = {}
        for name in child.keys():
            result[name] = child.string(name)
        return result

    def table_list(self, key: str) -> tuple["ConfigTable", ...]:
        value: object = self.require(key)
        if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
            raise ConfigError(self.at(key), "必须是表数组")
        return tuple(ConfigTable.of(item, f"{self.at(key)}[{index}]") for index, item in enumerate(value))

    def _check_bounds(self, key: str, value: float, lo: float | None, hi: float | None) -> None:
        if lo is not None and value < lo:
            raise ConfigError(self.at(key), f"必须 ≥ {lo}，实际 {value}")
        if hi is not None and value > hi:
            raise ConfigError(self.at(key), f"必须 ≤ {hi}，实际 {value}")
