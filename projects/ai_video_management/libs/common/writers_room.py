from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json

WRITERS_ROOM_VERSION = "1.0.0"
MAX_CALLS = 100
MAX_REWRITES = 3
SCENE_TIMEOUT_S = 1800
RELATION_DIMENSIONS = ("trust", "respect", "affection", "fear", "resentment", "debt", "suspicion", "dependency", "rivalry")
QUALITY_DIMENSIONS = ("character_consistency", "dialogue_naturalness", "emotional_consistency", "relationship_consistency", "knowledge_consistency", "plot_logic", "timeline", "pacing", "creative_balance", "subtext", "visual_storytelling", "ai_ness")


@dataclass(frozen=True)
class EditorSpec:
    id: str
    name: str
    focus: str
    tags: tuple[str, ...]


EDITORS = (
    EditorSpec("comedy", "搞笑", "关系反差、误解、嘴硬；不破坏危险和悲伤的分量", ("comedy",)),
    EditorSpec("emotion", "感人", "克制照顾、遗憾、小动作和回忆；避免煽情解释", ("emotion",)),
    EditorSpec("friendship", "兄弟情 / 友情", "默契、互坑、经历与关键保护；关系要有铺垫", ("friendship",)),
    EditorSpec("combat", "战斗", "目的、环境、空间、战术、能力和代价；禁止突然升级", ("combat",)),
    EditorSpec("romance", "爱情", "试探、边界与行动中的偏爱；不能强加关系", ("romance",)),
    EditorSpec("suspense", "悬疑", "信息差和可追踪线索；不能为了悬念降智", ("suspense",)),
    EditorSpec("growth", "人物成长", "旧策略失效、选择的代价、改变与复发", ("growth",)),
    EditorSpec("world", "世界观", "用行动显露世界规则，不写设定说明书", ("world",)),
    EditorSpec("foreshadowing", "伏笔", "已有线索与回收依据，不创造无出处呼应", ("foreshadowing",)),
    EditorSpec("visual", "视觉叙事", "用可见动作、空间和道具代替解释，确保观众能理解", ()),
)


def content_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()


