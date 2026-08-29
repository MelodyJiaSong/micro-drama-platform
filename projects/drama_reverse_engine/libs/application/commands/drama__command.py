from __future__ import annotations

import hashlib
import re
import shutil
import time
from pathlib import Path
from typing import AsyncIterator

from libs.application.commands.ingest__command import IngestCommand
from libs.application.dtos.drama__dto import DramaCdto
from libs.common.constants import MAX_UPLOAD_BYTES
from libs.domain.errors.workspace__error import WorkspaceError
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace
from libs.infrastructure.writers.artifact__writer import ArtifactWriter
from libs.infrastructure.writers.pipelinestate__writer import PipelineStateWriter


class DramaCommand:
    """FR-1.2 + project lifecycle. The authorization declaration is enforced at the
    application layer (SEC-12): no declaration record, no drama."""

    def __init__(self, ingest: IngestCommand, writer: ArtifactWriter, states: PipelineStateWriter,
                 workspace: SafeWorkspace) -> None:
        self._ingest = ingest
        self._writer = writer
        self._states = states
        self._workspace = workspace

    def create(self, drama_id: str, title: str, declaration_accepted: bool,
               declared_by: str, declaration_version: str,
               gate_a_enabled: bool = False, gate_b_enabled: bool = False) -> DramaCdto:
        if not declaration_accepted:
            raise WorkspaceError("authorization declaration must be accepted before creating a drama (SEC-12)")
        stub = {
            "declaration_version": declaration_version,
            "declared_by": declared_by,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        stub["sha256"] = hashlib.sha256(
            f"{stub['declaration_version']}|{stub['declared_by']}|{stub['ts']}".encode("utf-8")
        ).hexdigest()
        self._writer.write_json(f"{drama_id}/authorization_stub.json", stub)
        self._writer.write_json(f"{drama_id}/drama.json", {
            "drama_id": drama_id, "title": title,
            "gate_a_enabled": gate_a_enabled, "gate_b_enabled": gate_b_enabled,
        })
        return DramaCdto(drama_id=drama_id, title=title)

    async def create_and_upload(self, filename: str, title: str, declaration_accepted: bool,
                                declared_by: str, chunks: AsyncIterator[bytes]) -> tuple[str, str, list[str]]:
        """Follow-up 003 upload-first flow: one upload = one new entry. The drama_id is
        derived from the filename; a rejected upload removes the just-created entry so
        no empty drama lingers in the nav."""
        drama_id = _auto_drama_id(filename)
        final_title = title.strip() or Path(filename).stem
        self.create(drama_id, final_title, declaration_accepted, declared_by, "v1")
        try:
            episodes = await self.stream_upload(drama_id, filename, chunks)
        except Exception:
            shutil.rmtree(self._workspace.resolve(drama_id), ignore_errors=True)
            raise
        return drama_id, final_title, episodes

    async def stream_upload(self, drama_id: str, filename: str, chunks: AsyncIterator[bytes],
                            max_bytes: int = MAX_UPLOAD_BYTES) -> list[str]:
        """SEC-01/02: consume the async upload stream and write to disk with a running
        byte cap — abort AND delete the partial file the moment the cap is exceeded,
        BEFORE the whole payload lands (never buffers the full upload in RAM). The magic
        byte check ('ftyp' at offset 4) runs once ≥12 header bytes are available."""
        upload_rel = f"{drama_id}/uploads/{Path(filename).name}"
        abs_path = Path(self._workspace.resolve(upload_rel))
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        written = 0
        header = b""
        checked = False
        try:
            with abs_path.open("wb") as fh:
                async for chunk in chunks:
                    if not checked:
                        header += chunk
                        if len(header) >= 12:
                            checked = True
                            if not _looks_like_mp4(header):
                                raise WorkspaceError("upload rejected: not an mp4/mov container (magic-byte check)")
                    written += len(chunk)
                    if written > max_bytes:
                        raise WorkspaceError("upload rejected: exceeds 2GB limit (aborted mid-stream)")
                    fh.write(chunk)
            if not checked and not _looks_like_mp4(header):
                raise WorkspaceError("upload rejected: not an mp4/mov container (magic-byte check)")
        except WorkspaceError:
            abs_path.unlink(missing_ok=True)
            # drain the remaining stream before rejecting: responding while the
            # browser is still sending the body reads as a connection reset on the
            # client ("TypeError: Failed to fetch") and the 400 detail is lost
            async for _ in chunks:
                pass
            raise
        return self.register_uploaded_source(drama_id, upload_rel, written)

    def register_uploaded_source(self, drama_id: str, upload_rel_path: str, size_bytes: int) -> list[str]:
        """Validate the uploaded mp4 (FR-1.1), split into episodes (FR-1.3), and init
        each episode's pipeline state. Returns episode rel dirs."""
        validation = self._ingest.validate_media(upload_rel_path, size_bytes)
        if not validation.ok:
            Path(self._workspace.resolve(upload_rel_path)).unlink(missing_ok=True)
            raise WorkspaceError(f"upload rejected: {validation.reason}")
        split = self._ingest.split_episodes(drama_id, upload_rel_path)
        episode_dirs = []
        for rel_clip in split.episode_rel_paths:
            ep_dir = rel_clip.rsplit("/", 1)[0]
            self._states.init_state(ep_dir)
            episode_dirs.append(ep_dir)
        return episode_dirs


def _looks_like_mp4(head: bytes) -> bool:
    # ISO-BMFF: bytes 4-8 are the major box type 'ftyp' for mp4/mov
    return len(head) >= 12 and head[4:8] == b"ftyp"


def _auto_drama_id(filename: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_]+", "_", Path(filename).stem).strip("_").lower()[:24]
    ts = time.strftime("%Y%m%d%H%M%S", time.gmtime())
    return f"{slug}_{ts}" if slug else f"drama_{ts}"
