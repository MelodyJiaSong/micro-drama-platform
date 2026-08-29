from __future__ import annotations

from dependency_injector import providers

from libs.infrastructure.errors.ffmpeg__error import FfmpegError

_MP4_HEAD = b"\x00\x00\x00\x18ftypmp42" + b"\x00" * 8


def _create(client, drama_id: str = "d1", accepted: bool = True):
    return client.post("/api/dramas", json={
        "drama_id": drama_id, "title": "重生之逆袭", "declaration_accepted": accepted,
        "declared_by": "operator-a",
    })


def test_declaration_enforced_at_api_layer(app_ctx) -> None:
    client, _, root = app_ctx
    resp = _create(client, accepted=False)
    assert resp.status_code == 400
    assert not (root / "d1").exists()


def test_create_writes_stub_and_drama_json(app_ctx) -> None:
    client, _, root = app_ctx
    assert _create(client).status_code == 200
    assert (root / "d1/authorization_stub.json").exists()
    assert (root / "d1/drama.json").exists()


def test_chinese_title_roundtrips_utf8(app_ctx) -> None:
    client, _, root = app_ctx
    _create(client)
    assert "重生之逆袭" in (root / "d1/drama.json").read_text(encoding="utf-8")
    assert client.get("/api/dramas").json()["dramas"][0]["title"] == "重生之逆袭"


def test_drama_id_with_path_separator_rejected(app_ctx) -> None:
    client, _, _ = app_ctx
    assert _create(client, drama_id="../evil").status_code == 400


def test_upload_rejects_non_video_extension(app_ctx) -> None:
    client, _, _ = app_ctx
    _create(client)
    resp = client.post("/api/dramas/d1/upload", files={"file": ("evil.exe", b"MZ", "application/octet-stream")})
    assert resp.status_code == 400


def test_upload_rejects_mp4_extension_with_wrong_magic_bytes(app_ctx) -> None:
    client, _, _ = app_ctx
    _create(client)
    resp = client.post("/api/dramas/d1/upload",
                       files={"file": ("evil.mp4", b"MZ\x90\x00" + b"\x00" * 20, "video/mp4")})
    assert resp.status_code == 400 and "magic-byte" in resp.json()["detail"]


def test_upload_first_rejects_without_declaration_and_leaves_no_entry(app_ctx) -> None:
    client, _, _ = app_ctx
    resp = client.post("/api/uploads", files={"file": ("ok.mp4", _MP4_HEAD, "video/mp4")},
                       data={"declaration_accepted": "false"})
    assert resp.status_code == 400 and "declaration" in resp.json()["detail"]
    assert client.get("/api/dramas").json()["dramas"] == []


def test_upload_first_bad_magic_leaves_no_entry(app_ctx) -> None:
    client, _, _ = app_ctx
    resp = client.post("/api/uploads", files={"file": ("evil.mp4", b"MZ" + b"\x00" * 20, "video/mp4")},
                       data={"declaration_accepted": "true", "title": "假片"})
    assert resp.status_code == 400 and "magic-byte" in resp.json()["detail"]
    assert client.get("/api/dramas").json()["dramas"] == []


def test_upload_maps_ffmpeg_split_failure_to_400(app_ctx) -> None:
    client, container, _ = app_ctx
    _create(client)

    class _BoomIngest:
        def validate_media(self, rel_path: str, size_bytes: int):
            return type("V", (), {"ok": True, "reason": ""})()

        def split_episodes(self, drama_id: str, rel: str):
            raise FfmpegError("blackdetect", 1, "boom")

    container.ingest_command.override(providers.Object(_BoomIngest()))
    resp = client.post("/api/dramas/d1/upload", files={"file": ("ok.mp4", _MP4_HEAD, "video/mp4")})
    assert resp.status_code == 400 and "ffmpeg" in resp.json()["detail"]


def test_tree_consumer_walk_shape(app_ctx) -> None:
    """Contract test: the UI walks dramas[].children[].{episode_rel_dir,stage,...} —
    recursive descent must find every declared field (development.md move 2/3)."""
    client, container, root = app_ctx
    _create(client)
    states = container.state_writer()
    (root / "d1/ep01").mkdir(parents=True, exist_ok=True)
    states.init_state("d1/ep01")
    data = client.get("/api/dramas").json()
    assert isinstance(data["dramas"], list)
    node = data["dramas"][0]
    for key in ("drama_id", "title", "gate_a_enabled", "gate_b_enabled", "children"):
        assert key in node
    child = node["children"][0]
    for key in ("episode_rel_dir", "stage", "failed_reason", "gate_hold", "degradations",
                "busy", "shot_count", "artifacts"):
        assert key in child
    assert child["stage"] == "ingest"
    assert child["artifacts"] == {"script": False, "dialogue": False, "novel": False, "prompts": False}
