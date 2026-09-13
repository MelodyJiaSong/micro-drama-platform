# -*- coding: utf-8 -*-
"""光源与热态措辞的一致性检查 —— 全仓唯一一份实现（格式契约 K32 的可执行版）。

契约出处：`.claude/agent_refs/project/ai_video.md` rule 16.8 / 16.9 ·
`CLAUDE.md` § 光源与热态措辞 self-check · `ai_videos__格式契约` K32。

起因：hy2 shot04 是白天刨土的镜，坑底却冒火星。两个独立成因——
措辞把「多年前烧过的石头」写成了「被烧得发红」（模型按**当前状态**画，汉语没有过去时），
而 `渲染样式:` 这条**全镜共用串**里写死了「冷白灰环境与暖橙火光强色温对比」，
于是白天的镜也在被要求画暖橙火光。

## 两条检查的精度取舍（重要，初版在这里翻过车）

**C1 共用串污染 —— 判得准，所以是 blocker。**
判据就一句：**`渲染样式:` 行里不许出现任何点名具体光源的词。**
理由：`渲染样式:` 按构造就是「对每一镜都成立」的那条串，而**光源是分镜的属性，不是全片的属性**——
哪一镜有火、有月光、有霓虹，属于该镜的 `光线:` 行。
不需要语义、不会误伤写在单镜 `光线:` 里的霓虹/烛光（那是该镜真有的东西）。

初版曾把判据写成「该 token 出现在**每一个** shot 里才报」，想借此避免误伤。
结果是**部分污染直接逃掉**：hy2 修好 shot04 之后变成 11/12，就再也报不出来了，
而那 11 镜的债一点没少。判据必须与「有多少镜中招」无关。

**C2 热态词 —— 判不准，所以只报 warning 并附原句，交人判断。**
「烧红/余烬/通红」是痕迹还是状态，要读上下文才知道；而「本镜有没有在燃的火」没有跨剧通用的
结构化信号（`用火视觉底线` 只有 hy2 的生成器 emit，拿它当通用判据会把真有火的镜判成无火）。
初版把 C2 做成 blocker 并用关键词猜有没有火，结果 413 个 shot 里误报一片——
**一个在全语料上大面积报警的检查，等于没有检查**。宁可少报、报准。

扫描前一律剔掉含否定词的分句：`光线:` 里「**没有**闪电」是反向声明，不算提到该光源。
`_deleted/` 目录（历史归档）不扫。

用法：
    import prompt_light
    prompt_light.gate(md_by_shot, legacy={"shot01"})   # 生成器构建闸门

    python tools/prompt_light.py                        # 全仓巡检
    python tools/prompt_light.py ai_videos/huangye_shenghuo/hy2
"""
import io
import os
import re
import sys
from dataclasses import dataclass

# 点名**某个具体光源**的措辞。出现在全镜共用串里就是污染。
LIGHT_TOKENS: tuple[str, ...] = (
    "火光", "暖橙", "橙红辉光", "烛光", "月光", "闪电", "霓虹", "灯光", "夕阳", "篝火",
)
# 「正在发生」的热态词 —— 描述状态，不描述痕迹。
HEAT_TOKENS: tuple[str, ...] = (
    "烧红", "烧得发红", "发红发脆", "通红", "红热", "炽热", "余烬", "冒着烟", "尚有余温",
)

_NEGATION = re.compile(r"(没有|不许|不出现|绝不|不会|无任何|不发|不冒|不掉|不溅|禁止|不存在|无任何)")
_CLAUSE = re.compile(r"[；;。\n]")
SKIP_DIRS: tuple[str, ...] = ("_deleted", "previz", "renders")


@dataclass(frozen=True)
class Issue:
    shot: str
    level: str      # blocker | warning
    code: str       # C1 | C2
    detail: str


def _scannable(text: str) -> str:
    """剔掉含否定词的分句：反向声明不算「提到」。"""
    return "；".join(c for c in _CLAUSE.split(text) if not _NEGATION.search(c))


def positive(md: str) -> str | None:
    b = re.findall(r"```text\n(.*?)\n```", md, re.S)
    return b[0] if b else None


def style_line(pos: str) -> str:
    for ln in pos.split("\n"):
        if ln.startswith("渲染样式:"):
            return ln
    return ""


