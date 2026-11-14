# -*- coding: utf-8 -*-
"""从 6.83d 原版脚本读出全图点位：野怪营地（刷新点、营地占位区、组合池）、肉山、神符、
边路/秘密商店、两方外塔。基地内建筑仍以 base_layout_manifest.json 为唯一源，这里不复制。

    python build_map_features.py      → map_features.json
"""
from __future__ import annotations

import hashlib
import json
import re
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "base_layout_refs" / "scripts_war3map.j"
CARDS = "../../2_世界观人设/characters/中立_neutral"

UNITS = {  # rawcode → (中文, English, 野怪卡)
    "njg1": ("丛林捕猎者", "Jungle Stalker", "m25_Jungle_Stalker"), "njga": ("远古丛林捕猎者", "Elder Jungle Stalker", "m25_Jungle_Stalker"),
    "nbdo": ("蓝龙人监工", "Blue Dragonspawn Overseer", "m23_Dragonspawn"), "nbds": ("蓝龙人巫师", "Blue Dragonspawn Sorcerer", "m23_Dragonspawn"),
    "nbdk": ("黑蜉蝣", "Black Drake", "m24_Black_Dragon"), "nbwm": ("黑龙", "Black Dragon", "m24_Black_Dragon"),
    "ngst": ("岩石傀儡", "Rock Golem", "m22_Rock_Golem"), "nggr": ("宝石傀儡", "Emerald Golem", "m22_Rock_Golem"),
    "n0LC": ("雷霆蜥蜴（大）", "Thunder Lizard (large)", "m26_Thunder_Lizard"), "n0LD": ("雷霆蜥蜴（小）", "Thunder Lizard (small)", "m26_Thunder_Lizard"),
    "nfpc": ("极地熊怪勇士", "Polar Furbolg Champion", "m21_Polar_Furbolg"), "nfpu": ("极地熊怪战士", "Polar Furbolg Ursa Warrior", "m21_Polar_Furbolg"),
    "nsth": ("萨特地狱召唤者", "Satyr Hellcaller", "m17_Satyr"), "nstl": ("萨特窃魂者", "Satyr Soulstealer", "m17_Satyr"), "nsat": ("萨特诡计师", "Satyr Trickster", "m17_Satyr"),
    "nowe": ("暴怒的枭兽", "Enraged Wildkin", "m20_Wildkin"), "nowb": ("枭兽", "Wildkin", "m20_Wildkin"),
    "ndtr": ("黑暗巨魔", "Dark Troll", "m19_Dark_Troll"), "ndtw": ("黑暗巨魔首领", "Dark Troll Warlord", "m19_Dark_Troll"),
    "ncen": ("半人马先行者", "Centaur Outrunner", "m18_Centaur"), "ncnk": ("半人马可汗", "Centaur Khan", "m18_Centaur"),
    "n026": ("泥土傀儡", "Mud Golem", "m15_Mud_Golem"),
    "nogm": ("食人魔拳手", "Ogre Mauler", "m16_Ogre"), "nomg": ("食人魔法师", "Ogre Magi", "m16_Ogre"),
    "nwlg": ("巨狼", "Giant Wolf", "m14_Giant_Wolf"), "n00S": ("头狼", "Alpha Wolf", "m14_Giant_Wolf"),
    "ngh1": ("鬼魂", "Ghost", "m11_Ghost"), "npfl": ("魔能野兽", "Fel Beast", "m12_Fel_Beast"),
    "nftb": ("森林巨魔狂战士", "Forest Troll Berserker", "m9_Forest_Troll"), "nfsh": ("森林巨魔牧师", "Forest Troll High Priest", "m9_Forest_Troll"),
    "nkol": ("狗头人工头", "Kobold Taskmaster", "m8_Kobold"), "nkob": ("狗头人", "Kobold", "m8_Kobold"), "nkot": ("狗头人隧道工", "Kobold Tunneler", "m8_Kobold"),
    "ngns": ("豺狼刺客", "Gnoll Assassin", "m10_Gnoll_Assassin"),
    "n0HW": ("鹰身女妖侦察者", "Harpy Scout", "m13_Harpy"), "n0HX": ("鹰身女妖风暴巫婆", "Harpy Storm", "m13_Harpy"),
    "n00L": ("肉山", "Roshan", "m7_Roshan"),
}
SIZE = {"PIO": "远古", "P1O": "远古", "RLO": "大营", "RNO": "大营", "RSO": "大营", "RMO": "大营",
        "RPO": "中营", "RQO": "中营", "RUO": "中营", "P0O": "中营", "RTO": "小营", "RRO": "小营"}
