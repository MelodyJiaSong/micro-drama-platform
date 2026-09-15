"""DI wiring for the jimeng_web_bridge API (development.md §5).

Routes and MCP tools receive application Query/Command instances only; infrastructure
Readers/Writers/Clients are Singleton providers feeding those Factories and are imported
nowhere else under `apps/` (except transport-edge middleware and error mapping).
"""
from __future__ import annotations

import copy
import os
from collections.abc import Sequence
from pathlib import Path

from dependency_injector import containers, providers

from libs.application.commands.drama_config__command import DramaConfigCommand
from libs.application.commands.global_config__command import GlobalConfigCommand
from libs.application.commands.session__command import SessionCommand
from libs.application.mappers.drama_config__mapper import DramaConfigMapper
from libs.application.mappers.entity__mapper import EntityMapper
from libs.application.queries.artifact__query import ArtifactQuery
from libs.application.queries.drama_config__query import DramaConfigQuery
from libs.application.queries.entity__query import EntityQuery
from libs.application.queries.global_config__query import GlobalConfigQuery
from libs.application.queries.session__query import SessionQuery
from libs.application.queries.thumbnail__query import ThumbnailQuery
from libs.common.app_settings import AppSettings
from libs.common.clock import SystemClock
from libs.common.paths import RepoSandbox
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.infrastructure.clients.jimeng_browser__client import JimengBrowserClient, default_profile_dir
from libs.infrastructure.clients.jimeng_page__map import JimengPageMap
from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.daos.jimeng_page__dao import BrowserSettingsDao, StepTimeoutsDao
from libs.infrastructure.readers.batch__reader import BatchReader
from libs.infrastructure.readers.drama_config__reader import DramaConfigReader
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from libs.infrastructure.readers.global_config__reader import GlobalConfigReader
from libs.infrastructure.readers.jimeng_history__reader import RESPONSE_PATTERNS
from libs.infrastructure.readers.operation__reader import OperationReader
from libs.infrastructure.readers.shot_prompt__reader import ShotPromptReader
from libs.infrastructure.readers.store_record__reader import EntitySnapshotReader, QueueStateReader
from libs.infrastructure.readers.thumbnail__reader import ThumbnailReader
from libs.infrastructure.readers.toml_file__reader import TomlFileReader
from libs.infrastructure.writers.drama_config__writer import DramaConfigWriter
from libs.infrastructure.writers.global_config__writer import GlobalConfigWriter
from libs.infrastructure.writers.store_record__writer import EntitySnapshotWriter


def load_global_config(
    reader: GlobalConfigReader, test_mode: bool, env_overrides: Sequence[tuple[str, str]]
) -> GlobalConfig:
    """The effective global config: the TOML file with `JIMENG_BRIDGE_PROFILE_DIR` / `DREAMINA_CLI_PATH` applied."""
    data = copy.deepcopy(dict(reader.read().data))
    for dotted, value in env_overrides:
        section, key = dotted.split(".", 1)
        data[section] = {**dict(data.get(section) or {}), key: value}
    return GlobalConfig.from_dict(data, test_mode)