def check_drama(md_by_shot: dict[str, str]) -> list[Issue]:
    """一部剧（或一集）整体过一遍。C1 需要横向比对，所以必须整部一起看。"""
    if not md_by_shot:
        return []
    pos = {s: positive(md) for s, md in md_by_shot.items()}
    pos = {s: p for s, p in pos.items() if p}
    if not pos:
        return []
    out: list[Issue] = []

    # ── C1：共用串点名了具体光源（出现在**每一个** shot 的 渲染样式 行）──
    styles = {s: _scannable(style_line(p)) for s, p in pos.items()}
    for tok in LIGHT_TOKENS:
        hit = [s for s, ln in styles.items() if tok in ln]
        if hit:
            out.extend(Issue(s, "blocker", "C1",
                             "`渲染样式:` 是全镜共用串，却点名了具体光源「%s」"
                             "——它对每一镜都成立吗？不成立就拆成条件分句，"
                             "没有该光源的镜要反向声明（rule 16.9）" % tok)
                       for s in sorted(hit))

    # ── C2：热态词（只报 warning，附原句交人判断）──
    for s in sorted(pos):
        scan = _scannable(pos[s])
        for tok in HEAT_TOKENS:
            if tok not in scan:
                continue
            sent = next((c.strip() for c in _CLAUSE.split(scan) if tok in c), "")
            out.append(Issue(s, "warning", "C2",
                             "热态词「%s」：如果它写的是**痕迹**（多年前烧过），"
                             "模型会画成**状态**（真的在发红冒火星）。原句：…%s…"
                             % (tok, sent[:60])))
    return out


def gate(md_by_shot: dict[str, str], legacy: set[str] | None = None) -> list[Issue]:
    """生成器的构建闸门。

    `legacy` ＝ 显式的技术债清单（已按旧串出过渲染、暂不改的镜号）。
    **清单只减不增**：新镜不在里面，一旦犯同样的错就直接终止生成。
    """
    legacy = legacy or set()
    issues = check_drama(md_by_shot)
    hard = [i for i in issues if i.level == "blocker" and i.shot not in legacy]
    if hard:
        raise SystemExit(
            "光源措辞不合格 %d 处（rule 16.9 / 格式契约 K32）：\n" % len(hard)
            + "\n".join("  %s [%s] %s" % (i.shot, i.code, i.detail) for i in hard))
    return issues


def _load(root: str) -> dict[str, dict[str, str]]:
    """按「剧」归组 —— C1 要横向比对，必须同一部剧的镜放一起。"""
    out: dict[str, dict[str, str]] = {}
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            # `shotlist.md` 也以 shot 开头，但它是清单不是镜
            if not (fn.startswith("shot") and fn.endswith(".md")) or fn == "shotlist.md":
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, "ai_videos").replace(os.sep, "/")
            key = rel.split("/5_6_")[0] if "/5_6_" in rel else os.path.dirname(rel)
            out.setdefault(key, {})[fn[:-3]] = io.open(p, encoding="utf-8").read()
    return out


def _scan(root: str) -> int:
    dramas = _load(root)
    n = sum(len(v) for v in dramas.values())
    print("扫描 %d 部剧 / %d 个 shot md（已跳过 %s）" % (len(dramas), n, "、".join(SKIP_DIRS)))
    blockers = 0
    for drama in sorted(dramas):
        issues = check_drama(dramas[drama])
        if not issues:
            continue
        b = [i for i in issues if i.level == "blocker"]
        w = [i for i in issues if i.level == "warning"]
        blockers += len(b)
        print("\n%s" % drama)
        seen: dict[str, list[str]] = {}
        for i in b:
            seen.setdefault(i.detail, []).append(i.shot)
        for d, shots in sorted(seen.items()):
            print("  ❌ C1 %s" % d[:110])
            print("     %d/%d 镜: %s" % (len(set(shots)), len(dramas[drama]),
                                        ", ".join(sorted(set(shots))[:14])))
        for i in w:
            print("  ⚠ %s %s" % (i.shot, i.detail[:140]))
    if blockers == 0:
        print("\n无 blocker ✔")
    return blockers


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(1 if _scan(sys.argv[1] if len(sys.argv) > 1 else "ai_videos") else 0)
