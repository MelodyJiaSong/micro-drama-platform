from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator
import json
import os
import uuid

from libs.common.writers_room import content_hash
from libs.common.writers_room_paths import bible_path, room_path, story_path


class WritersRoomWriter:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root

    @staticmethod
    def text(path: Path, value: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
        temp.write_text(value, encoding="utf-8", newline="\n")
        os.replace(temp, path)

    def json(self, path: Path, value: Any) -> None:
        self.text(path, json.dumps(value, ensure_ascii=False, indent=2))

    @contextmanager
    def lock(self, slug: str, name: str = "write") -> Iterator[None]:
        path = room_path(self.root, slug) / f"{name}.lock"
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            raise RuntimeError("编剧室已有写入/运行锁；请等待，崩溃恢复须核实旧进程已退出。") from None
        try:
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            yield
        finally:
            path.unlink(missing_ok=True)

    def create(self, seed: dict[str, Any], config: dict[str, Any]) -> None:
        slug = seed["slug"]
        target = story_path(self.root, slug)
        target.mkdir(parents=True, exist_ok=False)
        self.json(bible_path(self.root, slug) / "seed.json", seed)
        self.json(bible_path(self.root, slug) / "config.json", config)
        self.text(target / "README.md", f"# {slug}\n\n编剧室工作稿；按 A 模式逐集人工批准后输出正式剧本。\n")

    def commit(self, slug: str, parent: str | None, payload: dict[str, Any], script: str) -> str:
        room = room_path(self.root, slug)
        with self.lock(slug):
            head_path = room / "head.json"
            head = json.loads(head_path.read_text(encoding="utf-8")) if head_path.exists() else {"revision": None}
            if head["revision"] != parent:
                raise RuntimeError("版本已被其他运行更新，请重新读取后续跑。")
            revision = content_hash({"parent": parent, "payload": payload, "script": script})
            self.text(room / "revisions" / f"{revision}.md", script)
            self.json(room / "revisions" / f"{revision}.json", dict(payload, revision=revision, parent=parent))
            # 单一原子 HEAD 同时发布剧本引用和 memory。之前的 immutable payload 不会成为已接受状态。
            self.json(head_path, {"revision": revision})
            return revision
