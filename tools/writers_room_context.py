"""构建角色专用上下文；作者全局资料不自动进入角色包。

人格源必须先清理否定式秘密泄漏。observations 是已审核的可感知标注，
不是把原始全知剧本交给模型自行过滤。本工具不替代逐拍知识审查。
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path


OWN_MODEL_FIELDS = (
    "key", "name", "profession", "age", "core_identity", "goal_priority",
    "goal_priority_semantics", "initial_knowledge", "not_known", "rules",
    "voice_examples", "habitual_failure_patterns",
)
OWN_ABILITY_FIELDS = ("mundane_allowed", "supernatural_allowed", "new_unlocks")
OUTGOING_FIELDS = (
    "from", "to", "social", "known_boundary", "wants", "trust_gain_trigger",
    "trust_loss_trigger", "from_perception_bias", "transition_semantics",
)


def build_character_packet(bibles: dict, relationships: dict, character_id: str,
                           *, state_view: dict | None = None,
                           observations: list[dict] | None = None) -> dict:
    matches = [c for c in bibles["characters"] if c["key"] == character_id]
    if len(matches) != 1:
        raise ValueError("角色必须在人物源中唯一存在")
    own = matches[0]
    if state_view is not None and state_view.get("character_id") != character_id:
        raise ValueError("动态视图不属于当前角色，拒绝混用")
    model = {key: copy.deepcopy(own[key]) for key in OWN_MODEL_FIELDS if key in own}
    model["dimensions"] = [
        {"id": d["id"], "label": d["label"], "critical_questions": [
            {"id": q["id"], "question": q["question"], "answer": q["answer"]}
            for q in d["critical_questions"]
        ]}
        for d in own["dimensions"] if d["id"] != "growth"
    ]
    abilities = own.get("ability_boundary", {})
    model["ability_boundary"] = {
        key: copy.deepcopy(abilities[key]) for key in OWN_ABILITY_FIELDS if key in abilities
    }
    outgoing = [
        {key: copy.deepcopy(edge[key]) for key in OUTGOING_FIELDS if key in edge}
        for edge in relationships.get("edges", []) if edge["from"] == character_id
    ]
    dynamic = None
    if state_view is not None:
        current = state_view["character_state"]
        if any(event.get("actor") != character_id for event in current.get("recent_events", [])):
            raise ValueError("动态事件含其他角色，拒绝混用")
        if any(not key.startswith(character_id + "->") for key in current.get("relationships", {})):
            raise ValueError("动态关系含其他角色出向关系，拒绝混用")
        # 全局 facts、全员状态和作者伏笔不在动态白名单内。
        dynamic = {key: copy.deepcopy(current[key]) for key in
                   ("knowledge", "relationships", "physical", "recent_events") if key in current}
    return {
        "schema_version": 1,
        "character_id": character_id,
        "as_of": state_view.get("as_of", "故事开场前") if state_view else "故事开场前",
        "own_model": model,
        "outgoing_relationships_at_start": outgoing,
        "own_current_state": dynamic,
        "observable_annotations": copy.deepcopy(observations or []),
        "instruction": (
            "技术角色ID和模型里的他人称呼不是角色已知姓名；名字只按知识事件或当面介绍使用。"
            "动态认识优先于开场基线；关系触发是可能性，不是已经发生。"
            "只根据自身模型、自己所知和现场可感知事实作选择；允许误判、夸口、犹豫与错误。"
            "主观声称不变成事实，不添能力。人格定义也不意味着本人会说出准确的心理诊断。"
        ),
        "scope": "结构白名单；不声称自动验证可感知标注或穷尽对白的隐含知识",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("room", type=Path)
    ap.add_argument("character")
    ap.add_argument("--state", type=Path)
    ap.add_argument("--observations", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    sources = [args.room / "character_bibles.json", args.room / "relationship_baseline.json"]
    if args.state:
        sources.append(args.state)
    if args.observations:
        sources.append(args.observations)
    blobs = {p: p.read_bytes() for p in sources}
    values = {p: json.loads(blob.decode("utf-8")) for p, blob in blobs.items()}
    packet = build_character_packet(
        values[sources[0]], values[sources[1]], args.character,
        state_view=values[args.state] if args.state else None,
        observations=values[args.observations] if args.observations else None,
    )
    packet["input_sha256"] = {p.as_posix(): hashlib.sha256(b).hexdigest() for p, b in blobs.items()}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"角色包已写入 {args.out}；未包含全局人物、事实与成长维")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
