from __future__ import annotations

from libs.infrastructure.readers.artifact__reader import ArtifactReader

_TEXT_SUFFIXES = (".md", ".json", ".jsonl", ".txt")


class ArtifactQuery:
    """Read any workspace artifact for the UI (path already sandboxed by SafeWorkspace)."""

    def __init__(self, artifacts: ArtifactReader) -> None:
        self._artifacts = artifacts

    def read_text(self, rel_path: str) -> str | None:
        if not rel_path.endswith(_TEXT_SUFFIXES):
            return None
        if not self._artifacts.exists(rel_path):
            return None
        return self._artifacts.read_text(rel_path)

    def shot_files(self, episode_rel_dir: str) -> list[str]:
        manifest_rel = f"{episode_rel_dir}/compose_manifest.json"
        if not self._artifacts.exists(manifest_rel):
            return []
        return list(self._artifacts.read_json(manifest_rel)["shot_files"])
