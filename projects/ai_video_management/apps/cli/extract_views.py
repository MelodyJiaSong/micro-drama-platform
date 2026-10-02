"""CLI entry: extract a character turntable's 3 views + audio + 2 s trim into `views/`.

Same command as the 🎞 一键提取 button (`CharacterVideoCommand.extract_views`),
so the timestamps and file names stay defined once
(`libs/domain/value_objects/character_video__valueobject.py`). Used by the repo
tool `tools/char_assets.py` to batch a whole drama.

Usage (from the project root):
    python -m apps.cli.extract_views ai_videos/{drama}/2_世界观人设/characters/{char}/{char}_turntable.mp4 [...]

Paths are repo-relative. Prints one JSON line per video; exit 1 if any failed.
"""
from __future__ import annotations

import json
import sys

from apps.api.container import Container
from libs.common.repo_root import RepoRoot

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    container = Container()
    container.repo_root_path.override(RepoRoot.find().path)
    command = container.character_video_command()
    failed = 0
    for rel in argv:
        try:
            payload = command.extract_views(rel).to_payload()
        except Exception as exc:  # noqa: BLE001 — report per video, keep going
            payload = {"src": rel, "error": f"{type(exc).__name__}: {exc}"}
        failed += bool(payload.get("error") or payload.get("failures"))
        print(json.dumps(payload, ensure_ascii=False), flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
