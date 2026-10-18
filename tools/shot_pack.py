# -*- coding: utf-8 -*-
"""六模块剧的出片资料包：每镜一个 `资料包/`，把 prompt 参考的全部文件复制一份进去，并与源文件保持一致。

    python tools/shot_pack.py sync <集目录> [镜头key]     # 建 / 更新本集（或一镜）的资料包
    python tools/shot_pack.py sync --all [--quiet]        # 全仓六模块剧（Claude Stop hook 每回合跑）
    python tools/shot_pack.py check <集目录> | --all       # 只报告，不改
    python tools/shot_pack.py cmd <集目录> <镜头key>       # 打印这一镜的草稿提交命令（会扣积分，只在用户决定生成后执行）

资料包 ＝ `{镜头目录}/资料包/`（派生缓存，gitignored）：
    `01_图片1_ep1_s4_st2_overhead.png`、`02_图片2_c14_Brother_Sammuel.png` … `prompt.txt` 与 `manifest.json`。
    正本 prompt 的「参考：」行是 `key_id=>@` 占位（follow-up 229）；资料包的 prompt.txt 按上传顺序把 @ 填成
    @图片N / @视频N / @音频N（同类文件各自从 1 编号），--image / --video / --audio 照资料包顺序给，编号就对得上。
    文件是**复制**（不是链接）：资料包可以整个拿去上传，不会被源文件后来的改动悄悄改掉。

一致性（follow-up 228）——manifest 记每个源文件的路径与 sha256：
    - **更新**：源文件内容变了（例如重画了背景图、换了声样）而 prompt 不用变 → 重新复制，manifest 记新指纹；
    - **失效**：prompt 本身要重编译才对得上 → 清空资料包，只留 `_失效.md` 写明原因，免得把旧包拿去出片。
      失效条件：prompts.json 不是当前编译器版本；分镜在编译后改过（单场编译的场按这一场比，follow-up 259）；参考文件不在了；overhead.toml 在画图之后改过；
      overhead 判定要 previz 而 prompt 里还是 overhead 图（或反过来）。
生成永远人点：本工具不提交。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from tools import episode_shots as es  # noqa: E402
from tools.previz.seedance_ref import MODEL_ALIASES, MODEL_LIMITS  # noqa: E402

PACK = "资料包"
MANIFEST = "manifest.json"
INVALID = "_失效.md"
# 编译器版本只在管理应用 libs/common/episode_workflow.py 维护一份；这里读它，不另抄（v8 时抄写的 7 漏改，82 个资料包全被判失效）
COMPILER_VERSION = int(re.search(r"^COMPILER_VERSION = (\d+)$", (REPO / "projects" / "ai_video_management" / "libs" / "common" / "episode_workflow.py")
                                 .read_text(encoding="utf-8"), re.M).group(1))
FLAG = {"image": "--image", "video": "--video", "audio": "--audio"}
KIND_ZH = {"image": "图片", "video": "视频", "audio": "音频"}
UPLOAD = "upload"             # 上传用副本：大图缩到长边 UPLOAD_MAX_PX、转 JPEG；其余原样（follow-up 229：9 MB 三视图上传超时）
UPLOAD_MAX_PX = 1536
UPLOAD_MAX_BYTES = 300 * 1024      # follow-up 229：VPN 下上传约 20 KB/s，单个文件超过约 400 KB 会超时
# Seedance 参考图的宽高比与短边限制（follow-up 231：怪物三视图 3840×720 ≈ 5.3:1、缩到 1536×288 后短边也不够，
# 带狼的镜两次都「final generation failed」，人物三视图在范围内的镜全部成功）。超出就把图居中贴到同底色画布上补成 PAD_RATIO。
IMAGE_RATIO_RANGE = (0.4, 2.5)
PAD_RATIO = 2.0


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fingerprint(value) -> str:
    """与管理应用 libs/common/episode_workflow.fingerprint 同算法：判分镜在编译后有没有改过。"""
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def shot_dir(ep_dir: Path, scene: str, key: str) -> Path:
    return ep_dir / "scenes" / scene / "shots" / key.rsplit("_", 1)[-1]


def scene_revision(scene: dict, filming_source) -> str:
    """与管理应用 libs/common/episode_workflow.scene_revision 同算法：单场编译时记下的来源（follow-up 259）。"""
    return fingerprint({"scene": scene, "source_revision": filming_source})


STALE_FILMING = "分镜在编译之后改过：确定分镜后重新编译"


def episode_problems(ep_dir: Path) -> tuple[list[dict], str]:
    """(本集已编译的镜头, 整集级失效原因)。分镜改过的场，其镜头带 `stale` 原因：
    场里记了 `source`（单场编译，follow-up 259）就按这一场比；没记的老场按整集比。"""
    prompts = json.loads((ep_dir / "prompts.json").read_text(encoding="utf-8"))
    scenes = prompts["content"].get("scenes", [])
    if prompts["content"].get("compiler_version") != COMPILER_VERSION:
        shots = [dict(shot, scene=scene["id"]) for scene in scenes for shot in scene["shots"]]
        return shots, "prompts.json 是编译器 v%s 的结果，当前是 v%d：重新编译" % (prompts["content"].get("compiler_version"), COMPILER_VERSION)
    filming = json.loads((ep_dir / "filming.json").read_text(encoding="utf-8"))
    episode_fresh = prompts.get("source_revision") == fingerprint({"content": filming["content"], "source_revision": filming["source_revision"]})
    current = {scene["id"]: scene for scene in filming["content"]["scenes"]}
    shots = []
    for scene in scenes:
        if "source" in scene:
            fresh = scene["id"] in current and scene["source"] == scene_revision(current[scene["id"]], filming["source_revision"])
        else:
            fresh = episode_fresh
        shots += [dict(shot, scene=scene["id"], **({} if fresh else {"stale": STALE_FILMING})) for shot in scene["shots"]]
    return shots, ""


def shot_problems(ep_dir: Path, shot: dict) -> list[str]:
    out = []
    sd = shot_dir(ep_dir, shot["scene"], shot["id"])
    for ref in shot.get("refs", []):
        if not (REPO / ref["path"]).is_file():
            out.append("%s（%s）的源文件不在了：%s" % (ref.get("key", ref.get("tag")), ref["role"], ref["path"]))
    decision = sd / "planning" / "previz.json"
    if decision.is_file():
        d = json.loads(decision.read_text(encoding="utf-8"))
        motion = next((r for r in shot.get("refs", []) if r["role"] in ("俯视站位图", "走位预演（绿幕小人偶）")), None)
        if motion and (motion["kind"] == "video") != bool(d.get("previz")):
            out.append("overhead 判定%s要 previz，prompt 里的运动参考是%s：重新编译" % ("" if d.get("previz") else "不", motion["role"]))
        ov = sd / "planning" / "overhead.toml"
        if ov.is_file() and d.get("overhead_sha256") and sha256(ov) != d["overhead_sha256"]:
            out.append("overhead.toml 在画图之后改过：重跑 tools/shot_overhead.py 后重新编译")
        elif motion and motion["kind"] == "video":
            out += previz_problems(sd)
    if not shot.get("refs"):
        out.append("这条 prompt 没有参考清单：重新编译")
    return out


def previz_problems(sd: Path) -> list[str]:
    """走位预演视频是不是按当前 overhead 渲染的：配置要等于 overhead 现在生成的，渲染戳要等于配置现在的输入
    （EP1 s4 曾经 overhead 改了、previz 没重渲，资料包照旧送出旧走位，follow-up 279）。"""
    from tools import overhead_previz
    from tools.previz.planschema import PREVIZ_STAMP, render_inputs
    cfg = sd / "previz" / "previz_config.toml"
    stamp = sd / "previz" / (sd.name + PREVIZ_STAMP)
    redo = "重跑 python tools/overhead_previz.py %s --render 后再 sync" % sd.relative_to(REPO).as_posix()
    try:
        current = overhead_previz.config(sd)
    except Exception as exc:          # overhead 本身读不出：交给 overhead 那一项去报
        return ["按 overhead 生成 previz 配置失败（%s）：%s" % (exc, redo)]
    if not cfg.is_file() or cfg.read_text(encoding="utf-8") != current:
        return ["previz_config.toml 不是按当前 overhead 生成的：" + redo]
    if not stamp.is_file() or json.loads(stamp.read_text(encoding="utf-8")) != render_inputs(cfg):
        return ["走位预演视频不是按当前 previz 配置渲染的：" + redo]
    return []


def upload_tags(refs: list[dict]) -> list[str]:
    """上传顺序编号：同类文件各自从 1 编号（@图片1、@图片2、@音频1 …）。"""
    seen: dict[str, int] = {}
    out = []
    for r in refs:
        seen[r["kind"]] = seen.get(r["kind"], 0) + 1
        out.append("@%s%d" % (KIND_ZH[r["kind"]], seen[r["kind"]]))
    return out


def pack_name(i: int, tag: str, ref: dict) -> str:
    return "%02d_%s_%s%s" % (i, tag.lstrip("@"), ref["key"], Path(ref["path"]).suffix)


def filled(text: str, refs: list[dict]) -> str:
    """把「参考：」行里的 `key=>@` 占位填成上传编号 `key=>@图片N`；正文仍按 key 指认参考。"""
    out = []
    for line in text.split("\n"):
        if line.startswith("参考："):
            for r, tag in zip(refs, upload_tags(refs)):
                line = line.replace("`%s=>@`" % r["key"], "`%s=>%s`" % (r["key"], tag), 1)
        out.append(line)
    return "\n".join(out)


def wanted(shot: dict) -> dict:
    refs = shot.get("refs", [])
    return {"compiler_version": COMPILER_VERSION, "key": shot["id"], "prompt_sha256": hashlib.sha256(shot["text"].encode("utf-8")).hexdigest(),
            "refs": [{"tag": tag, "key": r["key"], "kind": r["kind"], "role": r["role"], "src": r["path"], "file": pack_name(i, tag, r)}
                     for i, (r, tag) in enumerate(zip(refs, upload_tags(refs)), 1)]}


def state(pack: Path, shot: dict) -> str:
    """ok / missing / stale（要更新）。"""
    m = pack / MANIFEST
    if not m.is_file():
        return "missing"
    have = json.loads(m.read_text(encoding="utf-8"))
    want = wanted(shot)
    if {k: have.get(k) for k in ("compiler_version", "key", "prompt_sha256")} != {k: want[k] for k in ("compiler_version", "key", "prompt_sha256")}:
        return "stale"
    if [{k: r.get(k) for k in ("tag", "key", "kind", "role", "src", "file")} for r in have.get("refs", [])] != want["refs"]:
        return "stale"
    for r in have["refs"]:
        src, dst = REPO / r["src"], pack / r["file"]
        if not dst.is_file() or not src.is_file() or not r.get("upload") or not (pack / r["upload"]).is_file():
            return "stale"
        if r["kind"] == "image" and not upload_fits(pack / r["upload"]):   # 旧规则做的上传副本（follow-up 231 前没补边）
            return "stale"
        st = src.stat()
        if st.st_size != r.get("size") or int(st.st_mtime) != r.get("mtime"):      # 快路径：大小与修改时间都没变就不算哈希
            if sha256(src) != r.get("sha256"):
                return "stale"
    return "ok"


def build(pack: Path, shot: dict) -> None:
    if pack.is_dir():
        shutil.rmtree(pack)
    pack.mkdir(parents=True)
    man = wanted(shot)
    (pack / UPLOAD).mkdir()
    for r in man["refs"]:
        src = REPO / r["src"]
        shutil.copyfile(src, pack / r["file"])
        st = src.stat()
        r.update(sha256=sha256(src), size=st.st_size, mtime=int(st.st_mtime), upload=upload_copy(pack, r))
    (pack / "prompt.txt").write_text(filled(shot["text"], shot.get("refs", [])) + "\n", encoding="utf-8", newline="\n")
    (pack / MANIFEST).write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def upload_fits(path: Path) -> bool:
    from PIL import Image
    with Image.open(path) as im:
        w, h = im.size
    return IMAGE_RATIO_RANGE[0] <= w / h <= IMAGE_RATIO_RANGE[1]


def upload_copy(pack: Path, r: dict) -> str:
    """上传用副本（相对资料包）：图片长边超过 UPLOAD_MAX_PX 或文件超过 UPLOAD_MAX_BYTES 就缩图并存 JPEG，
    其余原样复制。整套资料包里的原尺寸副本不动，供人核对；提交命令只传「上传/」里的文件。"""
    full = pack / r["file"]
    # 文件名只用 ASCII：Dreamina CLI 上传文件名带中文的文件实测失败（follow-up 229：同一批里只有中文名的两张没传上去）
    dst = pack / UPLOAD / ("%s_%s%s%s" % (r["file"][:2], r["kind"], r["tag"].lstrip("@")[2:], full.suffix))
    if r["kind"] == "image":
        from PIL import Image
        with Image.open(full) as im:
            w, h = im.size
            odd = not IMAGE_RATIO_RANGE[0] <= w / h <= IMAGE_RATIO_RANGE[1]
            if odd or max(im.size) > UPLOAD_MAX_PX or full.stat().st_size > UPLOAD_MAX_BYTES:
                im = im.convert("RGB")
                if odd:     # 补边，不裁：三视图的三个面都要留着
                    tw, th = (w, round(w / PAD_RATIO)) if w > h else (round(h * PAD_RATIO / 4), h)
                    canvas = Image.new("RGB", (max(tw, w), max(th, h)), im.getpixel((2, 2)))
                    canvas.paste(im, ((canvas.width - w) // 2, (canvas.height - h) // 2))
                    im = canvas
                im.thumbnail((UPLOAD_MAX_PX, UPLOAD_MAX_PX), Image.LANCZOS)
                dst = dst.with_suffix(".jpg")
                im.save(dst, "JPEG", quality=85)
                return dst.relative_to(pack).as_posix()
    shutil.copyfile(full, dst)
    return dst.relative_to(pack).as_posix()


def invalidate(pack: Path, reasons: list[str]) -> bool:
    note = "# 资料包已失效\n\n不要拿这个资料包出片。原因：\n\n" + "".join("- %s\n" % r for r in reasons) + \
           "\n修好后重新编译，再跑 `python tools/shot_pack.py sync <集目录>`。\n"
    if pack.is_dir() and (pack / INVALID).is_file() and (pack / INVALID).read_text(encoding="utf-8") == note \
            and not any(p.name != INVALID for p in pack.iterdir()):
        return False
    if pack.is_dir():
        shutil.rmtree(pack)
    pack.mkdir(parents=True)
    (pack / INVALID).write_text(note, encoding="utf-8", newline="\n")
    return True


def model_problems(shot: dict, model: str) -> list[str]:
    limits = MODEL_LIMITS.get(MODEL_ALIASES.get(model, model))
    if not limits:
        return ["未知模型 %s：不借用别的模型上限" % model]
    out = []
    for kind, key in (("image", "max_images"), ("video", "max_videos"), ("audio", "max_audios")):
        n = sum(1 for r in shot.get("refs", []) if r["kind"] == kind)
        if n > limits[key]:
            out.append("%s 有 %d 个，超过 %s 上限 %d" % (kind, n, model, limits[key]))
    return out


def episodes() -> list[Path]:
    out = []
    for marker in sorted((REPO / "ai_videos").glob("*/workflow.json")):
        try:
            if json.loads(marker.read_text(encoding="utf-8")).get("workflow") != "three-module-v1":
                continue
        except (OSError, ValueError):
            continue
        out += sorted(p.parent for p in (marker.parent / "episodes").glob("ep*/prompts.json"))
    return out


def run(ep_dir: Path, key: str | None, fix: bool, quiet: bool) -> int:
    shots, ep_reason = episode_problems(ep_dir)
    model = es.settings(es.drama_root(ep_dir)).get("prompt", {}).get("model", "seedance2.5")
    counts = {"ok": 0, "updated": 0, "invalid": 0, "stale": 0, "missing": 0}
    for shot in shots:
        if key and shot["id"] != key:
            continue
        pack = shot_dir(ep_dir, shot["scene"], shot["id"]) / PACK
        reasons = [r for r in (ep_reason, shot.get("stale")) if r] + shot_problems(ep_dir, shot) + model_problems(shot, model)
        if reasons:
            counts["invalid"] += 1
            changed = invalidate(pack, reasons) if fix else False
            if not quiet or changed:
                print("  ✗ %s 资料包%s：%s" % (shot["id"], "已失效" if fix else "应失效", "；".join(reasons)))
            continue
        st = state(pack, shot)
        if st == "ok":
            counts["ok"] += 1
            continue
        if fix:
            build(pack, shot)
            counts["updated"] += 1
            if not quiet:
                print("  → %s 资料包%s（%d 个参考）" % (shot["id"], "已建" if st == "missing" else "已更新", len(shot.get("refs", []))))
        else:
            counts[st] += 1
            print("  ⚠ %s 资料包%s" % (shot["id"], "缺" if st == "missing" else "与源文件不一致"))
    if not quiet or counts["updated"] or (not fix and (counts["stale"] or counts["missing"])):
        print("%s：%s" % (ep_dir.relative_to(REPO).as_posix(), " · ".join("%s %d" % (k, v) for k, v in counts.items() if v)))
    return 1 if (not fix and (counts["stale"] or counts["missing"] or counts["invalid"])) else 0


def command(ep_dir: Path, key: str) -> int:
    shots, ep_reason = episode_problems(ep_dir)
    shot = next((s for s in shots if s["id"] == key), None)
    if shot is None:
        print("  ✗ prompts.json 里没有 %s" % key)
        return 1
    if ep_reason or shot.get("stale"):
        print("  ✗ %s 的 prompt 要重新编译：%s" % (key, ep_reason or shot["stale"]))
        return 1
    pack = shot_dir(ep_dir, shot["scene"], key) / PACK
    if state(pack, shot) != "ok" or (pack / INVALID).is_file():
        print("  ✗ %s 的资料包不是最新：先跑 python tools/shot_pack.py sync %s" % (key, ep_dir.relative_to(REPO).as_posix()))
        return 1
    prompt = es.settings(es.drama_root(ep_dir)).get("prompt", {})
    duration = next(int(line[3:-1]) for line in shot["text"].splitlines() if line.startswith("时长："))
    man = json.loads((pack / MANIFEST).read_text(encoding="utf-8"))
    # 绝对路径（Windows 下 CLI 认不出相对路径：follow-up 229 实测 0/4 上传），传「上传/」里的副本
    args = [x for r in man["refs"] for x in (FLAG[r["kind"]], '"%s"' % (pack / r["upload"]).resolve())]
    # 两步出片（follow-up 265）：这里只打印草稿的命令；正式条要带上用户通过的草稿，由 shot_take 组装
    print("草稿提交（会扣积分，只在用户决定生成后执行）：\n  python tools/service_call.py --target %s -- dreamina multimodal2video %s "
          "--prompt=\"$(Get-Content -Raw %s)\" --duration=%d --ratio=%s --video_resolution=%s --model_version=%s --poll=0"
          % (ep_dir.relative_to(REPO).as_posix(), " ".join(args), (pack / "prompt.txt").relative_to(REPO).as_posix(),
             duration, prompt.get("ratio", "16:9"), prompt.get("draft_resolution", "480p"), prompt.get("model", "seedance2.5")))
    print("草稿经用户在管理界面点「通过」后，正式条用：python tools/shot_take.py submit %s %s --stage final"
          % (ep_dir.relative_to(REPO).as_posix(), key))
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="六模块剧出片资料包")
    ap.add_argument("action", choices=["sync", "check", "cmd"])
    ap.add_argument("episode", nargs="?", type=Path)
    ap.add_argument("key", nargs="?")
    ap.add_argument("--all", action="store_true", help="全仓六模块剧的所有已编译集")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    if a.action == "cmd":
        return command(a.episode.resolve(), a.key)
    targets = episodes() if a.all else [a.episode.resolve()]
    rc = 0
    for ep in targets:
        try:
            rc |= run(ep, a.key, a.action == "sync", a.quiet)
        except (OSError, ValueError, KeyError, es.ShotError) as e:
            print("  ✗ %s：%s" % (ep, e))
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
