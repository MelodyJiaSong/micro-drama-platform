"""Centralized media store for `ai_videos/` — Cloudflare R2 + a tracked manifest.

Media (video / image / audio / pdf) is gitignored and therefore invisible to
version control. This package mirrors the tree into an S3-compatible bucket — the object key
is the path under `ai_videos/`, so the bucket browses like the drama folder —
and records `path -> sha256` in `ai_videos/assets.json`, which IS tracked:
the manifest diffs, reviews and reverts like any other file, while the bytes live
outside git.
"""
