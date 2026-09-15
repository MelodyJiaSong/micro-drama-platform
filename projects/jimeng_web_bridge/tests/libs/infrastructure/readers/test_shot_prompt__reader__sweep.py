from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import pytest

from libs.common.paths import RepoSandbox
from libs.infrastructure.errors.shot_parse__error import ShotParseError
from libs.infrastructure.readers.shot_prompt__reader import ShotPromptReader

_SHOT_MD_RE = re.compile(r"^shot\d+\.md$")


@pytest.mark.requires_real_repo
def test_repo_sweep_never_raises_and_never_silently_empty(real_repo_root: Path, real_sandbox: RepoSandbox) -> None:
    reader = ShotPromptReader(real_sandbox)
    shots = sorted(
        path
        for path in (real_repo_root / "ai_videos").rglob("shot*.md")
        if _SHOT_MD_RE.match(path.name) and "_deleted" not in path.parts
    )
    assert shots
    stats: Counter[str] = Counter()
    for path in shots:
        rel = path.relative_to(real_repo_root).as_posix()
        try:
            dao = reader.read(rel)
        except ShotParseError as error:
            stats[f"parse_error:{error.code}"] += 1
            continue
        refs = dao.references
        stats["files"] += 1
        stats["items"] += len(refs.items)
        stats["unrecognized"] += len(refs.unrecognized)
        stats["integrity_mismatch"] += int(not refs.integrity_ok)
        stats.update(f"legacy:{finding.kind}" for finding in refs.legacy)
        if refs.line_count:
            assert refs.items or refs.legacy or refs.unrecognized or refs.declares_none, rel
        if not refs.legacy and not refs.unrecognized:
            assert refs.integrity_ok, rel
    print(f"shot sweep over {len(shots)} files: {dict(sorted(stats.items()))}")
    assert not any(key.startswith("parse_error:") for key in stats), dict(stats)
