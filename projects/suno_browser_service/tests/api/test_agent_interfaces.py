import asyncio
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from projects.suno_browser_service.tests.api.test_pipeline import live_pipeline, pipeline_site, TOKEN
from projects.suno_browser_service.libs.common.settings import REPO_ROOT


def test_mcp_and_cli_share_real_http_jobs_and_verified_downloads(live_pipeline, tmp_path, monkeypatch):
    client, settings, site = live_pipeline
    base = str(client.base_url).rstrip("/")
    monkeypatch.setenv("SUNO_SERVICE_URL", base)
    media = tmp_path / "reference.wav"
    media.write_bytes(site.audio)
    env = {**os.environ, "SUNO_SERVICE_URL": base, "SUNO_SERVICE_TOKEN": TOKEN}
    request = {"prompt": "A quiet piano", "format": "wav"}

    async def exercise() -> str:
        params = StdioServerParameters(command=sys.executable, args=[str(REPO_ROOT / "projects/suno_browser_service/apps/mcp/main.py")], env=env)
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = (await session.list_tools()).tools
                assert len(tools) == 10
                for tool in tools:
                    assert tool.description
                    assert all(field.get("description") for field in tool.inputSchema["properties"].values()), tool.name
                create_tool = next(t for t in tools if t.name == "suno_create")
                assert "references" in create_tool.inputSchema["$defs"]["GenerationRequest"]["properties"]
                capabilities = await session.call_tool("suno_capabilities", {})
                assert not capabilities.isError and "request_schema" in capabilities.structuredContent
                upload = await session.call_tool("suno_upload_reference", {"path": str(media), "rights_confirmed": True})
                assert not upload.isError
                assert upload.structuredContent["id"] == hashlib.sha256(site.audio).hexdigest()
                plan = await session.call_tool("suno_plan", {"request": {**request, "references": [{"asset_id": upload.structuredContent["id"]}], "options": {"audio_influence": 40}}})
                assert not plan.isError and plan.structuredContent["browser_called"] is False
                assert site.submissions == []
                created = await session.call_tool("suno_create", {"request": request, "idempotency_key": "mcp-once"})
                assert not created.isError
                job_id = created.structuredContent["id"]
                again = await session.call_tool("suno_create", {"request": request, "idempotency_key": "mcp-once"})
                assert again.structuredContent["id"] == job_id
                waited = await session.call_tool("suno_wait_job", {"job_id": job_id, "seconds": 45})
                assert not waited.isError and waited.structuredContent["job"]["status"] == "completed", waited
                got = await session.call_tool("suno_get_job", {"job_id": job_id})
                assert got.structuredContent["next_action"] == "download_files"
                downloaded = await session.call_tool("suno_download", {"job_id": job_id, "output_directory": str(tmp_path / "delivered")})
                assert not downloaded.isError
                assert len(downloaded.structuredContent["files"]) == 2
                for item in downloaded.structuredContent["files"]:
                    assert Path(item["path"]).read_bytes() == site.audio
                assert not (await session.call_tool("suno_list_jobs", {})).isError
                assert (await session.call_tool("suno_resume_job", {"job_id": job_id, "song_urls": []})).isError
                return job_id

    job_id = asyncio.run(exercise())
    cli = REPO_ROOT / "projects/suno_browser_service/apps/cli/main.py"
    result = subprocess.run([sys.executable, str(cli), "get", "--job", job_id], env=env, capture_output=True, text=True, encoding="utf-8", timeout=20)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["result"]["status"] == "completed"
    invalid = subprocess.run([sys.executable, str(cli), "get", "--job", "invalid"], env=env, capture_output=True, text=True, encoding="utf-8", timeout=20)
    assert invalid.returncode == 1 and json.loads(invalid.stdout)["error"]["code"] == "invalid_job_id"
    assert TOKEN not in result.stdout + result.stderr + invalid.stdout + invalid.stderr
    assert len(site.submissions) == 1
