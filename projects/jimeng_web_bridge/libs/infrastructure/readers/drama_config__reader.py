from __future__ import annotations

from libs.common import drama_ref
from libs.common.paths import RepoSandbox
from libs.infrastructure.daos.config_file__dao import ConfigFileDao
from libs.infrastructure.errors.config_io__error import DramaRootNotFoundError
from libs.infrastructure.errors.sandbox__error import SandboxError
from libs.infrastructure.readers.toml_file__reader import TomlFileReader


class DramaConfigReader:
    def __init__(self, sandbox: RepoSandbox) -> None:
        self._sandbox: RepoSandbox = sandbox
        self._toml: TomlFileReader = TomlFileReader()

    def config_rel(self, drama_rel: str) -> str:
        if (
            drama_ref.canonical_rel_violation(drama_rel) is not None
            or drama_ref.drama_root_rel(self._sandbox.repo_root, drama_rel.split("/")) != drama_rel
        ):
            raise DramaRootNotFoundError(drama_rel)
        return f"{drama_rel}/{drama_ref.DRAMA_CONFIG_NAME}"

    def read(self, drama_rel: str) -> ConfigFileDao:
        rel = self.config_rel(drama_rel)
        verdict = self._sandbox.check_read(rel)
        if verdict.path is None:
            raise SandboxError(verdict.violation or "rejected", verdict.rel)
        # A case variant or 8.3 short name resolves elsewhere than the canonical rel it claims to be.
        if verdict.rel != rel or not verdict.path.parent.is_dir():
            raise DramaRootNotFoundError(drama_rel)
        return self._toml.read(verdict.path, rel)
