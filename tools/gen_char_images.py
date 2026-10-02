# -*- coding: utf-8 -*-
"""每张人物卡出一张立绘、每张剧情物件卡出一张锚点图。

卡 `characters/{dir}/{dir}.md` 里 `# Seedream 立绘 prompt`（`--kind props`：`props/{dir}/{dir}.md` 里
`# 锚点图 prompt`，三视图卡没有这个标题、不在此列）标题之后、首行 ＝ 目录名的第一个 ```text 块 →
`{dir}/{dir}.png`。块内没有 `负面词` 行的，接上其后 `## 负向` 节的块。首行路由键与 `参考:` / `比例:` 这类
给人看的行不发给模型。立绘零参考图（纯文字自由生成）。
画幅读块里 `比例:` 行的比值（限 `gen_bg_images.RATIOS`；不带比值的「比例：真人正常比例…」是身形描述，不算），
读不到用 KINDS 的缺省；命令行 `--aspect` 显式给了才覆盖（2026-09-30：m7 / m9 写 16:9，工具写死 9:16 出成竖幅）。

引擎按 `tools/image_engine.py`（rule 4l）：人物立绘是第一张锚点 → 先走 ElevenLabs；剧情物件按简单单物件
→ 先走即梦（复杂物件加 `--engine elevenlabs`）。首选失败再退另一家；超即梦 1600 字的只能走 ElevenLabs。

用法（仓库根目录）：
    python tools/gen_char_images.py plan --drama shengji_zhilu
    python tools/gen_char_images.py run  --drama shengji_zhilu [--only c1,m3] [--shard k/n] [--force]
    python tools/gen_char_images.py run  --drama shengji_zhilu --kind props --only p3,p9
已出图的跳过，可中断可续跑。
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from tools import gen_bg_assets as gba  # noqa: E402  即梦并发安全提交
from tools import gen_bg_images as bgi  # noqa: E402  即梦可重试错误的判据
from tools import gen_images_xianjian as dm  # noqa: E402
from tools import image_engine as ie  # noqa: E402
from tools import image_fetch as el  # noqa: E402

# 目录 → (标题, 卡里读不到画幅时的缺省, 是否第一张锚点的难图)
KINDS = {"characters": (re.compile(r"^# Seedream 立绘 prompt.*$", re.M), "9:16", True),
         "props": (re.compile(r"^# 锚点图 prompt.*$", re.M), "1:1", False)}
BLOCK = re.compile(r"```text\n(.*?)\n```", re.S)
NEG = re.compile(r"^## 负向[^\n]*\n+```text\n(.*?)\n```", re.S | re.M)
DROP = ("参考:", "参考用法:", "比例:", "上传:")
ASPECT = re.compile(r"^比例[:：][^\n]*?(\d+:\d+)", re.M)
# rule 22.1：中文相貌词自带东亚默认值，人物立绘第一句必须写死人种 / 地域（实测 shengji c14 / c16 漏写即塌成东亚脸）。
# 只查写没写、不查写的哪一种——仙侠剧写「中国」同样合格。m 键（怪物）豁免。
ETHNIC = re.compile(r"白人|欧洲|西欧|北欧|东亚|中国|华人|汉族|亚洲|黑人|非洲|拉丁|南亚|中东|阿拉伯|西方奇幻|人种|族裔")
# 建立视频抽的锚点三面帧：webapp `CharacterViewExtractor` 写 `views/{卡目录}_{front|side|back}.png`
# （projects/ai_video_management/libs/domain/value_objects/character_video__valueobject.py）。
VIEWS_DIR = "views"
# 旧名：导入器的改名 pass 曾把 views/ 按文件名排序改成 views1/2/3.png（back < front < side；
# shengji_zhilu follow-up 048，c2_Duke 看图核实）。盘上旧图不改名——已进 R2 索引 assets.json。
LEGACY_VIEW_INDEX: dict[str, int] = {"back": 1, "front": 2, "side": 3}


def anchor_frame(char_dir: Path, role: str) -> Path:
    """人物锚点帧（role ∈ front / side / back）：新名优先，没有退旧名 `views{N}.png`；都没有返回新名，由调用方报缺。"""
    d = char_dir / VIEWS_DIR
    new = d / f"{char_dir.name}_{role}.png"
    old = d / f"{VIEWS_DIR}{LEGACY_VIEW_INDEX[role]}.png"
    return old if not new.is_file() and old.is_file() else new


class Job:
    def __init__(self, d: Path, head: re.Pattern, aspect: str) -> None:
        self.dir, self.name = d, d.name
        self.out = d / f"{d.name}.png"
        text = (d / f"{d.name}.md").read_text(encoding="utf-8")
        h = head.search(text)
        if not h:
            raise SystemExit(f"{d.name}：卡里没有「{head.pattern}」")
        tail = text[h.end():]
        body = next((m.group(1) for m in BLOCK.finditer(tail)
                     if m.group(1).split("\n")[0].strip() == d.name), None)
        if body is None:
            raise SystemExit(f"{d.name}：立绘标题后没有首行为目录名的 text 块")
        a = ASPECT.search(body)
        self.aspect = a.group(1) if a else aspect
        if self.aspect not in bgi.RATIOS:
            raise SystemExit(f"{d.name}：立绘块「比例:」行写的 {self.aspect} 不在允许的画幅 {bgi.RATIOS} 里")
        lines = [l for l in body.split("\n")[1:] if not l.startswith(DROP)]
        self.prompt = "\n".join(lines).strip()
        first = re.split(r"[，。\n]", self.prompt, maxsplit=1)[0]
        self.no_ethnic = head is KINDS["characters"][0] and not d.name.startswith("m") and not ETHNIC.search(first)
        if "负面词" not in self.prompt:
            n = NEG.search(tail)
            neg = n.group(1) if n else neg_section(text)
            if neg:
                self.prompt += "\n" + gba.neg_line(neg)


def neg_section(text: str) -> str:
    """立绘块自己没带负向、卡里 `## 负向` 节又拆成多组时：有「负向提示词」成串就只用它，
    否则拼各组，跳过标明不进图像的声音 / 剧情 / 动作组。"""
    m = re.search(r"^## 负向[^\n]*\n(.*?)(?=^#{1,2} )", text, re.S | re.M)
    if not m:
        return ""
    sec, picked = m.group(1), []
    for b in re.finditer(r"```[a-z]*\n(.*?)\n```", sec, re.S):
        label = sec[max(0, b.start() - 200):b.start()].rsplit("```", 1)[-1]
        if "负向提示词" in label:
            return b.group(1)
        if not re.search(r"声音|音效|剧情|动作层|出戏动作|玩家行为|不进图像", label):
            picked.append(b.group(1).strip().rstrip("，,"))
    return "，".join(picked)


def run_one(j: Job, engine: str, args: argparse.Namespace) -> str:
    part = j.out.with_name(j.out.stem + ".part.png")
    if engine == ie.DREAMINA:
        # 网络超时先退避重试，别一失败就退贵的 ElevenLabs（实测 2026-09-25 即梦接口 2–5s 才回头，CLI 频繁超时）
        for attempt in range(bgi.UPLOAD_RETRIES + 1):
            try:
                url, cost = gba._dm_submit(j.prompt, [], j.aspect, wait_s=900)
                break
            except RuntimeError as e:
                if not bgi.RETRYABLE.search(str(e)) or attempt == bgi.UPLOAD_RETRIES:
                    raise
                print(f"  ! {j.name} 即梦网络失败（第 {attempt + 1} 次），重试：{str(e)[:120]}", flush=True)
                time.sleep(45 * (attempt + 1))
        dm.download(url, part)
        part.replace(j.out)
        return f"credits={cost}"
    key = el.api_key()
    gid = el.create(key, j.prompt, model=args.model, quality=args.quality,
                    aspect=j.aspect, resolution=args.resolution)
    el.wait_download(key, gid, part)
    part.replace(j.out)
    return f"gid={gid}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=("plan", "run"))
    ap.add_argument("--drama", required=True, help="相对 ai_videos/，如 shengji_zhilu")
    ap.add_argument("--only", default="", help="逗号分隔的键前缀，如 c1,m3")
    ap.add_argument("--model", default=el.DEFAULT_MODEL)
    ap.add_argument("--quality", default="medium", choices=("low", "medium", "high"))
    ap.add_argument("--resolution", default="2K", choices=("1K", "2K", "4K"))
    ap.add_argument("--kind", default="characters", choices=tuple(KINDS))
    ap.add_argument("--aspect", default=None, choices=bgi.RATIOS,
                    help="显式覆盖；缺省读立绘块的「比例:」行，读不到按 --kind：人物 9:16、物件 1:1")
    ap.add_argument("--engine", default=ie.AUTO, choices=ie.CHOICES,
                    help="auto ＝ 按 rule 4l：人物立绘 ElevenLabs、剧情物件即梦")
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    head, aspect, anchor = KINDS[args.kind]
    root = REPO / "ai_videos" / args.drama / "2_世界观人设" / args.kind
    only = [s for s in args.only.split(",") if s]
    dirs = sorted(d for d in root.iterdir()
                  if d.is_dir() and (d / f"{d.name}.md").is_file()
                  and (not only or d.name.split("_")[0] in only)
                  and head.search((d / f"{d.name}.md").read_text(encoding="utf-8")))
    jobs = [Job(d, head, aspect) for d in dirs]
    if args.aspect:
        for j in jobs:
            j.aspect = args.aspect
    if args.step == "plan":
        for j in jobs:
            print(f"  {j.name:<16} {j.aspect:<5} {len(j.prompt):>5} 字{'  已出图' if j.out.is_file() else ''}"
                  f"{'  ⚠ 首句缺人种（rule 22.1），run 会拒绝' if j.no_ethnic else ''}")
        return 0
    k, n = (int(x) for x in args.shard.split("/"))
    todo = [j for j in jobs if args.force or not j.out.is_file()][k::n]
    bare = [j.name for j in todo if j.no_ethnic]
    if bare:
        raise SystemExit(f"立绘 prompt 第一句没写人种 / 地域（rule 22.1，不写就会塌成东亚脸）：{', '.join(bare)}"
                         "——开篇写「一名西欧白人…」并补一行面部骨相，再出图")
    first = ie.first_choice(anchor, args.engine)
    failed = []
    for j in todo:
        t0 = time.time()
        order = [first, ie.other(first)] if args.engine == ie.AUTO else [first]
        if len(j.prompt) > dm.PROMPT_MAX:
            order = [ie.ELEVENLABS]
        errs = []
        for eng in order:
            try:
                tag = run_one(j, eng, args)
                print(f"  ✓ {j.name} {eng} {len(j.prompt)} 字 {time.time() - t0:.0f}s {tag}", flush=True)
                break
            except (SystemExit, Exception) as e:  # noqa: BLE001 —— 首选失败退另一家；都失败记下、继续
                errs.append(f"{eng}：{str(e)[:200]}")
                print(f"  ! {j.name} {errs[-1]}", flush=True)
        else:
            print(f"  ✗ {j.name}：{' | '.join(errs)}", flush=True)
            failed.append(j.name)
    if failed:
        print(f"失败 {len(failed)}：{', '.join(failed)}（重跑同一条命令即可续）")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
