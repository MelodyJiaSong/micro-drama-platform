from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace


class ArtifactWriter:
    def __init__(self, workspace: SafeWorkspace) -> None:
        self._workspace = workspace

    def resolve(self, rel_path: str) -> str:
        return self._workspace.resolve(rel_path)

    def ensure_dir(self, rel_dir: str) -> str:
        path = Path(self._workspace.resolve(rel_dir))
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    def write_json(self, rel_path: str, payload: Any) -> None:
        path = Path(self._workspace.resolve(rel_path))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def write_text(self, rel_path: str, text: str) -> None:
        path = Path(self._workspace.resolve(rel_path))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def copy(self, src_rel: str, dst_rel: str) -> None:
        import shutil

        dst = Path(self._workspace.resolve(dst_rel))
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(self._workspace.resolve(src_rel), dst)

    def append_jsonl(self, rel_path: str, payload: Any) -> None:
        path = Path(self._workspace.resolve(rel_path))
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def delete_file(self, rel_path: str) -> None:
        Path(self._workspace.resolve(rel_path)).unlink(missing_ok=True)

    def delete_tree(self, rel_dir: str) -> None:
        import shutil

        path = Path(self._workspace.resolve(rel_dir))
        if path.exists():
            shutil.rmtree(path)
