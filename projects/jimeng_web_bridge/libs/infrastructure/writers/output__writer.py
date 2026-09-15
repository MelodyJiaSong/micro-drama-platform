from __future__ import annotations

import hashlib
import json
import os
import secrets
import shutil
from collections.abc import Mapping
from dataclasses import replace
from datetime import datetime, timedelta, timezone, tzinfo
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from libs.common.enums import OnExisting
from libs.common.paths import AI_VIDEOS_DIR_NAME, RepoSandbox, segment_violation
from libs.infrastructure.clients.ffprobe__client import FfprobeClient
from libs.infrastructure.daos.output__dao import (
    ArchivedFileDao, FinalizedOutputDao, MediaProbeDao, OutputExpectationDao, PromotedFileDao,
)
from libs.infrastructure.errors.output__error import (
    DownloadShaMismatchError, DownloadSizeMismatchError, InvalidCandidateError, MediaMismatchError, OutputError,
    OutputExistsError, OutputPathRejectedError, PromoteTargetExistsError, SidecarWriteError, TimezoneUnavailableError,
)

SIDECAR_SUFFIX: str = ".jimeng.json"
CANDIDATES_DIR_NAME: str = "_candidates"
DELETED_DIR_NAME: str = "_deleted"
_STAGING_PREFIX: str = ".jimeng-staging-"
_CHUNK: int = 1024 * 1024
_MAX_DUP: int = 999

# FR-44 whitelist, in the order the keys are written (stable diffs). A nested tuple lists the allowed sub-keys.
SIDECAR_FIELDS: tuple[tuple[str, tuple[str, ...] | None], ...] = (
    ("job_id", None), ("batch_id", None), ("attempt", None), ("backend", None),
    ("source", ("type", "path", "block_key")), ("prompt_sha256", None), ("negative_prompt_sha256", None),
    ("negative_prompt_sent", None),
    ("references", ("name", "kind", "path", "entity", "sha256")),
    ("params", ("model", "ratio", "resolution", "count", "duration_s", "reference_mode")),
    ("platform_task_id", None),
    ("credits_estimated", ("static", "page")), ("credits_charged", None),
    ("confirmed_at", None), ("confirmer", None), ("submitted_at", None), ("finished_at", None),
    ("durations", ("prepare_s", "queue_wait_s", "render_s", "download_s")),
    ("web_version", None), ("cli_version", None), ("browser_version", None),
    ("output", ("sha256", "size", "duration_s", "width", "height")),
    ("promoted_from", None),
)

# Used only when the OS has no IANA database (Windows without the `tzdata` package); DST-free zones only.
_FIXED_OFFSET_HOURS: dict[str, int] = {
    "UTC": 0, "Asia/Shanghai": 8, "Asia/Chongqing": 8, "Asia/Hong_Kong": 8, "Asia/Taipei": 8,
    "Asia/Singapore": 8, "Asia/Tokyo": 9, "Asia/Seoul": 9,
}


def zone_for(name: str) -> tzinfo:
    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError) as error:
        if name in _FIXED_OFFSET_HOURS:
            return timezone(timedelta(hours=_FIXED_OFFSET_HOURS[name]), name)
        raise TimezoneUnavailableError(f"无法解析时区 {name}（缺 tzdata）", config_key="time.timezone") from error


def timestamp_label(at: datetime, timezone_name: str) -> str:
    return at.astimezone(zone_for(timezone_name)).strftime("%Y%m%d-%H%M%S")