# 区域编号与名称（本剧制作命名）；side 按 6.83d 地形里营地在河道哪一岸判定（W4 落在河道分区，但位于北岸，属天灾）。
CAMP_REGION = {
    "Z4": ("J3", "sentinel", "近卫远古营地"), "X5": ("J4", "sentinel", "近卫大营（西）"), "M4": ("J5", "sentinel", "近卫中营（中）"),
    "V4": ("J6", "sentinel", "近卫大营（东）"), "K4": ("J7", "sentinel", "近卫中营（东）"), "Y4": ("J8", "sentinel", "近卫小营"),
    "W4": ("K3", "scourge", "天灾大营（西）"), "X4": ("K4", "scourge", "天灾小营"), "J4": ("K5", "scourge", "天灾中营（西）"),
    "V5": ("K6", "scourge", "天灾中营（中）"), "L4": ("K7", "scourge", "天灾大营（东）"), "H4": ("K8", "scourge", "天灾远古营地"),
}
TOWERS = {"e00S": ("sentinel", "近卫防御塔"), "u00M": ("scourge", "天灾一塔"), "u00D": ("scourge", "天灾二塔"), "u00N": ("scourge", "天灾三塔")}


def rawcode(n: str) -> str:
    return struct.pack(">I", int(n)).decode("latin-1")


