from __future__ import annotations

from pathlib import Path

import pytest
from dependency_injector import providers
from fastapi.testclient import TestClient

from apps.api.app_factory import create_app
from apps.api.container import Container
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace


@pytest.fixture()
def app_ctx(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DRE_API_TOKEN", raising=False)
    container = Container()
    container.workspace.override(providers.Object(SafeWorkspace(root=str(tmp_path))))
    app = create_app(serve_static=False, container=container)
    return TestClient(app), container, tmp_path