def interview_questions() -> list[dict[str, object]]:
    groups = {
        "identity": ("核心认同", ["最想被怎样看待？", "最不能接受什么对待？", "最害怕失去什么？", "利益、感情、原则冲突时先保什么？", "自认是什么人，但做过什么相反的事？"], ["尊严与认可", "亲近的人与归属", "原则与责任", "安全与自由"]),
        "psychology": ("心理与防御", ["被戳到痛处时先怎么反应？", "被真心关心时通常怎么回应？", "什么最容易引起羞耻或愤怒？", "害怕时会怎样掩饰？", "做错事之后怎样面对愧疚？"], ["沉默或退出", "玩笑或转移话题", "控制或反击", "讨好或解释"]),
        "cognition": ("思维与判断", ["先相信什么判断事情？", "哪类事情最有经验？", "最容易误解别人什么？", "发现判断错了会怎么做？", "何时愿意承认自己不知道？"], ["亲眼观察", "过往经验", "可信的人", "规则与权威"]),
        "speech": ("语言与声口", ["通常怎么拒绝别人？", "怎么向人求助？", "生气时语言怎样变化？", "怎么表达关心？", "撒谎时哪里容易露馅？"], ["直接短句", "委婉绕开", "用玩笑包装", "先说行动或条件"]),
        "behavior": ("行为规则", ["当众被羞辱时怎么做？", "受到威胁时先保护什么？", "面对弱者会怎么行动？", "失去控制时做什么？", "什么情况会打破平时的习惯？"], ["先观察再行动", "立即抢先行动", "寻求同伴协助", "撤退或拖延"]),
        "goals": ("目标与代价", ["长远最想得到什么？", "眼前最需要解决什么？", "不愿让人知道的目标是什么？", "为目标愿意付出什么？", "目标失败时会怎样改变策略？"], ["证明自己的价值", "保护某个人", "找回或修复失去的东西", "获得自由与安全"]),
        "relationships": ("关系与变化", ["怎样才开始信任一个人？", "朋友让自己失望时怎么做？", "欠了人情如何偿还？", "面对权威和朋友表达有何不同？", "什么事件会真正改变两人的关系？"], ["观察实际行动", "一起承担风险", "坦诚交流", "长期履行承诺"]),
    }
    choices = {
        "identity_1": ["能扛事、可靠", "聪明、有本事", "独立、不受摆布"],
        "identity_2": ["当众羞辱", "亲近的人背叛", "替自己做决定"],
        "identity_3": ["重要的人", "尊严和能力", "自由和安全"],
        "identity_4": ["先保亲近的人", "先守原则", "先保眼前生存"],
        "identity_5": ["自认勇敢，却逃过一次", "自认冷淡，却舍不得放手", "自认正直，却隐瞒过真相"],
        "psychology_1": ["沉默后离开", "用玩笑挡回去", "立即反击"],
        "psychology_2": ["转移话题", "嘴上拒绝，行动接受", "直接回应"],
        "psychology_3": ["被说没有本事", "被当成累赘", "自己伤害了信任自己的人"],
        "psychology_4": ["说得比平时多", "话更少、动作更谨慎", "试着控制每一个细节"],
        "psychology_5": ["直接认错", "先弥补，再说原因", "拖延或辩解，后来才面对"],
        "cognition_1": ["亲眼所见", "经验和直觉", "可信的人"],
        "cognition_2": ["实践与手艺", "人情和察言观色", "书本、制度与规则"],
        "cognition_3": ["把沉默当拒绝", "把关心当轻视", "把自信当可靠"],
        "cognition_4": ["马上调整并承认", "先补救，晚一点认错", "继续撑到无法维持"],
        "cognition_5": ["发现证据不足时", "信任的人追问时", "试过失败以后"],
        "speech_1": ["直接说不", "给条件或替代办法", "开玩笑绕过去"],
        "speech_2": ["直接叫名字、说需要", "把请求说成交换", "到撑不住才开口"],
        "speech_3": ["更短、更轻", "说快、打断对方", "客气得不自然"],
        "speech_4": ["做一件实际的小事", "损两句，再帮忙", "一句很短的问候"],
        "speech_5": ["解释过多", "刻意不看人", "回答太快或重复问句"],
        "behavior_1": ["先沉默再反击", "当场顶回去", "记住，等有把握再算账"],
        "behavior_2": ["身边的人", "退路与主动权", "眼前最关键的物件或任务"],
        "behavior_3": ["不声张地帮一把", "先问清对方真正需要什么", "装作不在意，仍留下来"],
        "behavior_4": ["把能做的事一件件数清", "抢先行动", "找一个可信的人协助"],
        "behavior_5": ["重要的人遭到伤害", "自己的旧办法伤害了别人", "有人愿意替自己承担代价"],
        "goals_1": ["成为被需要的人", "保护与安顿亲近的人", "获得独立生活的能力"],
        "goals_2": ["兑现已经答应的事", "走出眼前的危险", "找到继续留下的理由"],
        "goals_3": ["让某人后悔看轻自己", "修补一件不敢承认的过错", "离开别人安排的生活"],
        "goals_4": ["时间、钱和面子", "人情与关系风险", "身体代价，但不出卖他人"],
        "goals_5": ["换办法继续", "缩小目标先保住一个人", "短暂退出，重新判断"],
        "relationships_1": ["对方按约回来", "一起承担具体风险", "对方敢说不知道或做不到"],
        "relationships_2": ["先把事问清", "嘴上冷淡，仍留退路", "暂时拉开距离"],
        "relationships_3": ["记住，找实际机会还", "立即做等值交换", "替对方承担一次风险"],
        "relationships_4": ["对权威客气，对朋友直接", "对权威逞强，对朋友开玩笑", "两边都短句，但行动不同"],
        "relationships_5": ["关键时刻按承诺出现", "承认错误并实际承担代价", "尊重自己不愿说出的边界"],
    }
    return [{"id": f"{group}_{i+1}", "dimension": label, "title": title, "options": [{"value": chr(65+j), "label": option} for j, option in enumerate(choices[f"{group}_{i+1}"])], "multiple": False} for group, (label, titles, _options) in groups.items() for i, title in enumerate(titles)]
