import os

from libs.common.enums import SubType
from libs.infrastructure.readers.canon__reader import CanonReader
from libs.infrastructure.readers.layout__reader import LayoutReader

from tests.conftest import FIXTURES


def test_detect_novel_layout():
    layout = LayoutReader(FIXTURES).detect("mini_drama")
    assert layout.sub_type is SubType.NOVEL
    assert layout.episodes == ("ep01",)
    paths = LayoutReader(FIXTURES).shot_paths(layout, "ep01")
    assert [os.path.basename(p) for p in paths] == ["shot01.md", "shot02.md"]
    script, dialogue = LayoutReader(FIXTURES).script_paths(layout, "ep01")
    assert script and script.endswith("script.md")
    assert dialogue and dialogue.endswith("dialogue.md")


def test_canon_reader_extracts_locked_tag_and_voice():
    layout = LayoutReader(FIXTURES).detect("mini_drama")
    canon = CanonReader().read(layout.canon_dir)
    assert len(canon.characters) == 1
    card = canon.characters[0]
    assert card.name == "林小雨"
    assert card.locked_tag == "林小雨 — 青衫束发 玉簪 剑眉星目"
    assert card.voice_id == "TX-test-01"
    assert "境界体系" in canon.world_text
