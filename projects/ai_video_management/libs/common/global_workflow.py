from __future__ import annotations

CATALOG_PATH = ".agents/references/project/workflow_catalog.json"
GLOBAL_MAX_BYTES = 1024 * 1024
GLOBAL_PREFIXES = (".agents/", ".claude/", ".codex/", "tools/", "ai_videos/_")
GLOBAL_ENTRIES = frozenset({"AGENTS.md", "CONVENTIONS.md", "CLAUDE.md", ".mcp.json"})


def source_identity(path: str, scope: str = "repo") -> str | None:
    if any(part in {"", ".", ".."} or ":" in part or "\\" in part for part in path.split("/")):
        return None
    if any(part.lower() in {"memory", "auth.json", ".auth.json", "auth.toml", "credentials.json", ".credentials.json", "credentials.toml"} or part.lower().startswith(".env") for part in path.split("/")):
        return None
    return f"{scope}:{path}" if scope in {"repo", "user"} else None


def global_source_id(path: str, scope: str = "repo", episode: str | None = None) -> str | None:
    identity = source_identity(path, scope)
    if not identity:
        return None
    if path in GLOBAL_ENTRIES or path.startswith(GLOBAL_PREFIXES):
        return identity
    if episode:
        drama = episode.split("/episodes/", 1)[0]
        local_specs = f"specs/ai_video/{drama.split('/')[-1]}/"
        if not path.startswith((f"{drama}/", local_specs, ".audit/")):
            return identity
    return None


class GlobalWorkflowError(Exception):
    def __init__(self, message: str, status_code: int = 404) -> None:
        super().__init__(message)
        self.status_code = status_code
