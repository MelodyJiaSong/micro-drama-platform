import re
from typing import Callable

from libs.common.constants import PROMPT_FIELD_ALIASES
from libs.common.enums import FieldStatus
from libs.domain.errors.eval__error import RubricError
from libs.domain.value_objects.grounding__valueobject import GroundingBundle
from libs.domain.value_objects.judgment__valueobject import FieldResult
from libs.domain.value_objects.rubric__valueobject import RubricField
from libs.domain.value_objects.shot__valueobject import ShotUnit

RuleFn = Callable[[ShotUnit, GroundingBundle, dict], tuple[bool | None, list[str]]]


def _scope_text(shot: ShotUnit, scope: str) -> str:
    if scope == "prompt_body":
        return shot.prompt_body
    if scope == "dialogue_field":
        return shot.prompt_fields.get("台词", "")
    if scope == "voice_blocks":
        return "\n".join(block.raw for block in shot.voice_blocks)
    return shot.raw_text


def _char_count_max(shot: ShotUnit, _: GroundingBundle, params: dict) -> tuple[bool | None, list[str]]:
    limit = int(params.get("max", 2000))
    count = shot.prompt_char_count
    ok = count <= limit
    return ok, [f"视频 prompt 全字符数 {count} / 上限 {limit}"]


def _required_prompt_fields(shot: ShotUnit, _: GroundingBundle, params: dict) -> tuple[bool | None, list[str]]:
    required = params.get("fields", [])
    missing = [
        name for name in required
        if PROMPT_FIELD_ALIASES.get(str(name), str(name)) not in shot.prompt_fields
    ]
    if missing:
        return False, [f"缺失字段: {', '.join(missing)}"]
    return True, ["必备字段齐全"]


def _forbidden_pattern(shot: ShotUnit, _: GroundingBundle, params: dict) -> tuple[bool | None, list[str]]:
    pattern = str(params.get("pattern", ""))
    scope = str(params.get("scope", "prompt_body"))
    text = _scope_text(shot, scope)
    hits = re.findall(pattern, text)
    if hits:
        sample = ", ".join(str(h) for h in hits[:5])
        return False, [f"{params.get('description', '禁用模式')} 命中 {len(hits)} 处: {sample}"]
    return True, [f"{params.get('description', '禁用模式')} 未命中"]


def _required_pattern(shot: ShotUnit, _: GroundingBundle, params: dict) -> tuple[bool | None, list[str]]:
    pattern = str(params.get("pattern", ""))
    scope = str(params.get("scope", "prompt_body"))
    if re.search(pattern, _scope_text(shot, scope)):
        return True, [f"{params.get('description', '必需模式')} 已命中"]
    return False, [f"{params.get('description', '必需模式')} 未命中: {pattern}"]


def _duration_range(shot: ShotUnit, _: GroundingBundle, params: dict) -> tuple[bool | None, list[str]]:
    if shot.duration_s is None:
        return False, ["时长字段缺失或无法解析"]
    lo, hi = float(params.get("min", 4)), float(params.get("max", 15))
    ok = lo <= shot.duration_s <= hi
    return ok, [f"时长 {shot.duration_s}s（要求 {lo}–{hi}s）"]


def _aspect_ratio(shot: ShotUnit, _: GroundingBundle, params: dict) -> tuple[bool | None, list[str]]:
    expected = str(params.get("expected", "9:16"))
    if shot.aspect_ratio is None:
        return False, ["比例字段缺失"]
    ok = shot.aspect_ratio == expected
    return ok, [f"比例 {shot.aspect_ratio}（要求 {expected}）"]


def _voice_block_when_dialogue(shot: ShotUnit, _: GroundingBundle, params: dict) -> tuple[bool | None, list[str]]:
    if not shot.has_dialogue:
        return True, ["无台词，不需配音块"]
    if not shot.voice_blocks:
        return False, ["有台词但缺少 台词配音 块"]
    problems = []
    for block in shot.voice_blocks:
        missing = [
            label for label, value in
            (("音色", block.timbre), ("类型", block.vtype), ("台词", block.line))
            if not value
        ]
        if block.duration_target_s is None:
            missing.append("时长目标")
        if missing:
            problems.append(f"{block.speaker or '?'} 配音块缺 {', '.join(missing)}")
    if problems:
        return False, problems
    return True, [f"配音块齐全（{len(shot.voice_blocks)} 块）"]


