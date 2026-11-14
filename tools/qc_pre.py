# -*- coding: utf-8 -*-
"""出片前闸门：技能视频提交前，先把「目标」定死——规格齐、参考对、体型对、每个角色的立场与视线说得通。

用法（仓库根目录；<技能目录> 形如 ai_videos/{剧}/…/skills/k601_Chaos_Bolt）：
    python tools/qc_pre.py machine <技能目录>     # 机检：出场角色卡里有身高、该英雄四条合计 ≥ 53 s、审核敏感词
    python tools/qc_review.py <技能目录> --pre    # 多视角独立审稿（规格、开场图、每个角色的立场与视线…）
    python tools/qc_pre.py gate <技能目录>        # 闸门；skill_pack submit 会自动调它，不过不提交

为什么要有出片前闸门（dota_yingxiong follow-up 266）
--------------------------------------------------
dota 一周日志复盘里返工的头号原因是「先出片、再定目标」：规格一轮补一点、参考用错、体型不对，
每一轮都要等出完片才发现。出片后的闸门只能在花完一轮之后拦；查文字和图在出片前，最便宜、也最早。
结论写进技能目录的 `qc_pre.json`，**绑定资料包清单的 prompt sha 与每张参考的 sha**——
规格或参考一改，结论自动作废，必须重审。只对有剧级登记表的剧生效。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qc  # noqa: E402
import scale_table  # noqa: E402

PACK = "资料包"
PRE_STAGES = {"ref_image", "spec", "prompt", "keyframe"}
RESULT = "qc_pre.json"
BUDGET_S = 53
FRAMING = 0.62
PAUSE_S = 1.0   # demo_standard.md §3：每条技能首尾各 0.5 s 停顿，原片不够 53 s 时可补


def manifest(sd: Path) -> dict:
    p = sd / PACK / "manifest.json"
    if not p.exists():
        raise SystemExit(f"{sd.name} 没有资料包清单：先跑 python tools/skill_pack.py sync")
    return json.loads(p.read_text(encoding="utf-8"))


def digest(sd: Path) -> str:
    m = manifest(sd)
    parts = [m.get("prompt_sha256", "")] + [r.get("sha256", "") for r in m.get("refs", [])]
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


def drama_name(sd: Path) -> str:
    d = qc.drama_dir_of(sd)
    if not d:
        raise SystemExit(f"{sd} 不在任何剧目录里")
    return d.relative_to(qc.REPO / "ai_videos").as_posix()


def cast(sd: Path) -> list[str]:
    """出场角色＝资料包里键名正好是一张人物卡的参考（死亡参考、特效图等不算）。"""
    cards = scale_table.cards(drama_name(sd))
    return [r["key"] for r in manifest(sd).get("refs", []) if r.get("key") in cards]


def frames(sd: Path) -> dict[str, Path]:
    out = {}
    for r in manifest(sd).get("refs", []):
        for role in ("start", "peak"):
            if str(r.get("key", "")).endswith(f"_{role}") and r.get("src"):
                out[role] = qc.REPO / r["src"]
    return out


IMG = (".png", ".jpg", ".jpeg", ".webp")


def identity_images(sd: Path) -> list[Path]:
    """出场角色的身份立绘（资料包里键名是人物卡的那几张）——审锁定特征要对照它们。"""
    cards = set(cast(sd))
    return [qc.REPO / r["src"] for r in manifest(sd).get("refs", [])
            if r.get("key") in cards and r.get("src") and Path(r["src"]).suffix.lower() in IMG]


def original_refs(sd: Path, model_limit: int = 3) -> list[Path]:
    """原版参考：本技能的 DotA 1 原版截帧（ref/skills/dota1_{kNNN}_*）＋英雄原版模型图（ref/model/，取前几张）。
    这些才是「参考是不是对、是不是 6.83d」要审的对象；我们自己出的开场图 / 峰值图是真人电影质感，不拿来判版本。"""
    hero, kid = sd.parent.parent, sd.name.split("_")[0]
    skill = sorted(p for p in (hero / "ref" / "skills").glob(f"dota1_{kid}_*") if p.suffix.lower() in IMG)
    model = sorted((p for p in (hero / "ref" / "model").glob("*") if p.suffix.lower() in IMG),
                   key=lambda p: (not p.name.startswith("dota1_"), p.name))[:model_limit]   # DotA 1 原版图优先，野怪 / 百科图排后
    return skill + model


def spec_text(card_md: Path) -> str:
    """规格＝技能卡「技能视频 prompt」里的 text 块：只给要求，不给作者的审片理由。"""
    if not card_md.is_file():
        return ""
    text = card_md.read_text(encoding="utf-8")
    sec = text.split("## 技能视频 prompt", 1)[-1] if "## 技能视频 prompt" in text else text
    m = re.search(r"```text\n(.*?)```", sec, re.S)
    return (m.group(1) if m else sec)[:6000].strip()


def card_of(sd: Path) -> Path:
    return sd / f"{sd.name}.md"


def seconds(spec: str) -> int | None:
    m = re.search(r"^时长：\s*(\d+)\s*秒", spec, re.M)
    return int(m.group(1)) if m else None


def machine(sd: Path) -> list[tuple[str, str, str, str]]:
    reg = qc.registry(qc.drama_dir_of(sd))
    spec = spec_text(card_of(sd))
    items: list[tuple[str, str, str, str]] = []
    if "spec.scale_table" in reg:
        hs = scale_table.heights(drama_name(sd), cast(sd))
        missing = [h.key for h in hs if not h.meters]
        listing = "；".join(f"{h.name} {h.meters:g} m（{h.kind}）" for h in hs if h.meters)
        items.append(("spec.scale_table", "fail" if missing or not hs else "pass", "machine",
                      f"卡里缺身高：{'、'.join(missing)}" if missing else (listing or "资料包里认不出出场角色")))
    if "spec.duration_budget" in reg:
        siblings = sorted(p for p in sd.parent.glob("k*") if (p / f"{p.name}.md").is_file())
        secs = {p.name: seconds(spec_text(p / f"{p.name}.md")) for p in siblings}
        known = {k: v for k, v in secs.items() if v}
        total = sum(known.values())
        if len(known) < 4:
            items.append(("spec.duration_budget", "未审", "machine", f"该英雄技能卡未齐（{len(known)}/4），现合计 {total} s"))
        else:
            padded = total + PAUSE_S * len(known)
            items.append(("spec.duration_budget", "pass" if padded >= BUDGET_S else "fail", "machine",
                          f"四条原片合计 {total} s，加首尾停顿 {padded:g} s（要求 ≥ {BUDGET_S} s）：" + "、".join(f"{k.split('_')[0]} {v}s" for k, v in known.items())))
    if "spec.onetake" in reg:                                 # 本剧技能视频一律一镜到底（follow-up 295）
        ok = "一镜到底" in spec or "不剪切" in spec
        items.append(("spec.onetake", "pass" if ok else "fail", "machine",
                      "规格写明了一镜到底 / 不剪切" if ok else "规格没写一镜到底：在「要求」行补「一个连续固定镜头，一镜到底，不剪切、不转场、不跳时」"))
    if "keyframe.framing_match" in reg:                       # 取景不一致是切镜的根因（follow-up 295）
        fr = frames(sd)
        if "start" in fr and "peak" in fr:
            import subprocess
            import numpy as np
            import motion_check as mc

            def gray(p: Path):
                raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", "scale=%d:%d,format=gray" % (mc.W, mc.H),
                                      "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
                return np.frombuffer(raw, np.uint8).reshape(mc.H, mc.W).astype(np.float32)
            ov = mc.edge_overlap(gray(fr["start"]), gray(fr["peak"]))
            items.append(("keyframe.framing_match", "pass" if ov >= FRAMING else "fail", "machine",
                          "开场图与峰值图边缘重合 %.2f（要求 ≥ %.2f；同一镜头约 0.76，跨剪切约 0.54）" % (ov, FRAMING)))
        else:
            items.append(("keyframe.framing_match", "未审", "machine", "资料包里缺开场图或峰值图"))
    c = reg.get("prompt.moderation_words")
    if c and c.words:
        body = "\n".join(ln for ln in spec.splitlines() if not ln.startswith("负面词"))   # 负面词里本来就写着这些词
        hits = sorted({w for w in c.words if w in body})
        items.append(("prompt.moderation_words", "fail" if hits else "pass", "machine",
                      f"命中会触发审核的词：{'、'.join(hits)}" if hits else "未命中词表"))
    return items


def record(sd: Path, items: list[tuple[str, str, str, str]]) -> None:
    qc.record_into(sd / RESULT, digest(sd), qc.registry(qc.drama_dir_of(sd)), items, {"skill": sd.name})


def gate(sd: Path, when: set[str] | None = None) -> tuple[list[str], list[str]]:
    drama = qc.drama_dir_of(sd)
    if not drama or not (drama / qc.DRAMA_REG).exists():
        return [], []                                       # 没启用自检的剧不拦
    p = sd / RESULT
    if not p.exists():
        return [f"没有 {RESULT}：先跑 qc_pre.py machine 与 qc_review.py --pre"], []
    data = json.loads(p.read_text(encoding="utf-8"))
    block = [] if data.get("sha256") == digest(sd) else [f"{RESULT} 绑定的规格或参考已改过——结论作废，重审"]
    b2, soft = qc.verdict_problems(data, qc.registry(drama), PRE_STAGES, when or set())
    return block + b2, soft


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", choices=("machine", "gate"))
    ap.add_argument("skill_dir")
    ap.add_argument("--when", action="append", default=[])
    a = ap.parse_args(argv)
    sd = Path(a.skill_dir).resolve()
    if a.action == "machine":
        items = machine(sd)
        record(sd, items)
        for cid, verdict, _, ev in items:
            print(f"{cid:24} {verdict:4}  {ev}")
        return 0
    block, soft = gate(sd, set(a.when))
    for s in soft:
        print(f"· {s}", file=sys.stderr)
    for b in block:
        print(f"✗ {b}", file=sys.stderr)
    print(("出片前闸门不通过" if block else "出片前闸门通过") + f"（{sd.name}）")
    return 1 if block else 0


if __name__ == "__main__":
    sys.exit(main())
