# -*- coding: utf-8 -*-
"""配图硬闸门（用户 2026-11-05，follow-up 054）：「每个 tile 必须有高质量的配图，不然我宁愿不出片。」

    python ai_videos/paihangbang/_tools/tile_gate.py check  [<ep_dir> ...] [--variant chosen|default|risk|all]
    python ai_videos/paihangbang/_tools/tile_gate.py sheet  <ep_dir>          # 逐卡审图拼图 + tile_review.json 待审条目
    python ai_videos/paihangbang/_tools/tile_gate.py record <ep_dir> --reviewer 名字 [--pass T01 T02 ...|all-pending]
                                                             [--fail T07=原因 ...]

规则正文在 bible.md §4「配图硬性要求」，本脚本只做机检与记录：
- check：按将要发布的版本（默认读 release_choices.json；英文 data.json 与中文 data.zh.json 都查）逐卡判——
  ① 卡上必须有图：无图、占位、image_risk 扣下且没有 image_alt 的卡一律不过；
  ② 分辨率：裁成卡片比例后高度 ≥ MIN_CROP_H（与 tile_images.py 同口径，不放大）；
  ③ 独立逐卡审图：卡上实际显示的每张图在 tile_review.json 里有 verdict = pass，且 sha256 与当前文件一致
     （换图即失效，须重审）。AI 生成图算合格配图、不设比例上限，但同样要过 ②③。
  任一卡不过 = 本期该版本不得收录、不得上传。缺图项都在榜尾时提示可截短到的 N（不少于 MIN_N，中间名次不跳）。
- sheet：把要审的图按卡片比例和裁切焦点裁好拼成 `_build/tile_review/sheet_NN.jpg`（每格标 T 编号、名次、名称、AI、裁后像素），
  并在 tile_review.json 里为新图或换过的图建 pending 条目。审图人必须是另起上下文的独立审片（子代理或 tools/qc_review.py 进程），不是作者。
- record：审图人逐张记结论；fail 必须写原因。
退出码：check 有不过的期返回 1。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
SERIES = HERE.parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "projects" / "rank_scroll"))
from rank_scroll.contract import ContractError, load_episode  # noqa: E402

CARD_H = 800
MIN_CROP_H = 1000          # 与 tile_images.py 一致：1080p 下前 10 名卡高 800×1.06，留余量、不放大
MIN_N = 30                 # bible §2.1：题材允许 30–100
REVIEW = "tile_review.json"
PENDING = "待独立审图"
CHOICES = SERIES / "release_choices.json"
Image.MAX_IMAGE_PIXELS = None


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def size(p: Path) -> tuple[int, int]:
    with Image.open(p) as im:
        w, h = im.size
        if im.getexif().get(274, 1) in (5, 6, 7, 8):
            w, h = h, w
    return w, h


def crop_h(w: int, h: int, target: float, fit: str = "cover") -> int:
    """原图高里「对应整张卡高」的像素数（cover 裁切后高；contain 时按整图放入后的缩放比折算），与 MIN_CROP_H 比。"""
    if fit == "contain":
        return int(max(h, w / target))
    return int(h if w / h >= target else w / target)


def chosen_variant(ep: Path) -> str:
    choices = json.loads(CHOICES.read_text(encoding="utf-8")) if CHOICES.is_file() else {}
    return choices.get(ep.name, "default")


def load_review(ep: Path) -> dict:
    f = ep / REVIEW
    return json.loads(f.read_text(encoding="utf-8")) if f.is_file() else {"tiles": {}}


def save_review(ep: Path, rev: dict) -> None:
    (ep / REVIEW).write_text(json.dumps(rev, ensure_ascii=False, indent=1), encoding="utf-8")


def shown(ep: Path, variant: str) -> tuple[list[dict], list[str]]:
    """该版本（英文 + 中文）每张卡实际显示的图。返回 (卡列表, 合同错误)。"""
    target = (json.loads((ep / "data.json").read_text(encoding="utf-8")).get("layout") or {}).get("card_w", 600) / CARD_H
    cards, errors = [], []
    for lang in ("en", "zh"):
        if lang == "zh" and not (ep / "data.zh.json").is_file():
            continue
        try:
            e, _ = load_episode(ep, allow_risk_images=(variant == "risk"), lang=lang)
        except ContractError as err:
            errors += [f"[{lang}] {m}" for m in err.args[0]] if err.args and isinstance(err.args[0], list) else [f"[{lang}] {err}"]
            continue
        for it in e.items:
            rel = it.image.resolve().relative_to(ep.resolve()).as_posix() if it.image else None
            cards.append({"lang": lang, "rank": it.rank, "name": it.name, "image": rel, "path": it.image,
                          "ai": it.image_ai, "withheld": it.image_withheld, "focus": it.image_focus, "fit": it.image_fit, "target": target})
    return cards, errors


def judge(ep: Path, variant: str) -> dict:
    cards, errors = shown(ep, variant)
    rev = load_review(ep)["tiles"]
    fails: list[tuple[int, str, str]] = []           # (rank, name, 原因)
    seen: dict[str, str] = {}
    en_bad: set[tuple[int, str]] = set()            # 英文版已报过的（名次, 原因），中文版同样的问题不重复列
    for c in cards:
        tag = "" if c["lang"] == "en" else "（中文版）"
        if c["path"] is None:
            why = "图被扣下（image_risk，无 image_alt）" if c["withheld"] else "无图 / 占位卡"
            if c["lang"] == "en":
                en_bad.add((c["rank"], why))
            if (c["rank"], why) not in en_bad or c["lang"] == "en":
                fails.append((c["rank"], c["name"], tag + why))
            continue
        rel = c["image"]
        if rel not in seen:
            w, h = size(c["path"])
            ch = crop_h(w, h, c["target"], c["fit"])
            why = []
            if ch < MIN_CROP_H:
                why.append(f"分辨率不足：{w}×{h}，裁成卡片后高 {ch} px < {MIN_CROP_H}")
            r = rev.get(rel)
            same = r and r.get("sha256") == sha256(c["path"]) and r.get("fit", "cover") == c["fit"]   # 换图或换放法，旧结论都失效
            if same and r.get("verdict") == "fail":
                why.append(f"审图不合格：{r.get('note') or '（未写原因）'}")
            elif not same or r.get("verdict") != "pass" or not r.get("reviewer"):
                why.append(PENDING)                   # 没审过、换过图（旧结论失效）或待定
            seen[rel] = "；".join(why)
            if seen[rel]:                             # 同一张图（中英文版共用）只报一次
                fails.append((c["rank"], c["name"], tag + seen[rel]))
    n = sum(c["lang"] == "en" for c in cards)
    pending = [f for f in fails if f[2].endswith(PENDING)]
    hard = [f for f in fails if f not in pending]
    bad = sorted({r for r, _, _ in hard})
    cut = None
    if bad and not errors:
        k = sum(c["lang"] == "en" and c["rank"] < bad[0] for c in cards)   # 缺图项全在榜尾时可截到的 N
        cut = k if k >= MIN_N else 0
    return {"episode": ep.name, "variant": variant, "n": n, "ok": not fails and not errors,
            "fails": hard, "pending": pending, "errors": errors, "cut": cut,
            "ai": len({c["image"] for c in cards if c["ai"]}), "images": len({c["image"] for c in cards if c["image"]})}


def gate(ep: Path, variant: str | None = None) -> dict:
    """给 release.py / upload.py 调用：返回 judge 结果，ok=False 即本期该版本不得收录、不得上传。"""
    return judge(ep, variant or chosen_variant(ep))


def report(r: dict) -> None:
    head = f"{'✅' if r['ok'] else '⛔'} {r['episode']} [{r['variant']}] {r['n']} 卡，图 {r['images']} 张（AI {r['ai']}）"
    print(head)
    for m in r["errors"]:
        print("   合同错误：" + m)
    for rank, name, why in sorted(r["fails"]):
        print(f"   #{rank:>2} {name[:36]:36} {why}")
    if r["pending"]:
        print(f"   另有 {len(r['pending'])} 张图{PENDING}（没审过或换过图；跑 sheet 后由独立审图人 record）")
    if r["fails"]:
        bad = len({x[0] for x in r["fails"]})
        print(f"   → {bad} 个名次有卡缺图或不合格，" + (f"可从榜尾截短到 Top {r['cut']}（截短后重做标题 / 片头 / 洞察 / 计分板再渲）" if r["cut"]
                                     else f"缺图项不全在榜尾（截短后少于 {MIN_N}），本期不出，除非补齐"))


def cmd_check(eps: list[Path], variant: str) -> int:
    bad = 0
    for ep in eps:
        variants = ["default", "risk"] if variant == "all" else [chosen_variant(ep) if variant == "chosen" else variant]
        for v in variants:
            r = judge(ep, v)
            report(r)
            bad += not r["ok"]
    print(f"\n{len(eps)} 期，{bad} 个版本未过配图闸门" if len(eps) > 1 else "")
    return 1 if bad else 0


def cover(im: Image.Image, w: int, h: int, focus: tuple[float, float]) -> Image.Image:
    s = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * s)), max(h, round(im.height * s))), Image.LANCZOS)
    x = round((im.width - w) * focus[0])
    y = round((im.height - h) * focus[1])
    return im.crop((x, y, x + w, y + h))


def contain(im: Image.Image, w: int, h: int, focus: tuple[float, float]) -> Image.Image:
    """与渲染器 draw_contain 同口径：整图放入，同图 cover 放大、模糊、压暗填空。"""
    from PIL import ImageEnhance, ImageFilter
    bg = ImageEnhance.Brightness(cover(im, w, h, (0.5, 0.5)).filter(ImageFilter.GaussianBlur(18 * w / 800))).enhance(0.65)
    s = min(w / im.width, h / im.height)
    fg = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    bg.paste(fg, (round((w - fg.width) * focus[0]), round((h - fg.height) * focus[1])))
    return bg


def cmd_sheet(ep: Path, per: int = 10) -> None:
    rev = load_review(ep)
    tiles = rev.setdefault("tiles", {})
    todo, cards = [], {}
    for v in ("default", "risk"):
        cs, errors = shown(ep, v)
        for m in errors:
            print("合同错误：" + m)
        for c in cs:
            if c["image"] and c["image"] not in cards:
                cards[c["image"]] = {**c, "variants": set()}
            if c["image"]:
                cards[c["image"]]["variants"].add(v)
    next_id = 1 + max((int(t["id"][1:]) for t in tiles.values() if t.get("id")), default=0)
    for rel, c in sorted(cards.items(), key=lambda kv: kv[1]["rank"]):
        h = sha256(c["path"])
        t = tiles.get(rel)
        if t is None:
            t = tiles[rel] = {"id": f"T{next_id:02d}"}
            next_id += 1
        if t.get("sha256") != h or t.get("fit", "cover") != c["fit"]:
            if t.get("verdict"):
                t["previous"] = {k: t.get(k) for k in ("verdict", "note", "reviewer", "date")}
            t.update({"sha256": h, "verdict": "pending", "note": "", "reviewer": "", "date": ""})
        w, hh = size(c["path"])
        t.update({"rank": c["rank"], "name": c["name"], "ai": c["ai"], "variants": sorted(c["variants"]),
                  "px": f"{w}x{hh}", "crop_h": crop_h(w, hh, c["target"], c["fit"]), "fit": c["fit"]})
        if t["verdict"] != "pass":
            todo.append((t["id"], rel, c))
    save_review(ep, rev)
    out = ep / "_build" / "tile_review"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("sheet_*.jpg"):
        old.unlink()
    cw = 300
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    for s in range(0, len(todo), per):
        chunk = todo[s:s + per]
        ch = round(cw / chunk[0][2]["target"])
        cols = 5
        rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (cw + 12) + 12, rows * (ch + 70) + 12), (24, 24, 28))
        d = ImageDraw.Draw(sheet)
        for k, (tid, rel, c) in enumerate(chunk):
            x, y = 12 + (k % cols) * (cw + 12), 12 + (k // cols) * (ch + 70)
            with Image.open(c["path"]) as raw:
                raw.draft("RGB", (cw * 3, ch * 3))
                im = ImageOps.exif_transpose(raw).convert("RGB")
            sheet.paste(contain(im, cw, ch, c["focus"]) if c["fit"] == "contain" else cover(im, cw, ch, c["focus"]), (x, y))
            t = tiles[rel]
            col = (255, 90, 90) if t["crop_h"] < MIN_CROP_H else (230, 230, 230)
            d.text((x, y + ch + 4), f"{tid}  #{c['rank']}  {'AI  ' if c['ai'] else ''}{t['crop_h']}px", fill=col, font=font)
            d.text((x, y + ch + 28), c["name"][:30], fill=(180, 180, 180), font=font)
        p = out / f"sheet_{s // per + 1:02d}.jpg"
        sheet.save(p, quality=90)
        print(p)
    print(f"待审 {len(todo)} 张（共 {len(cards)} 张显示图）。审图人看拼图（必要时打开原图）后用 record 记结论。")


def cmd_record(ep: Path, reviewer: str, passes: list[str], fails: list[str]) -> None:
    rev = load_review(ep)
    by_id = {t["id"]: t for t in rev["tiles"].values()}
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    for spec in fails:
        tid, _, note = spec.partition("=")
        if tid not in by_id:
            sys.exit(f"没有 {tid}（先跑 sheet）")
        if not note.strip():
            sys.exit(f"{tid}：fail 必须写原因（T07=逆光远景、主体辨认不出）")
        by_id[tid].update({"verdict": "fail", "note": note.strip(), "reviewer": reviewer, "date": now})
    if passes == ["all-pending"]:                     # fail 先记，余下的待审才算 pass
        passes = [i for i, t in by_id.items() if t.get("verdict") == "pending"]
    for tid in passes:
        if tid not in by_id:
            sys.exit(f"没有 {tid}（先跑 sheet）")
        by_id[tid].update({"verdict": "pass", "note": "", "reviewer": reviewer, "date": now})
    save_review(ep, rev)
    left = sum(t.get("verdict") == "pending" for t in by_id.values())
    print(f"已记 pass {len(passes)}、fail {len(fails)}；仍待审 {left}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("eps", nargs="*", type=Path)
    c.add_argument("--variant", choices=["chosen", "default", "risk", "all"], default="chosen")
    s = sub.add_parser("sheet")
    s.add_argument("ep", type=Path)
    r = sub.add_parser("record")
    r.add_argument("ep", type=Path)
    r.add_argument("--reviewer", required=True)
    r.add_argument("--pass", dest="passes", nargs="*", action="extend", default=[])
    r.add_argument("--fail", dest="fails", nargs="*", action="extend", default=[])
    a = ap.parse_args()
    if a.cmd == "check":
        eps = a.eps or sorted(p for p in (SERIES / "episodes").iterdir() if (p / "data.json").is_file())
        return cmd_check([p.resolve() for p in eps], a.variant)
    if a.cmd == "sheet":
        cmd_sheet(a.ep.resolve())
    else:
        cmd_record(a.ep.resolve(), a.reviewer, a.passes, a.fails)
    return 0


if __name__ == "__main__":
    sys.exit(main())
