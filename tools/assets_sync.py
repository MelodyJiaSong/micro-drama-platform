"""Sync `ai_videos/` media to Cloudflare R2, indexed by a tracked manifest.

Media is gitignored, so git alone cannot answer "which bytes belong to this
commit". This tool keeps the bytes in an S3-compatible bucket and the index —
`ai_videos/assets.json`, path -> sha256 — in git, where it diffs and reverts
like any other file.

The bucket mirrors the drama tree: the object key IS the path under
`ai_videos/`, so `wushen_juexing/2_世界观人设/characters/...` browses in the R2
dashboard exactly as it does on disk.

Usage:
    python tools/assets_sync.py status
    python tools/assets_sync.py push [--dry-run] [--stage-manifest] [--soft-fail]
    python tools/assets_sync.py pull [--dry-run] [--auto]
    python tools/assets_sync.py check [--push]
    python tools/assets_sync.py prune [--yes]
    python tools/assets_sync.py install-hooks

`status` needs no credentials. Credentials for the rest come from a gitignored
`.env` at the repo root — see tools/assets/.env.example.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# Media paths are Chinese; a Windows console defaults to cp1252 and a bare
# print() of one kills the run mid-upload. Hooks inherit that console.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.assets.manifest import AssetEntry, Manifest  # noqa: E402
from tools.assets.plan import SyncPlan, build, human_bytes, unreferenced_keys  # noqa: E402
from tools.assets.r2 import R2Store  # noqa: E402
from tools.assets.scanner import scan  # noqa: E402

MANIFEST_PATH = REPO_ROOT / "ai_videos" / "assets.json"
MEDIA_ROOT = REPO_ROOT / "ai_videos"
MANIFEST_REL = "ai_videos/assets.json"
_SAVE_EVERY = 25


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


def _stage_manifest() -> None:
    subprocess.run(["git", "add", "--", MANIFEST_REL],
                   cwd=REPO_ROOT, check=False, capture_output=True)


def _next_manifest(local: dict[str, AssetEntry], manifest: Manifest,
                   prune_missing: bool) -> dict[str, AssetEntry]:
    """The index describes the whole project, not this machine.

    An entry with no local file is ambiguous — deleted here, or simply never
    pulled — and dropping it would erase another machine's media from the index
    for everyone. So missing entries are KEPT unless --prune-missing says the
    absence is deliberate.
    """
    kept = {} if prune_missing else {rel: e for rel, e in manifest.assets.items() if rel not in local}
    return {**kept, **local}


def _push(stage_manifest: bool, prune_missing: bool = False) -> int:
    local, manifest, plan, _ = _load()
    absent = len(manifest.assets) - len([r for r in manifest.assets if r in local])
    if absent and not prune_missing:
        print(f"note: {absent} manifest entries have no local file — kept in the index "
              f"(--prune-missing to drop them, `pull` to fetch them)")
    if not plan.upload:
        nxt = _next_manifest(local, manifest, prune_missing)
        if manifest.assets != nxt:
            Manifest(assets=nxt, updated="").save(MANIFEST_PATH)
            if stage_manifest:
                _stage_manifest()
            print(f"manifest refreshed: {len(nxt)} entries")
        else:
            print("nothing to push")
        return 0
    moved = len(plan.renames)
    print(f"push: {len(plan.upload)} files, {human_bytes(plan.upload_bytes)} to upload"
          f"{f' ({moved} moved server-side, no transfer)' if moved else ''}")
    store = R2Store.from_env(REPO_ROOT)
    # A previous run may have died partway through: anything already in the
    # bucket at the same key and size is treated as landed and not re-sent.
    # Paths the manifest knows that changed in place (drifted) always go up
    # again — size equality is only trusted for paths the index never saw.
    remote_sizes = dict(store.list_objects())
    # Checkpoint state: everything already true of the bucket. Files waiting to
    # go up are excluded, except drifted ones, which stay at their old digest —
    # that is still what the bucket holds until this run overwrites it.
    confirmed = {rel: e for rel, e in _next_manifest(local, manifest, prune_missing).items()
                 if rel not in plan.upload}
    confirmed.update({rel: manifest.assets[rel] for rel in plan.drifted})
    done = 0
    for rel, entry in plan.upload.items():
        moved_from = plan.renames.get(rel)
        if remote_sizes.get(rel) == entry.size and rel not in plan.drifted:
            label = "already in bucket"
        elif moved_from is not None and store.exists(moved_from):
            store.copy(moved_from, rel)
            label = f"moved from {moved_from}"
        else:
            store.upload(rel, MEDIA_ROOT / rel)
            label = human_bytes(entry.size)
        confirmed[rel] = entry
        done += 1
        print(f"  [{done}/{len(plan.upload)}] {rel} ({label})", flush=True)
        if done % _SAVE_EVERY == 0:
            Manifest(assets=confirmed, updated="").save(MANIFEST_PATH)
    final = _next_manifest(local, manifest, prune_missing)
    Manifest(assets=final, updated="").save(MANIFEST_PATH)
    if stage_manifest:
        _stage_manifest()
    print(f"manifest written: {MANIFEST_REL} ({len(final)} entries)"
          f"{' (staged)' if stage_manifest else ''}")
    return 0


def cmd_push(dry_run: bool, stage_manifest: bool, soft_fail: bool, prune_missing: bool) -> int:
    if dry_run:
        _, _, plan, _ = _load()
        if not plan.upload:
            print("nothing to push")
            return 0
        print(f"push: {len(plan.upload)} files, {human_bytes(plan.upload_bytes)} to upload")
        for rel in plan.upload:
            print(f"  + {rel}")
        return 0
    if not soft_fail:
        return _push(stage_manifest, prune_missing)
    try:
        return _push(stage_manifest, prune_missing)
    except Exception as err:  # a commit must not fail because R2 is unreachable
        print(f"assets_sync: media not uploaded ({err}) — the pre-push hook will "
              f"catch it before this leaves the machine", file=sys.stderr)
        return 0


def cmd_pull(dry_run: bool, auto: bool) -> int:
    _, _, plan, _ = _load()
    if not plan.download:
        if not auto:
            print("nothing to pull")
        return 0
    print(f"assets_sync: pulling {len(plan.download)} media files, "
          f"{human_bytes(plan.download_bytes)}", flush=True)
    if dry_run:
        for rel in plan.download:
            print(f"  ↓ {rel}")
        return 0
    try:
        store = R2Store.from_env(REPO_ROOT)
        done = 0
        for rel in plan.download:
            store.download(rel, MEDIA_ROOT / rel)
            done += 1
            print(f"  [{done}/{len(plan.download)}] {rel}", flush=True)
    except Exception as err:
        print(f"assets_sync: pull failed ({err}) — run "
              f"python tools/assets_sync.py pull when ready", file=sys.stderr)
        return 0 if auto else 2
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


def cmd_check(auto_push: bool) -> int:
    """Drift check for git hooks. Exit 1 when the manifest does not describe the
    media actually on disk — i.e. pushing now would publish an index that lies
    about the bytes. With --push, send the bytes first, leaving only the (fast)
    commit of the refreshed index to the user."""
    _, manifest, plan, _ = _load()
    if plan.upload:
        stale = len(plan.upload) - len(plan.drifted)
        print(
            f"assets out of sync: {stale} media file(s) missing from the manifest"
            f"{f', {len(plan.drifted)} changed in place' if plan.drifted else ''}"
            f" ({human_bytes(plan.upload_bytes)})",
            file=sys.stderr,
        )
        if auto_push:
            print("assets_sync: uploading them now…", file=sys.stderr)
            try:
                _push(stage_manifest=False)
            except Exception as err:
                print(f"  upload failed: {err}", file=sys.stderr)
                print("  run: python tools/assets_sync.py push", file=sys.stderr)
                return 1
            sys.stdout.flush()  # keep the transfer log above the verdict
            print("assets_sync: bytes are in R2 and the index was refreshed — but it "
                  "is not in this commit, so the push is refused; otherwise the index "
                  "would ship behind its own objects.", file=sys.stderr)
            print(f"  git add {MANIFEST_REL} && git commit && git push", file=sys.stderr)
            return 1
        print("  run: python tools/assets_sync.py push", file=sys.stderr)
        print(f"  then commit {MANIFEST_REL}", file=sys.stderr)
        return 1
    if plan.download:
        print(
            f"note: {len(plan.download)} manifest entries are not on this machine "
            f"({human_bytes(plan.download_bytes)}) — assets_sync.py pull to fetch",
            file=sys.stderr,
        )
    return 0


def cmd_install_hooks() -> int:
    """Copy the git hooks into .git/hooks, pinned to this interpreter.

    `.git/hooks` is not versioned, so every clone installs its own; the
    templates in tools/assets/hooks/ are the tracked source.
    """
    hooks_dir = REPO_ROOT / ".git" / "hooks"
    if not hooks_dir.is_dir():
        raise RuntimeError(f"{hooks_dir} does not exist — is this a git repo?")
    source = REPO_ROOT / "tools" / "assets" / "hooks"
    for template in sorted(source.iterdir()):
        if template.suffix:
            continue
        body = template.read_text(encoding="utf-8").replace("@PYTHON@", Path(sys.executable).as_posix())
        target = hooks_dir / template.name
        if target.exists() and "assets_sync" not in target.read_text(encoding="utf-8"):
            print(f"skipped {target.name}: already exists and is not ours", file=sys.stderr)
            continue
        target.write_text(body, encoding="utf-8", newline="\n")
        target.chmod(0o755)
        print(f"installed .git/hooks/{template.name}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="compare local media against the manifest (no credentials needed)")
    check = sub.add_parser("check", help="exit 1 if the manifest is stale (used by the pre-push hook)")
    check.add_argument("--push", action="store_true", help="upload the missing bytes before refusing")
    sub.add_parser("install-hooks", help="install the git hooks that sync media with pull/push")
    push = sub.add_parser("push", help="upload new/changed media and rewrite the manifest")
    push.add_argument("--dry-run", action="store_true")
    push.add_argument("--stage-manifest", action="store_true",
                      help="git add the refreshed manifest (used by the pre-commit hook)")
    push.add_argument("--soft-fail", action="store_true",
                      help="warn instead of failing when R2 is unreachable")
    push.add_argument("--prune-missing", action="store_true",
                      help="drop manifest entries with no local file (deliberate deletions)")
    pull = sub.add_parser("pull", help="download manifest entries missing locally")
    pull.add_argument("--dry-run", action="store_true")
    pull.add_argument("--auto", action="store_true",
                      help="hook mode: stay quiet when there is nothing to do, never fail")
    prune = sub.add_parser("prune", help="delete bucket objects no longer referenced")
    prune.add_argument("--yes", action="store_true", help="actually delete (default: list only)")
    args = parser.parse_args()
    try:
        if args.command == "status":
            return cmd_status()
        if args.command == "check":
            return cmd_check(args.push)
        if args.command == "install-hooks":
            return cmd_install_hooks()
        if args.command == "push":
            return cmd_push(args.dry_run, args.stage_manifest, args.soft_fail, args.prune_missing)
        if args.command == "pull":
            return cmd_pull(args.dry_run, args.auto)
        return cmd_prune(args.yes)
    except RuntimeError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
