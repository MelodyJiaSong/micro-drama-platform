# -*- coding: utf-8 -*-
"""镜间切口（接缝）判定 —— 全仓唯一一份实现。

契约出处：`CLAUDE.md` 【TOP PRIORITY】· `.claude/agent_refs/project/ai_video_jingbie.md` §2.0 ·
`ai_video.md` rule 16.5–16.7 · `ai_videos__格式契约` K31。

用户要的是**两条 clip 首尾直接相接就成片**，不需要转场、补帧、色彩对齐或任何接缝处理。
达成它的判据有两条，缺一不可：

1. **景别差**（信号 A）——比的是**上镜落幅 ÷ 下镜起幅**的 `人占画高`，不是两镜的标称景别。
   强 ＝ ≥2.0 或 ≤0.5（跳两档）；中 ＝ 1.5–2.0（一档）；弱 ＝ 其余。
2. **两端机位不得相同**（rule 16.5）——`人占画高` 只量人、不量画框。两端若是同一个机位
   同一个取景，只要其中一端「人走出了画」，比值就会虚高成 ✅，而观众看到的是同一个画面在跳。
   共用固定机位的对比帧设计只能落在**镜内**或**隔着别的镜**，不能落在**接缝两端**。

中档（一档）要靠场域差（换 plate / 换时段光照 / 机位方位 ≥45°）兜底才算合格，
而**兜底的理由必须写下来**：在后一镜上挂 `jbnote="…"`。没写理由的中档一律判不合格——
「我觉得这里换了场地应该看得出来」不是判据。

每镜需要带的字段：
    jb    = (起幅人占画高, 起幅景别名, 落幅人占画高, 落幅景别名)
    jbcam = (起幅机位标签, 落幅机位标签)
    jbnote= 可选。仅当与上一镜的比值落在中档时需要，写清场域差是什么。

人占画高的量尺（jingbie §1）：
    远景 ≤0.15 / 全景 0.15–0.45 / 中景 0.45–0.75 / 近景 0.75–1.10 /
    特写 >1.10（人不完整入画；纯物体微距按「若有人站在那里会占几屏」外推）。
"""
from dataclasses import dataclass

STRONG_HI: float = 2.0
STRONG_LO: float = 0.5
MID_HI: float = 1.5
MID_LO: float = 1.0 / 1.5


@dataclass(frozen=True)
class Seam:
    """一个接缝的判定结果。"""
    prev_n: int
    next_n: int
    out_v: float
    out_name: str
    in_v: float
    in_name: str
    out_cam: str
    in_cam: str
    ratio: float
    verdict: str
    ok: bool
    note: str | None

    def line(self) -> str:
        """写进 shotlist.md 审计表的一行。"""
        return "| shot%02d→shot%02d | %s %.2f | %s %.2f | **%.2f** | `%s` → `%s` | %s |" % (
            self.prev_n, self.next_n, self.out_name, self.out_v,
            self.in_name, self.in_v, self.ratio, self.out_cam, self.in_cam,
            self.verdict + ("（%s）" % self.note if self.note else ""))

    def context(self) -> str:
        """写进后一镜 `## Shot context` 的「与前一镜的切口」句。"""
        tail = ("**两条 clip 首尾直接相接即可，不需要任何转场、补帧或接缝处理。**"
                if self.ok else "**⚠ 不合格，必须改。**")
        return ("上一镜 shot%02d 落幅 **%s %.2f**（机位 `%s`）→ 本镜起幅 **%s %.2f**（机位 `%s`），"
                "**比值 %.2f — %s**。%s%s" % (
                    self.prev_n, self.out_name, self.out_v, self.out_cam,
                    self.in_name, self.in_v, self.in_cam, self.ratio, self.verdict,
                    ("场域差兜底：%s。" % self.note) if self.note else "", tail))


def verdict(prev: dict, nxt: dict) -> Seam:
    out_v, out_name = prev["jb"][2], prev["jb"][3]
    in_v, in_name = nxt["jb"][0], nxt["jb"][1]
    out_cam, in_cam = prev["jbcam"][1], nxt["jbcam"][0]
    note = nxt.get("jbnote")
    r = out_v / in_v

    if out_cam == in_cam:
        v, ok, note = "❌ 同机位同取景（rule 16.5）", False, None
    elif r >= STRONG_HI or r <= STRONG_LO:
        v, ok, note = "✅ 强（跳两档以上）", True, None
    elif (r >= MID_HI or r <= MID_LO) and note:
        v, ok = "✅ 中（一档）+ 场域差", True
    elif r >= MID_HI or r <= MID_LO:
        v, ok = "❌ 中（一档）但没写场域差理由", False
    else:
        v, ok, note = "❌ 弱（观众读作跳帧）", False, None

    return Seam(prev["n"], nxt["n"], out_v, out_name, in_v, in_name,
                out_cam, in_cam, r, v, ok, note)


def audit(shots: list[dict]) -> list[Seam]:
    """逐对判定。任一接缝不合格直接终止生成 —— 不合格的分镜不许生成出去。"""
    seams = [verdict(a, b) for a, b in zip(shots, shots[1:])]
    bad = [s for s in seams if not s.ok]
    if bad:
        raise SystemExit("镜间切口不合格 %d 处：" % len(bad) + "；".join(
            "shot%02d→shot%02d %.2f %s" % (s.prev_n, s.next_n, s.ratio, s.verdict) for s in bad))
    return seams


def table(seams: list[Seam], generator: str) -> list[str]:
    """shotlist.md 末尾的审计表。"""
    head = [
        "",
        "---",
        "",
        "## 镜间切口审计（%d 个接缝）" % len(seams),
        "",
        "> 量尺＝**人占画高**（远景 ≤0.15 / 全景 0.15–0.45 / 中景 0.45–0.75 / "
        "近景 0.75–1.10 / 特写 >1.10）。比的是**上镜落幅 ÷ 下镜起幅**，"
        "强档 **≥2.0 或 ≤0.5**；中档（一档）要写明场域差才算合格。",
        "> 另一条硬约束：**上镜落幅与下镜起幅的机位标签不许相同**（rule 16.5）—— "
        "同机位同取景时，只要一端「人走出了画」比值就会虚高成合格，"
        "而观众看到的是同一个画框在跳。",
        "> 本表由 `%s` 经 `tools/shot_seam.py` 在生成时计算，"
        "**任一接缝不合格直接终止生成**。" % generator,
        "",
        "| 接缝 | 上镜落幅 | 下镜起幅 | 比值 | 机位（上→下） | 判定 |",
        "|---|---|---|---|---|---|",
    ]
    return head + [s.line() for s in seams]
