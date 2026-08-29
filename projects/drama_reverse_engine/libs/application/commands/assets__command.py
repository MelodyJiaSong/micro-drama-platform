from __future__ import annotations

from libs.application.dtos.assets__dto import ReferenceLibraryCdto
from libs.domain.value_objects.facecluster__valueobject import centroid, cluster_embeddings
from libs.infrastructure.clients.faceengine__client import FaceEngine
from libs.infrastructure.clients.ffmpeg__client import FfmpegClient
from libs.infrastructure.readers.artifact__reader import ArtifactReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter

_SAMPLE_EVERY_S = 1.0
_TOP_K_REFS = 5


class AssetsCommand:
    """FR-3.1/3.2/3.3: automatic character reference library from the source footage.

    Each cluster becomes a character card with top-K reference frames + a centroid.
    The locked Chinese descriptor is authored downstream (understand stage, FR-3.3) and
    re-pasted byte-identically into every shot prompt that names the character."""

    def __init__(
        self, ffmpeg: FfmpegClient, faces: FaceEngine,
        reader: ArtifactReader, writer: ArtifactWriter,
    ) -> None:
        self._ffmpeg = ffmpeg
        self._faces = faces
        self._reader = reader
        self._writer = writer

    def build_reference_library(self, drama_id: str, episode_rel_dirs: list[str], force: bool = False) -> ReferenceLibraryCdto:
        out_rel = f"{drama_id}/characters/library.json"
        if self._reader.exists(out_rel) and not force:
            data = self._reader.read_json(out_rel)
            return ReferenceLibraryCdto(
                character_count=len(data["characters"]), face_count=data["face_count"],
                degradations=data["degradations"], skipped=True,
            )
        if not self._faces.available:
            self._writer.write_json(out_rel, {"characters": [], "face_count": 0,
                                              "degradations": ["face_backend_unavailable"]})
            return ReferenceLibraryCdto(0, 0, ["face_backend_unavailable"])

        faces = []
        for ep_rel in episode_rel_dirs:
            source_abs = self._writer.resolve(f"{ep_rel}/source.mp4")
            duration = self._ffmpeg.probe(source_abs).duration_s
            t = 0.0
            while t < duration:
                frame_rel = f"{ep_rel}/frames/f{int(t * 1000):08d}.png"
                frame_abs = self._writer.resolve(frame_rel)
                self._writer.ensure_dir(f"{ep_rel}/frames")
                self._ffmpeg.extract_frame(source_abs, t, frame_abs)
                faces.extend(self._faces.detect(frame_abs, frame_rel, t))
                t += _SAMPLE_EVERY_S

        min_size = max(3, int(0.01 * len(faces)))
        clusters = cluster_embeddings([f.embedding for f in faces], min_cluster_size=min_size)
        characters = []
        for cluster in clusters:
            members = [faces[i] for i in cluster.member_indices]
            top = sorted(members, key=lambda f: -f.quality)[:_TOP_K_REFS]
            characters.append({
                "character_id": cluster.cluster_id,
                "name": f"角色{cluster.cluster_id}",
                # descriptor (锁定中文描述符) is authored by the understand stage (FR-4);
                # empty at library-build time by design
                "descriptor": "",
                "centroid": list(centroid([f.embedding for f in members])),
                "refs": [{"frame_rel_path": f.frame_rel_path, "at_s": f.at_s, "quality": f.quality} for f in top],
                "face_count": len(members),
            })
        self._writer.write_json(out_rel, {"characters": characters, "face_count": len(faces), "degradations": []})
        return ReferenceLibraryCdto(character_count=len(characters), face_count=len(faces), degradations=[])
