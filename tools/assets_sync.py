"""Sync `ai_videos/` media to Cloudflare R2, indexed by a tracked manifest.

Media is gitignored, so git alone cannot answer "which bytes belong to this
commit". This tool keeps the bytes in an S3-compatible bucket and the index —
`ai_videos/assets.json`, path -> sha256 — in git, where it diffs and reverts
like any other file.

Usage:
    python tools/assets_sync.py status
    python tools/assets_sync.py push [--dry-run]
    python tools/assets_sync.py pull [--dry-run]
    python tools/assets_sync.py prune [--yes]

`status` needs no credentials. Credentials for the rest come from a gitignored
`.env` at the repo root — see tools/assets/.env.example.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.assets.manifest import AssetEntry, Manifest  # noqa: E402
from tools.assets.plan import SyncPlan, build, human_bytes, unreferenced_keys  # noqa: E402
from tools.assets.r2 import R2Store  # noqa: E402
from tools.assets.scanner import scan  # noqa: E402

MANIFEST_PATH = REPO_ROOT / "ai_videos" / "assets.json"
MEDIA_ROOT = REPO_ROOT / "ai_videos"


def _load() -> tuple[dict[str, AssetEntry], Manifest, SyncPlan, int]:
    result = scan(REPO_ROOT)
    manifest = Manifest.load(MANIFEST_PATH)
    return result.entries, manifest, build(result.entries, manifest), result.skipped_tracked


def cmd_status() -> int:
    local, manifest, plan, tracked = _load()
    print(f"local media   : {len(local)} files, {human_bytes(sum(e.size for e in local.values()))}")
    print(f"manifest      : {len(manifest.assets)} files, {human_bytes(manifest.total_bytes)}"
          f"{f' (updated {manifest.updated})' if manifest.updated else ''}")
    print(f"in sync       : {plan.unchanged}")
    print(f"to push       : {len(plan.upload)} files, {human_bytes(plan.upload_bytes)}"
          f"{f' ({len(plan.drifted)} changed in place)' if plan.drifted else ''}")
    print(f"to pull       : {len(plan.download)} files, {human_bytes(plan.download_bytes)}")
    print(f"in git        : {tracked} files left to version control, never uploaded")
    for rel in list(plan.upload)[:10]:
        print(f"  + {rel}")
    if len(plan.upload) > 10:
        print(f"  … {len(plan.upload) - 10} more")
    for rel in list(plan.download)[:10]:
        print(f"  ↓ {rel}")
    if len(plan.download) > 10:
        print(f"  … {len(plan.download) - 10} more")
    return 0


def cmd_push(dry_run: bool) -> int:
    local, _, plan, _ = _load()
    if not plan.upload:
        print("nothing to push")
        return 0
    print(f"push: {len(plan.upload)} files, {human_bytes(plan.upload_bytes)}")
    if dry_run:
        for rel in plan.upload:
            print(f"  + {rel}")
        return 0
    store = R2Store.from_env(REPO_ROOT)
    done = 0
    for rel, entry in plan.upload.items():
        if not store.exists(entry.key):
            store.upload(entry.key, MEDIA_ROOT / rel)
        done += 1
        print(f"  [{done}/{len(plan.upload)}] {rel}")
    Manifest(assets=local, updated="").save(MANIFEST_PATH)
    print(f"manifest written: {MANIFEST_PATH.relative_to(REPO_ROOT)} ({len(local)} entries)")
    return 0


def cmd_pull(dry_run: bool) -> int:
    _, _, plan, _ = _load()
    if not plan.download:
        print("nothing to pull")
        return 0
    print(f"pull: {len(plan.download)} files, {human_bytes(plan.download_bytes)}")
    if dry_run:
        for rel in plan.download:
            print(f"  ↓ {rel}")
        return 0
    store = R2Store.from_env(REPO_ROOT)
    done = 0
    for rel, entry in plan.download.items():
        store.download(entry.key, MEDIA_ROOT / rel)
        done += 1
        print(f"  [{done}/{len(plan.download)}] {rel}")
    return 0


def cmd_prune(confirmed: bool) -> int:
    manifest = Manifest.load(MANIFEST_PATH)
    if not manifest.assets:
        print("refusing to prune against an empty manifest")
        return 1
    store = R2Store.from_env(REPO_ROOT)
    orphans = unreferenced_keys(manifest, list(store.list_keys()))
    if not orphans:
        print("no unreferenced objects")
        return 0
    print(f"{len(orphans)} objects in the bucket are not referenced by the manifest")
    if not confirmed:
        for key in orphans[:20]:
            print(f"  - {key}")
        print("re-run with --yes to delete them permanently")
        return 0
    store.delete(orphans)
    print(f"deleted {len(orphans)} objects")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="compare local media against the manifest (no credentials needed)")
    push = sub.add_parser("push", help="upload new/changed media and rewrite the manifest")
    push.add_argument("--dry-run", action="store_true")
    pull = sub.add_parser("pull", help="download manifest entries missing locally")
    pull.add_argument("--dry-run", action="store_true")
    prune = sub.add_parser("prune", help="delete bucket objects no longer referenced")
    prune.add_argument("--yes", action="store_true", help="actually delete (default: list only)")
    args = parser.parse_args()
    try:
        if args.command == "status":
            return cmd_status()
        if args.command == "push":
            return cmd_push(args.dry_run)
        if args.command == "pull":
            return cmd_pull(args.dry_run)
        return cmd_prune(args.yes)
    except RuntimeError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
