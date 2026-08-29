from __future__ import annotations

import json
from pathlib import Path

from libs.application.commands.assets__command import AssetsCommand
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace
from libs.infrastructure.daos.face__dao import FaceDao
from libs.infrastructure.daos.media__dao import MediaInfoDao
from libs.infrastructure.readers.artifact__reader import ArtifactReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter

_HERO = (1.0, 0.0)
_RIVAL = (0.0, 1.0)


class _FakeFfmpeg:
    def probe(self, path: str) -> MediaInfoDao:
        return MediaInfoDao(3.0, 720, 1280, True)

    def extract_frame(self, path: str, at_s: float, out_path: str) -> None:
        Path(out_path).write_bytes(b"png")


class _FakeFaces:
    available = True

    def detect(self, image_abs_path: str, frame_rel_path: str, at_s: float) -> list[FaceDao]:
        return [
            FaceDao(frame_rel_path, at_s, (0, 0, 10, 10), _HERO, quality=0.5 + at_s / 10),
            FaceDao(frame_rel_path, at_s, (20, 0, 30, 10), _RIVAL, quality=0.9),
        ]


class _NullFaces:
    available = False

    def detect(self, image_abs_path: str, frame_rel_path: str, at_s: float) -> list[FaceDao]:
        return []


def _cmd(tmp_path: Path, faces: object) -> tuple[AssetsCommand, SafeWorkspace]:
    ws = SafeWorkspace(root=str(tmp_path))
    writer = ArtifactWriter(ws)
    writer.write_text("d1/ep01/source.mp4", "fake")
    cmd = AssetsCommand(
        ffmpeg=_FakeFfmpeg(), faces=faces,  # type: ignore[arg-type]
        reader=ArtifactReader(ws), writer=writer,
    )
    return cmd, ws


def test_library_built_with_clusters_and_topk_refs(tmp_path: Path) -> None:
    cmd, ws = _cmd(tmp_path, _FakeFaces())
    result = cmd.build_reference_library("d1", ["d1/ep01"], force=False)
    assert result.character_count == 2
    assert result.face_count == 6  # 3 sampled frames x 2 faces
    library = json.loads(Path(ws.resolve("d1/characters/library.json")).read_text(encoding="utf-8"))
    refs = library["characters"][0]["refs"]
    assert len(refs) <= 5
    assert refs[0]["quality"] >= refs[-1]["quality"]
    assert library["characters"][0]["descriptor"] == ""  # authored later by understand stage


def test_no_face_backend_degrades_explicitly(tmp_path: Path) -> None:
    cmd, _ = _cmd(tmp_path, _NullFaces())
    result = cmd.build_reference_library("d1", ["d1/ep01"])
    assert result.character_count == 0
    assert result.degradations == ["face_backend_unavailable"]


def test_second_build_skips_idempotently(tmp_path: Path) -> None:
    cmd, _ = _cmd(tmp_path, _FakeFaces())
    first = cmd.build_reference_library("d1", ["d1/ep01"])
    second = cmd.build_reference_library("d1", ["d1/ep01"])
    assert not first.skipped and second.skipped
