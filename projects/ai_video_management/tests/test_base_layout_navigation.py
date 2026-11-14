import json
from pathlib import Path

import pytest

from libs.infrastructure.readers.tree__reader import TreeReader


class Exposed:
    def __init__(self, root):
        self.root = root

    def excluded_dirs(self):
        return set()


@pytest.mark.parametrize("key,route", [("base_layout", "/base-layout"), ("map_regions", "/map-regions")])
@pytest.mark.parametrize("lazy", [False, True])
@pytest.mark.parametrize("layout,visible", [
    ("0_research/layout.json", True),
    ("../outside.json", False),
    ("/outside.json", False),
    ("0_research/missing.json", False),
    (None, False),
])
def test_layout_navigation_stays_in_existing_drama(tmp_path: Path, lazy, layout, visible, key, route):
    drama = tmp_path / "ai_videos/demo"
    (drama / "0_research").mkdir(parents=True)
    (drama / "0_research/layout.json").write_text("{}")
    (drama.parent / "outside.json").write_text("{}")
    (drama / "workflow.json").write_text(json.dumps({"workflow": "three-module-v1", key: layout}))
    node = TreeReader(Exposed(tmp_path))._walk_project(drama, lazy=lazy)
    entries = [c for c in node["children"] if c["name"] == key]
    assert len(entries) == int(visible)
    if visible:
        assert entries[0]["navigation_href"] == route + "?path=ai_videos%2Fdemo%2F0_research%2Flayout.json"
        assert entries[0]["path"] == f"ai_videos/demo/stages/{key}"
