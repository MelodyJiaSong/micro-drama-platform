from __future__ import annotations

import os

from dependency_injector import containers, providers

from libs.application.commands.probe__command import ProbeCommand
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace
from libs.infrastructure.clients.gemini__client import GeminiClient
from libs.infrastructure.clients.qwen__client import QwenClient


class ProbeContainer(containers.DeclarativeContainer):
    workspace = providers.Singleton(
        SafeWorkspace,
        root=providers.Callable(lambda: os.environ.get("DRE_WORKSPACE", os.path.join(os.getcwd(), "workspace"))),
    )
    gemini = providers.Singleton(GeminiClient, api_key=providers.Callable(lambda: os.environ.get("GEMINI_API_KEY", "")))
    qwen = providers.Singleton(QwenClient, api_key=providers.Callable(lambda: os.environ.get("DASHSCOPE_API_KEY", "")))
    probe_command = providers.Factory(ProbeCommand, gemini=gemini, qwen=qwen, workspace=workspace)
