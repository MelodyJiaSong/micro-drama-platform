"""`.glb` / `.gltf` ride the media path so white-model meshes preview in the UI.

The mesh is what image-to-3D hands back; being able to judge it (thin structures,
silhouette, wheel arches) in the browser is what keeps the user out of Blender for
the accept/reject decision. Served `inline` — an `attachment` disposition would make
the browser download it instead of letting <model-viewer> fetch it.
"""
from __future__ import annotations

from pathlib import Path

from libs.common.exposed_tree import (
    ALLOWED_EXTENSIONS,
    MEDIA_EXTENSIONS,
    TREE_VISIBLE_EXTENSIONS,
    ExposedTree,
)
from libs.common.safe_resolve import SafeResolver
from libs.application.queries.media__query import MediaQuery
from libs.domain.value_objects.media__valueobject import MediaPath

REL = "ai_videos/drama/2_世界观人设/props/obj/obj.glb"


def _seed(root: Path) -> None:
    p = root / REL
    p.parent.mkdir(parents=True)
    p.write_bytes(b"glTF\x02\x00\x00\x00")


def test_glb_and_gltf_are_media_and_tree_visible() -> None:
    for ext in (".glb", ".gltf"):
        assert ext in MEDIA_EXTENSIONS
        assert ext in TREE_VISIBLE_EXTENSIONS
        # Must stay OUT of ALLOWED_EXTENSIONS so /api/file never decodes it as text.
        assert ext not in ALLOWED_EXTENSIONS


def test_media_path_accepts_glb_so_archive_and_delete_work() -> None:
    assert MediaPath(rel=REL).rel == REL


def test_glb_serves_inline_with_gltf_binary_type(tmp_path: Path) -> None:
    _seed(tmp_path)
    query = MediaQuery(ExposedTree(tmp_path), SafeResolver(tmp_path))

    result = query.serve(REL)

    assert result.media_type == "model/gltf-binary"
    assert result.disposition == "inline"
    assert result.resolved_path == tmp_path / REL


def test_gltf_serves_as_json_flavoured_gltf(tmp_path: Path) -> None:
    p = tmp_path / REL.replace(".glb", ".gltf")
    p.parent.mkdir(parents=True)
    p.write_text("{}", encoding="utf-8")
    query = MediaQuery(ExposedTree(tmp_path), SafeResolver(tmp_path))

    result = query.serve(REL.replace(".glb", ".gltf"))

    assert result.media_type == "model/gltf+json"
    assert result.disposition == "inline"
