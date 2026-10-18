"""Scan the user OS Downloads folder and import recent media into a drama tree.

One-click "import + rename" for a drama (`POST /api/import-from-downloads`):

* A shot render named with its full key `ep{N}_s{N}_st{N}` (the compiled
  prompt's first line, which the generator carries into the download name)
  lands in `episodes/epNN/scenes/sN/shots/stN/renders/<take>/`, one folder per
  generation (follow-up 230). An incomplete or unknown shot key is reported
  unmatched, never guessed.
* An asset download carrying a routing key — background `bg{N}-{M}`, prop
  `p{N}-{M}` / `p{N}.glb`, equipment `e{N}-{M}` — is routed by that key into
  the asset's folder and named from the key alone; a character view `c{N}-{M}`
  reaches its card folder through the folder's id token and is named the same
  way. A series member also owns its series' `_series/` assets.
* Otherwise the filename is substring-matched against the drama's character /
  background / prop folder names.

Unmatched files are NOT imported — they stay untouched in Downloads and are
only reported back as `unmatched`. Only Downloads' immediate children are
scanned, restricted to media extensions with mtime within the last 7 days;
symlinks are skipped. The old 0–7 stage routes (`shots/shotNN` tags, scene
`bg{N}_{方位}` plates, intro cards, the actor pool and the performance
library) were removed in follow-up 233.

This module is the first place the backend reads from a path OUTSIDE
EXPOSED_TREE. Source-side hardening: basename validation, symlink refusal,
and shutil.move (never copy + delete in two steps that could leave orphans).
Destination is always inside the drama folder validated by MediaRenamer.
"""
from __future__ import annotations

import os
import re
import shutil
import time
from dataclasses import dataclass, field
from libs.common import asset_key, drama_layout, equipment_key, prop_key, scene_key, series_shared
from libs.common.production_key import SHOT_KEY_HINT_RE, first_shot_key, folder_shot_key
from pathlib import Path

from libs.common.exposed_tree import MEDIA_EXTENSIONS, ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.domain.errors.downloads__error import DownloadsDirMissingError
from libs.infrastructure.daos.equipment_route__dao import KIND_EQUIPMENT_VIEW, EquipmentRouteDao
from libs.infrastructure.daos.prop_route__dao import KIND_PROP_MESH, KIND_PROP_VIEW, PropRouteDao
from libs.infrastructure.daos.scene_route__dao import KIND_SUBJECT, KIND_VIEW, SceneRouteDao
from libs.infrastructure.readers.equipment_route__reader import EquipmentKeyRouter
from libs.infrastructure.readers.prop_route__reader import MODEL_EXTS, PropKeyRouter
from libs.infrastructure.readers.scene_route__reader import SceneKeyRouter
from libs.infrastructure.writers.character_video__writer import _VIEWS_SUBDIR
from libs.infrastructure.writers.media__writer import MediaRenamer, RenameResult

