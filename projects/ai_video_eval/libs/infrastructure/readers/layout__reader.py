import glob
import os
import re
from dataclasses import dataclass

from libs.common.enums import SubType
from libs.domain.errors.eval__error import ArtifactError


@dataclass(frozen=True)
class ProjectLayout:
    project: str
    root: str
    sub_type: SubType
    canon_dir: str | None
    script_dir: str | None
    shots_root: str
    episodes: tuple[str, ...]


class LayoutReader:
    def __init__(self, videos_root: str) -> None:
        self._videos_root = videos_root

    def detect(self, project: str) -> ProjectLayout:
        root = os.path.join(self._videos_root, project)
        if not os.path.isdir(root):
            raise ArtifactError(f"project not found: {root}")

        stage56 = self._find_dir(root, ("5_6_*", "*分镜与prompt*"))
        canon = self._find_dir(root, ("2_*", "*世界观人设*"))
        script = self._find_dir(root, ("4_*", "*剧本*"))

        if stage56 is None:
            legacy_eps = os.path.join(root, "episodes")
            if os.path.isdir(legacy_eps):
                eps = self._episode_names(legacy_eps)
                return ProjectLayout(project, root, SubType.NOVEL, root, root, legacy_eps, eps)
            raise ArtifactError(f"no 分镜 stage dir found under {root}")

        ep_dir = os.path.join(stage56, "episodes")
        if os.path.isdir(ep_dir):
            return ProjectLayout(
                project, root, SubType.NOVEL, canon, script, ep_dir, self._episode_names(ep_dir)
            )
        shots_dir = os.path.join(stage56, "shots")
        if os.path.isdir(shots_dir):
            return ProjectLayout(project, root, SubType.SHORT, canon, script, shots_dir, ())
        raise ArtifactError(f"neither episodes/ nor shots/ under {stage56}")

    def shot_paths(self, layout: ProjectLayout, ep: str | None) -> list[str]:
        if layout.sub_type is SubType.NOVEL:
            if ep is None:
                raise ArtifactError("episode required for novel-layout project")
            shots_dir = os.path.join(layout.shots_root, ep, "shots")
        else:
            shots_dir = layout.shots_root
        if not os.path.isdir(shots_dir):
            raise ArtifactError(f"shots dir not found: {shots_dir}")
        paths = []
        for shot_dir in sorted(os.listdir(shots_dir)):
            match = re.fullmatch(r"shot(\d+)", shot_dir)
            if not match:
                continue
            candidate = os.path.join(shots_dir, shot_dir, f"{shot_dir}.md")
            if os.path.isfile(candidate):
                paths.append(candidate)
        return paths

    def script_paths(self, layout: ProjectLayout, ep: str | None) -> tuple[str | None, str | None]:
        if layout.script_dir is None:
            return None, None
        if layout.sub_type is SubType.NOVEL and ep is not None:
            base = os.path.join(layout.script_dir, "episodes", ep)
            return self._existing(base, "script.md"), self._existing(base, "dialogue.md")
        return self._existing(layout.script_dir, "script.md"), self._existing(layout.script_dir, "dialogue.md")

    def structure_path(self, layout: ProjectLayout) -> str | None:
        outline = self._find_dir(layout.root, ("3_*", "*大纲*"))
        if outline is None:
            return None
        for name in ("structure.md", "arc_outline.md"):
            found = self._existing(outline, name)
            if found:
                return found
        return None

    @staticmethod
    def _episode_names(ep_dir: str) -> tuple[str, ...]:
        return tuple(
            sorted(name for name in os.listdir(ep_dir) if re.fullmatch(r"ep\d+", name))
        )

    @staticmethod
    def _find_dir(root: str, patterns: tuple[str, ...]) -> str | None:
        for pattern in patterns:
            hits = sorted(p for p in glob.glob(os.path.join(root, pattern)) if os.path.isdir(p))
            if hits:
                return hits[0]
        return None

    @staticmethod
    def _existing(base: str, name: str) -> str | None:
        path = os.path.join(base, name)
        return path if os.path.isfile(path) else None
