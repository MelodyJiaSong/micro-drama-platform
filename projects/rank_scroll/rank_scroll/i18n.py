"""屏上固定文字的中英对照（rank_scroll follow-up 015：中文版 --lang zh）。数据里的文字由各期 data.{lang}.json 提供，这里只放渲染器自己写的字。"""
from __future__ import annotations

STRINGS: dict[str, dict[str, str]] = {
    "en": {
        "no1": "No. 1",
        "sources_title": "SOURCES & CREDITS",
        "thanks": "Thanks for watching!",
        "next_rank": "Which ranking should we do next? Tell us in the comments.",
        "next_list": "Which list should we do next? Tell us in the comments.",
        "did_you_know": "DID YOU KNOW?",
        "photo": "Photo: ",
        "portrait": "Portrait: ",
        "ai_image": "AI IMAGE",
        "ai_credit": "AI-generated image, not a photo",
        "no_photo": "No free-licensed photo available",
        "tally_sub": "in the {kicker} · {title}",
        "more": "+ {n} more ({counts} each): ",
        "image_credits_line": "Image credits: shown on each card and listed in the description",
    },
    "zh": {
        "no1": "第 1 名",
        "sources_title": "数据来源与图片署名",
        "thanks": "感谢观看！",
        "next_rank": "下一期想看什么排行？欢迎在评论区告诉我们。",
        "next_list": "下一期想看什么榜单？欢迎在评论区告诉我们。",
        "did_you_know": "你知道吗？",
        "photo": "图：",
        "portrait": "肖像：",
        "ai_image": "AI 生成图",
        "ai_credit": "AI 生成图像，非实拍照片",
        "no_photo": "暂无可用的授权照片",
        "tally_sub": "{kicker} · {title}",
        "more": "另有 {n} 个（各 {counts} 个）：",
        "image_credits_line": "图片署名见各卡片右下角与视频简介",
    },
}


def t(lang: str, key: str, **kw: object) -> str:
    s = STRINGS.get(lang, STRINGS["en"]).get(key) or STRINGS["en"][key]
    return s.format(**kw) if kw else s
