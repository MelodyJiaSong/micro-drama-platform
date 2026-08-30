"""`ai_videos/assets.json` — the tracked path→content index.

The R2 object key IS the path under `ai_videos/`, so the bucket mirrors the
drama tree exactly — `wushen_juexing/5_6_分镜与prompt/episodes/ep01/shots/...`
browses in the dashboard the way it browses on disk. sha256 is still recorded,
but only to detect change; a rename moves an object server-side rather than
re-uploading it.

The manifest holds no bucket name, account id or endpoint — those are
credentials' neighbours and stay in the environment.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_VERSION: int = 1


@dataclass(frozen=True)
class AssetEntry:
    sha256: str
    size: int


@dataclass(frozen=True)
class Manifest:
    assets: dict[str, AssetEntry]
    updated: str

    @classmethod
    def empty(cls) -> Manifest:
        return cls(assets={}, updated="")

    @classmethod
    def load(cls, path: Path) -> Manifest:
        if not path.is_file():
            return cls.empty()
        data = json.loads(path.read_text(encoding="utf-8"))
        version = data.get("version")
        if version != MANIFEST_VERSION:
            raise ValueError(f"{path}: unsupported manifest version {version!r}")
        assets = {
            rel: AssetEntry(sha256=entry["sha256"], size=int(entry["size"]))
            for rel, entry in data.get("assets", {}).items()
        }
        return cls(assets=assets, updated=str(data.get("updated", "")))

    def save(self, path: Path) -> None:
        payload = {
            "version": MANIFEST_VERSION,
            "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "assets": {
                rel: {"sha256": self.assets[rel].sha256, "size": self.assets[rel].size}
                for rel in sorted(self.assets)
            },
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    @property
    def total_bytes(self) -> int:
        return sum(e.size for e in self.assets.values())
