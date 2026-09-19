# 时空旅行 · 伦敦大火前一夜

> *Posted to the Past · The Last Night of Old London, 1666*（英文片名草案，定稿在 `5_6_分镜与prompt/publish.md`）
> 系列第 3 站 · 目录 `ai_videos/shikong_lvxing/sk3/` · task_id `sk3-20260918-211545` · 开站 2026-09-18

## 这一站是什么

1666 年 9 月 1 日，星期六。伦敦人过了一个再平常不过的周末夜——塞缪尔·皮普斯去看了木偶戏，躲开不想碰见的熟人，在 Islington 吃喝，**一路唱着歌回家**，白天还把新书房打扫干净「为明天」，家里女仆们熬夜在准备第二天宴客的东西。

那场宴席永远没开成。次日凌晨约一点，布丁巷上「国王的面包师」家起火，四天烧掉城内约八成。

旅行者**妮娅**在这一天走进伦敦，逛完这座城，住一晚，然后留下来看着它烧起来。她想在面包铺打烊前找到那个面包师，跟他说一句「今晚把炉子扒干净」。她找到了，也说了。**什么都没有改变。**

## 与其他站的不同

本站是系列第一个 **「Titanic 型」** 站：有观众已知的倒计时、有一个注定失败的任务、有一道可越过的边界、**当地人可以开口**。依据是对 Chloe VS History 全 7 条长片的实测——归一化日均播放里领先一倍的两条，与落后的五条之间唯一系统性的差别就是这四件结构装置。拆解见 `../_series/format_teardown_chloe.md`。

sk1（汴京）维持原来的游览型不变，两种形态各跑一集后由数据决定系列走向。

## 目录

| 路径 | 内容 |
|---|---|
| `0_research/dossier.md` | 史料 dossier 15 节。**开工前先读 §0 的三条**：9/1 全天没有任何可引用的对白 · 那句市长名言查无一手出处 · 火场里其他人的话全是转述 |
| `0_research/parts/w1–w6` | 六路并行调研的原始事实注册表（253 条，机检 `python tools/facts_registry.py ai_videos/shikong_lvxing/sk3`） |
| `0_research/refs/` | 130 张公版历史图（Hollar 长卷、火前火后双联、复辟期服饰…），**本站画面的 img2img 底本**；索引进 git、图走 R2 |
| `0_research/masters/` | hero 图的未缩放原始底片（刻意放在 `refs/` 树外，见 dossier §15b 第 5 条） |
| `1_立项/concept.md` | 立项策划单：三件套、形态铁律、四格、一日时间线、密度合同、生产提示 |
| `2_世界观人设/` | `world.md`（建模原点、光表、bg 清单）· `style_guide.md` · `casting.md`（**§0 真实人物能否开口的四档判定表**）· `relationships.md` · `scenes/london/bg0–bg13`（14 张主体卡 + 锚点图）· `props/p1–p13`（13 张物件卡 + 27 张图）· `characters/c21–c30` |
| `3_大纲/outline.md` | 49 镜骨架 + 全片曲线 + 四位 NPC 盼头落点 |
| `4_剧本/{script.md, dialogue.md}` | 全片台词（英文成片 + 中文译配）与发声总表（含语速核算） |
| `5_6_分镜与prompt/` | `shotlist.md` · `all_shot_prompts.md` · `publish.md`（四站发布页）· `shots/shot01–49/`（卡 + previz 配置 + previz mp4） |
| `2_世界观人设/scenes/london/_blender/london.blend` | 整城白模。**由 `tools/build_london.py` 确定性生成，不手改**；校验渲图在 `_blender/check/` |
| `props/p{2,4,8,9}/*.blend` | 四件走 Hyper3D 的白模，全部过 `whitemodel_normalize` 闸门 |

## 怎么重跑

```
python tools/gen_sk3_assets.py            # 场景/物件/人物卡（--check 校验无漂移）
python tools/gen_shots_sk3.py             # 49 镜卡 + shotlist + all_shot_prompts
python tools/gen_previz_sk3.py            # 只写 38 份 previz 配置
python tools/gen_previz_sk3.py --blend-only  # 每镜的 previz .blend（秒级）
python tools/gen_previz_sk3.py --render      # 出 mp4（分钟级 / 镜，见下）
python tools/image_fetch.py --drama shikong_lvxing/sk3 --scene bg0-1
blender -b --factory-startup --python tools/build_london.py -- --out <path>
```

**所有卡都是生成产物，手改会被 `--check` 打回**——改数据（`tools/sk3_data/*.toml`）再重跑。

### previz 渲染怎么跑（踩过坑，照这个来）

**别用普通后台跑**：渲染进程挂在 shell 下，shell 一被回收 blender 就死，留下 48 字节的半成品 mp4（只有容器头），
而父进程退出码仍是 0、日志里连 `Blender quit` 都没有——看上去像「跑完了但没输出」。用 PowerShell 真正脱离：

```powershell
Get-Process blender -ErrorAction SilentlyContinue | Stop-Process -Force   # 先确认为 0，rule 4h ⑥
Start-Process python -ArgumentList "-u","tools/gen_previz_sk3.py","--render" `
  -NoNewWindow -PassThru -RedirectStandardOutput previz_batch.log -RedirectStandardError previz_batch.err
```

- **支持断点续跑**：已有 >10 KB mp4 的镜自动跳过；48 字节的半成品会被重渲。
- **判断成没成看日志末尾有没有 `Blender quit`**，不要看文件大小、也不要只看退出码。
- 成本：约 3.1 s/帧 @640×360、6 fps ⇒ 22 s 的镜约 7 分钟；38 镜约 3–4 小时。

偏离登记 `specs/ai_video/sk3/divergence.md`（D1–D10）· 变更日志 `specs/ai_video/sk3/changelog.md`

## 待办（最要紧的三条）

1. **片长 21.0 分钟，超系列 15–16 分钟档**（D10）。没擅自砍——每镜时长都经语速闸门核算，砍时长台词会溢出；压缩顺序见 `5_6_分镜与prompt/publish.md` §7。
2. **`dossier §0b` 六条待人工核成 `human`**，尤其 `timeline.003`（整集架在它上面，却是全 dossier tier 最低）。
3. **建模坐标是推算的**，驱动 hero 镜前应以 Ogilby & Morgan 1676 实测图套合替换。
