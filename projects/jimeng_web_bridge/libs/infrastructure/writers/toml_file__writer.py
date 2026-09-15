from __future__ import annotations

import codecs
import contextlib
import hashlib
import json
import os
import tempfile
import threading
from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import tomlkit
from tomlkit.exceptions import TOMLKitError
from tomlkit.items import AoT, Array

from libs.infrastructure.daos.config_file__dao import ConfigFileDao
from libs.infrastructure.errors.config_io__error import (
    ConfigConflictError,
    ConfigParseError,
    ConfigWriteError,
)
from libs.infrastructure.readers.toml_file__reader import TomlFileReader

_PATH_LOCKS: dict[str, threading.Lock] = {}
_PATH_LOCKS_GUARD: threading.Lock = threading.Lock()


class TomlFileWriter:
    """Round-trip save: only changed values are touched, so comments, key order and line endings survive.

    The hash check and the replace run under a process-wide lock keyed by the resolved path, so separate
    writer instances (drama or global, one per request) still serialise and the later save gets a conflict.
    """

    def __init__(self) -> None:
        self._reader: TomlFileReader = TomlFileReader()

    def save(
        self, path: Path, location: str, data: Mapping[str, object], expected_sha256: str | None
    ) -> ConfigFileDao:
        with _lock_for(path):
            current = self._current(path, location, expected_sha256)
            original = None if current is None else self._reader.decode(current, location)
            document = self._reader.parse_document(original or "", location)
            try:
                _merge(document, data)
                rendered = document.as_string()
            except (TOMLKitError, TypeError, ValueError) as error:
                raise ConfigParseError(location, str(error)) from error
            return self._write(path, location, _line_endings_like(rendered, original), _has_bom(current))

    def save_text(self, path: Path, location: str, text: str, expected_sha256: str | None) -> ConfigFileDao:
        with _lock_for(path):
            current = self._current(path, location, expected_sha256)
            incoming = text.removeprefix("﻿")
            self._reader.parse_document(incoming, location)
            original = None if current is None else self._reader.decode(current, location)
            return self._write(path, location, _line_endings_like(incoming, original), _has_bom(current))

    def _current(self, path: Path, location: str, expected_sha256: str | None) -> bytes | None:
        try:
            current = path.read_bytes() if path.is_file() else None
        except OSError as error:
            raise ConfigWriteError(location, _os_detail(error)) from error
        current_sha256 = None if current is None else hashlib.sha256(current).hexdigest()
        if current_sha256 != expected_sha256:
            raise ConfigConflictError(location, expected_sha256, current_sha256)
        return current

    def _write(self, path: Path, location: str, text: str, has_bom: bool) -> ConfigFileDao:
        payload = (codecs.BOM_UTF8 if has_bom else b"") + text.encode("utf-8")
        try:
            descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
        except OSError as error:
            raise ConfigWriteError(location, _os_detail(error)) from error
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, path)
        except BaseException as error:
            with contextlib.suppress(OSError):
                os.unlink(temp_name)
            if isinstance(error, OSError):
                raise ConfigWriteError(location, _os_detail(error)) from error
            raise
        return ConfigFileDao(
            location=location,
            exists=True,
            data=tomlkit.parse(text).unwrap(),
            sha256=hashlib.sha256(payload).hexdigest(),
            raw_text=text,
        )


def _lock_for(path: Path) -> threading.Lock:
    key = os.path.normcase(str(path.resolve()))
    with _PATH_LOCKS_GUARD:
        return _PATH_LOCKS.setdefault(key, threading.Lock())


def _has_bom(current: bytes | None) -> bool:
    return current is not None and current.startswith(codecs.BOM_UTF8)


def _line_endings_like(text: str, original: str | None) -> str:
    if original is None:
        return text
    unified = text.replace("\r\n", "\n")
    return unified.replace("\n", "\r\n") if "\r\n" in original else unified


def _os_detail(error: OSError) -> str:
    return f"{type(error).__name__}: {error.strerror or 'operating system error'}"


def _merge(container: MutableMapping[str, Any], data: Mapping[str, object]) -> None:
    for key in [key for key in container if key not in data]:
        del container[key]
    for key, value in data.items():
        if key not in container:
            container[key] = value
            continue
        current = container[key]
        if isinstance(value, Mapping) and isinstance(current, MutableMapping):
            _merge(current, value)
        elif _mergeable_sequence(current, value):
            _merge_sequence(current, value)
        elif not _same(_plain(current), value):
            container[key] = value


def _mergeable_sequence(current: object, value: object) -> bool:
    if not isinstance(value, (list, tuple)):
        return False
    if isinstance(current, Array):
        return True
    return isinstance(current, AoT) and bool(value) and all(isinstance(item, Mapping) for item in value)


def _merge_sequence(current: MutableSequence[Any], value: Sequence[object]) -> None:
    """Aligns old and new elements so untouched entries keep their own comments and inline/table style.

    An element whose content reappears elsewhere is a move, not an edit: the original tomlkit item is
    re-inserted at its new position, so a reordered `[[references.rules]]` entry keeps its comments.
    """
    old_keys = [_canonical(_plain(item)) for item in current]
    new_keys = [_canonical(item) for item in value]
    opcodes = SequenceMatcher(a=old_keys, b=new_keys, autojunk=False).get_opcodes()
    unmatched_old = {old_keys[i] for tag, i1, i2, _, _ in opcodes if tag != "equal" for i in range(i1, i2)}
    unmatched_new = {new_keys[j] for tag, _, _, j1, j2 in opcodes if tag != "equal" for j in range(j1, j2)}
    moved = unmatched_old & unmatched_new
    deletions: list[int] = []
    insertions: list[int] = []
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal":
            continue
        olds = [i for i in range(i1, i2) if old_keys[i] not in moved]
        news = [j for j in range(j1, j2) if new_keys[j] not in moved]
        pairs = min(len(olds), len(news))
        for old_index, new_index in zip(olds[:pairs], news[:pairs]):
            _merge_element(current, old_index, value[new_index])
        deletions.extend(i for i in range(i1, i2) if i not in olds[:pairs])
        insertions.extend(j for j in range(j1, j2) if j not in news[:pairs])
    detached: dict[str, list[Any]] = {}
    for index in sorted(deletions, reverse=True):
        detached.setdefault(old_keys[index], []).append(current[index])
        del current[index]
    for index in sorted(insertions):
        reusable = detached.get(new_keys[index])
        current.insert(index, reusable.pop() if reusable else _new_element(current, value[index]))


def _merge_element(current: MutableSequence[Any], index: int, value: object) -> None:
    existing = current[index]
    if isinstance(value, Mapping) and isinstance(existing, MutableMapping):
        _merge(existing, value)
    elif not _same(_plain(existing), value):
        current[index] = value


def _new_element(current: MutableSequence[Any], value: object) -> object:
    if not isinstance(current, AoT) or not isinstance(value, Mapping):
        return value
    table = tomlkit.table()
    table.update(value)
    table.add(tomlkit.nl())
    return table


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)


def _plain(item: object) -> object:
    unwrap = getattr(item, "unwrap", None)
    return unwrap() if callable(unwrap) else item


def _same(left: object, right: object) -> bool:
    if isinstance(left, Mapping) and isinstance(right, Mapping):
        return left.keys() == right.keys() and all(_same(left[key], right[key]) for key in left)
    if isinstance(left, list) and isinstance(right, (list, tuple)):
        return len(left) == len(right) and all(_same(a, b) for a, b in zip(left, right))
    return type(left) is type(right) and left == right
