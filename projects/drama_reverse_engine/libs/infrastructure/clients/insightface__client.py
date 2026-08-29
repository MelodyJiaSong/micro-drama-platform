from __future__ import annotations

from libs.infrastructure.daos.face__dao import FaceDao


class InsightFaceEngine:
    """FaceEngine backend on insightface (optional heavy extra). available=False when
    the package is not installed — callers degrade per NFR-O1."""

    def __init__(self) -> None:
        try:
            from insightface.app import FaceAnalysis

            self._app = FaceAnalysis(name="buffalo_l")
            self._app.prepare(ctx_id=-1)
            self.available = True
        except Exception:
            self._app = None
            self.available = False

    def detect(self, image_abs_path: str, frame_rel_path: str, at_s: float) -> list[FaceDao]:
        if not self.available:
            return []
        import cv2  # bundled with insightface's opencv dependency

        img = cv2.imread(image_abs_path)
        if img is None:
            return []
        return [
            FaceDao(
                frame_rel_path=frame_rel_path, at_s=at_s,
                bbox=tuple(int(v) for v in face.bbox),  # type: ignore[arg-type]
                embedding=tuple(float(v) for v in face.normed_embedding),
                quality=float(getattr(face, "det_score", 0.5)),
            )
            for face in self._app.get(img)
        ]
