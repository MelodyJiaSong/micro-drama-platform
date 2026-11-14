# -*- coding: utf-8 -*-
"""自检与自我进化：把「自检过了」变成可核对的记录，把用户每次抓到的问题变成一条新检查。

用法（仓库根目录）：
    python tools/qc.py record <出片目录> --check video.slowmo=pass --evidence "…" --by machine
    python tools/qc.py record <出片目录> --check video.timeline=未审 --evidence "原因" --by review
    python tools/qc.py record <出片目录> --check video.gaze=审不了 --reason 看不清 --evidence "拼图里脸只有几个像素" --by review
    python tools/qc.py gate <出片目录> [--when 一镜到底]          # 交付 / 进成片前必过
    python tools/qc.py override <出片目录> --check video.timeline --kind accept|false_positive --note "用户原话" --followup NNN
    python tools/qc.py defect <剧> --category video.scale --artifact <路径> --caught-by user --followup 245 --note "…"
    python tools/qc.py escapes [<剧> ...]                          # 逃逸分析：为什么检查没抓到
    python tools/qc.py stats [<剧> ...]                            # 逃逸率、按类别、未审次数

设计（CONVENTIONS「自检与自我进化」；dota_yingxiong follow-up 257）
------------------------------------------------------------------
· **检查要查什么只有一个出处**：`.agents/references/project/qc_checks.toml`。所有会话读同一份，
  一个会话加的检查，别的会话下次出片就生效——不再靠用户在几个会话里各说一遍（dota 241 / 245）。
· **结论落文件、绑 sha**：出片目录里的 `qc.json`。产物改过（sha 对不上）结论作废；
  `review.md` 照写，给人看理由；`qc.json` 给闸门与统计读。
· **审稿类检查不许作者自判**：`kind = review` 的闸门项必须 `--by review`（独立上下文的审稿人）。
  做不了独立审稿就记「未审」并写原因——闸门照样放行，但每一次都进 stats，周复盘看得见（AGENTS「不由作者自审冒充通过」）。
  dota 一周的教训：用户免了逐条确认后，提到独立审稿的 14 条里 8 条是未审，全周只有 1 条写明审过。

两层、三种结论（2026-11-14，dota_yingxiong follow-up 354；两周审稿复盘）
--------------------------------------------------------------------
复盘 1457 条审稿结论：61% 判 fail，其中六成写着「拿不准 / 看不清」；几乎全 fail 的检查（时间轴 55/0、
锁定特征 53/1、技能长相 53/1、视线 105/3）判据都是规格里的精确秒数、身高比与措辞——审查变成了「照没照
这一版规格」，闸门全红后只好成批放行或跳过。所以：
· **两层**（登记表每条 `layer`）：`quality` 通用质量——只看产物本身有没有观众看得出的错，与规格写法、
  流程版本无关，所有剧、所有时间的产物都适用；`spec` 对照规格——拿产物和**它自己当时的**规格比，
  不要求精确到秒，只有大偏差判 fail（默认容差 SPEC_TOLERANCE，单条可用 `tolerance` 改写）。
· **三种结论**：pass / fail / 审不了（`--reason 材料缺|看不清`）。「拿不准就判 fail」取消。
  材料缺：通用质量项挡住（补材料、修工具再审）；对照规格项只记录（旧产物缺新版材料不算片子差）。
  看不清：放行但列为「待人看」并计数。「未审」仍指没人审成（审稿进程失败等）。
· **不设版本豁免**：取消 CUTOFF；旧审稿规则（REVIEW_RULE 之前、「拿不准就判 fail」）下审稿给的 fail 一律重审。
· **放行分两种**（`--kind`）：accept＝检查判对了、用户接受这次的瑕疵；false_positive＝检查判错了
  （只有它提示放松检查）。放行绑定该检查的定义（check_sha），检查一改放行作废；一句用户原话只管一类检查，
  要用同一句放行另一类，须 `--mention` 给出原话里点到这一类的字。
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import tomllib
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / ".agents" / "references" / "project" / "qc_checks.toml"   # 仓库级：只收有共用规则撑着的
DRAMA_REG = "qc_checks.toml"                                                    # 剧级：ai_videos/{剧}/qc_checks.toml
SPECS = REPO / "specs"
VERDICTS = ("pass", "fail", "审不了", "未审")
REASONS = ("材料缺", "看不清")                       # 「审不了」的两种原因：缺判这一项要用的材料 / 材料在但看不清
LAYERS = ("quality", "spec")
LAYER_NAME = {"quality": "通用", "spec": "对照规格"}
REVIEW_RULE = 2                                      # 审稿规则版本：2＝三种结论、取消「拿不准就判 fail」（follow-up 354）
OVERRIDE_KINDS = ("accept", "false_positive")
SPEC_TOLERANCE = ("时间不要求精确到秒：某一拍提前或推迟不超过 2 秒（或不超过这一拍时长的一半，取较大者）算对上；"
                  "缺拍、顺序颠倒、多出明显的动作，或偏差超出这个范围才判 fail。数量与比例：差到一眼看得出才判 fail"
                  "（相对大小偏离卡上比例约三成以上）。小偏差判 pass，并在 evidence 里记下偏了多少。")
BY = ("machine", "review", "author")
CAUGHT = ("user", "machine", "review")
MEDIA = (".mp4", ".mov", ".webm", ".png", ".jpg", ".jpeg", ".wav", ".mp3")


@dataclass(frozen=True)
class Check:
    id: str
    stage: str
    kind: str
    gate: bool
    auto: bool
    when: str
    desc: str
    sources: tuple[str, ...]
    level: str                  # 仓库级 / 剧级
    basis: str
    how: str = ""               # 怎么判（独立审稿的提示词用它）
    perspective: str = "director"   # 由哪个视角审：character（每个角色各一个审稿人）/ director / audience / fidelity
    words: tuple[str, ...] = ()     # 词表类机检用（如审核敏感词），跟检查放在一起
    layer: str = "quality"          # quality 通用质量 / spec 对照规格（follow-up 354）
    tolerance: str = ""             # spec 层的容差；空＝SPEC_TOLERANCE

    @property
    def sha(self) -> str:
        """检查的定义指纹：放行绑定它，措辞、判法、层级或容差一改，旧放行作废。"""
        body = json.dumps([self.id, self.stage, self.kind, self.when, self.desc, self.how, self.layer, self.tolerance],
                          ensure_ascii=False)
        return hashlib.sha256(body.encode()).hexdigest()[:16]


def _load(path: Path, level: str) -> dict[str, Check]:
    raw = tomllib.loads(path.read_text(encoding="utf-8"))
    bad = [c["id"] for c in raw.get("check", []) if c.get("layer", "quality") not in LAYERS]
    if bad:
        raise SystemExit(f"{path.name}：layer 只能是 {LAYERS}：{bad}")
    return {c["id"]: Check(c["id"], c["stage"], c["kind"], bool(c.get("gate")), bool(c.get("auto")),
                           c.get("when", ""), c.get("desc", ""), tuple(c.get("sources", [])),
                           level, c.get("basis", ""), c.get("how", ""), c.get("perspective", "director"),
                           tuple(c.get("words", [])), c.get("layer", "quality"), c.get("tolerance", ""))
            for c in raw.get("check", [])}


def drama_dir_of(p: Path) -> Path | None:
    """从任意产物路径往上找到所属剧目录（第一个含剧级登记表或 workflow.json 的 ai_videos 子目录）。"""
    root = (REPO / "ai_videos").resolve()
    for d in [p, *p.parents]:
        if d == root or root not in d.parents:
            break
        if (d / DRAMA_REG).exists() or (d / "workflow.json").exists():
            return d
    return None


def registry(drama: Path | None = None) -> dict[str, Check]:
    """仓库级 + 剧级合并。同一 id 两层都有就报错——两层并存只会让「到底以哪条为准」说不清。"""
    out = _load(REGISTRY, "仓库级") if REGISTRY.exists() else {}
    dp = drama / DRAMA_REG if drama else None
    if dp and dp.exists():
        local = _load(dp, "剧级")
        dup = sorted(set(out) & set(local))
        if dup:
            raise SystemExit(f"检查 id 在仓库级与剧级重复：{dup}（{dp.relative_to(REPO)}）")
        out.update(local)
    return out


def drama_of_project(name: str) -> Path | None:
    for d in (REPO / "ai_videos" / name, *(REPO / "ai_videos").glob(f"*/{name}")):
        if d.is_dir():
            return d
    return None


def now() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat()


def artifact_of(rd: Path) -> Path:
    files = sorted(p for p in rd.iterdir() if p.suffix.lower() in MEDIA and not p.name.startswith(("mc_", "sheet")))
    if not files:
        raise SystemExit(f"{rd} 里没有产物文件")
    return max(files, key=lambda p: p.stat().st_size)          # 出片目录里最大的媒体文件就是原片


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load_qc(rd: Path) -> dict:
    p = rd / "qc.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def record_into(path: Path, digest: str, reg: dict[str, Check], items: list[tuple[str, ...]],
                extra: dict | None = None) -> None:
    """把 (检查id, 结论, by, 证据[, 审不了的原因]) 写进一份结论文件，绑定 digest。出片后（qc.json）与出片前（qc_pre.json）共用。"""
    qc = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    if qc.get("sha256") and qc["sha256"] != digest:
        qc = {"superseded": qc}                                  # 绑定的东西换了，旧结论留档但不再算数
    qc.update({**(extra or {}), "sha256": digest})
    checks = qc.setdefault("checks", {})
    for cid, verdict, by, evidence, *rest in items:
        reason = rest[0] if rest else ""
        if cid not in reg:
            raise SystemExit(f"登记表里没有检查 {cid}（新检查先加进剧级登记表）")
        if verdict not in VERDICTS:
            raise SystemExit(f"{cid} 的结论只能是 {VERDICTS}")
        if reg[cid].kind == "review" and by == "author" and verdict == "pass":
            raise SystemExit(f"{cid} 是审稿类检查，作者自判的 pass 不算——交独立审稿（--by review），做不了就记「未审」并写原因")
        if verdict in ("未审", "审不了") and not evidence:
            raise SystemExit(f"记「{verdict}」必须用 --evidence 写原因")
        if verdict == "审不了" and reason not in REASONS:
            raise SystemExit(f"{cid} 记「审不了」要写 --reason {'|'.join(REASONS)}")
        row = {"verdict": verdict, "by": by, "evidence": evidence or "", "at": now()}
        if verdict == "审不了":
            row["reason"] = reason
        if by == "review":
            row["rule"] = REVIEW_RULE
        checks[cid] = row
    path.write_text(json.dumps(qc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def cmd_record(a: argparse.Namespace) -> int:
    rd = Path(a.render_dir).resolve()
    art = artifact_of(rd)
    items = [(cid, verdict, a.by, a.evidence, a.reason) for cid, _, verdict in (i.partition("=") for i in a.check)]
    record_into(rd / "qc.json", sha(art), registry(drama_dir_of(rd)), items, {"artifact": art.name})
    print(f"QC 已记 {len(a.check)} 项 → {(rd / 'qc.json').relative_to(REPO) if rd.is_relative_to(REPO) else rd / 'qc.json'}")
    return 0


def gate_problems(rd: Path, stage: str, when: set[str]) -> tuple[list[str], list[str]]:
    """出片后闸门：返回 (挡住的, 放行但要进统计的)。不按出片日期豁免：通用质量对所有时间的产物都生效（follow-up 354）。"""
    qc = load_qc(rd)
    if not qc:
        return [f"没有 qc.json（先跑检查再 `qc.py record`）"], []
    block = [] if qc.get("sha256") == sha(artifact_of(rd)) else ["qc.json 的 sha 与当前产物不符——产物改过，结论作废，重查"]
    b2, soft = verdict_problems(qc, registry(drama_dir_of(rd)), {stage}, when | forced_when(rd))
    return block + b2, soft


def forced_when(p: Path) -> set[str]:
    """剧级 [policy] 强制的条件：skill_video_onetake → 技能视频一律按「一镜到底」查（dota_yingxiong follow-up 295）。"""
    drama = drama_dir_of(p)
    reg = drama / DRAMA_REG if drama else None
    if not reg or not reg.is_file() or "skills" not in p.parts:
        return set()
    pol = tomllib.loads(reg.read_text(encoding="utf-8")).get("policy", {})
    return {"一镜到底"} if pol.get("skill_video_onetake") else set()


def verdict_problems(qc: dict, reg: dict[str, Check], stages: set[str], when: set[str]) -> tuple[list[str], list[str]]:
    """按登记表核对一份结论：闸门项缺、不过、来源不对、通用项缺材料 → 挡；未审、看不清、用户放行 → 放行但计数。"""
    block, soft = [], []
    for c in reg.values():
        if c.stage not in stages or not c.gate or (c.when and c.when not in when):
            continue
        r = qc.get("checks", {}).get(c.id)
        tag = f"[{LAYER_NAME[c.layer]}]"
        ov = (r or {}).get("override")
        if ov and ov.get("check_sha") != c.sha:                   # 放行绑定检查定义：检查改过（或旧放行没绑定）就作废
            block.append(f"{c.id} 的放行已作废：放行后检查定义改过（或旧放行没绑定定义），按现在的检查重审或重新取得用户原话")
            continue
        if not r:
            block.append(f"{c.id} 没查（{c.desc}）")
        elif r["verdict"] in ("fail", "审不了") and ov:
            soft.append(f"{c.id} {'不通过' if r['verdict'] == 'fail' else '审不了'}{tag}但用户放行"
                        f"（{'接受这次的瑕疵' if ov.get('kind') == 'accept' else '判为误报'}）：{ov['note']}")
        elif r["verdict"] == "fail" and r.get("by") == "review" and r.get("rule", 1) < REVIEW_RULE:
            block.append(f"{c.id} 的不通过来自旧审稿规则（拿不准就判 fail），按现在的规则重审")
        elif r["verdict"] == "fail":
            block.append(f"{c.id} 不通过{tag}：{r['evidence']}")
        elif r["verdict"] == "审不了" and r.get("reason") == "材料缺" and c.layer == "quality":
            block.append(f"{c.id} 审不了{tag}（材料缺）：{r['evidence']}——补上材料或修好审稿工具再审")
        elif r["verdict"] == "审不了":
            soft.append(f"{c.id} 审不了{tag}（{r.get('reason', '')}）"
                        f"{'，待人看' if r.get('reason') == '看不清' else '，只记录'}：{r['evidence']}")
        elif r["verdict"] == "未审":
            soft.append(f"{c.id} 未审：{r['evidence']}")
        elif c.kind == "review" and r["by"] != "review":
            block.append(f"{c.id} 是审稿类，结论来自 {r['by']}，要独立审稿")
    return block, soft


def cmd_gate(a: argparse.Namespace) -> int:
    rd = Path(a.render_dir).resolve()
    block, soft = gate_problems(rd, a.stage, set(a.when))
    for s in soft:
        print(f"· {s}", file=sys.stderr)
    if block:
        for b in block:
            print(f"✗ {b}", file=sys.stderr)
        print(f"闸门不通过（{rd.name}）：没过不交、不进成片——便宜的改动做在上游再重出，每镜最多重出两次，仍不过就搁置交用户",
              file=sys.stderr)
        return 1
    print(f"闸门通过（{rd.name}）" + (f"，{len(soft)} 项放行但已记（未审 / 待人看 / 用户放行）" if soft else ""))
    return 0


def cmd_override(a: argparse.Namespace) -> int:
    """用户看过、放行闸门拦下的结果。两种（follow-up 354）：accept＝检查判对了、用户接受这次的瑕疵；
    false_positive＝检查判错了（只有它在 stats 里提示放松检查）。放行绑定产物 sha 与检查定义（check_sha），
    任一改动即作废；一句用户原话只管一类检查（同一句再放行另一类须 --mention 原话里点到这一类的字）。
    给技能目录时放行出片前闸门（qc_pre.json，follow-up 275）；规格或参考一改，qc_pre.json 作废，放行随之失效。"""
    rd = Path(a.render_dir).resolve()
    path = rd / "qc.json"
    if not path.exists() and (rd / "qc_pre.json").exists():
        path = rd / "qc_pre.json"
    qc = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    r = qc.get("checks", {}).get(a.check)
    if not r or r["verdict"] not in ("fail", "审不了"):
        raise SystemExit(f"{a.check} 在 {rd.name} 不是 fail / 审不了，没有可放行的")
    drama = drama_dir_of(rd)
    c = registry(drama).get(a.check)
    if not c:
        raise SystemExit(f"登记表里没有检查 {a.check}")
    spec = project(drama.name) if drama else None
    quote = re.sub(r"\s+", "", a.note)
    if spec:
        other = sorted({d["category"] for d in defects(spec) if d.get("caught_by") == "override"
                        and re.sub(r"\s+", "", d.get("note", "")) == quote and d["category"] != a.check})
        if other and not (a.mention and a.mention in a.note):
            raise SystemExit(f"这句用户原话已经放行过 {other}：一句原话只管一类检查。要放行 {a.check}，"
                             "请取得用户针对这一类的原话，或用 --mention 给出原话里点到这一类的字（须是原话的一部分）")
    r["override"] = {"note": a.note, "kind": a.kind, "check_sha": c.sha, "followup": a.followup or "", "at": now()}
    path.write_text(json.dumps(qc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if spec:
        rec = {"ts": now(), "category": a.check, "caught_by": "override", "kind": a.kind, "check_sha": c.sha,
               "artifact": str((rd / qc.get("artifact", "")).relative_to(REPO)), "followup": a.followup or "", "note": a.note}
        with (spec / "defects.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"已放行 {a.check}（{'接受瑕疵' if a.kind == 'accept' else '记为误报'}）：{a.note}")
    return 0


def project(name: str) -> Path:
    hits = [d for d in SPECS.glob(f"*/{name}") if d.is_dir()]
    if len(hits) != 1:
        raise SystemExit(f"找不到唯一的项目 {name}")
    return hits[0]


def defects(spec: Path) -> list[dict]:
    p = spec / "defects.jsonl"
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()] if p.exists() else []


def cmd_defect(a: argparse.Namespace) -> int:
    spec = project(a.project)
    reg = registry(drama_of_project(spec.name))
    if a.category not in reg and not a.category.startswith("new:"):
        raise SystemExit(f"类别 {a.category} 不在登记表；没有对应检查就写 new:<短名>，escapes 会提示新增")
    rec = {"ts": now(), "category": a.category, "artifact": a.artifact, "caught_by": a.caught_by,
           "followup": a.followup or "", "note": a.note or ""}
    with (spec / "defects.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"缺陷已记：{spec.name} · {a.category} · {a.caught_by}")
    return 0


def specs_for(names: list[str]) -> list[Path]:
    return [project(n) for n in names] if names else sorted(d for d in SPECS.glob("*/*") if (d / "defects.jsonl").exists())


def escape_reason(d: dict, reg: dict[str, Check]) -> tuple[str, str]:
    """用户抓到的缺陷 → (原因, 该做的动作)。四种原因对应四种进化动作。"""
    cat = d["category"]
    if cat.startswith("new:") or cat not in reg:
        return "没有这条检查", f"在登记表新增 {cat.removeprefix('new:')}，带上来源"
    c = reg[cat]
    rd = (REPO / d["artifact"]).parent if d.get("artifact") else None
    rec = load_qc(rd).get("checks", {}).get(cat) if rd and rd.is_dir() else None
    if rec is None:
        if not c.gate:
            return "有检查但不是闸门", f"{cat} 改成闸门（gate = true）"
        if not d.get("artifact"):
            return "闸门建立前交付", f"只计入基线；之后 {cat} 由闸门挡" + ("（还缺机检工具）" if not c.auto else "")
        return "这件产物没走闸门", "查交付路径为什么没调 `qc.py gate`"
    if rec["verdict"] == "审不了":
        return "审稿审不了", f"给 {cat} 补审稿材料或做机检指标；还做不到就交人看（{rec.get('reason', '')}）"
    if rec["verdict"] == "pass":
        return "检查放过了", f"用这个例子收紧 {cat} 的阈值 / 改审稿清单措辞，存进回归样本"
    if not c.auto:
        return "只靠审稿、还没自动化", f"给 {cat} 做机检工具"
    return "检查报了但仍交付", "查闸门为什么没挡住"


def cmd_escapes(a: argparse.Namespace) -> int:
    n, todo_auto = 0, set()
    for spec in specs_for(a.project):
        reg = registry(drama_of_project(spec.name))
        todo_auto |= {f"{c.id}（{c.level}）" for c in reg.values() if c.gate and not c.auto}
        for d in defects(spec):
            if d["caught_by"] != "user":
                continue
            why, todo = escape_reason(d, reg)
            n += 1
            print(f"[{spec.name}] {d['category']}（follow-up {d.get('followup') or '-'}）：{why} → {todo}")
    print(f"\n用户抓到的缺陷 {n} 条；闸门项里还没自动化的 {len(todo_auto)} 条：{'、'.join(sorted(todo_auto))}")
    return 0


def cmd_stats(a: argparse.Namespace) -> int:
    allrows = [d for spec in specs_for(a.project) for d in defects(spec)]
    fps = Counter(d["category"] for d in allrows if d["caught_by"] == "override" and d.get("kind") == "false_positive")
    accepted = Counter(d["category"] for d in allrows if d["caught_by"] == "override" and d.get("kind") == "accept")
    rows = [d for d in allrows if d["caught_by"] != "override"]
    by = Counter(d["caught_by"] for d in rows)
    total = sum(by.values())
    rate = by["user"] / total if total else 0.0
    print(f"缺陷 {total} 条：用户 {by['user']} · 机检 {by['machine']} · 审稿 {by['review']}；逃逸率 {rate:.0%}（目标 → 0）")
    for cat, k in Counter(d["category"] for d in rows if d["caught_by"] == "user").most_common(8):
        print(f"  用户抓到最多：{cat} × {k}")
    for cat, k in fps.most_common(8):
        print(f"  误报（检查判错、你放行了）：{cat} × {k} —— 多次误报就放松或改写这条检查")
    for cat, k in accepted.most_common(8):
        print(f"  接受瑕疵（检查判对、你决定照用）：{cat} × {k} —— 不是放松检查的理由")
    tally: Counter[str] = Counter()
    for qc in REPO.glob("ai_videos/**/renders/*/qc.json"):
        for r in json.loads(qc.read_text(encoding="utf-8")).get("checks", {}).values():
            if r["verdict"] in ("未审", "审不了"):
                tally[r["verdict"] + (f"·{r['reason']}" if r.get("reason") else "")] += 1
    print(f"未审记录 {tally['未审']} 项（独立审稿缺位的次数）；审不了：材料缺 {tally['审不了·材料缺']} · 看不清 {tally['审不了·看不清']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record")
    r.add_argument("render_dir")
    r.add_argument("--check", action="append", required=True, help="检查id=pass|fail|审不了|未审，可重复")
    r.add_argument("--evidence", default="")
    r.add_argument("--reason", default="", choices=("", *REASONS), help="审不了的原因")
    r.add_argument("--by", choices=BY, required=True)
    g = sub.add_parser("gate")
    g.add_argument("render_dir")
    g.add_argument("--stage", default="video")
    g.add_argument("--when", action="append", default=[], help="规格声明的条件要求，如 一镜到底")
    o = sub.add_parser("override")
    o.add_argument("render_dir")
    o.add_argument("--check", required=True)
    o.add_argument("--kind", required=True, choices=OVERRIDE_KINDS,
                   help="accept＝检查判对了、用户接受这次的瑕疵；false_positive＝检查判错了")
    o.add_argument("--note", required=True, help="用户原话（一句原话只管一类检查）")
    o.add_argument("--mention", default="", help="同一句原话放行另一类时：原话里点到这一类的字")
    o.add_argument("--followup")
    d = sub.add_parser("defect")
    d.add_argument("project")
    d.add_argument("--category", required=True)
    d.add_argument("--artifact", default="")
    d.add_argument("--caught-by", choices=CAUGHT, required=True)
    d.add_argument("--followup")
    d.add_argument("--note")
    for name in ("escapes", "stats"):
        s = sub.add_parser(name)
        s.add_argument("project", nargs="*")
    a = ap.parse_args(argv)
    return {"record": cmd_record, "gate": cmd_gate, "defect": cmd_defect, "override": cmd_override,
            "escapes": cmd_escapes, "stats": cmd_stats}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
