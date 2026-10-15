"""Per-shot 资料包 status for the UI (follow-up 229).

The pack itself is built by `tools/shot_pack.py` (copies every referenced file, writes manifest.json with source sha256,
fills the 参考 line's `key=>@` placeholders with upload numbers; the Claude Stop hook syncs it every turn). This reader
only reports what is on disk: `ok`, `stale` (a source file changed size or time since the copy, or the prompt changed),
`invalid` (the tool emptied it and left `_失效.md` with the reason), or `missing`.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from libs.common.production_key import first_shot_key

PACK = "资料包"
MANIFEST = "manifest.json"
INVALID = "_失效.md"


class ShotPackReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root

    def read(self, episode_path: str, prompts: dict[str, Any]) -> dict[str, dict[str, Any]]:
        episode = self.root / episode_path
        out: dict[str, dict[str, Any]] = {}
        for scene in prompts.get("scenes", []):
            for shot in scene["shots"]:
                key = first_shot_key(shot["id"])
                if key is None:
                    continue
                out[shot["id"]] = self._one(key.folder(episode) / PACK, shot)
        return out

    def _rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def _one(self, pack: Path, shot: dict[str, Any]) -> dict[str, Any]:
        base = {"path": self._rel(pack), "files": [], "prompt": "", "reason": ""}
        if (pack / INVALID).is_file():
            return {**base, "status": "invalid", "reason": (pack / INVALID).read_text(encoding="utf-8")}
        manifest = pack / MANIFEST
        if not manifest.is_file():
            return {**base, "status": "missing"}
        data = json.loads(manifest.read_text(encoding="utf-8"))
        files = [{"tag": r.get("tag", ""), "key": r.get("key", ""), "kind": r["kind"], "role": r["role"],
                  "path": self._rel(pack / r["file"]), "src": r["src"]} for r in data.get("refs", [])]
        status = "ok"
        if data.get("prompt_sha256") != hashlib.sha256(shot["text"].encode("utf-8")).hexdigest() \
                or [r["src"] for r in data.get("refs", [])] != [r["path"] for r in shot.get("refs", [])]:
            status = "stale"
        for r in data.get("refs", []):
            src, copy = self.root / r["src"], pack / r["file"]
            if not src.is_file() or not copy.is_file() or src.stat().st_size != r.get("size") \
                    or int(src.stat().st_mtime) != r.get("mtime"):
                status = "stale"
        prompt = pack / "prompt.txt"
        return {**base, "status": status, "files": files, "prompt": self._rel(prompt) if prompt.is_file() else ""}
