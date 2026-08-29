"""Centralized media store for `ai_videos/` — Cloudflare R2 + a tracked manifest.

Media (video / image / audio / pdf) is gitignored and therefore invisible to
version control. This package keeps a content-addressed copy in an S3-compatible
bucket and records `path -> sha256` in `ai_videos/assets.json`, which IS tracked:
the manifest diffs, reviews and reverts like any other file, while the bytes live
outside git.
"""
