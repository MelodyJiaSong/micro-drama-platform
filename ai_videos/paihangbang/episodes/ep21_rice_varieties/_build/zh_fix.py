# -*- coding: utf-8 -*-
"""ep21 中文版人工修订（zh_edition.py merge 之后跑；幂等）。卡名去掉括号英文（卡面放不下、也不利于口播），统一标题与封面用词。

    python ai_videos/paihangbang/episodes/ep21_rice_varieties/_build/zh_fix.py
"""
import json
import re
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
P = EP / "data.zh.json"
TOP = {"title": "世界各地30种大米", "kicker": "30种大米", "youtube_title": "世界各地30种大米"}
# 发布稿文案覆盖在 ../zh_publish.json（zh_publish.py 读取）
BADGE = {9: "“最佳大米”2020、2021", 1: "日本种植最多的大米", 19: "曾专供苏丹御膳", 23: "2008年起受欧盟地理标志保护", 28: "2012年起墨西哥原产地保护"}
TAGS = {24: {1: "塞入蔬菜做马赫希"}, 9: {1: "2013年泰国首个欧盟地理标志"}, 19: {1: "2017年获土耳其原产地保护"}, 29: {1: "从14磅（约6公斤）种子起步"}}
INSIGHT = {8: "糯米不含麸质：英文名glutinous指像胶一样黏，与麸质（gluten）无关。"}   # 第 2 轮复核 R2-m
NAME = {6: "班兰香米", 12: "查克豪黑米", 13: "戈宾多博格米", 14: "马塔红米", 15: "久姆拉红米", 17: "德夫齐拉米",
        18: "哈希米香米", 19: "托斯亚大米", 23: "卡罗利诺米", 25: "奥法达米"}


def main() -> None:
    d = json.loads(P.read_text(encoding="utf-8"))
    d.update(TOP)
    for it in d["items"]:
        r = it["rank"]
        it["name"] = NAME.get(r, re.sub(r"（[^）]*）$", "", it["name"]))
        if r in BADGE:
            it["badge"] = BADGE[r]
        for k, v in TAGS.get(r, {}).items():
            it["tags"][k]["text"] = v
    for ins in d.get("insights", []):
        if ins["after_rank"] in INSIGHT:
            ins["text"] = INSIGHT[ins["after_rank"]]
    P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("data.zh.json fixed")


if __name__ == "__main__":
    main()
