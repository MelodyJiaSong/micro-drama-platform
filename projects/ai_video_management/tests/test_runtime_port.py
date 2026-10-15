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
        # Every write is origin-checked (follow-up 239); probe a PUT and a POST that
        # was unchecked before. These apps serve the REAL repo root, so each probe
        # carries an empty body: once the gate admits it, request validation fails
        # (422) before any handler or filesystem work runs.
        for method, url in (('PUT', '/api/file'), ('POST', '/api/archive-media')):
            good = client.request(method, url, json={}, headers={
                'Origin': 'http://127.0.0.1:18766', 'Host': '127.0.0.1:18766'})
            assert good.status_code == 422, (method, url, good.text)
            bad_origin = client.request(method, url, json={}, headers={
                'Origin': 'http://127.0.0.1:8766', 'Host': '127.0.0.1:18766'})
            assert bad_origin.status_code == 403, (method, url, bad_origin.text)
            bad_host = client.request(method, url, json={}, headers={'Host': '127.0.0.1:8766'})
            assert bad_host.status_code == 403, (method, url, bad_host.text)
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