class OutputWriter:
    """Atomic, never-overwriting placement of generated files under `ai_videos/` plus their sidecars (FR-35, FR-42–45).

    Bytes are never modified: verification reads the temp file, placement is a rename (or a hashed copy when the temp
    file lives on another volume), and a name that is already taken gets a `_dupN` suffix instead of being replaced.
    """

    def __init__(self, sandbox: RepoSandbox, prober: FfprobeClient) -> None:
        self._sandbox = sandbox
        self._prober = prober

    def current_sha256(self, rel: str) -> str | None:
        verdict = self._sandbox.check_read(rel)
        if not verdict.ok or verdict.path is None or not verdict.path.is_file():
            return None
        return _sha256(verdict.path)

    def finalize(
        self,
        temp_path: Path,
        target_dir_rel: str,
        file_name: str,
        expected: OutputExpectationDao,
        sidecar: Mapping[str, object],
    ) -> FinalizedOutputDao:
        target_dir = self._target_dir(target_dir_rel)
        _check_file_name(file_name)
        try:
            probe = self._verify(temp_path, expected)
        except OutputError:
            temp_path.unlink(missing_ok=True)
            raise
        target_dir.mkdir(parents=True, exist_ok=True)
        placed = self._place(temp_path, target_dir, file_name, expected.sha256)
        output = FinalizedOutputDao(
            path_rel=self._rel(placed), sidecar_rel=None, sha256=expected.sha256, size=expected.size,
            duration_s=probe.duration_s, width=probe.width, height=probe.height,
        )
        body = dict(sidecar)
        body["output"] = {
            "sha256": output.sha256, "size": output.size, "duration_s": output.duration_s,
            "width": output.width, "height": output.height,
        }
        sidecar_path = placed.with_name(placed.name + SIDECAR_SUFFIX)
        try:
            self._write_sidecar(sidecar_path, body)
        except OSError as error:
            raise SidecarWriteError(f"产物已落盘，但 sidecar 写入失败：{error}", output) from error
        return replace(output, sidecar_rel=self._rel(sidecar_path))

    def promote(self, candidate_rel: str, on_existing: OnExisting, archive_label: str) -> PromotedFileDao:
        candidate = self._candidate(candidate_rel)
        _check_file_name(archive_label)
        key = candidate.parent.name
        subject_dir = candidate.parent.parent.parent
        target = subject_dir / f"{key}{candidate.suffix}"
        target_sidecar = target.with_name(target.name + SIDECAR_SUFFIX)
        archived: tuple[ArchivedFileDao, ...] = ()
        if target.exists() or target_sidecar.exists():
            if on_existing is OnExisting.FAIL:
                raise PromoteTargetExistsError(f"{self._rel(target)} 已存在", config_key="outputs.on_existing")
            archived = self._archive(target, target_sidecar, subject_dir, archive_label)
        sha256, size = self._copy_new(candidate, target)
        body = _read_json(candidate.with_name(candidate.name + SIDECAR_SUFFIX))
        output = body.get("output") if isinstance(body.get("output"), dict) else {}
        body["output"] = {**output, "sha256": sha256, "size": size}
        body["promoted_from"] = self._rel(candidate)
        try:
            self._write_sidecar(target_sidecar, body)
        except OSError as error:
            raise OutputError(f"升格文件已写入，但 sidecar 写入失败：{error}") from error
        return PromotedFileDao(
            candidate_rel=self._rel(candidate), target_rel=self._rel(target), sidecar_rel=self._rel(target_sidecar),
            sha256=sha256, size=size, archived=archived,
        )

    def _verify(self, temp_path: Path, expected: OutputExpectationDao) -> MediaProbeDao:
        if not temp_path.is_file():
            raise DownloadSizeMismatchError("下载的临时文件不存在")
        size = temp_path.stat().st_size
        if size != expected.size:
            raise DownloadSizeMismatchError(f"文件大小 {size} 与下载记录 {expected.size} 不一致")
        if _sha256(temp_path) != expected.sha256:
            raise DownloadShaMismatchError("文件 sha256 与下载记录不一致")
        probe = self._prober.probe(temp_path)
        if expected.duration_s is not None:
            if probe.duration_s is None or abs(probe.duration_s - expected.duration_s) > expected.duration_tolerance_s:
                raise MediaMismatchError(
                    f"时长 {probe.duration_s} s 与期望 {expected.duration_s} s 相差超过 {expected.duration_tolerance_s} s"
                )
        if expected.ratio is not None and not _ratio_matches(probe, expected.ratio, expected.ratio_tolerance):
            raise MediaMismatchError(f"画面 {probe.width}×{probe.height} 与期望比例 {expected.ratio} 不一致")
        return probe

    def _place(self, source: Path, target_dir: Path, file_name: str, sha256: str) -> Path:
        staged = source if _same_volume(source, target_dir) else self._stage(source, target_dir, sha256)
        stem, ext = _split_name(file_name)
        try:
            for index in range(1, _MAX_DUP + 1):
                target = target_dir / (file_name if index == 1 else f"{stem}_dup{index}{ext}")
                if target.exists() or target.with_name(target.name + SIDECAR_SUFFIX).exists():
                    continue
                try:
                    _move_new(staged, target)
                except FileExistsError:
                    continue
                if staged is not source:
                    source.unlink(missing_ok=True)
                return target
        except BaseException:
            if staged is not source:
                staged.unlink(missing_ok=True)
            raise
        if staged is not source:
            staged.unlink(missing_ok=True)
        raise OutputExistsError(f"{self._rel(target_dir)} 下 {file_name} 的候选名称全部被占用")

    def _stage(self, source: Path, target_dir: Path, sha256: str) -> Path:
        staged = target_dir / f"{_STAGING_PREFIX}{secrets.token_hex(6)}.tmp"
        try:
            copied_sha = _copy_hashing(source, staged)
        except BaseException:
            staged.unlink(missing_ok=True)
            raise
        if copied_sha != sha256:
            staged.unlink(missing_ok=True)
            raise DownloadShaMismatchError("跨卷复制后 sha256 不一致")
        return staged

    def _copy_new(self, source: Path, target: Path) -> tuple[str, int]:
        staged = target.parent / f"{_STAGING_PREFIX}{secrets.token_hex(6)}.tmp"
        try:
            sha256 = _copy_hashing(source, staged)
            size = staged.stat().st_size
            _move_new(staged, target)
        except FileExistsError as error:
            staged.unlink(missing_ok=True)
            raise OutputExistsError(f"{self._rel(target)} 已存在，不覆盖") from error
        except BaseException:
            staged.unlink(missing_ok=True)
            raise
        return sha256, size

    def _archive(self, target: Path, target_sidecar: Path, subject_dir: Path, label: str) -> tuple[ArchivedFileDao, ...]:
        relative_parts = subject_dir.parts[len(self._sandbox.read_root.parts):]
        archive_dir = self._sandbox.read_root.joinpath(DELETED_DIR_NAME, *relative_parts)
        archive_dir.mkdir(parents=True, exist_ok=True)
        archived: list[ArchivedFileDao] = []
        archived_media = _unique(archive_dir, f"{target.stem}.{label}{target.suffix}")
        if target.exists():
            _move_new(target, archived_media)
            archived.append(ArchivedFileDao(self._rel(target), self._rel(archived_media)))
        if target_sidecar.exists():
            archived_sidecar = _unique(archive_dir, archived_media.name + SIDECAR_SUFFIX)
            _move_new(target_sidecar, archived_sidecar)
            archived.append(ArchivedFileDao(self._rel(target_sidecar), self._rel(archived_sidecar)))
        return tuple(archived)

    def _write_sidecar(self, path: Path, body: Mapping[str, object]) -> None:
        text = json.dumps(whitelist_sidecar(body), ensure_ascii=False, indent=2) + "\n"
        staged = path.with_name(f"{_STAGING_PREFIX}{secrets.token_hex(6)}.json")
        try:
            staged.write_bytes(text.encode("utf-8"))
            _move_new(staged, path)
        except BaseException:
            staged.unlink(missing_ok=True)
            raise

    def _target_dir(self, rel: str) -> Path:
        verdict = self._sandbox.check_write(rel)
        if not verdict.ok or verdict.path is None:
            raise OutputPathRejectedError(f"输出目录不允许：{rel}（{verdict.violation}）")
        parts = verdict.path.parts[len(self._sandbox.read_root.parts):]
        if not _is_under(verdict.path, self._sandbox.read_root) or not parts or parts[0] == DELETED_DIR_NAME:
            raise OutputPathRejectedError(f"输出目录必须在 {AI_VIDEOS_DIR_NAME}/ 下且不在 {DELETED_DIR_NAME}/ 下：{rel}")
        return verdict.path

    def _candidate(self, rel: str) -> Path:
        verdict = self._sandbox.check_write(rel)
        if not verdict.ok or verdict.path is None or not _is_under(verdict.path, self._sandbox.read_root):
            raise OutputPathRejectedError(f"候选路径不允许：{rel}（{verdict.violation}）")
        path = verdict.path
        if (
            not path.is_file()
            or path.name.endswith(SIDECAR_SUFFIX)
            or path.name.startswith(_STAGING_PREFIX)
            or path.parent.parent.name != CANDIDATES_DIR_NAME
            or DELETED_DIR_NAME in path.parts[len(self._sandbox.read_root.parts):]
        ):
            raise InvalidCandidateError(f"不是 {CANDIDATES_DIR_NAME}/{{key}}/ 下的候选文件：{rel}")
        return path

    def _rel(self, path: Path) -> str:
        return self._sandbox.rel(path) or path.as_posix()


