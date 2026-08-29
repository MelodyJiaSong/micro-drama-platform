"""PDFs are tree-visible leaves served inline (follow-up 158).

A user drops reference decks (分镜 / 拍摄通告 PDFs) into a drama folder. Before
this, `.pdf` was in no extension allowlist, so the folder rendered as empty.
PDFs ride the MEDIA_EXTENSIONS path (raw FileResponse, no MAX_FILE_BYTES cap)
but must be served `inline` — an `<iframe>` honours Content-Disposition, so an
`attachment` pdf downloads instead of displaying.
"""
from __future__ import annotations

from pathlib import Path

from apps.api.routes._helpers import file_security_headers
from libs.application.queries.media__query import MediaQuery
from libs.common.exposed_tree import ALLOWED_EXTENSIONS, MEDIA_EXTENSIONS, ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.readers.tree__reader import TreeReader


def _query(root: Path) -> MediaQuery:
    return MediaQuery(exposed=ExposedTree(root), resolver=SafeResolver(root=root))


def test_pdf_is_media_but_never_text() -> None:
    assert ".pdf" in MEDIA_EXTENSIONS
    # /api/file would try to decode it as text
    assert ".pdf" not in ALLOWED_EXTENSIONS


def test_pdf_leaf_type_in_tree(tmp_path: Path) -> None:
    drama = tmp_path / "ai_videos" / "duikang_shangzeng"
    drama.mkdir(parents=True)
    (drama / "分镜.pdf").write_bytes(b"%PDF-1.7\n")
    node = TreeReader(ExposedTree(tmp_path))._leaf_for(drama / "分镜.pdf")
    assert node["type"] == "pdf"


def test_pdf_served_inline_as_application_pdf(tmp_path: Path) -> None:
    drama = tmp_path / "ai_videos" / "duikang_shangzeng"
    drama.mkdir(parents=True)
    (drama / "分镜.pdf").write_bytes(b"%PDF-1.7\n")
    qdto = _query(tmp_path).serve("ai_videos/duikang_shangzeng/分镜.pdf")
    assert qdto.media_type == "application/pdf"
    assert qdto.disposition == "inline"


def test_video_still_served_as_attachment(tmp_path: Path) -> None:
    drama = tmp_path / "ai_videos" / "duikang_shangzeng"
    drama.mkdir(parents=True)
    (drama / "a.mp4").write_bytes(b"\x00")
    qdto = _query(tmp_path).serve("ai_videos/duikang_shangzeng/a.mp4")
    assert qdto.disposition == "attachment"


def test_chinese_filename_survives_in_rfc5987_form() -> None:
    headers = file_security_headers("对抗熵增_分镜.pdf", "inline")
    disposition = headers["Content-Disposition"]
    assert disposition.startswith("inline; ")
    # ASCII fallback is lossy; filename* carries the real name
    assert 'filename="_.pdf"' in disposition
    assert "filename*=UTF-8''%E5%AF%B9%E6%8A%97" in disposition
