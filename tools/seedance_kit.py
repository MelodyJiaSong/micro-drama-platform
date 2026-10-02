# -*- coding: utf-8 -*-
"""Seedance 网页出片资料包：把一镜要上传的东西备好，最后一步「生成」留给人点（`ai_video.md` rule 12.4-K）。

    python tools/seedance_kit.py open  魔兽世界 ep1 shot2      # 先对齐 → 打开资料包 + prompt 进剪贴板 + 在本剧指定的 Chrome 账号里开即梦
    python tools/seedance_kit.py build <shot 目录或 shotNN.md>  # 只对齐，不打开
    python tools/seedance_kit.py check [--all]                  # 列出和原始文件对不上的资料包
    python tools/seedance_kit.py sync --all [--quiet]           # 全部对齐（Stop hook 每回合结束跑一次）

资料包是**派生缓存**（每镜目录下 `资料包/`，gitignored、不进 R2），正本永远是 shot md 与各资产目录：
- 参考文件按 shot md「Reference uploads」的顺序、按上传顺序编号命名（`01_视频1_…mp4`、`03_图片1_…png`），
  **硬链接到原始文件**——与原文件是同一份数据，原文件原地改写时资料包当场就是新的，也不多占盘；
- 原文件被整个换掉（先删后写、改名覆盖）时硬链接会脱钩：`open` 每次先对齐，Stop hook 在每个 Claude 回合结束时
  `sync --all`，判据是「还是不是同一个文件」（O(1)），脱钩就重链；
- Seedance 主体（资产包 entity）不进资料包——网页上从「主体」里 @，名字 ＝ `{entity_prefix}_{卡目录名}`；
- `prompt.txt` 取 shot md 的「## Seedance prompt」块（精简稿，rule 12.4-P；旧镜没有就取「## 视频 prompt」），只把 `参考:` 行的
  `=>@` 按上传顺序填成 `@视频1 / @图片1`，主体填 `@{entity 名}`——正本 shot md 仍是裸 `=>@`（rule 12.4-C）；
  这里能代填编号，是因为上传顺序由资料包的文件编号定死了。
- `open` 是出片前最后一道闸门（rule 44）：本集要有跟得上当前分镜结构、且被整集观感审过的 animatic（`tools/animatic.py`）；
  `seedance.toml` 的 `legacy_eps` 里的集不查。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AI = REPO / "ai_videos"
KIT_SUB = "资料包"                            # 每镜目录下的资料包
META = ("prompt.txt", "使用说明.txt", "kit.json")
CONFIG = "seedance.toml"
VERSION = 4                                   # 资料包的拼法变了就加 1，旧包一律判过期
KIND = {".mp4": "视频", ".mov": "视频", ".webm": "视频", ".png": "图片", ".jpg": "图片", ".jpeg": "图片", ".webp": "图片",
        ".mp3": "音频", ".wav": "音频", ".m4a": "音频"}
UPLOAD = re.compile(r"^\s*-\s+(?P<label>.+?)\s+→\s+(?:\[`[^`]+`\]\((?P<rel>[^)]+)\)|(?P<entity>在 Seedance 里 @.*))\s*$")
REF_ITEM = re.compile(r"`([^`]+?)=>@`")
CHROME = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Google/Chrome/Application/chrome.exe"


@dataclass(frozen=True)
class Ref:
    label: str            # 参考行里的项名（去掉括号说明）
    src: Path | None      # 本地文件；None ＝ Seedance 主体
    kind: str             # 视频 / 图片 / 音频 / 主体
    n: int                # 同类里的第几个（上传后网页上的 @视频1 / @图片2）
    entity: str = ""


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def key(label: str) -> str:
    return re.split(r"[（(]", label, 1)[0].strip()


def same(a: Path, b: Path) -> bool:
    """资料包里的文件与原始文件是不是同一份数据：硬链接看 inode，退回复制的比大小再比内容。"""
    if not (a.is_file() and b.is_file()):
        return False
    if os.path.samefile(a, b):
        return True
    return a.stat().st_size == b.stat().st_size and sha(a) == sha(b)


# ─────────────────────────── 定位 ───────────────────────────

def drama_of(shot_md: Path) -> Path:
    for q in shot_md.parents:
        if (q / CONFIG).is_file():
            return q
        if q.parent == AI:
            return q
    raise SystemExit(f"{shot_md} 不在 ai_videos/ 下")


def config_or_empty(d: Path) -> dict:
    p = d / CONFIG
    return tomllib.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def config(drama: Path) -> dict:
    cfg = config_or_empty(drama)
    if not cfg:
        raise SystemExit(f"{drama.name} 没有 {CONFIG}（entity_prefix / chrome_profile / url 等），先建它")
    return cfg


def resolve(args: list[str]) -> Path:
    """`<shot 目录 | shotNN.md>` 或 `<剧名或别名> <ep> <shot>` → shotNN.md。"""
    if len(args) == 1:
        p = Path(args[0]).resolve()
        md = p / f"{p.name}.md" if p.is_dir() else p
        if not md.is_file():
            raise SystemExit(f"找不到 {md}")
        return md
    if len(args) != 3:
        raise SystemExit("用法：<shot 目录> 或 <剧名/别名> <ep> <shot>，如「魔兽世界 ep1 shot2」")
    name, ep, shot = args
    ep = "ep%02d" % int(re.sub(r"\D", "", ep))
    shot = "shot%02d" % int(re.sub(r"\D", "", shot))
    drama = find_drama(name)
    mds = [p for p in drama.rglob(f"{shot}.md") if p.parent.name == shot and p.parent.parent.parent.name == ep]
    if len(mds) != 1:
        raise SystemExit(f"{drama.name} {ep} {shot}：找到 {len(mds)} 个 shot md")
    return mds[0]


def find_drama(name: str) -> Path:
    """剧名 → `ai_videos/{剧}`：目录名，或该剧 `seedance.toml` 的 alias（如「魔兽世界」）。"""
    dramas = [d for d in AI.iterdir() if d.is_dir() and not d.name.startswith((".", "_"))]
    hit = [d for d in dramas if d.name == name or name in config_or_empty(d).get("alias", [])]
    if len(hit) != 1:
        raise SystemExit(f"剧「{name}」对不上（{CONFIG} 的 alias 里登记别名）：{[d.name for d in hit] or '无'}")
    return hit[0]


def kit_dir(md: Path) -> Path:
    return md.parent / KIT_SUB


# ─────────────────────────── 读 shot md ───────────────────────────

def parse(md: Path, cfg: dict) -> tuple[list[Ref], str, dict]:
    text = md.read_text(encoding="utf-8")
    front = dict(re.findall(r"^(\w+):\s*(.+)$", text.split("---", 2)[1], re.M)) if text.startswith("---") else {}
    m = (re.search(r"^## Seedance prompt[^\n]*\n+```text\n(.*?)\n```", text, re.S | re.M)
         or re.search(r"^## 视频 prompt\s*\n+```text\n(.*?)\n```", text, re.S | re.M))
    if not m:
        raise SystemExit(f"{md.name} 没有「## Seedance prompt」或「## 视频 prompt」text 块")
    prompt = m.group(1)
    ups = {}
    for line in text.split("\n"):
        u = UPLOAD.match(line)
        if u:
            ups[key(u.group("label"))] = u
    ref_line = next((l for l in prompt.split("\n") if l.startswith("参考:")), "")
    refs, count = [], {}
    for item in REF_ITEM.findall(ref_line):
        u = ups.get(key(item))
        if u is None:
            raise SystemExit(f"{md.name}：参考行的「{item}」在 Reference uploads 里找不到对应文件")
        if u.group("entity"):
            refs.append(Ref(key(item), None, "主体", 0, f"{cfg['entity_prefix']}_{key(item)}"))   # 大小写照卡目录名（实测 wow_c1_Aaron）
            continue
        src = (md.parent / u.group("rel")).resolve()
        kind = KIND.get(src.suffix.lower())
        if kind is None:
            raise SystemExit(f"{md.name}：{src.name} 不认识的文件类型")
        count[kind] = count.get(kind, 0) + 1
        refs.append(Ref(key(item), src, kind, count[kind]))
    if not refs:
        raise SystemExit(f"{md.name}：参考行是空的")
    return refs, prompt, front


def kit_prompt(prompt: str, refs: list[Ref]) -> str:
    by = {r.label: r for r in refs}

    def fill(m: re.Match) -> str:
        r = by[key(m.group(1))]
        tag = f"@{r.entity}" if r.kind == "主体" else f"@{r.kind}{r.n}"
        return f"`{m.group(1)}=>{tag}`"
    return "\n".join(REF_ITEM.sub(fill, l) if l.startswith("参考:") else l for l in prompt.split("\n"))


def dest_name(i: int, r: Ref) -> str:
    return f"{i:02d}_{r.kind}{r.n}_{r.src.name}"


# ─────────────────────────── 一致性 ───────────────────────────

def stale(md: Path) -> list[str]:
    """资料包与原始文件对不上的地方；空列表 ＝ 一致。"""
    kd = kit_dir(md)
    man = kd / "kit.json"
    if not man.is_file():
        return ["还没建过"]
    k = json.loads(man.read_text(encoding="utf-8"))
    why = []
    if k.get("version") != VERSION:
        why.append(f"资料包拼法版本 {k.get('version')} → {VERSION}")
    if k.get("shot_md_sha") != sha(md):
        why.append(f"{md.name} 改过")
    for f in k.get("files", []):
        src = REPO / f["src"]
        if not src.is_file():
            why.append(f"源文件没了：{f['src']}")
        elif not same(kd / f["dest"], src):
            why.append(f"与原始文件对不上：{f['dest']}")
    extra = [p.name for p in kd.iterdir() if p.name not in META and p.name not in {f["dest"] for f in k.get("files", [])}]
    if extra:
        why.append(f"多出来的文件：{'、'.join(extra[:3])}")
    return why


def place(src: Path, dest: Path) -> None:
    """dest 与 src 做成同一份数据：优先硬链接（原地改写即同步），跨盘等做不了就复制。"""
    if same(dest, src):
        return
    if dest.exists() or dest.is_symlink():
        dest.unlink()
    try:
        os.link(src, dest)
    except OSError:
        shutil.copy2(src, dest)


def build(md: Path) -> Path:
    drama = drama_of(md)
    cfg = config(drama)
    refs, prompt, front = parse(md, cfg)
    missing = [r.src for r in refs if r.src is not None and not r.src.is_file()]
    if missing:
        raise SystemExit("资料包建不起来，缺源文件（先生成它们）：\n  " + "\n  ".join(str(p.relative_to(REPO)) for p in missing))
    kd = kit_dir(md)
    kd.mkdir(parents=True, exist_ok=True)
    legacy = kd / "上传"                         # v2 的子目录：v3 起文件直接放资料包里
    if legacy.is_dir():
        shutil.rmtree(legacy)
    files, i = [], 0
    for r in refs:
        if r.src is None:
            continue
        i += 1
        d = dest_name(i, r)
        place(r.src, kd / d)
        files.append({"src": r.src.relative_to(REPO).as_posix(), "dest": d, "kind": r.kind, "n": r.n,
                      "linked": os.path.samefile(kd / d, r.src)})
    keep = {f["dest"] for f in files} | set(META)
    for p in kd.iterdir():
        if p.is_file() and p.name not in keep:
            p.unlink()
    (kd / "prompt.txt").write_text(kit_prompt(prompt, refs), encoding="utf-8")
    ents = [r for r in refs if r.kind == "主体"]
    dur = front.get("duration_s", "")
    ratio = re.search(r"^比例:\s*(\S+)", prompt, re.M)
    lines = [f"{md.parent.parent.parent.name} {md.parent.name}（资料包由 tools/seedance_kit.py 生成，别手改；正本是 {md.relative_to(REPO).as_posix()}）", "",
             f"设置：{cfg.get('model', '即梦 Seedance 2.5')} · {cfg.get('mode', '全能参考')} · {ratio.group(1) if ratio else '16:9'} · "
             f"{cfg.get('resolution', '720P')} · {dur}s", "",
             "1. 把下面编号的文件按编号顺序拖进参考区（一次全选拖进去也行，拖完核对网页上视频 / 图片的编号与文件名里的一致）："]
    lines += [f"   {f['dest']}" for f in files]
    lines += ["2. 点进输入框，Ctrl+V 粘贴（prompt 已在剪贴板；参考行里的 @视频1 / @图片1 已按上面的编号填好）。"]
    if ents:
        lines += ["3. 参考行里这几处要从「主体」@（网页只认菜单里点出来的主体）：" + "、".join(f"@{r.entity}（{r.label}）" for r in ents)]
    lines += [f"{4 if ents else 3}. 核对无误后自己点「生成」。"]
    if dur and float(re.search(r"\d+(?:\.\d+)?", dur).group()) > float(cfg.get("max_seconds", 30)):
        lines.insert(3, f"⚠ 本镜 {dur}s 超过网页单条上限 {cfg.get('max_seconds', 30)}s，要拆镜。")
    (kd / "使用说明.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (kd / "kit.json").write_text(json.dumps({"version": VERSION, "shot_md": md.relative_to(REPO).as_posix(), "shot_md_sha": sha(md),
                                             "files": files, "entities": [r.entity for r in ents]}, ensure_ascii=False, indent=1),
                                 encoding="utf-8")
    return kd


# ─────────────────────────── 打开 ───────────────────────────

def chrome_profile_dir(name: str) -> str:
    st = json.loads((Path(os.environ["LOCALAPPDATA"]) / "Google/Chrome/User Data/Local State").read_text(encoding="utf-8"))
    for d, v in st.get("profile", {}).get("info_cache", {}).items():
        if name in (v.get("name"), v.get("gaia_name"), v.get("user_name"), d):
            return d
    raise SystemExit(f"Chrome 里没有叫「{name}」的账号（{CONFIG} 的 chrome_profile）")


def animatic_gate(md: Path, cfg: dict) -> None:
    """出片前先看过整集 animatic（rule 44）：legacy_eps 里的集豁免。"""
    ep = md.parent.parent.parent.name
    if ep in cfg.get("legacy_eps", []):
        return
    import animatic                                # animatic 反过来 import 本模块，放在这里免循环
    bad = animatic.problems(md.parent.parent.parent)
    if bad:
        raise SystemExit("出片前闸门没过（rule 44）：\n  " + "\n  ".join(bad))


def open_kit(md: Path) -> None:
    cfg = config(drama_of(md))
    animatic_gate(md, cfg)
    kd = build(md)
    subprocess.run(["powershell", "-NoProfile", "-Command",
                    f"Get-Content -Raw -Encoding UTF8 -LiteralPath '{kd / 'prompt.txt'}' | Set-Clipboard"], check=True)
    os.startfile(kd)   # noqa: S606 — 只开本地文件夹
    subprocess.Popen([str(CHROME), f"--profile-directory={chrome_profile_dir(cfg['chrome_profile'])}", cfg["url"]])
    print((kd / "使用说明.txt").read_text(encoding="utf-8"))


def mark_broken(md: Path, why: str) -> None:
    kd = kit_dir(md)
    for p in kd.iterdir():
        if p.is_file() and p.name != "kit.json":
            p.unlink()
    (kd / "使用说明.txt").write_text(f"⚠ 资料包暂不可用，别拿这里的东西出片：\n{why}\n修好源文件后跑 python tools/seedance_kit.py open …\n",
                                     encoding="utf-8")
    (kd / "kit.json").write_text(json.dumps({"version": -1, "shot_md": md.relative_to(REPO).as_posix(), "broken": why},
                                            ensure_ascii=False), encoding="utf-8")


def after_write(before: dict[Path, bytes | None]) -> int:
    """生成器写完 shot md 当场调（follow-up 039：「请确保资料包永远是最新状态」）：报出这次真改了哪几镜，
    再把本集每一镜的资料包对齐——没建过的也建，不等回合结束的 Stop hook。返回不可用的镜数（缺源文件）。"""
    changed = [md.stem for md, old in before.items() if old != md.read_bytes()]
    print("本次改动的 shot：" + ("、".join(changed) or "无（与上次逐字一致）"))
    rebuilt, broken = 0, []
    for md in before:
        if not stale(md):
            continue
        try:
            build(md)
            rebuilt += 1
        except SystemExit as e:
            mark_broken(md, str(e))
            broken.append(f"{md.stem}：{e}")
    for b in broken:
        print(f"  ⚠ 资料包暂不可用 {b}")
    print(f"资料包：{len(before)} 镜，这次对齐 {rebuilt} 个，" + (f"{len(broken)} 个不可用" if broken else "全部与原始文件一致"))
    return len(broken)


def all_kits() -> list[Path]:
    out = []
    for p in AI.glob(f"**/shots/*/{KIT_SUB}/kit.json"):
        md = REPO / json.loads(p.read_text(encoding="utf-8"))["shot_md"]
        if md.is_file():
            out.append(md)
        else:                                   # 镜被删了：资料包跟着删，不留孤儿
            shutil.rmtree(p.parent)
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=("open", "build", "check", "sync"))
    ap.add_argument("target", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--quiet", action="store_true", help="只在真的对齐了东西时说话（Stop hook 用）")
    a = ap.parse_args()
    if a.step in ("open", "build"):
        md = resolve(a.target)
        if a.step == "open":
            open_kit(md)
        else:
            print(build(md))
        return 0
    mds = all_kits() if a.all else [resolve(a.target)]
    bad = [(md, w) for md in mds if (w := stale(md))]
    for md, w in bad:
        if a.step == "sync":
            try:
                build(md)
                print(f"资料包已对齐：{md.parent.relative_to(AI).as_posix()}（{'；'.join(w[:3])}）")
            except SystemExit as e:              # 源文件缺了：清掉旧素材、标成不可用，下次 sync 再试——不留半套旧包给人拿去出片
                mark_broken(md, str(e))
                print(f"⚠ 资料包暂不可用：{md.parent.relative_to(AI).as_posix()}——{e}")
        else:
            print(f"⚠ {md.relative_to(REPO).as_posix()}：{'；'.join(w[:4])}")
    if not a.quiet:
        print(f"{len(mds)} 个资料包，{len(bad)} 个与原始文件对不上" + ("，已对齐" if a.step == "sync" and bad else ""))
    return 0 if a.step == "sync" or not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
