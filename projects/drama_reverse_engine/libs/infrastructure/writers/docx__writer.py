from __future__ import annotations

import io
import zipfile

_CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    "</Types>"
)
_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
    'Target="word/document.xml"/></Relationships>'
)

# 行类型 → run 样式，对齐 webapp ScriptView 调色板（follow-up 008/009）与
# sample_juben.docx 的蓝色台词体例
_STYLES: dict[str, dict[str, str | bool]] = {
    "ep": {"bold": True, "size": "32"},
    "outline": {"highlight": "green"},
    "scene": {"bold": True, "highlight": "yellow"},
    "cast": {"highlight": "green"},
    "action": {},
    "insert": {"color": "E36C0A"},
    "line": {"color": "0000FF"},
    "os": {"color": "7030A0"},
    "heading": {"bold": True},
    "plain": {},
    "blank": {},
}


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _run_props(style: dict[str, str | bool]) -> str:
    props = ['<w:rFonts w:eastAsia="宋体"/>']
    if style.get("bold"):
        props.append("<w:b/>")
    if "color" in style:
        props.append(f'<w:color w:val="{style["color"]}"/>')
    if "highlight" in style:
        props.append(f'<w:highlight w:val="{style["highlight"]}"/>')
    if "size" in style:
        props.append(f'<w:sz w:val="{style["size"]}"/><w:szCs w:val="{style["size"]}"/>')
    return "<w:rPr>" + "".join(props) + "</w:rPr>"


def build_docx(paragraphs: list[tuple[str, str]]) -> bytes:
    """(text, style_class) 段落列表 → 最小 WordprocessingML .docx 字节（零外部依赖）。"""
    body_parts: list[str] = []
    for text, cls in paragraphs:
        style = _STYLES.get(cls, {})
        run = (f"<w:r>{_run_props(style)}"
               f'<w:t xml:space="preserve">{_escape(text)}</w:t></w:r>') if text else ""
        body_parts.append(f"<w:p>{run}</w:p>")
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:body>" + "".join(body_parts) + "</w:body></w:document>"
    )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", _CONTENT_TYPES)
        zf.writestr("_rels/.rels", _RELS)
        zf.writestr("word/document.xml", document)
    return buf.getvalue()
