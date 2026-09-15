from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path


class EnvFileWriter:
    """Upserts one KEY=value line in a dotenv file, leaving every other line untouched."""

    def upsert(self, path: Path, key: str, value: str) -> None:
        existing = path.read_text(encoding="utf-8-sig") if path.is_file() else ""
        pattern = re.compile(rf"^\s*(export\s+)?{re.escape(key)}\s*=.*$")
        lines = existing.splitlines()
        replaced = False
        for index, line in enumerate(lines):
            if pattern.match(line):
                lines[index] = f"{key}={value}"
                replaced = True
        if not replaced:
            lines.append(f"{key}={value}")
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temp_name = tempfile.mkstemp(prefix=".env.", dir=str(path.parent))
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write("\n".join(lines) + "\n")
        os.replace(temp_name, path)
