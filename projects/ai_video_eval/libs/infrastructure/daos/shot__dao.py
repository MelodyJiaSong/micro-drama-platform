from dataclasses import dataclass, field


@dataclass(frozen=True)
class VoiceBlockDao:
    raw: str
    fields: dict[str, str] = field(compare=False)


@dataclass(frozen=True)
class ShotDao:
    path: str
    raw_text: str
    envelope: dict[str, str] = field(compare=False)
    title: str = ""
    novel_excerpt: str = ""
    context_bullets: dict[str, str] = field(default_factory=dict, compare=False)
    prompt_title: str = ""
    prompt_fields: dict[str, str] = field(default_factory=dict, compare=False)
    prompt_body: str = ""
    voice_blocks: tuple[VoiceBlockDao, ...] = ()
