"""Tree-aggregate queries: build the recursive TreeNode shape consumed
by the frontend sidebar. Pure projection — no domain invariant to enforce.
"""
from __future__ import annotations

from libs.application.dtos.tree__dto import TreeQdto
from libs.infrastructure.readers.tree__reader import TreeReader


class TreeQuery:
    def __init__(self, reader: TreeReader) -> None:
        self._reader = reader

    def build(self, lazy: bool = False) -> TreeQdto:
        return TreeQdto(root=self._reader.build(lazy=lazy))

    def subtree(self, path: str, depth: int | None = 1) -> TreeQdto:
        """One lazy folder's contents (follow-up 280)."""
        return TreeQdto(root=self._reader.subtree(path, depth))
