"""Both startup paths must use the configured port for the Origin/Host gate."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


def test_custom_port_in_both_startup_paths() -> None:
    script = """
from fastapi.testclient import TestClient
from apps.api import main, asgi
assert main.PORT == asgi.PORT == 18766
for app in (main.create_app(main._build_container(False), serve_static=False), asgi.app):
    with TestClient(app) as client:
        # A nonexistent endpoint isolates Origin validation from filesystem work.
        good = client.post('/api/not-an-endpoint', headers={
            'Origin': 'http://127.0.0.1:18766', 'Host': '127.0.0.1:18766'})
        assert good.status_code == 404, good.text
        bad = client.post('/api/not-an-endpoint', headers={
            'Origin': 'http://127.0.0.1:8766', 'Host': '127.0.0.1:18766'})
        assert bad.status_code == 403, bad.text
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=Path(__file__).resolve().parents[1],
        env={**os.environ, "BACKEND_PORT": "18766"},
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
