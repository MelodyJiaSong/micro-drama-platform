from __future__ import annotations

import io
import zipfile
from pathlib import Path

from libs.application.dtos.export__dto import ExportFileCdto
from libs.domain.errors.export__error import ExportArtifactMissingError, UnknownExportSelectionError
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace
from libs.domain.value_objects.scriptformat__valueobject import classify_script_line
from libs.infrastructure.writers.docx__writer import build_docx

_EPISODE_FILES = ("novel.md", "script.md", "dialogue.md", "all_shot_prompts.md")

_EXPORTABLES: dict[str, tuple[str, str]] = {
    "novel": ("novel.md", "小说"),
    "script": ("script.md", "剧本"),
    "dialogue": ("dialogue.md", "台词"),
    "prompts": ("all_shot_prompts.md", "分镜prompt"),
}
_MEDIA_TYPES = {
    "md": "text/markdown; charset=utf-8",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "zip": "application/zip",
}


def _to_docx(text: str, is_script: bool) -> bytes:
    if is_script:
        paragraphs = [(line, classify_script_line(line)) for line in text.split("\n")]
    else:
        paragraphs = [(line, "heading" if line.startswith("#") else "plain") for line in text.split("\n")]
    return build_docx(paragraphs)


class ExportCommand:
    """FR-12: one-click deliverable zip of the reverse-engineered text — novel, script,
    dialogue, per-shot prompts (台词配音 prompt is embedded in each shotNN.md) + character
    cards + authorization stub. Arcnames are workspace-relative only (Zip Slip safe)."""

    def __init__(self, workspace: SafeWorkspace) -> None:
        self._workspace = workspace

    def export_drama(self, drama_id: str, out_rel_path: str) -> str:
        root = Path(self._workspace.resolve(drama_id))
        out = Path(self._workspace.resolve(out_rel_path))
        out.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
            self._add_if_exists(zf, root, "authorization_stub.json", drama_id)
            self._add_if_exists(zf, root, "characters/library.json", drama_id)
            for char_png in sorted(root.glob("chars/**/*.png")):
                zf.write(char_png, f"{drama_id}/{char_png.relative_to(root).as_posix()}")
            for ep_dir in sorted(p for p in root.iterdir() if p.is_dir() and p.name.startswith("ep")):
                ep_rel = f"{drama_id}/{ep_dir.name}"
                for name in _EPISODE_FILES:
                    self._add_if_exists(zf, ep_dir, name, ep_rel)
                for shot_md in sorted(ep_dir.glob("shots/shot*/shot*.md")):
                    zf.write(shot_md, f"{ep_rel}/{shot_md.relative_to(ep_dir).as_posix()}")
        return out_rel_path

    def export_artifacts(self, episode_rel_dir: str, artifacts: list[str], fmt: str) -> ExportFileCdto:
        """Follow-up 009: selectable per-artifact export — one selection downloads the
        file directly (md verbatim / docx converted, script colored per line class);
        multiple selections bundle into a zip."""
        if fmt not in ("md", "docx"):
            raise UnknownExportSelectionError(f"未知导出格式：{fmt}（可选 md / docx）")
        unknown = [a for a in artifacts if a not in _EXPORTABLES]
        if unknown or not artifacts:
            raise UnknownExportSelectionError(
                f"未知产物选择：{'、'.join(unknown) or '（空）'}（可选 {'/'.join(_EXPORTABLES)}）")
        ep_dir = Path(self._workspace.resolve(episode_rel_dir))
        ep_name = episode_rel_dir.rsplit("/", 1)[-1]
        items: list[tuple[str, bytes]] = []
        for key in artifacts:
            source_name, label = _EXPORTABLES[key]
            path = ep_dir / source_name
            if not path.exists():
                raise ExportArtifactMissingError(f"{label}（{source_name}）尚未生成，无法导出")
            text = path.read_text(encoding="utf-8")
            data = _to_docx(text, key == "script") if fmt == "docx" else text.encode("utf-8")
            items.append((f"{ep_name}_{label}.{fmt}", data))
        export_dir = ep_dir / "export"
        export_dir.mkdir(parents=True, exist_ok=True)
        if len(items) == 1:
            filename, data = items[0]
            (export_dir / filename).write_bytes(data)
            return ExportFileCdto(rel_path=f"{episode_rel_dir}/export/{filename}",
                                  filename=filename, media_type=_MEDIA_TYPES[fmt])
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for filename, data in items:
                zf.writestr(filename, data)
        bundle = f"{ep_name}_导出.zip"
        (export_dir / bundle).write_bytes(buf.getvalue())
        return ExportFileCdto(rel_path=f"{episode_rel_dir}/export/{bundle}",
                              filename=bundle, media_type=_MEDIA_TYPES["zip"])

    @staticmethod
    def _add_if_exists(zf: zipfile.ZipFile, base: Path, rel_name: str, arc_prefix: str) -> None:
        path = base / rel_name
        if path.exists():
            zf.write(path, f"{arc_prefix}/{rel_name}")
