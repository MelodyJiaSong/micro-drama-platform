# -*- coding: utf-8 -*-
"""技能样片的手势参考图（follow-up 068：样片＝2–3 张手势参考图 + 完整视频 prompt，不再用 Blender / Cascadeur 白模）。

图的 prompt 只写在技能卡 [[sample.keyframe]]（name / at / prompt / ref）；第一张文生图，后面的以 ref 那张图生图，保人和场景一致。
正本出到 `skills/{卡}/样片/手势图/{键}_{名}.png`，再拷一份进 `样片/资料包/` 给人上传；已有的跳过（--force 重出）。即梦提交即扣费。
资料包里的图被库外程序改名 / 删了（实测两次被批量改成「资料包N.png」）：--pack 只把正本拷回资料包，不出图。

    python tools/skill_keyframes.py <剧> <键或名>… [--force | --pack]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "tools"))
import skills_lib  # noqa: E402
from tools import gen_bg_assets as gba  # noqa: E402
from tools import gen_images_xianjian as dm  # noqa: E402

RATIO = "16:9"


def make(card: skills_lib.Card, force: bool) -> None:
    if not card.sample_keyframes:
        raise SystemExit(f"{card.key} {card.name}：卡里没有 [[sample.keyframe]]")
    for k in card.sample_keyframes:
        out = skills_lib.keyframe_path(card, k["name"])
        if out.is_file() and not force:
            print(f"  · {out.name} 已有，跳过")
            continue
        refs = [skills_lib.keyframe_path(card, k["ref"])] if k.get("ref") else []
        for r in refs:
            if not r.is_file():
                raise SystemExit(f"{card.key}：「{k['name']}」的参考图 {r.name} 还没有——先出它")
        out.parent.mkdir(parents=True, exist_ok=True)
        url, cost = gba._dm_submit(k["prompt"].strip(), refs, RATIO)
        part = out.with_name(out.stem + ".part" + out.suffix)
        dm.download(url, part)
        part.replace(out)
        print(f"  ✓ {card.key} {out.name}（{cost} 积分{'，参考 ' + refs[0].name if refs else ''}）", flush=True)
    for line in skills_lib.keyframe_pack(card):
        print(f"  · {card.key} 资料包：{line}")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("drama")
    ap.add_argument("keys", nargs="+")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--pack", action="store_true", help="只把手势图正本拷回资料包")
    a = ap.parse_args()
    cards = skills_lib.load(skills_lib.drama_of(Path(a.drama)))
    for key in a.keys:
        card = skills_lib.find(cards, key)
        if a.pack:
            print(f"{card.key}：" + ("；".join(skills_lib.keyframe_pack(card)) or "资料包已齐"))
        else:
            make(card, a.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
