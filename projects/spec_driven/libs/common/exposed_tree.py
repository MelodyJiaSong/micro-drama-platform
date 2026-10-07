from __future__ import annotations

from pathlib import Path

CANONICAL_STAGES: list[str] = [
    "user_input",
    "interview",
    "findings",
    "final_specs",
    "validation",
]
SCRATCH_DIRNAME: str = "__scratch__"
ALLOWED_EXTENSIONS: frozenset[str] = frozenset(
    {".md", ".json", ".yaml", ".yml", ".jsonl", ".txt", ".png", ".jpg"}
)
MAX_FILE_BYTES: int = 1_048_576
CONTEXT_ROOT_FILES: tuple[str, ...] = ("AGENTS.md", "CONVENTIONS.md", "CLAUDE.md")
CONTEXT_DIRS: dict[str, frozenset[str]] = {
    ".agents": frozenset({"skills", "references"}),
    ".claude": frozenset({"skills"}),
}
CONTEXT_FILES: frozenset[str] = frozenset({".agents/skill-aliases.json"})

_EXCLUDED_DIRS: frozenset[str] = frozenset(
    {"node_modules", ".git", ".audit", "__pycache__", ".pytest_cache", "dist", "build", ".vite"}
)


class ExposedTree:
    def __init__(self, repo_root: Path) -> None:
        self._root = repo_root.resolve()

    @property
    def root(self) -> Path:
        return self._root

    def context_root_files(self) -> list[Path]:
        return [self._root / name for name in CONTEXT_ROOT_FILES if (self._root / name).is_file()]

    def shared_skill_files(self) -> list[Path]:
        skills_dir = self._root / ".agents" / "skills"
        if not skills_dir.is_dir():
            return []
        return sorted(p for p in skills_dir.rglob("*.md") if p.is_file())

    def shared_references(self) -> list[Path]:
        refs_dir = self._root / ".agents" / "references"
        if not refs_dir.is_dir():
            return []
        return sorted(p for p in refs_dir.rglob("*.md") if p.is_file())

    def project_dirs(self) -> list[Path]:
        projects_root = self._root / "projects"
        if not projects_root.is_dir():
            return []
        return sorted(p for p in projects_root.iterdir() if p.is_dir())

    def project_stage_dirs(self, project_dir: Path) -> list[Path]:
        return [project_dir / s for s in CANONICAL_STAGES if (project_dir / s).is_dir()]

    def is_inside(self, rel: str) -> bool:
        if not rel or rel.startswith("/") or "\\" in rel or "\x00" in rel:
            return False
        candidate = (self._root / rel).resolve(strict=False)
        if not (candidate == self._root or self._root in candidate.parents):
            return False
        try:
            relative = candidate.relative_to(self._root)
        except ValueError:
            return False
        parts = relative.parts
        if not parts:
            return False
        first = parts[0]
        if first in CONTEXT_ROOT_FILES:
            return True
        if first in CONTEXT_DIRS:
            return relative.as_posix() in CONTEXT_FILES or (
                len(parts) >= 2 and parts[1] in CONTEXT_DIRS[first]
            )
        if first == "specs":
            return True
        if first == "projects":
            for seg in parts:
                if seg in _EXCLUDED_DIRS:
                    return False
            return True
        if first == "prompt_lab":
            for seg in parts:
                if seg in _EXCLUDED_DIRS:
                    return False
            return True
        return False

    def excluded_dirs(self) -> frozenset[str]:
        return _EXCLUDED_DIRS
