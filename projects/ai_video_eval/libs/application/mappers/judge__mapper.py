import json

from pydantic import BaseModel, Field, ValidationError

from libs.domain.value_objects.grounding__valueobject import GroundingBundle
from libs.domain.value_objects.judgment__valueobject import SampleJudgment
from libs.domain.value_objects.rubric__valueobject import (
    RubricDimension,
    RubricField,
    RubricSubcategory,
)
from libs.domain.value_objects.shot__valueobject import ShotUnit
from libs.infrastructure.errors.judge__error import JudgeSchemaError

_SYSTEM = (
    "你是一名 AI 短剧分镜质量评审专家。你收到：一个分镜文件（shotNN.md，含视频 prompt 与台词配音块）、"
    "它的 grounding 材料（小说原文摘录、角色/场景/道具卡切片、world 设定节选、本集剧本与台词、相邻镜）、"
    "以及本次要评的维度的评分字段清单（每个字段含判定说明与 1/3/5 分锚点描述）。\n"
    "要求：\n"
    "1. 只依据提供的材料判定，不引入外部知识；材料不足以判定时，压低 confidence 并在 justification 说明。\n"
    "2. 每个字段独立打分：grade 取 1-5 整数，对照锚点（1=严重缺陷，3=有可感问题，5=达标优秀；2/4 为居间）。\n"
    "3. evidence 必须是从分镜或 grounding 中逐字摘出的原文片段（短引文），不是转述。\n"
    "4. revision_hint 给一句具体可执行的修改建议（改哪个字段、怎么改）；grade>=4 时可为空字符串。\n"
    "5. 若两份 canon 材料互相矛盾导致无法判定，grade 给 3、confidence 给 0 并在 justification 开头写"
    "「CANON_CONFLICT:」加矛盾说明。\n"
    "6. 输出严格遵循给定 JSON schema，覆盖清单中的每个 field_id，一个不多一个不少。"
)


class _JudgmentModel(BaseModel):
    field_id: str
    grade: int = Field(ge=1, le=5)
    confidence: float
    justification: str
    evidence: list[str]
    revision_hint: str


class _JudgeOutputModel(BaseModel):
    judgments: list[_JudgmentModel]


class JudgeMapper:
    def system_prompt(self) -> str:
        return _SYSTEM

    def shared_blocks(self, shot: ShotUnit, grounding: GroundingBundle) -> list[dict]:
        parts: list[str] = [f"# 被评分镜 {shot.unit_id}\n\n{shot.raw_text}"]
        ground: list[str] = ["# Grounding 材料"]
        if grounding.novel_excerpt:
            ground.append(f"## 小说原文摘录\n{grounding.novel_excerpt}")
        for cslice in grounding.canon_slices:
            extra = ""
            if cslice.locked_tag:
                extra += f"\n【锁定描述符】{cslice.locked_tag}"
            if cslice.voice_id:
                extra += f"\n【voice_id】{cslice.voice_id}"
            ground.append(f"## {cslice.kind}卡：{cslice.name}{extra}\n{cslice.text}")
        for section in grounding.world_sections:
            ground.append(f"## world 设定节选\n{section}")
        if grounding.script_text:
            ground.append(f"## 本集 script.md\n{grounding.script_text}")
        if grounding.dialogue_text:
            ground.append(f"## 本集 dialogue.md\n{grounding.dialogue_text}")
        if grounding.structure_text:
            ground.append(f"## structure.md（单片结构）\n{grounding.structure_text}")
        if grounding.prev_shot:
            ground.append(
                f"## 上一镜 {grounding.prev_shot.shot_id}\nSummary: {grounding.prev_shot.summary}\n"
                f"```\n{grounding.prev_shot.prompt_excerpt}\n```"
            )
        if grounding.next_shot:
            ground.append(
                f"## 下一镜 {grounding.next_shot.shot_id}\nSummary: {grounding.next_shot.summary}\n"
                f"```\n{grounding.next_shot.prompt_excerpt}\n```"
            )
        if grounding.prior_ep_ending:
            ground.append(f"## 上一集结尾（script 末段）\n{grounding.prior_ep_ending}")
        return [
            {"type": "text", "text": "\n\n".join(parts)},
            {
                "type": "text",
                "text": "\n\n".join(ground),
                "cache_control": {"type": "ephemeral"},
            },
        ]

    def dimension_block(
        self, dim: RubricDimension, fields: list[tuple[RubricSubcategory, RubricField]]
    ) -> dict:
        lines = [
            f"# 本次评审维度：{dim.name_cn}（{dim.dim_id}）",
            dim.description,
            "",
            "## 评分字段清单",
        ]
        for sub, fld in fields:
            lines.extend(
                [
                    f"### field_id: {fld.field_id}",
                    f"- 子类: {sub.name_cn} ({sub.sub_id})",
                    f"- 名称: {fld.name_cn}",
                    f"- 判定说明: {fld.judge_instruction}",
                    f"- 1分锚点: {fld.anchors.get('g1', '')}",
                    f"- 3分锚点: {fld.anchors.get('g3', '')}",
                    f"- 5分锚点: {fld.anchors.get('g5', '')}",
                    "",
                ]
            )
        lines.append("对以上每个 field_id 输出一条 judgment。")
        return {"type": "text", "text": "\n".join(lines)}

    @staticmethod
    def output_schema(field_ids: list[str]) -> dict:
        return {
            "type": "object",
            "additionalProperties": False,
            "required": ["judgments"],
            "properties": {
                "judgments": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": [
                            "field_id",
                            "grade",
                            "confidence",
                            "justification",
                            "evidence",
                            "revision_hint",
                        ],
                        "properties": {
                            "field_id": {"type": "string", "enum": field_ids},
                            "grade": {"type": "integer", "enum": [1, 2, 3, 4, 5]},
                            "confidence": {"type": "number"},
                            "justification": {"type": "string"},
                            "evidence": {"type": "array", "items": {"type": "string"}},
                            "revision_hint": {"type": "string"},
                        },
                    },
                }
            },
        }

    @staticmethod
    def extract_json(text: str) -> str:
        stripped = text.strip()
        try:
            json.loads(stripped)
            return stripped
        except json.JSONDecodeError:
            pass
        import re

        match = re.search(r"```(?:json)?\s*\n(.*?)```", stripped, re.DOTALL)
        if match:
            candidate = match.group(1).strip()
            try:
                json.loads(candidate)
                return candidate
            except json.JSONDecodeError:
                pass
        start = stripped.find("{")
        end = stripped.rfind("}")
        if 0 <= start < end:
            return stripped[start : end + 1]
        return stripped

    @staticmethod
    def parse(text: str, expected_ids: list[str]) -> dict[str, SampleJudgment]:
        try:
            model = _JudgeOutputModel.model_validate(json.loads(JudgeMapper.extract_json(text)))
        except (json.JSONDecodeError, ValidationError) as exc:
            raise JudgeSchemaError(f"judge output failed validation: {exc}") from exc
        by_id: dict[str, SampleJudgment] = {}
        for judgment in model.judgments:
            if judgment.field_id not in expected_ids:
                continue
            by_id[judgment.field_id] = SampleJudgment(
                grade=judgment.grade,
                confidence=max(0.0, min(1.0, judgment.confidence)),
                justification=judgment.justification,
                evidence=tuple(judgment.evidence),
                revision_hint=judgment.revision_hint,
            )
        missing = [fid for fid in expected_ids if fid not in by_id]
        if missing:
            raise JudgeSchemaError(f"judge output missing fields: {missing}")
        return by_id

