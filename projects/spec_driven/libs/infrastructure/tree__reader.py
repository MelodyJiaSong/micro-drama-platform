from __future__ import annotations

from pathlib import Path
from typing import Any

from libs.common.exposed_tree import ALLOWED_EXTENSIONS, CONTEXT_DIRS, ExposedTree


class TreeReader:
    def __init__(self, exposed: ExposedTree) -> None:
        self._exposed = exposed
        self._root = exposed.root

    def build(self) -> dict[str, Any]:
        return {
            "type": "section",
            "name": "root",
            "path": "",
            "children": [
                self._context_section(),
                self._projects_section(),
            ],
        }

    def _context_section(self) -> dict[str, Any]:
        children: list[dict[str, Any]] = []

        for f in self._exposed.context_root_files():
            children.append(self._leaf_for(f))

        for name in CONTEXT_DIRS:
            directory = self._root / name
            if directory.is_dir():
                children.append({
                    "type": "directory", "name": name, "path": name,
                    "children": self._walk_filtered(
                        directory,
                        lambda p: self._exposed.is_inside(self._rel(p)) and self._is_allowed_leaf(p),
                    ),
                })

        return {
            "type": "section",
            "name": "Agent Conventions & Shared Context",
            "path": "",
            "children": children,
        }

    def _projects_section(self) -> dict[str, Any]:
        # FR-15: "Specs" subtree is `{type}/{name}/` mirrored from `specs/`.
        # Elide the literal `specs/` wrapper so task_type is the direct child.
        specs_dir = self._root / "specs"
        children: list[dict[str, Any]] = (
            self._walk_filtered(specs_dir, self._is_allowed_leaf)
            if specs_dir.is_dir()
            else []
        )
        return {
            "type": "section",
            "name": "Specs",
            "path": "",
            "children": children,
        }

    def _walk_filtered(self, directory: Path, leaf_predicate: Any) -> list[dict[str, Any]]:
        children: list[dict[str, Any]] = []
        excluded = self._exposed.excluded_dirs()
        try:
            entries = sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except OSError:
            return children
        for entry in entries:
            if entry.is_symlink():
                continue
            if entry.name in excluded:
                continue
            if entry.is_dir():
                sub = self._walk_filtered(entry, leaf_predicate)
                if sub:
                    children.append(
                        {
                            "type": "directory",
                            "name": entry.name,
                            "path": self._rel(entry),
                            "children": sub,
                        }
                    )
            elif entry.is_file():
                if leaf_predicate(entry):
                    children.append(self._leaf_for(entry))
        return children

    def _is_allowed_leaf(self, p: Path) -> bool:
        return p.suffix.lower() in ALLOWED_EXTENSIONS

    def _leaf_for(self, f: Path) -> dict[str, Any]:
        return {"type": "file", "name": f.name, "path": self._rel(f)}

    def _rel(self, p: Path) -> str:
        try:
            return p.resolve().relative_to(self._root).as_posix()
        except ValueError:
            return p.as_posix()
