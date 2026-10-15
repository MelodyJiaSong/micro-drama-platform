from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CastMember:
    """One person in a shot: the asset key from filming (`c1-1`), the name the prompt uses, and the files that pin them."""
    key: str
    name: str
    image: str               # three-view sheet (front / side / back of the same person)
    color: str
    voice: str | None = None
    look: str = ""           # the card's prompt-ready appearance text
    speaks: bool = False
    image_key: str = ""      # key id on the 参考 line: costume-stage folder (c1-1_…) or character card (c14_…)
    voice_key: str = ""      # key id of the voice sample: {card}_audio


@dataclass(frozen=True)
class PropItem:
    """A story prop in frame (`p475`): its anchor image pins shape, material and colour across shots (follow-up 231)."""
    key: str
    name: str
    image: str               # the prop card's anchor image
    image_key: str = ""      # key id on the 参考 line: the prop folder name (p475_葡萄手推车)
    look: str = ""           # the prop card's prompt-ready description


@dataclass(frozen=True)
class ShotMaterials:
    """Everything a shot's prompt references, resolved from disk before compiling.

    `motion` is the previz video when the overhead decision says the shot is complex, otherwise the overhead image
    drawn for the model. Paths are repo-relative. `errors` lists what is missing; compiling refuses while any remain.
    """
    motion_kind: str = ""          # "video" (previz) | "image" (overhead)
    motion: str = ""
    cast: tuple[CastMember, ...] = ()
    scene_image: str = ""
    errors: tuple[str, ...] = field(default_factory=tuple)
    scene_text: str = ""       # the background card's prompt-ready description
    scene_key: str = ""        # key id of the background: its folder name (bg2-6_武厅_兵器架)
    props: tuple[PropItem, ...] = ()


@dataclass(frozen=True)
class PromptSettings:
    """Drama-level prompt settings from the drama's workflow.json `prompt` block."""
    style: str = ""
    ratio: str = "16:9"
    negatives: str = ""
