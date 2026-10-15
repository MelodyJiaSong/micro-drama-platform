from __future__ import annotations

CATALOG_PATH = ".agents/references/project/workflow_catalog.json"
GLOBAL_MAX_BYTES = 1024 * 1024


def source_identity(path: str, scope: str = "repo") -> str | None:
    if any(part in {"", ".", ".."} or ":" in part or "\\" in part for part in path.split("/")):
        return None
    if any(part.lower() in {"memory", "auth.json", ".auth.json", "auth.toml", "credentials.json", ".credentials.json", "credentials.toml"} or part.lower().startswith(".env") for part in path.split("/")):
        return None
    return f"{scope}:{path}" if scope in {"repo", "user"} else None


class GlobalWorkflowError(Exception):
    def __init__(self, message: str, status_code: int = 404) -> None:
        super().__init__(message)
        self.status_code = status_code
