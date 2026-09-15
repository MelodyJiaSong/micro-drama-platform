from __future__ import annotations

from collections.abc import Mapping

from libs.application.dtos.drama_config__dto import ProposeCdto, SaveConfigCdto
from libs.application.mappers.drama_config__mapper import DramaConfigMapper
from libs.application.queries.drama_config__query import DramaConfigQuery
from libs.domain.errors.config__error import ConfigError
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.infrastructure.errors.config_io__error import ConfigParseError
from libs.infrastructure.readers.drama_config__reader import DramaConfigReader
from libs.infrastructure.readers.toml_file__reader import TomlFileReader
from libs.infrastructure.writers.drama_config__writer import DramaConfigWriter

BODY_FIELD: str = "<body>"


class DramaConfigCommand:
    def __init__(
        self,
        query: DramaConfigQuery,
        config_reader: DramaConfigReader,
        config_writer: DramaConfigWriter,
        toml_reader: TomlFileReader,
        mapper: DramaConfigMapper,
    ) -> None:
        self._query = query
        self._reader = config_reader
        self._writer = config_writer
        self._toml = toml_reader
        self._mapper = mapper

    def propose(self, drama_rel: str) -> ProposeCdto:
        """FR-3: never writes. A new file gets the full proposal; an existing one only a per-key diff."""
        root = self._query.drama_root(drama_rel)
        location = self._reader.config_rel(root)
        exists, current, current_sha256, parse_error = True, {}, None, None
        try:
            stored = self._reader.read(root)
            exists, current, current_sha256 = stored.exists, stored.data, stored.sha256
        except ConfigParseError as error:
            parse_error = error.detail
        proposed = self._mapper.carry_over(self._query.default_data(root), current)
        analysis = self._query.analyze(root, proposed)
        return ProposeCdto(
            drama_rel=root,
            location=location,
            exists=exists,
            current_sha256=current_sha256,
            current_parse_error=parse_error,
            proposed_data=proposed,
            proposed_toml=self._mapper.toml_text(proposed),
            diff=self._mapper.diff(current, proposed) if exists else (),
            validation_error=analysis.validation_error,
            needs_confirmation=analysis.needs_confirmation,
            entities=analysis.entities,
            reference_preview=analysis.reference_preview,
        )

    def save(
        self,
        drama_rel: str,
        data: Mapping[str, object] | None,
        text: str | None,
        expected_sha256: str | None,
    ) -> SaveConfigCdto:
        """FR-4: schema-validated before anything touches disk; a stale `expected_sha256` raises ConfigConflictError."""
        root = self._query.drama_root(drama_rel)
        if (data is None) == (text is None):
            raise ConfigError(BODY_FIELD, "data 与 text 必须且只能提供一个")
        location = self._reader.config_rel(root)
        parsed = data if text is None else self._toml.parse_document(text, location).unwrap()
        DramaConfig.from_dict(parsed, self._query.model_limits())
        if text is None:
            saved = self._writer.save(root, parsed, expected_sha256)
        else:
            saved = self._writer.save_text(root, text, expected_sha256)
        return SaveConfigCdto(drama_rel=root, location=saved.location, sha256=saved.sha256 or "")
