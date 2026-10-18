"""DI wiring for the ai_video_management API.

Per follow-ups 051 + 060 + 061: route handlers receive aggregate-level
application Query / Command instances (one Factory per aggregate). Each
aggregate class exposes one method per operation. The infrastructure
Readers / Writers are Singleton providers feeding into those Factories. The
route layer does NOT import infrastructure classes — see apps/api/routes/.

Per follow-up 062: routes split into apps/api/routes/{aggregate}__route.py.
`wiring_config` uses `packages=` so every per-aggregate route module's
@inject decorators bind automatically.

Follow-up 233 removed the providers of every old-pipeline feature; what is
left serves the episode workflow, the global workflow catalog, request logs,
the file tree / file / media browsing, the Downloads import, character view
extraction and the topic research workspace.
"""
from __future__ import annotations

from pathlib import Path

from dependency_injector import containers, providers

from libs.application.commands.character_video__command import CharacterVideoCommand
from libs.application.commands.downloads__command import DownloadsCommand
from libs.application.commands.episode_workflow__command import EpisodeWorkflowCommand
from libs.application.commands.file__command import FileCommand
from libs.application.commands.media__command import MediaCommand
from libs.application.commands.research__command import ResearchCommand
from libs.application.commands.review_reel__command import ReviewReelCommand
from libs.application.commands.shot_take__command import ShotTakeCommand
from libs.application.queries.character__query import CharacterQuery
from libs.application.queries.episode_workflow__query import EpisodeWorkflowQuery
from libs.application.queries.file__query import FileQuery
from libs.application.queries.global_workflow__query import GlobalWorkflowQuery
from libs.application.queries.media__query import MediaQuery
from libs.application.queries.request_log__query import RequestLogQuery
from libs.application.queries.research__query import ResearchQuery
from libs.application.queries.review_reel__query import ReviewReelQuery
from libs.application.queries.scene_cut__query import SceneCutQuery
from libs.application.queries.tree__query import TreeQuery
from libs.common.exposed_tree import ExposedTree
from libs.common.origin import BoundOrigin
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.readers.character__reader import CharacterReader
from libs.infrastructure.readers.episode_workflow__reader import EpisodeWorkflowReader
from libs.infrastructure.readers.equipment_route__reader import EquipmentKeyRouter
from libs.infrastructure.readers.file__reader import FileReader
from libs.infrastructure.readers.global_workflow__reader import GlobalWorkflowReader
from libs.infrastructure.readers.prop_route__reader import PropKeyRouter
from libs.infrastructure.readers.request_log__reader import RequestLogReader
from libs.infrastructure.readers.research__reader import ResearchReader
from libs.infrastructure.readers.review_reel__reader import ReviewReelReader
from libs.infrastructure.readers.scene_cut__reader import SceneCutReader
from libs.infrastructure.readers.scene_registry__reader import SceneRegistryReader
from libs.infrastructure.readers.scene_route__reader import SceneKeyRouter
from libs.infrastructure.readers.shot_materials__reader import ShotMaterialsReader
from libs.infrastructure.readers.tree__reader import TreeReader
from libs.infrastructure.writers.character_video__writer import CharacterViewExtractor
from libs.infrastructure.writers.downloads__writer import DownloadsImporter
from libs.infrastructure.writers.episode_workflow__writer import EpisodeWorkflowWriter
from libs.infrastructure.writers.file__writer import FileWriter
from libs.infrastructure.writers.media__writer import MediaArchiver, MediaRenamer
from libs.infrastructure.writers.research__writer import ResearchWriter
from libs.infrastructure.writers.review_reel__writer import ReviewReelWriter
from libs.infrastructure.writers.shot_take__writer import ShotTakeWriter
from libs.infrastructure.watchers.file_change__watcher import FileChangeWatcher


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["apps.api.routes"])

    repo_root_path: providers.Dependency[Path] = providers.Dependency()
    bound_origin: providers.Dependency[BoundOrigin] = providers.Dependency()

    # --- Episode workflow (three-module-v1) + global workflow catalog ---------
    episode_workflow_reader = providers.Singleton(EpisodeWorkflowReader, repo_root=repo_root_path)
    episode_workflow_writer = providers.Singleton(EpisodeWorkflowWriter, repo_root=repo_root_path)
    shot_materials_reader = providers.Singleton(ShotMaterialsReader, repo_root=repo_root_path)
    episode_workflow_query = providers.Factory(EpisodeWorkflowQuery, reader=episode_workflow_reader)
    episode_workflow_command = providers.Factory(EpisodeWorkflowCommand, reader=episode_workflow_reader, writer=episode_workflow_writer,
                                                 materials=shot_materials_reader)
    # 整集审片串联（follow-up 260）：writer 是单例，记着正在拼的任务
    review_reel_reader = providers.Singleton(ReviewReelReader, repo_root=repo_root_path)
    review_reel_writer = providers.Singleton(ReviewReelWriter, repo_root=repo_root_path)
    review_reel_query = providers.Factory(ReviewReelQuery, reader=review_reel_reader)
    review_reel_command = providers.Factory(ReviewReelCommand, reader=review_reel_reader, writer=review_reel_writer)
    scene_cut_reader = providers.Singleton(SceneCutReader, repo_root=repo_root_path)
    scene_cut_query = providers.Factory(SceneCutQuery, reader=scene_cut_reader)
    # 草稿条的用户审核（follow-up 265）
    shot_take_writer = providers.Singleton(ShotTakeWriter, repo_root=repo_root_path)
    shot_take_command = providers.Factory(ShotTakeCommand, writer=shot_take_writer)
    global_workflow_reader = providers.Singleton(GlobalWorkflowReader, repo_root=repo_root_path)
    global_workflow_query = providers.Factory(GlobalWorkflowQuery, reader=global_workflow_reader)

    # --- Infrastructure singletons -----------------------------------------
    exposed_tree: providers.Singleton[ExposedTree] = providers.Singleton(
        ExposedTree, repo_root=repo_root_path
    )
    safe_resolver: providers.Singleton[SafeResolver] = providers.Singleton(
        SafeResolver, root=repo_root_path
    )

    file_reader: providers.Singleton[FileReader] = providers.Singleton(
        FileReader, exposed=exposed_tree, resolver=safe_resolver
    )
    file_writer: providers.Singleton[FileWriter] = providers.Singleton(
        FileWriter, exposed=exposed_tree, resolver=safe_resolver
    )
    scene_registry_reader: providers.Singleton[SceneRegistryReader] = providers.Singleton(
        SceneRegistryReader
    )
    tree_reader: providers.Singleton[TreeReader] = providers.Singleton(
        TreeReader, exposed=exposed_tree, scene_registry=scene_registry_reader
    )
    # Live updates (follow-up 280): one ai_videos/ watcher per process, fanned out to /api/events.
    file_change_watcher: providers.Singleton[FileChangeWatcher] = providers.Singleton(
        FileChangeWatcher, exposed=exposed_tree
    )
    media_renamer: providers.Singleton[MediaRenamer] = providers.Singleton(
        MediaRenamer, exposed=exposed_tree, resolver=safe_resolver
    )
    media_archiver: providers.Singleton[MediaArchiver] = providers.Singleton(
        MediaArchiver, exposed=exposed_tree, resolver=safe_resolver
    )
    research_reader: providers.Singleton[ResearchReader] = providers.Singleton(
        ResearchReader, repo_root=repo_root_path
    )
    research_writer: providers.Singleton[ResearchWriter] = providers.Singleton(
        ResearchWriter, repo_root=repo_root_path, reader=research_reader
    )
    scene_key_router: providers.Singleton[SceneKeyRouter] = providers.Singleton(SceneKeyRouter)
    prop_key_router: providers.Singleton[PropKeyRouter] = providers.Singleton(PropKeyRouter)
    equipment_key_router: providers.Singleton[EquipmentKeyRouter] = providers.Singleton(EquipmentKeyRouter)
    downloads_importer: providers.Singleton[DownloadsImporter] = providers.Singleton(
        DownloadsImporter,
        exposed=exposed_tree,
        resolver=safe_resolver,
        renamer=media_renamer,
        scene_router=scene_key_router,
        prop_router=prop_key_router,
        equipment_router=equipment_key_router,
    )
    character_view_extractor: providers.Singleton[CharacterViewExtractor] = providers.Singleton(
        CharacterViewExtractor, exposed=exposed_tree, resolver=safe_resolver
    )
    character_reader: providers.Singleton[CharacterReader] = providers.Singleton(
        CharacterReader, exposed=exposed_tree, resolver=safe_resolver
    )
    request_log_reader = providers.Singleton(RequestLogReader, exposed_tree=exposed_tree)

    # --- Application-layer factories: one per aggregate Q/C -----------------
    media_command: providers.Factory[MediaCommand] = providers.Factory(
        MediaCommand, archiver=media_archiver, renamer=media_renamer
    )
    media_query: providers.Factory[MediaQuery] = providers.Factory(
        MediaQuery, exposed=exposed_tree, resolver=safe_resolver
    )
    file_command: providers.Factory[FileCommand] = providers.Factory(
        FileCommand, writer=file_writer
    )
    file_query: providers.Factory[FileQuery] = providers.Factory(
        FileQuery, reader=file_reader
    )
    tree_query: providers.Factory[TreeQuery] = providers.Factory(
        TreeQuery, reader=tree_reader
    )
    request_log_query = providers.Factory(RequestLogQuery, reader=request_log_reader)
    research_query: providers.Factory[ResearchQuery] = providers.Factory(
        ResearchQuery, reader=research_reader, writer=research_writer
    )
    research_command: providers.Factory[ResearchCommand] = providers.Factory(
        ResearchCommand, writer=research_writer
    )
    downloads_command: providers.Factory[DownloadsCommand] = providers.Factory(
        DownloadsCommand, importer=downloads_importer
    )
    character_video_command: providers.Factory[CharacterVideoCommand] = providers.Factory(
        CharacterVideoCommand, extractor=character_view_extractor
    )
    character_query: providers.Factory[CharacterQuery] = providers.Factory(
        CharacterQuery, reader=character_reader
    )