def build_browser_client(settings: AppSettings, config: GlobalConfig) -> JimengBrowserClient:
    """Test mode never touches the real profile or the installed Chrome: headless bundled chromium under the data dir."""
    if settings.test_mode:
        overridden = "browser.profile_dir" in settings.env_overridden_keys
        profile = Path(config.browser.profile_dir) if overridden else default_profile_dir(settings.data_dir)
        channel, headless = "chromium", True
    else:
        profile = Path(os.path.expanduser(config.browser.profile_dir))
        profile = profile if profile.is_absolute() else settings.project_root / profile
        channel, headless = config.browser.channel, False
    browser = BrowserSettingsDao(
        channel=channel, profile_dir=profile, start_url=config.browser.start_url, headless=headless, test_mode=settings.test_mode
    )
    return JimengBrowserClient(browser, JimengPageMap(), StepTimeoutsDao(), RESPONSE_PATTERNS)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["apps.api.routes"])

    settings = providers.Dependency()

    repo_root = providers.Callable(lambda s: s.repo_root, settings)
    data_dir = providers.Callable(lambda s: s.data_dir, settings)
    test_mode = providers.Callable(lambda s: s.test_mode, settings)
    global_config_path = providers.Callable(lambda s: s.global_config_path, settings)

    clock = providers.Singleton(SystemClock)
    sqlite_client = providers.Singleton(SqliteClient, db_path=providers.Callable(lambda d: d / "bridge.db", data_dir))
    sandbox = providers.Singleton(RepoSandbox, repo_root, providers.Callable(lambda d: (d,), data_dir))

    drama_tree_reader = providers.Singleton(DramaTreeReader, sandbox)
    drama_config_reader = providers.Singleton(DramaConfigReader, sandbox)
    drama_config_writer = providers.Singleton(DramaConfigWriter, sandbox)
    global_config_reader = providers.Singleton(GlobalConfigReader, global_config_path)
    global_config_writer = providers.Singleton(GlobalConfigWriter, global_config_path)
    shot_prompt_reader = providers.Singleton(ShotPromptReader, sandbox)
    toml_file_reader = providers.Singleton(TomlFileReader)
    entity_snapshot_reader = providers.Singleton(EntitySnapshotReader, sqlite_client)
    entity_snapshot_writer = providers.Singleton(EntitySnapshotWriter, sqlite_client)
    thumbnail_reader = providers.Singleton(ThumbnailReader, providers.Callable(lambda d: d / "tmp" / "thumbs", data_dir))

    drama_config_mapper = providers.Singleton(DramaConfigMapper)
    entity_mapper = providers.Singleton(EntityMapper)

    env_overrides = providers.Callable(lambda s: s.env_overrides, settings)
    global_config = providers.Callable(load_global_config, global_config_reader, test_mode, env_overrides)
    operation_reader = providers.Singleton(OperationReader, sqlite_client)
    queue_state_reader = providers.Singleton(QueueStateReader, sqlite_client)
    batch_reader = providers.Singleton(BatchReader, sqlite_client)
    browser_client = providers.Singleton(build_browser_client, settings, global_config)

    session_query = providers.Factory(
        SessionQuery,
        operation_reader,
        queue_state_reader,
        batch_reader,
        global_config.provider,
        browser_client.provider,
        clock,
        test_mode,
    )
    session_command = providers.Factory(SessionCommand, browser_client.provider)
    drama_config_query = providers.Factory(
        DramaConfigQuery,
        sandbox,
        drama_tree_reader,
        drama_config_reader,
        global_config_reader,
        shot_prompt_reader,
        entity_snapshot_reader,
        drama_config_mapper,
    )
    drama_config_command = providers.Factory(
        DramaConfigCommand, drama_config_query, drama_config_reader, drama_config_writer, toml_file_reader, drama_config_mapper
    )
    global_config_query = providers.Factory(
        GlobalConfigQuery,
        global_config_reader,
        drama_config_mapper,
        test_mode,
        env_overridden_keys=providers.Callable(lambda s: s.env_overridden_keys, settings),
        secret_values=providers.Callable(lambda s: (s.bearer_token,), settings),
    )
    global_config_command = providers.Factory(
        GlobalConfigCommand, global_config_reader, global_config_writer, toml_file_reader, drama_config_mapper, test_mode
    )
    entity_query = providers.Factory(
        EntityQuery, drama_config_query, entity_snapshot_reader, global_config_reader, clock, entity_mapper, test_mode
    )
    thumbnail_query = providers.Factory(ThumbnailQuery, sandbox, thumbnail_reader, global_config_reader, test_mode)
    artifact_query = providers.Factory(ArtifactQuery, providers.Callable(lambda d: d / "artifacts", data_dir))