def whitelist_sidecar(body: Mapping[str, object]) -> dict[str, object]:
    kept: dict[str, object] = {}
    for key, sub_keys in SIDECAR_FIELDS:
        if key not in body:
            continue
        value = body[key]
        if sub_keys is not None and isinstance(value, list):
            value = [{k: item[k] for k in sub_keys if k in item} for item in value if isinstance(item, dict)]
        elif sub_keys is not None and isinstance(value, dict):
            value = {k: value[k] for k in sub_keys if k in value}
        kept[key] = value
    return kept


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(_CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _copy_hashing(source: Path, target: Path) -> str:
    digest = hashlib.sha256()
    with source.open("rb") as reader, target.open("xb") as writer:
        for chunk in iter(lambda: reader.read(_CHUNK), b""):
            digest.update(chunk)
            writer.write(chunk)
        writer.flush()
        os.fsync(writer.fileno())
    return digest.hexdigest()


def _move_new(source: Path, target: Path) -> None:
    """Rename that refuses to replace an existing target (Windows `rename` already refuses; POSIX needs link+unlink)."""
    if os.name == "nt":
        os.rename(source, target)
        return
    os.link(source, target)
    os.unlink(source)


def _same_volume(source: Path, target_dir: Path) -> bool:
    probe = target_dir if target_dir.exists() else target_dir.parent
    try:
        return os.stat(source).st_dev == os.stat(probe).st_dev
    except OSError:
        return False


def _ratio_matches(probe: MediaProbeDao, ratio: str, tolerance: float) -> bool:
    try:
        left, right = (float(part) for part in ratio.split(":", 1))
    except ValueError:
        return False
    if left <= 0 or right <= 0 or probe.height <= 0:
        return False
    expected = left / right
    return abs(probe.width / probe.height - expected) / expected <= tolerance


def _split_name(file_name: str) -> tuple[str, str]:
    dot = file_name.rfind(".")
    return (file_name, "") if dot <= 0 else (file_name[:dot], file_name[dot:])


def _unique(directory: Path, name: str) -> Path:
    stem, ext = _split_name(name)
    for index in range(1, _MAX_DUP + 1):
        candidate = directory / (name if index == 1 else f"{stem}_dup{index}{ext}")
        if not candidate.exists():
            return candidate
    raise OutputExistsError(f"{directory} 下 {name} 的归档名全部被占用")


def _check_file_name(name: str) -> None:
    if "/" in name or "\\" in name or segment_violation(name) is not None or name.startswith(_STAGING_PREFIX):
        raise OutputPathRejectedError(f"文件名不合法：{name}")


def _is_under(path: Path, root: Path) -> bool:
    return [os.path.normcase(p) for p in path.parts[: len(root.parts)]] == [os.path.normcase(p) for p in root.parts]


def _read_json(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}
