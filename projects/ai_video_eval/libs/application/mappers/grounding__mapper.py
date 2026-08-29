import re

from libs.domain.value_objects.grounding__valueobject import (
    AdjacentShot,
    CanonSlice,
    GroundingBundle,
)
from libs.domain.value_objects.shot__valueobject import ShotUnit
from libs.infrastructure.daos.canon__dao import CanonBundleDao
from libs.infrastructure.daos.config__dao import GroundingConfigDao


class GroundingMapper:
    def __init__(self, config: GroundingConfigDao) -> None:
        self._config = config

    def build(
        self,
        shot: ShotUnit,
        canon: CanonBundleDao,
        script_text: str,
        dialogue_text: str,
        prev_shot: ShotUnit | None,
        next_shot: ShotUnit | None,
        prior_ep_script: str,
        structure_text: str,
    ) -> GroundingBundle:
        cfg = self._config
        notes: list[str] = []
        role_field = shot.prompt_fields.get("角色", "") + shot.shot_context.get("Characters", "")
        scene_field = shot.prompt_fields.get("场景", "") + shot.shot_context.get("Scene", "")

        slices: list[CanonSlice] = []
        for card in canon.characters:
            if card.name and card.name in role_field:
                slices.append(
                    CanonSlice(
                        name=card.name,
                        kind="character",
                        text=self._cap(card.text, cfg.card_max_chars),
                        locked_tag=card.locked_tag,
                        voice_id=card.voice_id,
                    )
                )
        for card in canon.scenes:
            if card.name and (card.name in scene_field or card.folder in scene_field):
                slices.append(CanonSlice(card.name, "scene", self._cap(card.text, cfg.card_max_chars)))
        for card in canon.props:
            if card.name and card.name in shot.prompt_body:
                slices.append(CanonSlice(card.name, "prop", self._cap(card.text, cfg.card_max_chars)))
        if not slices:
            notes.append("未命中任何角色/场景/道具卡切片")

        world_sections = self._world_slices(canon.world_text, role_field + scene_field, cfg.world_slice_max_chars)

        return GroundingBundle(
            novel_excerpt=shot.novel_excerpt,
            canon_slices=tuple(slices),
            world_sections=world_sections,
            script_text=self._cap(script_text, cfg.script_max_chars),
            dialogue_text=self._cap(dialogue_text, cfg.dialogue_max_chars),
            prev_shot=self._adjacent(prev_shot),
            next_shot=self._adjacent(next_shot),
            prior_ep_ending=self._tail(prior_ep_script, cfg.prior_ep_ending_max_chars),
            prior_ep_summaries="",
            structure_text=self._cap(structure_text, cfg.script_max_chars),
            notes=tuple(notes),
        )

    def _adjacent(self, shot: ShotUnit | None) -> AdjacentShot | None:
        if shot is None:
            return None
        return AdjacentShot(
            shot_id=shot.shot_id,
            summary=shot.shot_context.get("Summary", ""),
            prompt_excerpt=self._cap(shot.prompt_body, self._config.adjacent_prompt_max_chars),
        )

    @staticmethod
    def _world_slices(world_text: str, needles: str, max_chars: int) -> tuple[str, ...]:
        if not world_text:
            return ()
        sections = re.split(r"\n(?=## )", world_text)
        picked: list[str] = []
        budget = max_chars
        for section in sections:
            title = section.splitlines()[0] if section else ""
            keyword_hit = any(k in title for k in ("境界", "力量", "资质", "规格", "体系", "规则"))
            name_hit = any(tok and tok in needles for tok in re.findall(r"[一-鿿]{2,4}", title))
            if keyword_hit or name_hit:
                chunk = section[: min(len(section), budget)]
                if chunk:
                    picked.append(chunk)
                    budget -= len(chunk)
                if budget <= 0:
                    break
        return tuple(picked)

    @staticmethod
    def _cap(text: str, max_chars: int) -> str:
        return text if len(text) <= max_chars else text[:max_chars] + "\n…[截断]"

    @staticmethod
    def _tail(text: str, max_chars: int) -> str:
        return text if len(text) <= max_chars else "…[截断]\n" + text[-max_chars:]
