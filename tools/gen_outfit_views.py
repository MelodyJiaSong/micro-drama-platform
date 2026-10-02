# -*- coding: utf-8 -*-
"""换装三面图：装备表每个带 `view` 的阶段 → 人物卡目录下一个子目录，出正 / 侧 / 背三张图（ai_video.md rule 4m ⑥ 2026-09-26 修订）。

为什么是三面图而不是重出建立视频：人物的长相与声音在第一次的 turntable 里已经锁住（`views/` 下的锚点三面帧），
换装只换衣服——出三张图比重出一条 4 秒视频便宜，参考锚点图也更稳（follow-up 031，用户定调）。

数据全部现读，不另写一份（rule 4i ①）：
    穿什么      ← `equipment/loadouts/{人物}.toml` 该阶段的 `wear`，以及 `view = {key, name, refs, look, carry}`
    装备长相    ← 各件 `item.toml` 的 `lock` / `worn`；正面图 `{key}-1_正面.png` 当形制参考
    空着的槽    ← `equipment_lib.empty_clause`（不写，模型一定自动补一身甲）
    人          ← 人物卡的角色识别标签 + `views/{人物}_front|side|back.png`（第一次建立视频抽的锚点帧；旧名 views{N}.png 见 gen_char_images.anchor_frame）

落盘：`characters/{人物}/{view.key}_{view.name}/` ＝ 同名 md（三个 ```text 块，首行路由键 `{key}-1_正面 / -2_侧面 / -3_背面`）
+ `{key}-1_正面.png` 等三张图 + `gen_log.json`。
星形派生：正面挂锚点正面 + 本套最多 3 件装备的正面图；侧 / 背只挂本套正面（穿着以它为准）+ 锚点的侧 / 背（只借身形轮廓）。
引擎按 rule 4l：挂了锚点的派生图先走即梦；`--engine X` 显式指定时只用 X。
手部装备（露指 / 半指手套等）换装图锁不住（即梦三次都画成全指）：只锁身上其它部分，手由出片时另挂的装备正面图锁
（`specs/ai_video/shengji_zhilu/lessons.md` L16）。

用法（仓库根目录）：
    python tools/gen_outfit_views.py plan   --drama shengji_zhilu [--only c1-3,c2-1]
    python tools/gen_outfit_views.py build  --drama shengji_zhilu            # 写子目录与卡
    python tools/gen_outfit_views.py images --drama shengji_zhilu [--engine auto|dreamina|elevenlabs] [--force] [--shard k/n]
已出的图跳过，可中断可续跑；参考图还没出的那张跳过并报出来。
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import tomllib
from dataclasses import dataclass
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "tools"))
import check_stage2  # noqa: E402
import equipment_lib  # noqa: E402
from tools import gen_bg_assets as gba  # noqa: E402  即梦并发安全提交
from tools import gen_bg_images as bgi  # noqa: E402  上传副本、可重试判据
from tools import gen_char_images as gci  # noqa: E402  锚点帧在哪（新名 / 旧名 views{N}）
from tools import gen_images_xianjian as dm  # noqa: E402
from tools import image_engine as ie  # noqa: E402
from tools import image_fetch as el  # noqa: E402

VIEWS = (("1", "正面"), ("2", "侧面"), ("3", "背面"))
ANCHOR = {"正面": "front", "侧面": "side", "背面": "back"}
RATIO = "9:16"            # 跟锚点帧（views/*.png 720×1280）走
MAX_EQUIP_REFS = 3        # 即梦一次上传总量有上限（gen_bg_images 实测 4 张），锚点 1 + 装备 3
BG = "干净的浅灰无缝背景，阴天均匀散射光，脚下只有极淡的接触阴影"
# 有兵器的阶段在 view.pose 写握法：只写「横挎在肩上」不写手，模型画出一把悬在肩上没人扶的锤（c1-1 首批实测）
POSE = "双臂自然垂在身侧、两手空着"
STYLE = "真实影视质感，35mm 胶片颗粒，自然色，物理正确的材质与布料褶皱"
NEG = ("人脸变形，五官漂移，换脸，畸形肢体，多余手指，第二个人，画面文字，字幕，水印，logo，发光，特效光，光环，金光，魔法特效，"
       "现代服饰，塑料感材质，游戏截图质感，卡通渲染，三维动画感，背景道具，地面杂物")


@dataclass(frozen=True)
class Outfit:
    char: str             # c1_Aaron
    stage: equipment_lib.Stage
    key: str              # c1-3
    name: str             # 丢了锤
    refs: tuple[str, ...]
    look: str
    carry: tuple[tuple[str, str], ...]   # (装备键, 怎么带着)
    pose: str             # 站姿与手里怎么拿兵器；空 ＝ POSE

    @property
    def folder(self) -> str:
        return f"{self.key}_{self.name}"


def chars_dir(drama: str) -> Path:
    return REPO / "ai_videos" / drama / "2_世界观人设" / "characters"


def outfits(drama: str, only: list[str]) -> list[Outfit]:
    root = equipment_lib.equipment_root(chars_dir(drama))
    out: list[Outfit] = []
    for p in equipment_lib.loadout_paths(root):
        lo = equipment_lib.loadout(root, p.stem)
        raw = {s["id"]: s for s in tomllib.loads(p.read_text(encoding="utf-8")).get("stage", [])}
        for st in lo.stages:
            v = raw[st.id].get("view")
            if not v:
                continue
            unknown = set(v) - {"key", "name", "refs", "look", "carry", "pose"}
            if unknown:                       # schema 允许之外的键：报错，别让它静默失效（CLAUDE.md「一个名字只有一处定义」）
                raise SystemExit(f"{p.name} {st.id} view 里有不认识的键：{sorted(unknown)}")
            if not v["key"].startswith(lo.character.split("_")[0] + "-"):
                raise SystemExit(f"{p.name} {st.id}：view.key {v['key']} 不以 {lo.character.split('_')[0]}- 开头")
            if only and v["key"] not in only:
                continue
            refs = tuple(v.get("refs", []))
            if len(refs) > MAX_EQUIP_REFS:
                raise SystemExit(f"{v['key']}：refs {len(refs)} 件 > {MAX_EQUIP_REFS}（即梦一次上传总量有上限）")
            out.append(Outfit(lo.character, st, v["key"], v["name"], refs, v.get("look", ""),
                              tuple((c["key"], c["how"]) for c in v.get("carry", [])), v.get("pose", "")))
    keys = [o.key for o in out]
    if len(keys) != len(set(keys)):
        raise SystemExit(f"view.key 重复：{keys}")
    return out


def _root(drama: str) -> Path:
    return equipment_lib.equipment_root(chars_dir(drama))


def anchor(drama: str, o: Outfit, view: str) -> Path:
    return gci.anchor_frame(chars_dir(drama) / o.char, ANCHOR[view])


def equip_front(drama: str, k: str) -> Path:
    return equipment_lib.find(_root(drama), k) / f"{k}-1_正面.png"


def own(drama: str, o: Outfit, n: str, view: str) -> Path:
    return chars_dir(drama) / o.char / o.folder / f"{o.key}-{n}_{view}.png"


def label(drama: str, o: Outfit) -> str:
    card = (chars_dir(drama) / o.char / f"{o.char}.md").read_text(encoding="utf-8")
    lab = check_stage2._lock_string(card)
    if not lab:
        raise SystemExit(f"{o.char} 卡里没有角色识别标签")
    return lab


def gear(drama: str, o: Outfit, with_worn: bool) -> str:
    root = _root(drama)
    parts = []
    for k in o.stage.wear:
        it, row = equipment_lib.item(root, k), equipment_lib.row(root, k)
        held = o.pose and row.slot in ("主手", "副手")      # 手里怎么拿以 view.pose 为准，不再贴卡上的穿法（两处写法会打架）
        parts.append(f"{row.slot}——{it['lock']}" + (f"（{it['worn']}）" if with_worn and it.get("worn") and not held else ""))
    for k, how in o.carry:
        parts.append(f"{how}——{equipment_lib.lock(root, k)}")
    return "；".join(parts)


def empty(drama: str, o: Outfit) -> str:
    root = _root(drama)
    return equipment_lib.empty_clause(root, equipment_lib.loadout(root, o.char), o.stage)


def prompts(drama: str, o: Outfit, with_worn: bool = True) -> dict[str, tuple[str, list[str], list[Path]]]:
    """视图名 → (送审稿, 参考行句柄, 参考图路径)。首行路由键不进送审稿（它只给落盘与导入器用）。"""
    lab, eq, emp = label(drama, o), gear(drama, o, with_worn), empty(drama, o)
    look = ("本套状态：" + o.look + "。") if o.look else ""
    eq_refs = [(k, equip_front(drama, k)) for k in o.refs]
    out: dict[str, tuple[str, list[str], list[Path]]] = {}
    pose = o.pose or POSE
    front = (f"全身正面立绘，单人，正对镜头平视，站姿自然、双脚与肩同宽，{pose}；正面对镜头时他右手一侧在画面左边、左手一侧在画面右边；"
             f"头顶到脚底完整入画、居中；{BG}。\n"
             f"人物：与参考图一是同一个人——{lab}；脸、发型、体型、年龄感一律照参考图一，不美化、不重新设计。\n"
             f"衣着：底层衣物没被装备盖住的地方一律照参考图一。本套装备：{eq}。{look}\n"
             f"空着的地方：{emp or '无'}。\n"
             f"参考用法：参考图一只锁这个人的长相、体型与便服；其余参考图依次是{'、'.join(equipment_lib.row(_root(drama), k).name_zh for k, _ in eq_refs)}，"
             f"只锁这几件装备的形制、材质与配色，照搬装备外观，不照搬参考图的构图与背景。\n"
             f"风格：{STYLE}。\n负面词：{NEG}")
    out["正面"] = (front, [f"`{anchor(drama, o, '正面').stem}(锚点正面·长相、体型与便服)=>@`"] +
                   [f"`{k}-1_正面(装备·形制)=>@`" for k, _ in eq_refs],
                   [anchor(drama, o, "正面")] + [p for _, p in eq_refs])
    for n, view, turn in (("2", "侧面", "水平转到正左侧 90°，人物左侧身对镜头：画面里只看得见他身体的左半边，左肩与左臂正对镜头，"
                                        "脸是侧脸轮廓、只露一只眼，右半边身体被挡住"),
                          ("3", "背面", "水平转到正背面 180°，人物背对镜头、看不见脸，只看得见后脑勺与后背；左右与正面对调——他右手一侧（连同右手拿着的东西）在画面右边、"
                                        "左手一侧在画面左边")):   # 不写这句，背面图常把右手的锤画到左手（c1-1 首批实测）
        txt = (f"全身{view}立绘：与参考图一是同一个人、同一身穿着、同一个姿势（{pose}），只把机位绕人物{turn}；头顶到脚底完整入画、居中；{BG}。\n"
               f"衣着与装备一律照参考图一：{lab}；本套装备：{eq}。{look}\n"
               f"空着的地方同参考图一：{emp or '无'}。\n"
               f"参考用法：参考图一定这一身穿着与装备，形制、配色、位置一律不变；参考图二只锁这个人{view}的身形轮廓与站姿，不借它的衣着。\n"
               f"风格：{STYLE}。\n负面词：{NEG}")
        if view == "背面" and any(equipment_lib.row(_root(drama), k).slot == "副手" for k in o.stage.wear):
            # 只给拿着盾的阶段加：没盾的人写了「盾」字，模型会凭空画一面盾
            txt = txt.replace("左手一侧在画面左边", "左手一侧在画面左边；左臂上的盾从背后看只露出盾的背面（背带与握把），看不见盾面", 1)
        out[view] = (txt, [f"`{o.key}-1_正面(本套正面·穿着以此为准)=>@`", f"`{anchor(drama, o, view).stem}(锚点{view}·身形轮廓)=>@`"],
                     [own(drama, o, "1", "正面"), anchor(drama, o, view)])
    for v, (txt, _, _) in out.items():
        if len(txt) > dm.PROMPT_MAX and with_worn:
            return prompts(drama, o, with_worn=False)          # 超即梦硬限：先去掉各件的 `worn` 细节
    return out


def card(drama: str, o: Outfit) -> str:
    ps = prompts(drama, o)
    rng = f"{o.stage.shots[0]}–{o.stage.shots[1]}" if o.stage.shots else "整集"
    lines = [f"# {o.key} · {o.name}（{o.char} 换装三面图）", "",
             f"> **由 `tools/gen_outfit_views.py` 从装备表生成，不要手改。** 改穿着 ＝ 改 `equipment/loadouts/{o.char}.toml` 的 "
             f"`{o.stage.id}` 阶段（`wear` / `view`）后重跑。",
             f"> 阶段 `{o.stage.id}` · {'、'.join(o.stage.episodes) or '—'} {rng} · {o.stage.where}",
             f"> 身上：{'、'.join(o.stage.wear) or '只有便服'}" + (f"；随身：{'、'.join(k for k, _ in o.carry)}" if o.carry else ""),
             "> 长相与声音仍以第一次建立视频（`../views/`）为准；本目录三张图只换衣服（rule 4m ⑥）。", ""]
    for n, view in VIEWS:
        txt, handles, _ = ps[view]
        lines += [f"## {view}", "", "```text", f"{o.key}-{n}_{view}", "参考: " + "、".join(handles), txt, "```", ""]
    lines += ["## 出图后", "", f"存 `{o.key}-1_正面.png` / `{o.key}-2_侧面.png` / `{o.key}-3_背面.png`（与本 md 同目录）。先出正面，侧 / 背挂它。", ""]
    return "\n".join(lines)


def build(drama: str, os_: list[Outfit]) -> None:
    for o in os_:
        d = chars_dir(drama) / o.char / o.folder
        d.mkdir(exist_ok=True)
        (d / f"{o.folder}.md").write_text(card(drama, o), encoding="utf-8")
        print(f"  ✓ {o.char}/{o.folder}/")


def _log(d: Path, **kw: object) -> None:
    p = d / "gen_log.json"
    data = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
    data.update(kw)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def _mirror(p: Path) -> Path:
    """正面图的左右镜像副本（系统临时目录，可随时重建，不进仓库）。"""
    import tempfile
    from PIL import Image, ImageOps
    out = Path(tempfile.gettempdir()) / "outfit_mirror" / f"{p.stem}_mirror.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    ImageOps.mirror(Image.open(p).convert("RGB")).save(out)
    return out


def _dreamina(text: str, refs: list[Path], out: Path) -> int:
    for attempt in range(bgi.UPLOAD_RETRIES + 1):
        try:
            url, cost = gba._dm_submit(text, [bgi._upload_copy(r) for r in refs], RATIO, wait_s=900)
            part = out.with_name(out.stem + ".part.png")
            for i in range(4):        # 图已出、已扣费：下载断了只重下，不重交（实测 WinError 10054 连接被远端重置）
                try:
                    dm.download(url, part)
                    break
                except OSError:
                    if i == 3:
                        raise
                    time.sleep(10 * (i + 1))
            part.replace(out)
            return cost
        except RuntimeError as e:
            if not bgi.RETRYABLE.search(str(e)) or attempt == bgi.UPLOAD_RETRIES:
                raise
            print(f"    ! 即梦网络失败（第 {attempt + 1} 次），重试：{str(e)[:120]}", flush=True)
            time.sleep(45 * (attempt + 1))
    raise RuntimeError("unreachable")


def _eleven(text: str, refs: list[Path], out: Path) -> str:
    key = el.api_key()
    gid = el.create(key, text, model=el.DEFAULT_MODEL, quality="medium", aspect=RATIO, resolution="2K",
                    refs=[el.inline(bgi._upload_copy(p)) for p in refs])
    part = out.with_name(out.stem + ".part.png")
    el.wait_download(key, gid, part)
    part.replace(out)
    return gid


def images(drama: str, os_: list[Outfit], engine: str, force: bool) -> list[str]:
    failed: list[str] = []
    for o in os_:
        d = chars_dir(drama) / o.char / o.folder
        if not (d / f"{o.folder}.md").is_file():
            raise SystemExit(f"{o.folder} 还没有卡——先跑 build")
        ps = prompts(drama, o)
        for n, view in VIEWS:
            out = own(drama, o, n, view)
            if out.is_file() and not force:
                continue
            text, _, refs = ps[view]
            missing = [r for r in refs if not r.is_file()]
            if view == "背面" and not missing:
                # 模型照搬参考图里东西在画面哪一边——背面要的恰好是左右对调，所以喂本套正面的镜像
                # （c2-1 首批实测：文字写明「左右对调」仍把盾画在画面右边、剑在左边）
                refs = [_mirror(refs[0])] + refs[1:]
                text = text.replace("与参考图一是同一个人、同一身穿着", "参考图一是本套正面左右翻转后的镜像，按它的左右位置画背面；与它是同一个人、同一身穿着", 1)
            if missing:
                print(f"  ⏭ {out.name}：参考图还没有 {', '.join(m.name for m in missing)}", flush=True)
                failed.append(out.name)
                continue
            first = ie.first_choice(False, engine)
            order = [first] if engine != ie.AUTO else [first, ie.other(first)]
            if len(text) > dm.PROMPT_MAX:
                order = [e for e in order if e == ie.ELEVENLABS] or [ie.ELEVENLABS]
            t0, errs = time.time(), []
            for eng in order:
                try:
                    tag = (f"credits={_dreamina(text, refs, out)}" if eng == ie.DREAMINA else f"gid={_eleven(text, refs, out)}")
                    _log(d, **{f"{o.key}-{n}": {"engine": eng, "chars": len(text), "refs": [r.name for r in refs], "tag": tag}})
                    print(f"  ✓ {out.name} {eng} {len(text)} 字 {time.time() - t0:.0f}s {tag}", flush=True)
                    break
                except (SystemExit, Exception) as e:  # noqa: BLE001 —— 首选失败退另一家（auto 时）；都失败记下、继续
                    errs.append(f"{eng}：{str(e)[:200]}")
                    print(f"    ! {out.name} {errs[-1]}", flush=True)
            else:
                failed.append(out.name)
    return failed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=("plan", "build", "images"))
    ap.add_argument("--drama", required=True, help="相对 ai_videos/，如 shengji_zhilu")
    ap.add_argument("--only", default="", help="逗号分隔的 view.key，如 c1-3,c2-1")
    ap.add_argument("--engine", default=ie.AUTO, choices=ie.CHOICES)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--shard", default="0/1")
    args = ap.parse_args()
    os_ = outfits(args.drama, [s for s in args.only.split(",") if s])
    if args.step == "plan":
        for o in os_:
            ps = prompts(args.drama, o)
            miss = [r.name for v in ps.values() for r in v[2] if not r.is_file() and not r.name.startswith(o.key)]
            done = sum(own(args.drama, o, n, v).is_file() for n, v in VIEWS)
            print(f"  {'已出' if done == len(VIEWS) else '待出'} {done}/{len(VIEWS)} {o.char:<10} {o.folder:<16} {o.stage.id} {o.stage.shots} "
                  f"字数 {'/'.join(str(len(ps[v][0])) for _, v in VIEWS)}" + (f"  缺参考 {miss}" if miss else ""))
        return 0
    if args.step == "build":
        build(args.drama, os_)
        return 0
    k, n = (int(x) for x in args.shard.split("/"))
    failed = images(args.drama, os_[k::n], args.engine, args.force)
    if failed:
        print(f"未出 {len(failed)} 张：{', '.join(failed)}（参考图齐了 / 网络好了重跑同一条命令即续）")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
