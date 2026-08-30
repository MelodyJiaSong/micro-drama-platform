"""Diff local scan against the manifest — what to upload, download, or drop.

Change is decided from sha256, never mtime. A file that only moved is detected
by matching its digest against a manifest entry at another path: that becomes a
server-side copy (`renames`), not a re-upload, so moving a 300 MB take costs no
bandwidth.
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
    renames: dict[str, str]

    @property
    def upload_bytes(self) -> int:
        """Bytes actually leaving this machine — renames move server-side."""
        return sum(e.size for rel, e in self.upload.items() if rel not in self.renames)

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
    gone = {manifest.assets[rel].sha256: rel for rel in download}
    renames = {rel: gone[e.sha256] for rel, e in upload.items() if e.sha256 in gone}
    return SyncPlan(
        upload=upload, download=download, unchanged=unchanged, drifted=drifted, renames=renames
    )


def unreferenced_keys(manifest: Manifest, remote_keys: list[str]) -> list[str]:
    """Bucket keys the manifest no longer names — deleted or renamed-away files."""
    return sorted(k for k in remote_keys if k not in manifest.assets)


def human_bytes(n: int) -> str:
    size = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024
    return f"{size:.1f} TB"