NOT_MATCHED_DIR_NAME = "not_matched"
RENDERS_DIR_NAME = "renders"
DEFAULT_TIME_WINDOW_SECONDS = 7 * 24 * 60 * 60
DOWNLOADS_ENV_VAR = "AI_VIDEO_MGMT_DOWNLOADS_DIR"
_BASENAME_INVALID = re.compile(r"[\x00-\x1f/\\:*?\"<>|]")
# Edge guard for id-token matching — see `_token_hit`.
_ASCII_ALNUM = re.compile(r"[a-z0-9]")
# Sub-folders of an asset that are never a view destination.
_NON_VIEW_DIRS = frozenset({NOT_MATCHED_DIR_NAME, RENDERS_DIR_NAME, "frames", "archive"})
PROPS_DIR_NAME = "props"
# An OBJECT prop — a prop whose identity needs several
# camera angles, not one image — keeps each angle in its own view sub-folder
# `v{N}_{视角}` under the prop folder. The 视角 segment (everything after the
# `v{N}_` prefix) is the routing key and MUST be globally unique across the
# drama's prop views, because an
# out-of-image tool truncates the download filename to the prompt's first ~9
# chars: a pinyin prop handle (`sports_car_全景` → `sports_ca`) loses the angle
# entirely and all four views collide on one file. A leading Chinese view token
# (`车外全景`) survives any truncation, so the routing key is the 视角 itself.
# One canonical image per view folder → re-import OVERWRITES (re-rolls are the
# norm for an anchor image).
_PROP_VIEW_PREFIX = re.compile(r"^v\d+_")
# A SUBJECT folder — `bg{N}_{主体名}`, exactly two segments — holds several named
# views of one subject and one .md carrying all their prompts.
#
# Routing key = `bg{N}-{M}` — subject N, view M — pure ASCII, digits and a hyphen,
# ANYWHERE in the download name. Anchoring it to position 0 is wrong: generators
# wrap the prompt-derived name in their own prefix and suffix. Real example:
#   ElevenLabs_image_gpt-image-2_bg1-1_广场正向 参考_ _2026-08-30T09_22_13.png
#                                └ key ┘
# A hyphen, not a dot: a dot reads as an extension separator to some tools and to
# `Path.stem`, and invites truncation at the wrong place.
# The destination is named from the KEY ALONE (`bg1.1.png`), never from the
# download's text — that is what makes it immune to whatever the tool decorates
# the name with. The Chinese view name lives in the subject's .md, not the file.
# `{N}` is unique across the whole drama.
#
# A name can carry MORE THAN ONE key: some tools inline the prompt's head, and
# the head includes the `参考:` line, whose handle is another view's path. Real
# example — the target is bg2.1, the reference is bg1.1:
#   jimeng-2026-08-30-2988-bg2-1_主街正向 参考_ `bg1_广场_bg1-1.png(世界基调)=_….png
# FIRST match wins, and that is correct by construction, not by luck: the routing
# key is the prompt's FIRST line, so it always precedes anything quoted from the
# `参考:` line below it. `re.search` returns the leftmost match.
# A subject folder needs BOTH signals — neither alone is enough:
#   * shape `bg{N}_{主体名}` with exactly two segments, AND
#   * content: it carries its own `{folder}.md` holding every view's prompt
#     (an old two-segment plate folder like `bg5_高位俯瞰` has no such md).
_SUBJECT_FOLDER = re.compile(r"^bg(\d+)_[^_]+$")
_SUBJECT_KEY = re.compile(r"bg(\d+)-(\d+)")
# Script-generated asset folders under a prop: written by the render/previz
# tools with contract-bound filenames, never by a download. They are excluded
# from the folder-name rename pass, which would otherwise collapse
# `whitemodel/angles/sports_car_front.png` … to `angles1.png` … and break every
# downstream reference to the `{name}_{tag}.png` naming contract.
# A scenes tree has the same kind of tool-owned folders (follow-up 173), and the
# pass was collapsing them in the field (`_blender/_blender1.png`, `ref/ref1.jpg`):
# `_blender/` (`{bg}.blend` / `check_*.png`), `planning/`
# (`{bg}_floorplan.png`, shot flight plans), `ref/` (`r1.jpg`, named in
# `refs.md`), and a prop's `mesh/` (`p{N}.glb` + `p{N}_preview_*.png`).
# A character's `views/` (`{char}_{front|side|back}.png`, `CharacterViewExtractor`)
# was collapsed by name order to `views1/2/3.png` = back/front/side (shengji_zhilu follow-up 048).
GENERATED_DIR_NAMES = frozenset(
    {"whitemodel", "previz", "_clay", "_blender", "planning", "ref", "mesh", _VIEWS_SUBDIR}
)
_IMAGE_EXTS_LC = frozenset({".png", ".webp", ".jpg", ".jpeg"})
# The grammars a download's routing key can belong to (`_leftmost_grammar`).
_KEY_SCENE: str = "scene"
_KEY_PROP: str = "prop"
_KEY_EQUIPMENT: str = "equipment"


