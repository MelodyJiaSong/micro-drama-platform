import re

from libs.common.enums import SubType
from libs.domain.value_objects.shot__valueobject import DialogueLine, ShotUnit, VoiceBlock
from libs.infrastructure.daos.shot__dao import ShotDao, VoiceBlockDao

_DIALOGUE_LINE = re.compile(r"^[·•]\s*(.+?)〔(对白|内心独白|旁白|系统)〕\s*[:：]\s*(.*)$")
_NUMBER = re.compile(r"(\d+(?:\.\d+)?)")
_RATIO = re.compile(r"(\d+\s*:\s*\d+)")


class ShotMapper:
    def map(
        self,
        dao: ShotDao,
        project: str,
        sub_type: SubType,
        ep: str | None,
        shot_id: str,
        index_in_scope: int,
        total_in_scope: int,
    ) -> ShotUnit:
        duration = self._parse_duration(
            dao.prompt_fields.get("时长", "") or dao.envelope.get("duration", "")
        )
        aspect = self._parse_ratio(dao.prompt_fields.get("比例", ""))
        return ShotUnit(
            project=project,
            sub_type=sub_type,
            ep=ep,
            shot_id=shot_id,
            path=dao.path,
            raw_text=dao.raw_text,
            title=dao.title,
            novel_excerpt=dao.novel_excerpt,
            shot_context=dict(dao.context_bullets),
            prompt_title=dao.prompt_title,
            prompt_fields=dict(dao.prompt_fields),
            prompt_body=dao.prompt_body,
            voice_blocks=tuple(self._map_voice(block) for block in dao.voice_blocks),
            dialogue_lines=self._parse_dialogue(dao.prompt_fields.get("台词", "")),
            duration_s=duration,
            aspect_ratio=aspect,
            index_in_scope=index_in_scope,
            total_in_scope=total_in_scope,
        )

    @staticmethod
    def _parse_duration(text: str) -> float | None:
        match = _NUMBER.search(text)
        return float(match.group(1)) if match else None

    @staticmethod
    def _parse_ratio(text: str) -> str | None:
        match = _RATIO.search(text)
        return re.sub(r"\s", "", match.group(1)) if match else None

    @staticmethod
    def _parse_dialogue(field_text: str) -> tuple[DialogueLine, ...]:
        stripped = field_text.strip()
        if not stripped or stripped == "无" or stripped.startswith("无"):
            return ()
        lines = []
        for line in stripped.splitlines():
            match = _DIALOGUE_LINE.match(line.strip())
            if match:
                lines.append(
                    DialogueLine(
                        speaker=match.group(1).strip(),
                        dtype=match.group(2),
                        text=match.group(3).strip(),
                    )
                )
        return tuple(lines)

    def _map_voice(self, dao: VoiceBlockDao) -> VoiceBlock:
        fields = dao.fields
        return VoiceBlock(
            speaker=re.sub(r"[（(].*?[）)]", "", fields.get("角色", "")).strip(),
            timbre=fields.get("音色", ""),
            emotion=fields.get("情绪", ""),
            speed=fields.get("语速", ""),
            vtype=fields.get("类型", ""),
            line=fields.get("台词", ""),
            duration_target_s=self._parse_duration(fields.get("时长目标", "")),
            raw=dao.raw,
        )