def main() -> None:
    text = SCRIPT.read_bytes().decode("latin-1")
    lines = text.split("\r")
    rects = {m[0]: [float(v) for v in m[1:]] for m in re.findall(r"set (\w+)=Rect\((-?[\d.]+),(-?[\d.]+),(-?[\d.]+),(-?[\d.]+)\)", text)}
    center = lambda r: [(rects[r][0] + rects[r][2]) / 2, (rects[r][1] + rects[r][3]) / 2]

    def body(name: str) -> str:
        i = next(k for k, l in enumerate(lines) if l.startswith(f"function {name} "))
        j = next(k for k in range(i, len(lines)) if lines[k] == "endfunction")
        return " ".join(lines[i:j + 1])

    def unit(code: str) -> dict:
        zh, en, card = UNITS[code]
        return {"rawcode": code, "zh": zh, "en": en, "card": card}

    def combo(fn: str) -> dict:
        codes = [rawcode(c) for c in re.findall(r"CreateUnit\([^,]+,(\d+),", body(fn))]
        counts: dict[str, int] = {}
        for c in codes:
            counts[c] = counts.get(c, 0) + 1
        label = " + ".join(UNITS[c][0] + (f"×{n}" if n > 1 else "") for c, n in counts.items())
        return {"function": fn, "label": label, "units": [unit(c) for c in codes]}

    camps = []
    for i, line in enumerate(lines):
        m = re.match(r"set r2=(\w+)$", line)
        if not m or not lines[i - 1].startswith("set r1="):
            continue
        spawn_rect, area_rect = m.group(1), lines[i - 1][7:]
        call = re.search(r"call (\w+)\(GetRectCenterX\(r2\)", lines[i + 4])
        if spawn_rect not in CAMP_REGION or not call:
            continue
        pool = call.group(1)
        rid, side, name = CAMP_REGION[spawn_rect]
        combos = [combo(fn) for fn in re.findall(r"call (\w+)\(x,y\)", body(pool))]
        cards = sorted({u["card"] for c in combos for u in c["units"]}, key=lambda c: int(c.split("_")[0][1:]))
        camps.append({"id": rid, "kind": "camp", "name": name, "side": side, "size": SIZE[pool], "script_line": i + 1,
                      "spawn_rect": spawn_rect, "spawn": center(spawn_rect), "area_rect": area_rect, "area": rects[area_rect],
                      "pool": pool, "combos": combos, "cards": [f"{CARDS}/{c}/{c}.md" for c in cards]})
    assert len(camps) == 12 and len({c["spawn_rect"] for c in camps}) == 12, len(camps)
    roshan_line = next(i for i, l in enumerate(lines) if "CreateUnitAtLoc(Player(12),1848651852" in l)
    assert rawcode("1848651852") == "n00L"
    roshan = {"id": "R4", "kind": "roshan", "name": "肉山巢穴", "spawn_rect": "P4", "spawn": center("P4"), "script_line": roshan_line + 1,
              "units": [unit("n00L")], "cards": [f"{CARDS}/m7_Roshan/m7_Roshan.md"],
              "note": "肉山（Player 12 中立敌对）在 rect P4 中心生成；死后由同一函数重生。"}
    runes = [{"id": "rune_top", "kind": "rune", "name": "上路神符点", "spawn_rect": "G4", "spawn": center("G4")},
             {"id": "rune_bottom", "kind": "rune", "name": "下路神符点", "spawn_rect": "D4", "spawn": center("D4")}]
    pat = re.compile(r"CreateUnit\((\w+),(\d+),(-?[\d.]+),(-?[\d.]+),(-?[\d.]+)\)")
    shops, towers = [], []
    for i, line in enumerate(lines):
        for m in pat.finditer(line):
            code, x, y = rawcode(m.group(2)), float(m.group(3)), float(m.group(4))
            if code in ("u00Z", "u010"):
                shops.append({"id": f"side_shop_{'top' if x < 0 else 'bottom'}_{code}", "kind": "side_shop", "rawcode": code,
                              "name": "边路商店（上路）" if x < 0 else "边路商店（下路）", "spawn": [x, y], "script_line": i + 1})
            elif code == "uC74":
                shops.append({"id": f"secret_shop_{'sentinel' if x < 0 else 'scourge'}", "kind": "secret_shop", "rawcode": code,
                              "name": "近卫侧秘密商店" if x < 0 else "天灾侧秘密商店", "spawn": [x, y], "script_line": i + 1})
            elif code in TOWERS:
                side, name = TOWERS[code]
                towers.append({"id": f"tower_{len(towers) + 1:02d}", "kind": "tower", "rawcode": code, "side": side,
                               "name": name, "spawn": [x, y], "script_line": i + 1})
    fountains = {"sentinel": (-7296, -7200), "scourge": (6784, 6368)}
    ancients = {"sentinel": (-5632, -6144), "scourge": (5184, 4864)}
    lane_zh = {"top": "上路", "mid": "中路", "bottom": "下路"}
    for t in towers:
        x, y = t["spawn"]
        if ((x - ancients[t["side"]][0]) ** 2 + (y - ancients[t["side"]][1]) ** 2) ** .5 < 700:
            t["lane"], t["tier"] = "base", 4
        else:
            t["lane"] = "top" if x < -5000 or y > 5000 else "bottom" if y < -5000 or x > 5000 else "mid"
    for side in fountains:
        for lane in lane_zh:
            group = sorted([t for t in towers if t["side"] == side and t.get("lane") == lane],
                           key=lambda t: (t["spawn"][0] - fountains[side][0]) ** 2 + (t["spawn"][1] - fountains[side][1]) ** 2)
            assert len(group) == 3, (side, lane, len(group))
            for tier, t in zip((3, 2, 1), group):
                t["tier"] = tier
    for t in towers:
        side_zh = "近卫" if t["side"] == "sentinel" else "天灾"
        t["name"] = f"{side_zh}四塔（世界之树旁）" if t["lane"] == "base" else f"{side_zh}{lane_zh[t['lane']]}{'一二三'[t['tier'] - 1]}塔"
        t["id"] = f"tower_{t['side']}_{t['lane']}_t{t['tier']}" + ("" if t["lane"] != "base" else f"_{t['script_line']}")
    out = {"schema": 1, "title": "DotA 6.83d 全图点位", "coordinate_system": "WC3 world units: +x east, +y north",
           "source": {"file": "../base_layout_refs/scripts_war3map.j", "sha256": hashlib.sha256(SCRIPT.read_bytes()).hexdigest()},
           "note": "营地每次刷新从组合池随机抽一组，同一营地不连续重复同一组（d01 §5.1）；area 是脚本判断营地是否清空用的矩形，可当营地空地范围。"
                   "基地建筑、商人、出生圈见 base_layout_manifest.json；基地内的近卫塔/天灾四塔在那里也有实例。",
           "camps": camps, "roshan": roshan, "runes": runes, "shops": shops, "towers": towers}
    (HERE / "map_features.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", "utf8")
    print(len(camps), "camps;", len(towers), "towers;", len(shops), "shops")
    for t in towers:
        print(t["id"], t["name"], t["spawn"])
    for c in camps:
        print(c["id"], c["name"], c["size"], c["spawn"], "|", "；".join(x["label"] for x in c["combos"]))


main()
