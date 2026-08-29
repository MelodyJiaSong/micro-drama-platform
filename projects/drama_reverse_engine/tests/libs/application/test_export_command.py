from __future__ import annotations

import io
import zipfile
from pathlib import Path

import pytest

from libs.application.commands.export__command import ExportCommand
from libs.domain.errors.export__error import ExportArtifactMissingError, UnknownExportSelectionError
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace

_SCRIPT = "第1集：\n\n分集大纲：梗概。\n\n正文：\n\n1-1 日 内 酒馆内堂\n人物：裴远\n△推门而入。\n裴远（紧张）：你还敢回来？\n"


def _setup(tmp_path: Path) -> ExportCommand:
    ep = tmp_path / "d1" / "ep01"
    ep.mkdir(parents=True)
    (ep / "script.md").write_text(_SCRIPT, encoding="utf-8")
    (ep / "novel.md").write_text("# 第一章\n\n他回来了。\n", encoding="utf-8")
    (ep / "dialogue.md").write_text("# 台词表\n\n- [镜01] 裴远：「你还敢回来？」\n", encoding="utf-8")
    return ExportCommand(workspace=SafeWorkspace(root=str(tmp_path)))


def test_single_md_selection_downloads_file_directly(tmp_path: Path) -> None:
    result = _setup(tmp_path).export_artifacts("d1/ep01", ["script"], "md")
    assert result.filename == "ep01_剧本.md"
    assert (tmp_path / result.rel_path).read_text(encoding="utf-8") == _SCRIPT


def test_single_docx_script_is_colored(tmp_path: Path) -> None:
    result = _setup(tmp_path).export_artifacts("d1/ep01", ["script"], "docx")
    assert result.filename == "ep01_剧本.docx"
    with zipfile.ZipFile(tmp_path / result.rel_path) as zf:
        xml = zf.read("word/document.xml").decode("utf-8")
    assert '<w:color w:val="0000FF"/>' in xml  # 台词蓝 (sample_juben.docx 体例)
    assert '<w:highlight w:val="yellow"/>' in xml  # 场次行


def test_multi_selection_bundles_zip(tmp_path: Path) -> None:
    result = _setup(tmp_path).export_artifacts("d1/ep01", ["novel", "script", "dialogue"], "docx")
    assert result.filename == "ep01_导出.zip" and result.media_type == "application/zip"
    with zipfile.ZipFile(tmp_path / result.rel_path) as zf:
        assert set(zf.namelist()) == {"ep01_小说.docx", "ep01_剧本.docx", "ep01_台词.docx"}
        novel = zipfile.ZipFile(io.BytesIO(zf.read("ep01_小说.docx")))
        xml = novel.read("word/document.xml").decode("utf-8")
    assert "<w:b/>" in xml and "他回来了。" in xml  # markdown 标题行加粗、正文保留


def test_missing_artifact_and_unknown_selection_rejected(tmp_path: Path) -> None:
    cmd = _setup(tmp_path)
    with pytest.raises(ExportArtifactMissingError):
        cmd.export_artifacts("d1/ep01", ["prompts"], "md")  # all_shot_prompts.md 未生成
    with pytest.raises(UnknownExportSelectionError):
        cmd.export_artifacts("d1/ep01", ["script", "bogus"], "md")
    with pytest.raises(UnknownExportSelectionError):
        cmd.export_artifacts("d1/ep01", [], "md")
    with pytest.raises(UnknownExportSelectionError):
        cmd.export_artifacts("d1/ep01", ["script"], "pdf")
