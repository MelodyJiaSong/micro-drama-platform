from __future__ import annotations

from dependency_injector import containers, providers

from libs.application.commands.story_run__command import StoryRunCommand
from libs.infrastructure.readers.story_runs__reader import StoryRunsReader
from libs.infrastructure.writers.story_runs__writer import StoryRunsWriter
from libs.infrastructure.readers.story_input__reader import StoryInputReader
from libs.infrastructure.readers.story_selection__reader import StorySelectionReader
from libs.infrastructure.readers.episode_workflow__reader import EpisodeWorkflowReader


class Container(containers.DeclarativeContainer):
    repo_root_path = providers.Dependency()
    reader = providers.Singleton(StoryRunsReader, repo_root=repo_root_path)
    writer = providers.Singleton(StoryRunsWriter, repo_root=repo_root_path)
    inputs = providers.Singleton(StoryInputReader, repo_root=repo_root_path)
    selections = providers.Singleton(StorySelectionReader, repo_root=repo_root_path)
    workflows = providers.Singleton(EpisodeWorkflowReader, repo_root=repo_root_path)
    command = providers.Factory(StoryRunCommand, reader=reader, writer=writer, inputs=inputs, selections=selections, workflows=workflows)