def _view_key(stem: str, folder_name: str) -> str | None:
    """The view key a subject-folder download is named after, or None.

    The out-of-image tool names the file from the prompt's first line, so the
    key is the leading whitespace-delimited word — `广场正向` out of
    `广场正向 电影级实拍 (1)`. Accepted only when it starts with one of the
    folder's own tokens, so an unrelated filename never renames itself into the
    folder's namespace.
    """
    head = stem.strip().split()[0] if stem.strip() else ""
    head = re.sub(r"\s*\(\d+\)$", "", head).strip()
    if not head:
        return None
    low = head.lower()
    tokens = [folder_name.lower()]
    if "_" in folder_name:
        tokens.extend(p.strip().lower() for p in folder_name.split("_") if len(p.strip()) >= 2)
    return head if any(low.startswith(t) for t in tokens if t) else None


@dataclass(frozen=True)
class _Candidate:
    folder: Path
    kind: str  # "character" | "scene" | "prop" | "shot"
    tokens: tuple[str, ...]  # already lowercased


@dataclass
class ImportResult:
    moved: list[dict[str, str]] = field(default_factory=list)
    unmatched: list[dict[str, str]] = field(default_factory=list)
    errors: list[dict[str, str]] = field(default_factory=list)
    rename: dict[str, object] | None = None

    def to_payload(self) -> dict[str, object]:
        return {
            "moved": list(self.moved),
            "unmatched": list(self.unmatched),
            "errors": list(self.errors),
            "rename": self.rename if self.rename is not None else {"renamed": [], "skipped": [], "errors": []},
        }


