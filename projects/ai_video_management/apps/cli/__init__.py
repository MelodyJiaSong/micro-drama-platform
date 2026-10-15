"""CLI entry points for ai_video_management.

`extract_views` extracts a character turntable's three views + audio + first-2s
trim into `views/` — the same command as the UI's 🖼 button. `tools/char_assets.py`
runs it per drama with this project's `.venv`:

    python -m apps.cli.extract_views ai_videos/{drama}/2_世界观人设/characters/{char}/{video}.mp4

from the project root. (The novel download / split CLIs went with follow-up 233.)
"""
