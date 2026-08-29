import hashlib
import json
from dataclasses import dataclass, field


@dataclass(frozen=True)
class CanonSlice:
    name: str
    kind: str
    text: str
    locked_tag: str | None = None
    voice_id: str | None = None


@dataclass(frozen=True)
class AdjacentShot:
    shot_id: str
    summary: str
    prompt_excerpt: str


@dataclass(frozen=True)
class GroundingBundle:
    novel_excerpt: str
    canon_slices: tuple[CanonSlice, ...] = ()
    world_sections: tuple[str, ...] = ()
    script_text: str = ""
    dialogue_text: str = ""
    prev_shot: AdjacentShot | None = None
    next_shot: AdjacentShot | None = None
    prior_ep_ending: str = ""
    prior_ep_summaries: str = ""
    structure_text: str = ""
    notes: tuple[str, ...] = field(default_factory=tuple)

    @property
    def content_hash(self) -> str:
        payload = json.dumps(
            {
                "novel": self.novel_excerpt,
                "canon": [(s.name, s.kind, s.text, s.locked_tag, s.voice_id) for s in self.canon_slices],
                "world": list(self.world_sections),
                "script": self.script_text,
                "dialogue": self.dialogue_text,
                "prev": (self.prev_shot.shot_id, self.prev_shot.summary, self.prev_shot.prompt_excerpt)
                if self.prev_shot
                else None,
                "next": (self.next_shot.shot_id, self.next_shot.summary, self.next_shot.prompt_excerpt)
                if self.next_shot
                else None,
                "prior_ending": self.prior_ep_ending,
                "prior_summaries": self.prior_ep_summaries,
                "structure": self.structure_text,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()