class DownloadsImporter:
    def __init__(
        self,
        exposed: ExposedTree,
        resolver: SafeResolver,
        renamer: MediaRenamer,
        downloads_dir: Path | None = None,
        time_window_seconds: int = DEFAULT_TIME_WINDOW_SECONDS,
        scene_router: SceneKeyRouter | None = None,
        prop_router: PropKeyRouter | None = None,
        equipment_router: EquipmentKeyRouter | None = None,
    ) -> None:
        self._exposed = exposed
        self._resolver = resolver
        self._renamer = renamer
        self._scene_router = scene_router or SceneKeyRouter()
        self._prop_router = prop_router or PropKeyRouter()
        self._equipment_router = equipment_router or EquipmentKeyRouter()
        self._downloads_dir = (downloads_dir or self._resolve_default_downloads_dir()).resolve()
        self._window = time_window_seconds

    @staticmethod
    def _resolve_default_downloads_dir() -> Path:
        override = os.environ.get(DOWNLOADS_ENV_VAR, "").strip()
        if override:
            return Path(override)
        return Path.home() / "Downloads"

    def import_drama(self, rel_drama_path: str) -> ImportResult:
        drama_dir = self._renamer.validate_drama(rel_drama_path)
        if not self._downloads_dir.is_dir():
            raise DownloadsDirMissingError(str(self._downloads_dir))
        candidates = self._collect_candidates(drama_dir)
        conflicts = series_shared.find_conflicts(drama_dir)
        cutoff = time.time() - self._window
        result = ImportResult()
        for src in self._iter_downloads(cutoff):
            if not self._is_safe_basename(src.name):
                result.errors.append({"path": self._display_src(src), "message": "invalid_basename"})
                continue
            keyed_name: str | None = None
            chosen = self._classify(src.name, candidates)
            production_key = first_shot_key(src.stem)
            if SHOT_KEY_HINT_RE.search(src.stem):
                hits = [c for c in candidates if c.kind == "shot" and production_key is not None and production_key.value in c.tokens]
                if len(hits) != 1:
                    result.unmatched.append({"from": self._display_src(src), "kind": "unmatched",
                                             "reason": "unknown_or_incomplete_shot_key" if not hits else "ambiguous_shot_key"})
                    continue
                chosen = hits[0]
            grammar = None if production_key is not None else self._leftmost_grammar(src.name, chosen)
            keyed = None if production_key is not None else self._keyed_route(src.name, grammar, drama_dir)
            if keyed is not None:
                dst_folder, kind, keyed_name = keyed.folder, keyed.kind, keyed.name
            elif grammar == _KEY_EQUIPMENT:
                # Equipment is imported by key only: an `e{N}` no single item
                # folder takes stays in Downloads, never handed to a word match
                # on whatever its `参考:` line quoted.
                item = equipment_key.first_key(src.stem)
                conflict = conflicts.for_key(item.base) if item is not None else None
                if conflict is not None and src.suffix.lower() not in MODEL_EXTS:
                    result.errors.append({"path": self._display_src(src), "message": conflict.message(self._rel)})
                else:
                    result.unmatched.append({"from": self._display_src(src), "kind": "unmatched"})
                continue
            elif chosen is None:
                # An object prop's view download carries only its 视角 token
                # (`车外全景`), never the pinyin prop handle, so it matches no
                # prop by name.
                view = self._match_view_any_prop(src.name, drama_dir)
                if view is None:
                    # A `bg{N}` subject owned by both the episode and `_series/`
                    # makes the keyed route refuse — report why.
                    subject = _SUBJECT_KEY.search(src.stem)
                    conflict = conflicts.for_key(f"bg{subject.group(1)}") if subject else None
                    if conflict is not None:
                        result.errors.append({"path": self._display_src(src), "message": conflict.message(self._rel)})
                        continue
                    # Truly unmatched → NOT imported: leave the file in Downloads
                    # untouched, only report it back (no not_matched/ folder).
                    result.unmatched.append({"from": self._display_src(src), "kind": "unmatched"})
                    continue
                dst_folder, kind = view, "prop_view"
            else:
                dst_folder, kind = chosen.folder, chosen.kind
                if chosen.kind == "prop":
                    view = self._match_prop_view(src.name, chosen.folder)
                    if view is not None:
                        dst_folder, kind = view, (
                        "scene_subject" if self._is_subject_folder(view) else "prop_view")
            if src.suffix.lower() in MODEL_EXTS and kind != KIND_PROP_MESH:
                # A GLB holds one object (2026-09-25) and every object is a prop:
                # it lands only in `props/p{N}_*/mesh/`, by prop key — never by a
                # name token, never in a character / scene / shot folder.
                result.unmatched.append({"from": self._display_src(src), "kind": "unmatched"})
                continue
            conflict = conflicts.owning(dst_folder)
            if conflict is not None:
                result.errors.append({"path": self._display_src(src), "message": conflict.message(self._rel)})
                continue
            # Canonical-named destinations: a keyed download is named from its key;
            # a name-matched asset download from its view key (or the folder name).
            # Shot renders keep their original download name.
            ext = src.suffix.lower()
            dst_name = src.name
            if keyed_name is not None:
                # Named from the routing key alone — immune to whatever prefix or
                # suffix the generator wrapped around it.
                dst_name = keyed_name
            elif kind in ("prop", "scene", "character"):
                # A subject folder holds several named views of one subject
                # (`广场/广场正向.png`, `玉佩/玉佩_完整.png`). The download is named
                # after the prompt's first line — the view key — so keep that key
                # as the filename instead of collapsing every view onto
                # `{folder}.ext`. Falls back to the folder name when the file
                # carries no view key of its own (the subject's canonical image).
                #
                # `asset_key` first: a `{prefix}{N}-{M}` routing key (`p3-2`,
                # `c1-1`) is matched ANYWHERE in the stem, so the generator's
                # own prefix (`ElevenLabs_image_gpt-image-2_…`) cannot hide it.
                # Without this, `p3-1` and `p3-2` both fell through to the
                # folder name and silently overwrote each other (rule 4b-A).
                _key = (asset_key.view_key_in(src.stem, dst_folder.name)
                        or _view_key(src.stem, dst_folder.name)
                        or dst_folder.name)
                dst_name = f"{_key}{ext}"
            if kind == "shot" and production_key is not None:
                # Six-module shots (ep1_s1_st1 keys): one generation = one folder under renders/ (follow-up 230), so the
                # take and later its review sit together.
                # The resolver only admits a new path whose parent exists, so renders/ is created (safely) first.
                safe_renders = self._resolver.resolve(self._rel(dst_folder))
                if safe_renders is None:
                    result.errors.append({"path": self._display_src(src), "message": "invalid_destination"})
                    continue
                safe_renders.mkdir(parents=True, exist_ok=True)
                dst_folder = dst_folder / Path(dst_name).stem
            safe_destination = self._resolver.resolve(self._rel(dst_folder))
            if safe_destination is None:
                result.errors.append({"path": self._display_src(src), "message": "invalid_destination"})
                continue
            try:
                dst_folder.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                result.errors.append({"path": self._display_src(src), "message": f"mkdir_failed: {exc}"})
                continue
            # Overwrite semantics: an object prop's `v{N}_{视角}` view folder holds
            # exactly ONE canonical image → clear stale media first.
            if kind == "prop_view":
                self._clear_folder_media(dst_folder)
            elif kind in ("prop", "scene", "character", KIND_SUBJECT, KIND_VIEW, KIND_PROP_VIEW,
                          KIND_EQUIPMENT_VIEW):
                # Overwrite only THIS view, never the folder's other views.
                self._clear_named_media(dst_folder, Path(dst_name).stem)
            dst = dst_folder / dst_name
            if dst.exists():
                try:
                    dst.unlink()
                except OSError as exc:
                    result.errors.append({"path": self._display_src(src), "message": f"overwrite_failed: {exc}"})
                    continue
            try:
                shutil.move(str(src), str(dst))
            except OSError as exc:
                result.errors.append({"path": self._display_src(src), "message": f"move_failed: {exc}"})
                continue
            result.moved.append({"from": self._display_src(src), "to": self._rel(dst), "kind": kind})
        rename_result = self._renamer.rename_drama(
            rel_drama_path,
            excluded_folder_names=frozenset(
                {NOT_MATCHED_DIR_NAME, RENDERS_DIR_NAME, "frames", *GENERATED_DIR_NAMES}
            ),
        )
        result.rename = rename_result.to_payload()
        return result

    def _collect_candidates(self, drama_dir: Path) -> list[_Candidate]:
        out: list[_Candidate] = []
        # Props (`2_世界观人设/props/{道具名}/`) are a sibling of characters/scenes.
        # A series member also owns its series' `_series/` assets (episode first).
        # Equipment is deliberately absent: it routes by `e{N}-{M}` key only
        # (`_keyed_route`), so an item's name words never pull other downloads in.
        for kind, layout_dir in (
            ("character", drama_layout.characters_dir),
            ("scene", drama_layout.background_dir),
            ("prop", drama_layout.props_dir),
        ):
            for child in series_shared.asset_dirs(drama_dir, layout_dir):
                out.append(_Candidate(folder=child, kind=kind, tokens=self._tokens(child.name)))
        episodes_dir = drama_layout.episodes_dir(drama_dir)
        if episodes_dir.is_dir():
            for ep in sorted(episodes_dir.iterdir()):
                if not ep.is_dir() or ep.is_symlink():
                    continue
                # Six-module shot folders `scenes/sN/shots/stN/`, keyed by their
                # full `ep{N}_s{N}_st{N}` key.
                for shot in drama_layout.episode_shot_dirs(ep):
                    key = folder_shot_key(shot)
                    if key is not None:
                        out.append(_Candidate(shot / RENDERS_DIR_NAME, "shot", (key.value,)))
        return out

    @staticmethod
    def _tokens(folder_name: str) -> tuple[str, ...]:
        tokens: list[str] = [folder_name.lower()]
        if "_" in folder_name:
            for part in folder_name.split("_"):
                part = part.strip().lower()
                if len(part) >= 2:
                    tokens.append(part)
        seen: dict[str, None] = {}
        for t in tokens:
            if t and t not in seen:
                seen[t] = None
        return tuple(seen)

    @staticmethod
    def _classify(filename: str, candidates: list[_Candidate]) -> _Candidate | None:
        name = filename.lower()
        key = first_shot_key(name)
        if key is not None:
            hits = [c for c in candidates if c.kind == "shot" and key.value in c.tokens]
            return hits[0] if len(hits) == 1 else None
        if SHOT_KEY_HINT_RE.search(name):
            return None
        kind_priority = {"shot": 4, "prop": 3, "scene": 2, "character": 1}
        best: tuple[int, int, str, _Candidate] | None = None  # (score, kind_rank, folder_name_lex, candidate)
        for cand in candidates:
            score = 0
            for token in cand.tokens:
                if token and _token_hit(token, name):
                    if len(token) > score:
                        score = len(token)
            if score == 0:
                continue
            key = (score, kind_priority[cand.kind], -ord_seq(cand.folder.name))
            if best is None or key > best[:3]:
                best = (*key, cand)
        return best[3] if best is not None else None

    @staticmethod
    def _leftmost_grammar(filename: str, chosen: _Candidate | None) -> str | None:
        """Whose routing key a download carries: the grammar of the LEFTMOST
        scene / prop / equipment key in its stem — the prompt's first line
        precedes anything quoted from its `参考:` line. It beats a token match
        that only starts after it: that token is a word inside the key's own
        name (`bg19_加瑞克的小屋` ⊃ character `加瑞克`). A shot match is never
        overridden — renders quote keys from `参考:`."""
        if chosen is not None and chosen.kind == "shot":
            return None
        stem = Path(filename).stem
        starts = {
            grammar: key.start
            for grammar, key in (
                (_KEY_SCENE, scene_key.first_key(stem)),
                (_KEY_PROP, prop_key.first_key(stem)),
                (_KEY_EQUIPMENT, equipment_key.first_key(stem)),
            )
            if key is not None
        }
        if not starts:
            return None
        grammar = min(starts, key=starts.__getitem__)
        if chosen is not None:
            name = filename.lower()
            hits = [pos for token in chosen.tokens if token and (pos := _token_pos(token, name)) >= 0]
            if hits and starts[grammar] > min(hits):
                return None
        return grammar

    def _keyed_route(
        self, filename: str, grammar: str | None, drama_dir: Path
    ) -> SceneRouteDao | PropRouteDao | EquipmentRouteDao | None:
        """Route by the download's routing key (`_leftmost_grammar`), which names
        both destination and file name: a scene key (`bg4_闪金镇` / `bg1-1`), a
        prop key (`p15-1_正面` / `p15.glb`) or an equipment key (`e12-1_正面`).

        A model file has no other route than its prop key, so it skips the token
        check (follow-up 174); one whose equipment key comes first is an
        equipment model, which is never imported."""
        src = Path(filename)
        if src.suffix.lower() in MODEL_EXTS:
            prop, item = prop_key.first_key(src.stem), equipment_key.first_key(src.stem)
            if prop is None or (item is not None and item.start < prop.start):
                return None
            return self._prop_router.route(filename, drama_dir)
        if grammar == _KEY_EQUIPMENT:
            return self._equipment_router.route(filename, drama_dir)
        if grammar == _KEY_PROP:
            return self._prop_router.route(filename, drama_dir)
        if grammar == _KEY_SCENE:
            return self._scene_router.route(filename, drama_dir)
        return None

    @staticmethod
    def _clear_folder_media(folder: Path) -> None:
        """Delete top-level media files in a folder (overwrite support for
        single-image `v{N}_{视角}` view folders). Subfolders, non-media, and
        symlinks are left untouched."""
        try:
            entries = list(folder.iterdir())
        except OSError:
            return
        for child in entries:
            try:
                if child.is_file() and not child.is_symlink() and child.suffix.lower() in MEDIA_EXTENSIONS:
                    child.unlink()
            except OSError:
                pass

    @staticmethod
    def _clear_named_media(folder: Path, stem: str) -> None:
        """Delete `{stem}.{img ext}` files in a folder (re-import of one view:
        replace only that view, never the folder's other images)."""
        try:
            entries = list(folder.iterdir())
        except OSError:
            return
        for child in entries:
            try:
                if (child.is_file() and not child.is_symlink()
                        and child.stem == stem and child.suffix.lower() in _IMAGE_EXTS_LC):
                    child.unlink()
            except OSError:
                pass

    @staticmethod
    def _subject_number(name: str) -> int | None:
        """The `{N}` of a `bg{N}_…` folder name, else None. Name-shape only —
        use `_is_subject_folder` to decide whether it IS a subject."""
        m = _SUBJECT_FOLDER.match(name)
        return int(m.group(1)) if m else None

    @classmethod
    def _is_subject_folder(cls, folder: Path) -> bool:
        """A multi-view subject folder carries its own `{folder}.md`."""
        return (cls._subject_number(folder.name) is not None
                and (folder / (folder.name + ".md")).is_file())

    def _match_subject_any_scene(self, filename: str, drama_dir: Path) -> Path | None:
        """The subject folder a `bg{N}-{M}` download belongs to, at any depth.

        Refuses to guess: if two scenes own the same `bg{N}_`, the drama has
        violated the "subject numbers are unique across the drama" convention
        and the file is reported unmatched rather than misrouted. A series
        member's `_series/` scenes count as the drama's own here. The import
        itself goes through `SceneKeyRouter.route`, which also picks the view
        folder inside; this is the subject lookup on its own.
        """
        key = scene_key.first_key(Path(filename).stem)
        if key is None or key.view is None:
            return None
        return self._scene_router.subject(key.subject, drama_dir)

    @staticmethod
    def _prop_view_token(folder_name: str) -> str | None:
        """The 视角 routing token of an object prop's `v{N}_{视角}` view folder:
        everything after the `v{N}_` prefix. The WHOLE tail is the token: an
        object's view names (`车外全景`, `车外正面`) are mutually exclusive by
        construction and carry no tail."""
        m = _PROP_VIEW_PREFIX.match(folder_name)
        if m is None:
            return None
        return folder_name[m.end():].strip().lower() or None

    @classmethod
    def _match_prop_view(cls, filename: str, prop_folder: Path) -> Path | None:
        """When a file matched an object prop by name, route it deeper into the
        `v{N}_{视角}` view folder whose 视角 token appears in the filename.
        A prop-level asset with no view token (the object card's own image, a
        turntable `.mp4`) stays at the prop root."""
        name = filename.lower()
        best: tuple[int, str, Path] | None = None
        try:
            children = sorted(prop_folder.iterdir(), key=lambda p: p.name)
        except OSError:
            return None
        for child in children:
            if not child.is_dir() or child.is_symlink() or child.name in _NON_VIEW_DIRS:
                continue
            token = cls._prop_view_token(child.name)
            if token is None or token not in name:
                continue
            key = (len(token), child.name)
            if best is None or key > best[:2]:
                best = (len(token), child.name, child)
        return best[2] if best is not None else None

    def _match_view_any_prop(self, filename: str, drama_dir: Path) -> Path | None:
        """Route an object-prop view download by its 视角 token alone, when
        `_classify` found no prop-name match — the normal case, since the
        download filename is truncated to the prompt's first line (`车外全景`)
        and never carries the pinyin prop handle.

        Scans every `props/*/v{N}_{视角}/` folder and routes to the one whose
        视角 token appears in the filename. Disambiguation when more than one
        prop owns the same 视角: keep only views whose PROP name token also
        appears in the filename; route iff that leaves exactly one folder (else
        None → unmatched, never a silent misroute)."""
        name = filename.lower()
        all_hits: list[Path] = []
        prop_scoped_hits: list[Path] = []
        for prop in series_shared.asset_dirs(drama_dir, drama_layout.props_dir):
            prop_present = any(tok in name for tok in self._tokens(prop.name))
            try:
                children = sorted(prop.iterdir(), key=lambda p: p.name)
            except OSError:
                continue
            for child in children:
                if not child.is_dir() or child.is_symlink() or child.name in _NON_VIEW_DIRS:
                    continue
                token = self._prop_view_token(child.name)
                if token is None or token not in name:
                    continue
                all_hits.append(child)
                if prop_present:
                    prop_scoped_hits.append(child)
        pool = prop_scoped_hits or all_hits
        unique = {p.resolve() for p in pool}
        return pool[0] if len(unique) == 1 else None

    def _iter_downloads(self, cutoff: float) -> list[Path]:
        out: list[Path] = []
        try:
            # (mtime, name): the same routing key downloaded twice → the NEWER
            # take is processed last and therefore wins, deterministically.
            entries = sorted(
                self._downloads_dir.iterdir(),
                key=lambda p: (p.stat().st_mtime, p.name),
            )
        except OSError:
            return out
        for child in entries:
            try:
                if child.is_symlink():
                    continue
                if not child.is_file():
                    continue
            except OSError:
                continue
            if child.suffix.lower() not in MEDIA_EXTENSIONS:
                continue
            try:
                stat = child.stat()
            except OSError:
                continue
            if stat.st_mtime < cutoff:
                continue
            out.append(child)
        return out

    @staticmethod
    def _is_safe_basename(name: str) -> bool:
        if not name or name in (".", ".."):
            return False
        if _BASENAME_INVALID.search(name):
            return False
        if len(name) > 255:
            return False
        return True

    def _rel(self, p: Path) -> str:
        try:
            return p.resolve().relative_to(self._resolver.root).as_posix()
        except (OSError, ValueError):
            return p.as_posix()

    def _display_src(self, p: Path) -> str:
        try:
            home = Path.home().resolve()
            rel = p.resolve().relative_to(home)
            return f"~/{rel.as_posix()}"
        except (OSError, ValueError):
            return p.name


