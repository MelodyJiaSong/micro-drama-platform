from dataclasses import dataclass


@dataclass(frozen=True)
class CharacterCardDao:
    name: str
    folder: str
    text: str
    locked_tag: str | None
    voice_id: str | None


@dataclass(frozen=True)
class SceneCardDao:
    name: str
    folder: str
    text: str


@dataclass(frozen=True)
class CanonBundleDao:
    world_text: str
    style_guide_text: str
    relationships_text: str
    characters: tuple[CharacterCardDao, ...]
    scenes: tuple[SceneCardDao, ...]
    props: tuple[SceneCardDao, ...]
