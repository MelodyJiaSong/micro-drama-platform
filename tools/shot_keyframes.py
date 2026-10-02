# -*- coding: utf-8 -*-
"""镜头状态图（follow-up 084：动作镜不再做 previz 白模 / Cascadeur，改用技能样片的做法——先出几张状态图，再用它们指导视频）。

状态图的 prompt 只写在生成器的 Shot(kf=({name, at, prompt, refs}, …))；一张图 ＝ 本镜某一秒附近的一个瞬间（姿势、站位、表情、手里的东西）。
第一张文生图 + 参考图（场景图、角色换装图、装备图），后面的再挂前一张图保人和场景一致。图出到 `shots/shotNN/状态图/{name}.png`，
参考行与资料包由生成器按 Shot.kf 自动挂（`python tools/gen_shots_szzl_{ep}.py` 重写盘）。已有的图跳过（--force 重出）。即梦提交即扣费。

    python tools/shot_keyframes.py ep01 S11 [S09 …] [--force] [--only 名字,名字]
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "tools"))
import szzl_shot_engine as E  # noqa: E402
from tools import gen_bg_assets as gba  # noqa: E402
from tools import gen_images_xianjian as dm  # noqa: E402

RATIO = "16:9"
PROMPT_MAX = 1550          # 即梦 prompt 硬限 1600
MAX_REFS = 5


def load_shots(ep: str):
    p = REPO / "tools" / ("gen_shots_szzl_%s.py" % ep)
    spec = importlib.util.spec_from_file_location("gen_shots_%s" % ep, p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod.SHOTS


def state_prompt(ep: str, s: "E.Shot", k: dict) -> str:
    """绿幕 + 没有五官的简化小人偶（颜色只是标记）：只给动作 / 姿势 / 位置的大概意思；长相、服装、场景、光线、特效都留给 Seedance 的文字。"""
    legend = E.kf_legend(ep, s).replace("绿幕上的小人偶：", "")
    return ("示意图，不是电影画面：纯绿色背景（绿幕，没有任何场景、地面纹理或背景物件），画面里只有简单的卡通小人偶，没有五官、没有衣服细节，"
            "只用单一颜色区分谁是谁（%s），小人偶的姿势要清楚、有力、不僵硬，让人一眼看懂这一瞬间的动作与位置。16:9。"
            "这一瞬间：%s。画面里没有文字、字幕、水印，没有特效与光效。" % (legend, k["prompt"].strip()))


def refs_of(ep: str, s: "E.Shot", k: dict, prev: Path | None) -> list[Path]:
    return []          # 状态图只给动作的大概意思：不挂场景 / 角色 / 装备参考，每张文生图


def make(ep: str, s: "E.Shot", force: bool, only: set[str]) -> None:
    if not s.kf:
        raise SystemExit("%s：镜表里没有 kf（状态图）" % s.key)
    prev: Path | None = None
    for k in s.kf:
        out = E.kf_path(ep, s, k["name"])
        if only and k["name"] not in only:
            prev = out if out.is_file() else prev
            continue
        if out.is_file() and not force:
            print("  · %s 已有，跳过" % out.name)
            prev = out
            continue
        refs = []
        prompt = state_prompt(ep, s, k)
        out.parent.mkdir(parents=True, exist_ok=True)
        for attempt in range(1, 5):                          # 上传偶发失败（多进程并发时全军覆没）：最多重试 3 次
            try:
                url, cost = gba._dm_submit(prompt, refs, RATIO)
                break
            except RuntimeError as e:
                if attempt == 4:
                    raise
                print("  ! 失败（%s），重试 %d" % (str(e)[:60], attempt), flush=True)
                time.sleep(15)
        part = out.with_name(out.stem + ".part" + out.suffix)
        dm.download(url, part)
        part.replace(out)
        print("  ✓ %s %s（%s 积分，参考 %d 张）" % (s.key, out.name, cost, len(refs)), flush=True)
        prev = out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("ep")
    ap.add_argument("shots", nargs="+")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only", default="")
    ap.add_argument("--dry", action="store_true", help="只打印 prompt 与参考，不提交")
    a = ap.parse_args()
    by_key = {s.key: s for s in load_shots(a.ep)}
    only = {x for x in a.only.split(",") if x}
    for key in a.shots:
        s = by_key[key]
        if a.dry:
            prev = None
            for k in s.kf:
                print("== %s %s（第 %g 秒）\n%s\n参考：%s\n" % (s.key, k["name"], k["at"], state_prompt(a.ep, s, k),
                                                           [r.name for r in refs_of(a.ep, s, k, prev if k.get("chain", True) else None)]))
                prev = E.kf_path(a.ep, s, k["name"])
        else:
            make(a.ep, s, a.force, only)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
