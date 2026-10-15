from __future__ import annotations

import hashlib
import json
from typing import Any

WORKFLOW_ID = "three-module-v1"
WORKFLOW_MARKER = "workflow.json"
MODULES = ("story", "filming", "prompts")
# Later stages are placeholders until designed: navigation lists them, but they have no episode documents yet.
PLACEHOLDER_STAGES = ("edit", "sound", "delivery")
MODULE_LABELS = {"story": "故事创作", "filming": "影视改编", "prompts": "Prompt 编译与出片"}
STAGE_LABELS = {**MODULE_LABELS, "edit": "剪辑", "sound": "声音与音乐", "delivery": "成片交付"}
MODULE_NAV_LABELS = {"story": "2_故事", "filming": "3_影视改编", "prompts": "4_Prompt编译与出片",
                     "edit": "5_剪辑", "sound": "6_声音与音乐", "delivery": "7_成片交付"}
WORLD_FACTS_FILE = "world_rules.md"
STATE_CHANGES_FILE = "state_changes.md"
COMPILER_VERSION = 9
VIDEO_SOUND_RULE = "仅保留本镜指定对白、自然环境声和动作声；不要背景音乐或配乐。"
SILENT_SHOT_RULE = "本镜没有人说话。"
ONE_TAKE_RULE = "连续镜头，不要切镜。不要字幕或水印。"
# v5 (follow-up 227): every shot carries references and says what each one is for.
# v6 (follow-up 228): one 参考 line; every person's three-view sheet and voice sample; the background image; the card's
# full appearance text and the background card's scene text; scene purpose, lip-sync and negative lines; up to 5000 chars.
# v7 (follow-up 229): the 参考 line lists `key_id=>@` placeholders; the body names references by key id, and the
# per-shot 资料包 fills each @ with the upload number (@图片1 …) in upload order.
# v8 (follow-up 231): shots may list story props (`props: ["p475"]`); each prop's anchor image joins the 参考 line after the
# three-view sheets, with a 道具 line carrying the prop card's description, so a cart or a bundle keeps one shape across shots.
# v9 (follow-up 245): the twin rule binds people only; animals (m* cast, e.g. three wolves from one card) appear as many
# times as the 画面 line says, and the negative line names people, not every character.
ANTI_TWIN_RULE = "画面中每个人物只出现一次，不要分身或双胞胎。"
ANIMAL_COUNT_RULE = "动物（{keys}）按「画面」写的数量出现，同一张三视图可以是几只同类。"
NATURAL_MOTION_RULE = "人物按真人自然表演：走路有重心起伏和摆臂，发力有预备和惯性，不照搬参考里人偶的僵硬姿势。"
OVERHEAD_USAGE = ("`{tag}`是本镜的俯视站位示意图，不是画面：上方为北，彩色圆点是人物（尖角＝面朝，箭头＝走位路线，旁边数字＝到达秒数），"
                  "红色机身与扇形是机位与视野，灰色方块是建筑与陈设。只按它安排机位、站位、朝向与走位先后；"
                  "图里的颜色、线条、箭头和文字都不出现在画面中，人物颜色也不是服装颜色。")
PREVIZ_USAGE = ("`{tag}`是绿幕前纯色小人偶的走位预演：只参考其中的机位、运镜、人物站位、朝向、走位路线和动作时刻；"
                "不参考人偶的外形与颜色，画面里不出现绿幕和人偶；人偶颜色只是身份标记，不是服装颜色。")
CAST_USAGE = ("每张人物三视图（{keys}）是同一个人的正面、侧面、背面，不是三个人；只取这个人的长相、发型、体型与服装，"
              "不取图里的姿势、站位和机位，三视图的浅灰背景不入画。")
SCENE_USAGE = "场景图`{scene}`只取材质、形制、陈设与色调，空间关系以`{motion}`为准，光线与时段按「光线」一行，场景图里的光向不照搬。"
PROP_USAGE = ("道具图（{keys}）是本镜出现的道具：只取它的形制、尺寸比例、材质与配色，画面里它就是这一件，不换成别的样式；"
              "不取道具图的浅灰背景、机位与摆放角度。")
VOICE_USAGE = "声音参考（{keys}）只取该人物的音色、音高与说话质感，不取内容；本镜不说话的人物不出声。"
LIP_SYNC_RULE = "画内说话的人嘴型与台词同步，正常语速与口型；每句只由标明的人说，其他人不开口。"
BASE_NEGATIVES = ("分身，双胞胎，同一人物出现两次，多出来的人，画面文字，字幕，水印，logo，背景音乐，"
                  "绿幕，纯色人偶，示意图的圆点、箭头、线条与文字")
CAST_KEY_RE = r"[cm][1-9]\d*(?:-[1-9]\d*)?"
PROP_KEY_RE = r"p[1-9]\d*"
PROMPT_MAX_CHARS = 5000


def fingerprint(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def scene_revision(scene: dict[str, Any], filming_source: str | None) -> str:
    """What one compiled scene was compiled from (follow-up 259): the filming scene plus the story revision the filming
    was based on. tools/shot_pack.py computes the same value to tell which scenes are stale."""
    return fingerprint({"scene": scene, "source_revision": filming_source})


def empty_document(module: str) -> dict[str, Any]:
    content = {"brief": "", "text": ""} if module == "story" else {"scenes": []}
    return {"content": content, "source_revision": None, "approved_revision": None}
