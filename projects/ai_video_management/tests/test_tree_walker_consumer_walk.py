"""Consumer-walk test.

Recursively descend `node.children` (the EXACT field the frontend reads). Catches
the class of bug where backend emits a different field than the frontend reads.
"""
from __future__ import annotations

from libs.common.exposed_tree import ExposedTree
from libs.infrastructure.readers.tree__reader import TreeReader
from tests.conftest import repo_root


def _walk(node: dict) -> None:
    assert "type" in node, f"node missing 'type': {node}"
    assert "name" in node, f"node missing 'name': {node}"
    assert "path" in node, f"node missing 'path': {node}"
    if node["type"] in ("section", "directory"):
        assert "children" in node, f"non-leaf missing 'children': {node!r}"
        for child in node["children"]:
            _walk(child)


def test_tree_consumer_walk() -> None:
    exposed = ExposedTree(repo_root())
    walker = TreeReader(exposed)
    tree = walker.build()
    _walk(tree)


def test_tree_sections_order() -> None:
    """Only the AI Videos section is left. (Follow-up 233 removed the
    Downloaded Novels / My Novel sections that follow-ups 096 / 113 had added.)"""
    exposed = ExposedTree(repo_root())
    walker = TreeReader(exposed)
    tree = walker.build()
    section_names = [child["name"] for child in tree["children"]]
    assert section_names == ["AI Videos"], section_names


def test_no_project_meta_or_collapsed_library_leaves() -> None:
    """The old project-type badge data and the collapsed actor / voice leaves
    are gone; `_actors/actor_NNNN/` is walked like any other folder."""
    exposed = ExposedTree(repo_root())
    tree = TreeReader(exposed).build()

    def walk(node: dict) -> None:
        assert "project_meta" not in node, node["path"]
        assert node["type"] not in ("actor", "voice"), node["path"]
        for child in node.get("children", []):
            walk(child)

    walk(tree)


def test_image_leaves_typed_as_image() -> None:
    exposed = ExposedTree(repo_root())
    walker = TreeReader(exposed)
    tree = walker.build()

    def collect_images(node: dict, out: list) -> None:
        if node.get("type") == "image":
            out.append(node)
        for c in node.get("children", []):
            collect_images(c, out)

    images: list = []
    collect_images(tree, images)
    for img in images:
        assert img["name"].lower().endswith((".png", ".jpg")), f"non-image typed as image: {img}"
