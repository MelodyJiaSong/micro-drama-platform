"""2.5D 主体（ep01 第 2 版，用户 2026-11-07 选 B）：把 Codex 侧面参考图抠成透明 PNG，并标定肩线。

    .cache/venvs/triposr/Scripts/python -I ai_videos/zhenshi_chidu/_tools/cutouts.py <集目录> [--only key1,key2]
    .cache/venvs/triposr/Scripts/python -I ai_videos/zhenshi_chidu/_tools/cutouts.py <集目录> --human <人像.png>

--env a.png b.png …：环境抠像（树、灌木），写 assets/cutouts/<名>.png。
--human：1.75 m 参照人（剪影发顶到鞋底 = 1.75 m），写 cutouts.json 的 "human" 条（head_top / bottom）；
已带透明背景的图不再抠像。

- 抠像只用 rembg 的 isnet-general-use（Apache-2.0；同 tools/local_3d.py 的规定，不用默认的非商用模型）。
- 边缘：alpha 收 1 px 再羽化，去掉白底留下的亮边。
- 肩线：在 data.json 记录的 landmark_x_frac（自后向前的长度比例）那一列，取躯干那一段不透明区的上沿 = 肩（鬐甲）顶
  （从离地 45% 高处所在的不透明段往上找，鹿角、牛角等背上方隔开的部分不算）；
  MANUAL 里的条目是看标定图后人工给的（列比例或肩顶像素），理由写在旁边。
- 地面：剪影最低点（近侧蹄底）。
产出 assets/cutouts/<key>.png、cutouts.json（像素量）与 _build/calib/cutouts_sheet.jpg（逐只标线，供看图核对）。
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
os.environ["U2NET_HOME"] = str(REPO / ".cache" / "models" / "rembg")
import rembg  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402

# 看标定图后人工修正：key → {"x_frac": 列比例} 或 {"top_px": 肩顶行（裁切后像素）}；理由写在 note
MANUAL: dict[str, dict] = {
    "08_giraffe_v3": {"x_frac": 0.36, "note": "背线转入颈部处（看图定）；列比例 0.52 落在脖子上。此处头顶约 4.6 m，在 HMW 4.5–6.0 m 内"},
    "22_grevys_zebra_v2": {"x_frac": 0.513, "note": "鬐甲在鬃毛起点（看图定）；列比例 0.636 落在颈部鬃毛上"},
    "03_white_rhinoceros_v2": {"flip": False, "note": "原图头已朝右；低头吃草，「头端更高」的自动判断把它翻反了（第 4 轮审片发现朝左）"},
}


def cut(img: Image.Image, session) -> Image.Image:
    im = rembg.remove(img.convert("RGB"), session=session)
    a = im.getchannel("A").filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
    a = a.point(lambda v: 0 if v < 12 else v)
    im.putalpha(a)
    return im.crop(a.getbbox())


def shoulder(im: Image.Image, x_frac: float, head_right: bool) -> tuple[int, int, int]:
    """返回 (肩所在列, 肩顶行, 剪影底行)；列附近 ±1% 宽取躯干上沿的中位数，抗毛发噪点。"""
    a = im.getchannel("A")
    w, h = im.size
    bottom = max(r for r in range(h) if any(a.getpixel((c, r)) > 128 for c in range(0, w, 2)))
    col = round((x_frac if head_right else 1 - x_frac) * (w - 1))
    tops = []
    for c in range(max(0, col - w // 100), min(w, col + w // 100 + 1)):
        r = int(bottom * 0.55)
        while r > 0 and a.getpixel((c, r)) <= 128:      # 落在两腿之间的空隙：往上找到躯干
            r -= 1
        while r > 0 and a.getpixel((c, r - 1)) > 128:   # 沿躯干往上到第一处透明
            r -= 1
        tops.append(r)
    tops.sort()
    return col, tops[len(tops) // 2], bottom


def head_is_right(im: Image.Image) -> bool:
    """头所在侧：剪影上沿最高点（头 / 角 / 驼峰）不可靠，改看前 15% 与后 15% 宽度里的不透明像素重心高度——头端更高。"""
    a = im.getchannel("A")
    w, h = im.size

    def mean_row(c0, c1):
        rows = [r for c in range(c0, c1, 3) for r in range(0, h, 3) if a.getpixel((c, r)) > 128]
        return sum(rows) / max(1, len(rows))
    return mean_row(int(w * 0.85), w) < mean_row(0, int(w * 0.15))


def main() -> None:
    ep = Path(sys.argv[1]).resolve()
    only = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
    data = json.loads((ep / "data.json").read_text(encoding="utf-8"))
    out = ep / "assets" / "cutouts"
    out.mkdir(parents=True, exist_ok=True)
    jpath = out / "cutouts.json"
    db = json.loads(jpath.read_text(encoding="utf-8")) if jpath.exists() else {}
    session = rembg.new_session("isnet-general-use")
    if "--env" in sys.argv:          # 环境抠像（树、灌木）：只抠图裁边，不标肩线
        for src in sys.argv[sys.argv.index("--env") + 1:]:
            if src.startswith("--"):
                break
            src_p = Path(src).resolve()
            im = cut(Image.open(src_p), session)
            dst = out / f"{src_p.stem}.png"
            im.save(dst)
            print("env", dst.name, im.size)
        return
    if "--human" in sys.argv:
        src = Path(sys.argv[sys.argv.index("--human") + 1]).resolve()
        im = Image.open(src)
        if im.mode == "RGBA" and im.getchannel("A").getextrema()[0] < 10:
            im = im.crop(im.getchannel("A").getbbox())
        else:
            im = cut(im, session)
        png = out / "human_man.png"
        im.save(png)
        a = im.getchannel("A")
        rows = [r for r in range(im.height) if any(a.getpixel((c, r)) > 128 for c in range(0, im.width, 2))]
        db["human"] = {"png": png.relative_to(REPO).as_posix(), "size": list(im.size), "head_top": rows[0],
                       "bottom": rows[-1], "source": src.relative_to(REPO).as_posix()}
        jpath.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
        print("human", db["human"])
        return
    for it in data["items"]:
        key = it["model"]["key"]
        if only and key not in only:
            continue
        src = ep / "assets" / "ref_images" / f"{key}.png"
        png = out / f"{key}.png"
        im = cut(Image.open(src), session)
        man = MANUAL.get(key, {})
        flipped = man["flip"] if "flip" in man else not head_is_right(im)
        if flipped:                         # 统一头朝右（列队从左往右走，动物面朝前进方向）
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        right = True
        im.save(png)
        col, top, bottom = shoulder(im, man.get("x_frac", it["model"].get("landmark_x_frac") or 0.6), right)
        if "top_px" in man:
            top = man["top_px"]
        db[key] = {"png": png.relative_to(REPO).as_posix(), "size": list(im.size), "shoulder_col": col,
                   "shoulder_top": top, "bottom": bottom, "flipped": flipped,
                   "method": "manual" if ("x_frac" in man or "top_px" in man) else "landmark_x_frac", "note": man.get("note", "")}
        print(key, im.size, "col", col, "top", top, "bottom", bottom, flush=True)
    jpath.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    sheet(ep, data, db)


def sheet(ep: Path, data: dict, db: dict) -> None:
    cells = []
    for it in data["items"]:
        key = it["model"]["key"]
        if key not in db:
            continue
        r = db[key]
        im = Image.open(REPO / r["png"]).convert("RGBA")
        bg = Image.new("RGBA", im.size, (200, 205, 210, 255))
        bg.alpha_composite(im)
        d = ImageDraw.Draw(bg)
        d.line([(r["shoulder_col"], r["bottom"]), (r["shoulder_col"], r["shoulder_top"])], fill=(255, 200, 0, 255), width=5)
        d.line([(0, r["shoulder_top"]), (bg.width, r["shoulder_top"])], fill=(255, 60, 0, 255), width=2)
        bg = bg.convert("RGB")
        bg.thumbnail((400, 300))
        cell = Image.new("RGB", (400, 330), (255, 255, 255))
        cell.paste(bg, ((400 - bg.width) // 2, 300 - bg.height))
        ImageDraw.Draw(cell).text((6, 306), f"#{it['rank']} {key} ({r['method']})", fill=(0, 0, 0),
                                  font=ImageFont.load_default(16))
        cells.append(cell)
    cols = 6
    sh = Image.new("RGB", (400 * cols, 330 * ((len(cells) + cols - 1) // cols)), (255, 255, 255))
    for i, c in enumerate(cells):
        sh.paste(c, ((i % cols) * 400, (i // cols) * 330))
    (ep / "_build" / "calib").mkdir(parents=True, exist_ok=True)
    sh.save(ep / "_build" / "calib" / "cutouts_sheet.jpg", quality=85)
    print("sheet ->", ep / "_build" / "calib" / "cutouts_sheet.jpg")


if __name__ == "__main__":
    main()
