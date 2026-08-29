from __future__ import annotations

import os

from dependency_injector import containers, providers

from libs.application.commands.assets__command import AssetsCommand
from libs.application.commands.compose__command import ComposeCommand
from libs.application.commands.drama__command import DramaCommand
from libs.application.commands.export__command import ExportCommand
from libs.application.commands.extract__command import ExtractCommand
from libs.application.commands.gate__command import GateCommand
from libs.application.commands.ingest__command import IngestCommand
from libs.application.commands.pipeline__command import PipelineCommand
from libs.application.commands.understand__command import UnderstandCommand
from libs.application.queries.artifact__query import ArtifactQuery
from libs.application.queries.drama__query import DramaQuery
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace
from libs.infrastructure.clients.ark__client import ArkClient
from libs.infrastructure.clients.asr__client import NullAsrTranscriber
from libs.infrastructure.clients.claude_composer__client import ClaudeLlmComposer
from libs.infrastructure.clients.claude_subtitle__client import ClaudeSubtitleExtractor
from libs.infrastructure.clients.claude_understanding__client import ClaudeVideoUnderstanding
from libs.infrastructure.clients.claudecli__client import ClaudeCliClient
from libs.infrastructure.clients.doubao_composer__client import DoubaoLlmComposer
from libs.infrastructure.clients.faceengine__client import NullFaceEngine
from libs.infrastructure.clients.ffmpeg__client import FfmpegClient
from libs.infrastructure.clients.gemini_understanding__client import GeminiVideoUnderstanding, QwenVideoUnderstanding
from libs.infrastructure.clients.shotdetect__client import FfmpegSceneShotDetector
from libs.infrastructure.clients.subtitle__client import NullSubtitleExtractor
from libs.infrastructure.clients.understanding__client import FallbackVideoUnderstanding
from libs.infrastructure.readers.artifact__reader import ArtifactReader
from libs.infrastructure.readers.pipelinestate__reader import PipelineStateReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter
from libs.infrastructure.writers.pipelinestate__writer import PipelineStateWriter


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


class Container(containers.DeclarativeContainer):
    """Composition root for the reverse-engineering service. Heavy/optional backends
    default to Null seams; real backends switch in via env keys (NFR-O1). OCR/ASR/
    InsightFace remain Null in the default install — the pipeline degrades per-column/
    per-stage, loudly. (Seedance/Seedream generation providers removed, follow-up 001.)
    LLM layer (follow-up 002): understand + compose default to the local Claude Code
    CLI (zero key); DRE_UNDERSTANDING=gemini_qwen / DRE_COMPOSER=doubao switch back
    to the keyed HTTP backends."""

    wiring_config = containers.WiringConfiguration(packages=["apps.api.routes"])

    workspace = providers.Singleton(
        SafeWorkspace, root=providers.Callable(lambda: _env("DRE_WORKSPACE", os.path.join(os.getcwd(), "workspace")))
    )
    artifact_reader = providers.Singleton(ArtifactReader, workspace=workspace)
    artifact_writer = providers.Singleton(ArtifactWriter, workspace=workspace)
    state_reader = providers.Singleton(PipelineStateReader, workspace=workspace)
    state_writer = providers.Singleton(PipelineStateWriter, workspace=workspace)

    ffmpeg = providers.Singleton(FfmpegClient)
    ark = providers.Singleton(ArkClient, api_key=providers.Callable(lambda: _env("ARK_API_KEY")))
    claude_cli = providers.Singleton(
        ClaudeCliClient,
        binary=providers.Callable(lambda: _env("DRE_CLAUDE_BIN", "claude")),
        model=providers.Callable(lambda: _env("DRE_CLAUDE_MODEL", "sonnet")),
    )

    shot_detector = providers.Singleton(FfmpegSceneShotDetector, ffmpeg=ffmpeg)
    subtitles = providers.Selector(
        providers.Callable(lambda: _env("DRE_SUBTITLES", "claude")),
        claude=providers.Singleton(ClaudeSubtitleExtractor, cli=claude_cli, ffmpeg=ffmpeg),
        null=providers.Singleton(NullSubtitleExtractor),
    )
    asr = providers.Singleton(NullAsrTranscriber)
    faces = providers.Singleton(NullFaceEngine)
    gemini_vlm = providers.Singleton(
        GeminiVideoUnderstanding, api_key=providers.Callable(lambda: _env("GEMINI_API_KEY"))
    )
    qwen_vlm = providers.Singleton(
        QwenVideoUnderstanding, api_key=providers.Callable(lambda: _env("DASHSCOPE_API_KEY"))
    )
    vlm = providers.Selector(
        providers.Callable(lambda: _env("DRE_UNDERSTANDING", "claude")),
        claude=providers.Singleton(ClaudeVideoUnderstanding, cli=claude_cli, ffmpeg=ffmpeg),
        gemini_qwen=providers.Singleton(FallbackVideoUnderstanding, primary=gemini_vlm, fallback=qwen_vlm),  # FR-4.4
    )
    composer = providers.Selector(
        providers.Callable(lambda: _env("DRE_COMPOSER", "claude")),
        claude=providers.Singleton(ClaudeLlmComposer, cli=claude_cli),
        doubao=providers.Singleton(DoubaoLlmComposer, ark=ark),
    )

    ingest_command = providers.Factory(IngestCommand, ffmpeg=ffmpeg, writer=artifact_writer)
    extract_command = providers.Factory(
        ExtractCommand, ffmpeg=ffmpeg, detector=shot_detector, subtitles=subtitles, asr=asr,
        reader=artifact_reader, writer=artifact_writer,
    )
    assets_command = providers.Factory(
        AssetsCommand, ffmpeg=ffmpeg, faces=faces, reader=artifact_reader, writer=artifact_writer,
    )
    understand_command = providers.Factory(
        UnderstandCommand, ffmpeg=ffmpeg, vlm=vlm, composer=composer,
        reader=artifact_reader, writer=artifact_writer,
    )
    compose_command = providers.Factory(
        ComposeCommand, composer=composer, reader=artifact_reader, writer=artifact_writer,
    )
    pipeline_command = providers.Factory(
        PipelineCommand, extract=extract_command, assets=assets_command, understand=understand_command,
        compose=compose_command, reader=artifact_reader, writer=artifact_writer,
        state_reader=state_reader, state_writer=state_writer,
    )
    drama_command = providers.Factory(
        DramaCommand, ingest=ingest_command, writer=artifact_writer, states=state_writer, workspace=workspace,
    )
    gate_command = providers.Factory(
        GateCommand, reader=state_reader, states=state_writer, writer=artifact_writer,
        artifacts=artifact_reader, workspace=workspace,
    )
    export_command = providers.Factory(ExportCommand, workspace=workspace)
    drama_query = providers.Factory(DramaQuery, states=state_reader, artifacts=artifact_reader)
    artifact_query = providers.Factory(ArtifactQuery, artifacts=artifact_reader)
