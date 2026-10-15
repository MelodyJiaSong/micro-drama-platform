"""Media-aggregate commands: archive / unarchive / delete / hard_delete /
purge_deleted / rename.

Single MediaCommand class over MediaArchiver + MediaRenamer. (The
refuse-if-actor-assigned check of follow-up 043 went with the actor pool and
casting in follow-up 233.)
"""
from __future__ import annotations

from libs.application.dtos.media__dto import (
    MediaHardDeleteCdto,
    MediaMoveCdto,
    MediaPurgeDeletedCdto,
    RenameMediaResultCdto,
)
from libs.application.mappers.media__mapper import MediaMapper
from libs.domain.errors.media__error import (
    AlreadyArchivedError,
    NotUnderDeletedError,
)
from libs.domain.value_objects.drama__valueobject import DramaPath
from libs.domain.value_objects.media__valueobject import (
    ArchiveState,
    MediaPath,
    classify_state,
)
from libs.infrastructure.writers.downloads__writer import RENDERS_DIR_NAME
from libs.infrastructure.writers.media__writer import MediaArchiver, MediaRenamer


class MediaCommand:
    def __init__(self, archiver: MediaArchiver, renamer: MediaRenamer) -> None:
        self._archiver = archiver
        self._renamer = renamer

    def archive(self, rel_path: str) -> MediaMoveCdto:
        media = MediaPath(rel=rel_path)
        if classify_state(media) is ArchiveState.ARCHIVED:
            raise AlreadyArchivedError("file is already inside an archive/ folder")
        return MediaMapper.move_to_cdto(self._archiver.archive(rel_path))

    def unarchive(self, rel_path: str) -> MediaMoveCdto:
        MediaPath(rel=rel_path)
        return MediaMapper.move_to_cdto(self._archiver.unarchive(rel_path))

    def delete(self, rel_path: str) -> MediaMoveCdto:
        """Soft-delete (move to ai_videos/_deleted/{path})."""
        MediaPath(rel=rel_path)
        return MediaMapper.move_to_cdto(self._archiver.delete(rel_path))

    def hard_delete(self, rel_path: str) -> MediaHardDeleteCdto:
        media = MediaPath(rel=rel_path)
        if not media.is_under_deleted:
            raise NotUnderDeletedError("hard_delete only operates inside ai_videos/_deleted/")
        deleted_rel = self._archiver.hard_delete(rel_path)
        return MediaHardDeleteCdto(deleted_rel=deleted_rel)

    def purge_deleted(self) -> MediaPurgeDeletedCdto:
        """Empty the recycle bin — recursively remove all of
        ai_videos/_deleted/ (every file type + folders), not just media."""
        return MediaPurgeDeletedCdto(count=self._archiver.purge_deleted())

    def rename(self, rel_drama_path: str) -> RenameMediaResultCdto:
        """Drama-scoped batch rename of image/video files to match their
        parent folder name."""
        DramaPath(rel=rel_drama_path)
        return MediaMapper.rename_to_cdto(
            self._renamer.rename_drama(
                rel_drama_path, excluded_folder_names=frozenset({"frames", RENDERS_DIR_NAME})
            )
        )
