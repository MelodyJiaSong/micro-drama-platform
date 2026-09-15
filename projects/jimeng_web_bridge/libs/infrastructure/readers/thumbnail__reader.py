from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

from libs.infrastructure.daos.thumbnail__dao import ThumbnailDao
from libs.infrastructure.errors.artifact__error import UnsupportedThumbnailSourceError

_IMAGE_SUFFIXES: frozenset[str] = frozenset({".png", ".jpg", ".jpeg", ".webp"})


class ThumbnailReader:
    """Downscaled JPEG previews of reference images for the confirm page (`/api/thumbs`).

    The caller has already sandbox-validated `source`; this class only renders and caches.
    """

    def __init__(self, cache_dir: Path) -> None:
        self._cache_dir = cache_dir

    def thumbnail(self, source: Path, max_edge: int) -> ThumbnailDao:
        if source.suffix.lower() not in _IMAGE_SUFFIXES:
            raise UnsupportedThumbnailSourceError(source.suffix)
        stat = source.stat()
        key = hashlib.sha1(f"{source.resolve()}|{stat.st_mtime_ns}|{stat.st_size}|{max_edge}".encode()).hexdigest()
        target = self._cache_dir / f"{key}.jpg"
        if not target.is_file():
            self._render(source, target, max_edge)
        with Image.open(target) as rendered:
            width, height = rendered.size
        return ThumbnailDao(path=target, content_type="image/jpeg", width=width, height=height)

    def _render(self, source: Path, target: Path, max_edge: int) -> None:
        try:
            with Image.open(source) as original:
                image = ImageOps.exif_transpose(original).convert("RGB")
        except (UnidentifiedImageError, Image.DecompressionBombError, OSError) as error:
            raise UnsupportedThumbnailSourceError(type(error).__name__) from error
        image.thumbnail((max_edge, max_edge))
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        temp = target.with_suffix(".tmp")
        image.save(temp, format="JPEG", quality=85)
        temp.replace(target)
