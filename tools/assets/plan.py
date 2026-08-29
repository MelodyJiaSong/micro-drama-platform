"""Diff local scan against the manifest — what to upload, download, or drop.

Everything is decided from sha256, so a file that was renamed locally is an
`add` + `remove` in the manifest but needs no transfer: its content is already
in the bucket under the same key.
"""
from __future__ import annotations

from dataclasses import dataclass

from tools.assets.manifest import AssetEntry, Manifest


@dataclass(frozen=True)
class SyncPlan:
    """`upload`/`download` are per-path; `keys_needed` collapses them to the
    distinct object keys a transfer actually has to move."""

    upload: dict[str, AssetEntry]
    download: dict[str, AssetEntry]
    unchanged: int
    drifted: dict[str, tuple[str, str]]

    @property
    def upload_bytes(self) -> int:
        return sum(e.size for e in self.upload.values())

    @property
    def download_bytes(self) -> int:
        return sum(e.size for e in self.download.values())


def build(local: dict[str, AssetEntry], manifest: Manifest) -> SyncPlan:
    upload: dict[str, AssetEntry] = {}
    drifted: dict[str, tuple[str, str]] = {}
    unchanged = 0
    for rel, entry in local.items():
        known = manifest.assets.get(rel)
        if known is None:
            upload[rel] = entry
        elif known.sha256 != entry.sha256:
            drifted[rel] = (known.sha256, entry.sha256)
            upload[rel] = entry
        else:
            unchanged += 1
    download = {rel: e for rel, e in manifest.assets.items() if rel not in local}
    return SyncPlan(upload=upload, download=download, unchanged=unchanged, drifted=drifted)


def unreferenced_keys(manifest: Manifest, remote_keys: list[str]) -> list[str]:
    live = {entry.key for entry in manifest.assets.values()}
    return sorted(k for k in remote_keys if k not in live)


def human_bytes(n: int) -> str:
    size = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024
    return f"{size:.1f} TB"
