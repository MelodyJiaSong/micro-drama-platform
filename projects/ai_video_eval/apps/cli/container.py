import os

from dependency_injector import containers, providers

from libs.application.commands.dispute__command import DisputeCommand
from libs.application.commands.eval_run__command import EvalRunCommand
from libs.application.mappers.grounding__mapper import GroundingMapper
from libs.application.mappers.judge__mapper import JudgeMapper
from libs.application.mappers.rubric__mapper import RubricMapper
from libs.application.mappers.shot__mapper import ShotMapper
from libs.application.mappers.verdict__mapper import VerdictMapper
from libs.application.queries.report__query import ReportQuery
from libs.application.queries.trends__query import TrendsQuery
from libs.infrastructure.clients.anthropic__client import AnthropicClient
from libs.infrastructure.clients.claude_code__client import ClaudeCodeClient
from libs.infrastructure.readers.canon__reader import CanonReader
from libs.infrastructure.readers.config__reader import ConfigReader
from libs.infrastructure.readers.layout__reader import LayoutReader
from libs.infrastructure.readers.rubric__reader import RubricReader
from libs.infrastructure.readers.run__reader import RunReader
from libs.infrastructure.readers.script__reader import ScriptReader
from libs.infrastructure.readers.shot__reader import ShotReader
from libs.infrastructure.writers.report__writer import ReportWriter
from libs.infrastructure.writers.run__writer import RunWriter

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _load_config():
    return ConfigReader(PROJECT_ROOT).read()


def _load_rubric():
    top, dims, content_hash = RubricReader(os.path.join(PROJECT_ROOT, "rubric")).read()
    return RubricMapper().map(top, dims, content_hash)


def _make_client(config):
    if config.judge_engine == "claude_code":
        return ClaudeCodeClient(config)
    return AnthropicClient(config)


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(_load_config)
    rubric = providers.Singleton(_load_rubric)

    layout_reader = providers.Singleton(
        LayoutReader, videos_root=providers.Callable(lambda c: c.videos_root, config)
    )
    shot_reader = providers.Singleton(ShotReader)
    canon_reader = providers.Singleton(CanonReader)
    script_reader = providers.Singleton(ScriptReader)
    run_reader = providers.Singleton(
        RunReader, runs_dir=providers.Callable(lambda c: c.runs_dir, config)
    )
    run_writer = providers.Singleton(
        RunWriter, runs_dir=providers.Callable(lambda c: c.runs_dir, config)
    )
    report_writer = providers.Singleton(ReportWriter)
    client = providers.Singleton(_make_client, config)

    shot_mapper = providers.Singleton(ShotMapper)
    grounding_mapper = providers.Singleton(
        GroundingMapper, config=providers.Callable(lambda c: c.grounding, config)
    )
    judge_mapper = providers.Singleton(JudgeMapper)
    verdict_mapper = providers.Singleton(VerdictMapper)

    eval_run_command = providers.Factory(
        EvalRunCommand,
        config=config,
        rubric=rubric,
        layout_reader=layout_reader,
        shot_reader=shot_reader,
        canon_reader=canon_reader,
        script_reader=script_reader,
        run_reader=run_reader,
        run_writer=run_writer,
        report_writer=report_writer,
        client=client,
        shot_mapper=shot_mapper,
        grounding_mapper=grounding_mapper,
        judge_mapper=judge_mapper,
        verdict_mapper=verdict_mapper,
    )
    dispute_command = providers.Factory(DisputeCommand, config=config, run_reader=run_reader)
    report_query = providers.Factory(
        ReportQuery,
        runs_dir=providers.Callable(lambda c: c.runs_dir, config),
        run_reader=run_reader,
    )
    trends_query = providers.Factory(TrendsQuery, run_reader=run_reader)