def _locked_descriptor_byte_match(shot: ShotUnit, grounding: GroundingBundle, params: dict) -> tuple[bool | None, list[str]]:
    role_field = shot.prompt_fields.get("角色", "")
    relevant = [
        s for s in grounding.canon_slices
        if s.kind == "character" and s.locked_tag and s.name and s.name in role_field
    ]
    if not relevant:
        return None, ["无可核对的锁定描述符（角色卡未命中或未提供锁定标签）"]
    misses = [s.name for s in relevant if s.locked_tag not in role_field]
    if misses:
        return False, [f"锁定描述符未逐字节出现在 角色: 字段: {', '.join(misses)}"]
    return True, [f"锁定描述符逐字节一致（{len(relevant)} 角色）"]


def _dialogue_speed_max(shot: ShotUnit, _: GroundingBundle, params: dict) -> tuple[bool | None, list[str]]:
    max_cps = float(params.get("max_cps", 5))
    if not shot.voice_blocks:
        return True, ["无配音块，不检语速"]
    notes, ok, computable = [], True, False
    for block in shot.voice_blocks:
        if block.duration_target_s is None or block.duration_target_s <= 0:
            notes.append(f"{block.speaker or '?'}: 时长目标缺失，无法核算语速")
            continue
        computable = True
        chars = len(re.sub(r"[\s，。！？、：；「」『』“”…—,.!?:;\"']", "", block.line))
        cps = chars / block.duration_target_s
        notes.append(f"{block.speaker or '?'}: {chars}字/{block.duration_target_s}s = {cps:.1f}字/秒")
        if cps > max_cps:
            ok = False
    if not computable:
        return None, notes
    return ok, notes


def _envelope_present(shot: ShotUnit, _: GroundingBundle, params: dict) -> tuple[bool | None, list[str]]:
    ok = shot.raw_text.lstrip().startswith("---")
    return ok, ["YAML envelope 存在" if ok else "缺少 YAML envelope"]


def _shot_context_required(shot: ShotUnit, _: GroundingBundle, params: dict) -> tuple[bool | None, list[str]]:
    keys = [str(k) for k in params.get("keys", [])]
    missing = [k for k in keys if k not in shot.shot_context]
    if missing:
        return False, [f"Shot context 缺行: {', '.join(missing)}"]
    return True, ["Shot context 必备行齐全"]


_REGISTRY: dict[str, RuleFn] = {
    "char_count_max": _char_count_max,
    "required_prompt_fields": _required_prompt_fields,
    "forbidden_pattern": _forbidden_pattern,
    "required_pattern": _required_pattern,
    "duration_range": _duration_range,
    "aspect_ratio": _aspect_ratio,
    "voice_block_when_dialogue": _voice_block_when_dialogue,
    "locked_descriptor_byte_match": _locked_descriptor_byte_match,
    "dialogue_speed_max": _dialogue_speed_max,
    "no_hex_colors": lambda shot, g, p: _forbidden_pattern(
        shot, g, {"pattern": r"#[0-9a-fA-F]{3,8}\b", "scope": "prompt_body", "description": "hex 色值"}
    ),
    "envelope_present": _envelope_present,
    "shot_context_required": _shot_context_required,
}


def known_rule_ids() -> set[str]:
    return set(_REGISTRY)


def evaluate_rule(
    fld: RubricField,
    dim_id: str,
    sub_id: str,
    shot: ShotUnit,
    grounding: GroundingBundle,
    overrides: dict[str, object] | None = None,
) -> FieldResult:
    if fld.rule_id not in _REGISTRY:
        raise RubricError(f"unknown rule_id '{fld.rule_id}' on field '{fld.field_id}'")
    params = dict(fld.rule_params)
    if overrides:
        if fld.rule_id == "aspect_ratio" and "aspect_ratio" in overrides:
            params["expected"] = overrides["aspect_ratio"]
    passed, notes = _REGISTRY[fld.rule_id](shot, grounding, params)
    if passed is None:
        return FieldResult(
            field_id=fld.field_id, dim_id=dim_id, sub_id=sub_id,
            status=FieldStatus.INCONCLUSIVE, grade=None, confidence=0.0, spread=0.0,
            justification="；".join(notes), evidence=tuple(notes), revision_hint="", source="rule",
        )
    grade = 5.0 if passed else 1.0
    hint = "" if passed else f"修复 {fld.name_cn}：{notes[0] if notes else fld.field_id}"
    return FieldResult(
        field_id=fld.field_id, dim_id=dim_id, sub_id=sub_id,
        status=FieldStatus.GRADED, grade=grade, confidence=1.0, spread=0.0,
        justification="；".join(notes), evidence=tuple(notes), revision_hint=hint, source="rule",
    )