def _token_hit(token: str, name: str) -> bool:
    """Substring test guarded at the token's ASCII-alphanumeric EDGES.

    An asset folder's id prefix is a short ascii token (`c1`, `p4`, `s10`), and a
    raw substring test matches it inside longer ascii runs: `p4` ⊂ "mp4" scored a
    hit on `props/p4_…` for EVERY `.mp4` download and — tying on token length
    with the character's own `c1`, then winning on kind_priority — pulled shot
    renders and character turntables into the prop folder (`p3` ⊂ "mp3" is the
    same bug on the audio path). `s1` ⊂ "s10_…" cross-matches two scenes.

    Only ASCII edges are guarded, so a Chinese token stays a plain substring
    match and the normal `c9_白发老妇` → `c9_姥姥` join key keeps working.
    """
    return _token_pos(token, name) >= 0


def _token_pos(token: str, name: str) -> int:
    """Index of `token`'s first edge-guarded hit in `name` (see `_token_hit`), or -1."""
    start = 0
    while True:
        i = name.find(token, start)
        if i < 0:
            return -1
        j = i + len(token)
        left_clash = _ASCII_ALNUM.match(token[0]) and i > 0 and _ASCII_ALNUM.match(name[i - 1])
        right_clash = _ASCII_ALNUM.match(token[-1]) and j < len(name) and _ASCII_ALNUM.match(name[j])
        if not left_clash and not right_clash:
            return i
        start = i + 1


def ord_seq(s: str) -> int:
    # Stable lex-tiebreaker hashed to a single int (higher = lexicographically smaller wins via negation).
    total = 0
    for ch in s[:32]:
        total = (total << 8) | (ord(ch) & 0xff)
    return total


__all__ = [
    "DEFAULT_TIME_WINDOW_SECONDS",
    "DOWNLOADS_ENV_VAR",
    "DownloadsImporter",
    "ImportResult",
    "NOT_MATCHED_DIR_NAME",
    "RENDERS_DIR_NAME",
    "RenameResult",
]
