import json
from pathlib import Path

from libs.common.options import SOURCE_RECORD, SOURCES_DIR
from libs.infrastructure.daos.source__dao import SourceDao
from libs.infrastructure.errors.library__error import SourceMissingError


class SourceReader:
    def __init__(self, library: Path) -> None:
        self._root = library / SOURCES_DIR

    def folder(self, source_id: str) -> Path:
        return self._root / source_id

    def exists(self, source_id: str) -> bool:
        return (self.folder(source_id) / SOURCE_RECORD).is_file()

    def load(self, source_id: str) -> SourceDao:
        record = self.folder(source_id) / SOURCE_RECORD
        if not record.is_file():
            raise SourceMissingError(source_id)
        data = json.loads(record.read_text(encoding="utf-8"))
        data["subtitle_files"] = tuple(data["subtitle_files"])
        return SourceDao(**data)

    def all(self) -> list[SourceDao]:
        if not self._root.is_dir():
            return []
        return [self.load(path.parent.name) for path in sorted(self._root.glob(f"*/{SOURCE_RECORD}"))]

    def path(self, source_id: str, name: str) -> Path:
        return self.folder(source_id) / name
