from __future__ import annotations

import io
import zipfile

from libs.infrastructure.writers.docx__writer import build_docx


def _document_xml(data: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        assert {"[Content_Types].xml", "_rels/.rels", "word/document.xml"} <= set(zf.namelist())
        return zf.read("word/document.xml").decode("utf-8")


def test_dialogue_line_colored_blue_and_scene_highlighted() -> None:
    xml = _document_xml(build_docx([
        ("1-1 日 内 酒馆内堂", "scene"),
        ("裴远（紧张）：你还敢回来？", "line"),
        ("裴远（内心独白）：此地不宜久留。", "os"),
        ("△推门而入。", "action"),
    ]))
    assert '<w:color w:val="0000FF"/>' in xml and "你还敢回来？" in xml
    assert '<w:color w:val="7030A0"/>' in xml
    assert '<w:highlight w:val="yellow"/>' in xml and "<w:b/>" in xml


def test_xml_special_chars_escaped_and_blank_line_kept() -> None:
    xml = _document_xml(build_docx([("A<B>&C", "plain"), ("", "blank"), ("尾行", "plain")]))
    assert "A&lt;B&gt;&amp;C" in xml
    assert "<w:p></w:p>" in xml
