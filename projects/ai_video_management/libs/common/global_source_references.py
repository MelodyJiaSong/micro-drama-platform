"""Find explicit repository references; templates and arbitrary prose are not paths."""
from __future__ import annotations

import posixpath
import re
from urllib.parse import unquote, urlsplit

from libs.common.global_workflow import source_identity


def source_references(path: str, text: str) -> set[str]:
    result = set(re.findall(r"(?:tools/[\w/.-]+\.(?:py|toml|json)|projects/ai_video_management/libs/[\w/.-]+\.py|\.agents/[\w/.-]+\.(?:md|json|toml))", text))
    for href in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", text):
        target = urlsplit(href)
        if target.scheme or target.netloc or not target.path:
            continue
        candidate = posixpath.normpath(posixpath.join(posixpath.dirname(path), unquote(target.path)))
        if source_identity(candidate) and candidate.endswith((".md", ".json", ".toml", ".py", ".rules")):
            result.add(candidate)
    return {candidate for candidate in result if source_identity(candidate)}
