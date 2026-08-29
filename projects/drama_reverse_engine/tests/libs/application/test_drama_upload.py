from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from libs.application.commands.drama__command import DramaCommand
from libs.domain.errors.workspace__error import WorkspaceError
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace
from libs.infrastructure.daos.media__dao import MediaInfoDao
from libs.infrastructure.writers.artifact__writer import ArtifactWriter
from libs.infrastructure.writers.pipelinestate__writer import PipelineStateWriter

_MP4_HEAD = b"\x00\x00\x00\x18ftypmp42" + b"\x00" * 8


class _FakeIngest:
    def validate_media(self, rel_path: str, size_bytes: int):
        return MediaInfoDao and type("V", (), {"ok": True, "duration_s": 120.0, "width": 720,
                                                "height": 1280, "reason": ""})()

    def split_episodes(self, drama_id: str, rel: str):
        return type("S", (), {"episode_rel_paths": [f"{drama_id}/ep01/source.mp4"], "confidences": ["high"]})()


def _cmd(tmp_path: Path) -> tuple[DramaCommand, Path]:
    ws = SafeWorkspace(root=str(tmp_path))
    return DramaCommand(ingest=_FakeIngest(), writer=ArtifactWriter(ws),  # type: ignore[arg-type]
                        states=PipelineStateWriter(ws), workspace=ws), tmp_path


async def _aiter(chunks):
    for chunk in chunks:
        yield chunk


def _upload(cmd: DramaCommand, drama_id: str, name: str, chunks, **kw):
    return asyncio.run(cmd.stream_upload(drama_id, name, _aiter(chunks), **kw))


def test_oversize_upload_aborted_midstream_and_file_deleted(tmp_path: Path) -> None:
    cmd, root = _cmd(tmp_path)
    chunks = (_MP4_HEAD + b"a" * 100, b"b" * 100, b"c" * 100)
    with pytest.raises(WorkspaceError, match="2GB"):
        _upload(cmd, "d1", "big.mp4", chunks, max_bytes=len(_MP4_HEAD) + 150)
    assert not (root / "d1/uploads/big.mp4").exists()  # partial file cleaned up


def test_non_mp4_magic_bytes_rejected_and_deleted(tmp_path: Path) -> None:
    cmd, root = _cmd(tmp_path)
    with pytest.raises(WorkspaceError, match="magic-byte"):
        _upload(cmd, "d1", "evil.mp4", [b"MZ\x90\x00" + b"\x00" * 20])
    assert not (root / "d1/uploads/evil.mp4").exists()


def test_valid_mp4_streams_and_registers_episodes(tmp_path: Path) -> None:
    cmd, _ = _cmd(tmp_path)
    assert _upload(cmd, "d1", "ok.mp4", [_MP4_HEAD + b"payload"]) == ["d1/ep01"]


def test_valid_mp4_in_tiny_chunks_not_falsely_rejected(tmp_path: Path) -> None:
    """Header split across sub-12-byte chunks must still pass (validator-13 minor)."""
    cmd, _ = _cmd(tmp_path)
    tiny = [_MP4_HEAD[i:i + 3] for i in range(0, len(_MP4_HEAD), 3)] + [b"payload"]
    assert _upload(cmd, "d1", "tiny.mp4", tiny) == ["d1/ep01"]


def test_reject_drains_remaining_stream_before_raising(tmp_path: Path) -> None:
    """A mid-stream reject must consume the rest of the body — otherwise the HTTP
    layer resets the connection and the browser sees "Failed to fetch", not the 400."""
    cmd, _ = _cmd(tmp_path)
    consumed: list[bytes] = []

    async def _gen():
        for chunk in (b"MZ\x90\x00" + b"\x00" * 20, b"tail1", b"tail2"):
            consumed.append(chunk)
            yield chunk

    with pytest.raises(WorkspaceError, match="magic-byte"):
        asyncio.run(cmd.stream_upload("d1", "evil.mp4", _gen()))
    assert len(consumed) == 3


def test_create_and_upload_builds_entry_from_filename(tmp_path: Path) -> None:
    """Follow-up 003: one upload = one new entry; id auto-derived, title = filename."""
    cmd, root = _cmd(tmp_path)

    async def _run():
        return await cmd.create_and_upload("My剧集01.mp4", "", True, "operator", _aiter([_MP4_HEAD]))

    drama_id, title, episodes = asyncio.run(_run())
    assert drama_id.startswith("my_") and title == "My剧集01"
    assert (root / drama_id / "drama.json").exists()
    assert (root / drama_id / "authorization_stub.json").exists()
    assert episodes == [f"{drama_id}/ep01"]


def test_create_and_upload_rejected_file_removes_entry(tmp_path: Path) -> None:
    cmd, root = _cmd(tmp_path)

    async def _run():
        return await cmd.create_and_upload("evil.mp4", "", True, "operator",
                                           _aiter([b"MZ\x90\x00" + b"\x00" * 20]))

    with pytest.raises(WorkspaceError, match="magic-byte"):
        asyncio.run(_run())
    assert not any(p.name != "uploads" for p in root.iterdir()), list(root.iterdir())  # no orphan entry


def test_create_and_upload_requires_declaration(tmp_path: Path) -> None:
    cmd, root = _cmd(tmp_path)

    async def _run():
        return await cmd.create_and_upload("ok.mp4", "", False, "operator", _aiter([_MP4_HEAD]))

    with pytest.raises(WorkspaceError, match="declaration"):
        asyncio.run(_run())
    assert list(root.iterdir()) == []


def test_filename_traversal_stripped(tmp_path: Path) -> None:
    cmd, root = _cmd(tmp_path)
    _upload(cmd, "d1", "../../etc/passwd.mp4", [_MP4_HEAD])
    assert (root / "d1/uploads/passwd.mp4").exists()
    assert not (tmp_path.parent / "etc").exists()
