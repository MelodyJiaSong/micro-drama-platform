# k31 洗礼 Purification — 参考研究（follow-up 087）

> 2026-10-23。暴雪 / Valve / DotA Allstars 版权素材，**只作人眼研究**：不上传生成、不挂进技能视频或峰值图参考。
> 所有下载经留痕脚本（`RequestLog.download` / `invoke("youtube","yt-dlp")`），日志在 `characters/request_log.md`（含 2 次 403 / 1 次 404 失败）。
> 整段视频不入库：截帧拼图后，原视频挪到本次会话 scratchpad（不在仓库）。下表文件都在 `ref/research_087/`。
> 读下载物的 Python 一律 `python -I`；拼图用 ffmpeg。

## 文件与观察

| # | 文件 | sha256 前 12 位 | 来源 | 看到了什么 |
|---|---|---|---|---|
| 1 | `dota2_official_purification_6fps_grid.jpg` | 已删：Dota 2 来源，follow-up 316 | | |
| 2 | `dota2_official_purification_closeup_grid.jpg` | 已删：Dota 2 来源，follow-up 316 | | |
| 3 | `yt_noCc0S--uys_dota2_early_purification_5fps_grid.jpg` | 已删：Dota 2 来源，follow-up 316 | | |
| 4 | `yt_swcf1Uh8JKA_dota1_purification_closeup_grid.jpg`（0.125 s 一帧） | 6408489ecd28 | YouTube「omniknight Dota 1 (Última batalla)」https://www.youtube.com/watch?v=swcf1Uh8JKA（DotA 1，魔兽 3 引擎） | **DotA 1 原版画面**：全能骑士对贴身的友方英雄施放，目标头上冒出治疗数字。一道**窄的金黄光束**从天上（画面右上斜下，是俯视透视）落到目标身上，光束粗细只比单位身体宽一点；落下同一瞬间目标脚下爆开一大片明黄色的贴地光盘，向外推到把旁边的敌方英雄也罩进去 |
| 5 | `yt_swcf1Uh8JKA_dota1_purification_after_grid.jpg`（0.2 s 一帧） | b9a321cf7a0c | 同上 | 光束约 0.6–0.8 s 后变细消失；贴地光盘 0.2–0.6 s 由亮黄转淡、外缘带一圈虚光，0.8 s 完全没了。光盘里的敌方英雄随即**倒地**（被这一下打死），尸体留在原地 |
| 6 | `yt_TSZhHLkIfkc_wc3_resurrection_2fps_grid.jpg`（全片 11 s，2 fps） | 7351cc5203b9 | YouTube「Warcraft 3 Resurrection」https://www.youtube.com/watch?v=TSZhHLkIfkc（魔兽 3 原版圣骑士复活术） | 施法者身上一根粗大光柱 + 升起的天使（那是施法者特效 ResurrectCaster，**不是**洗礼用的 ResurrectTarget）；每具复活的尸体身上另有一道细一些的竖直金光 |
| 7 | `yt_TSZhHLkIfkc_wc3_resurrection_closeup_grid.jpg`（5 fps 局部） | 4c5310803554 | 同上 | 光柱从画面顶边垂直贯下，边缘有流动的光纹，颜色偏金带绿（录像色偏）；天使光翼属于施法者特效，洗礼不取 |
| 8 | `yt_RSukFHPcntg_wc3_resurrect_targets_grid.jpg`（5 fps） | 114738187b50 | YouTube「Warcraft 3 - Human Hero - Paladin」https://www.youtube.com/watch?v=RSukFHPcntg | 多具尸体**同时**各落一道 ResurrectTarget 光：上方宽、贴地收拢的金黄光束，从天上斜落（俯视透视），脚下一团金光；**约 1 s**（0.8–1.8 s）后淡出。这就是 6.83d 洗礼套用的特效文件 |
| 9 | `yt_RSukFHPcntg_wc3_paladin_holylight_cast_grid.jpg`（8 fps 局部） | e34e897f0a22 | 同上 | 圣骑士施法动作在俯视画面里很小：施法者原地抬手一下，0.1 s 后目标身上落一道细竖金光（圣光术）。施法动作短促、不抡圆 |
| 10 | `wowpedia_BTNResurrection.webp`（64×64，WebP，原样保存） | 8c71d2746f1a | https://static.wikia.nocookie.net/wowpedia/images/a/a8/BTNResurrection.png | 魔兽 3 复活术图标；**与本卡 `icon/k31_icon_dota1.png`（DotA 1 洗礼图标）完全相同**：一道金色光束从右上角斜射下来，光源处白热 |
| 11 | `wowpedia_BTNResurrection-Reforged.webp`（256×256） | ea7d62513359 | https://static.wikia.nocookie.net/wowpedia/images/b/ba/BTNResurrection-Reforged.png | 重制版图标：竖直的金色光柱里升起展翅人影（复活意象）；光柱边缘有竖条纹理、金色微粒 |
| 12 | `wowpedia_Resurrection_TCG.webp`（1050×1200） | 431ee8cede93 | https://static.wikia.nocookie.net/wowpedia/images/a/a0/Resurrection_TCG.jpg（WoW 卡牌「Resurrection」插画） | 写实插画：祷告者双手上举，倒地者身上冒起一排向上的金白光丝与火花；光照亮周围石墙与人脸——**光是实在的光源** |
| 13 | `dota2_purification_icon.png` | 已删：Dota 2 来源，follow-up 316 | | |

失败未得：`warcraft.wiki.gg/images/Resurrection_TCG.jpg`、`…/BTNResurrection.png`（403）；archive.org 同图（404）；改从 wowpedia 静态 CDN 取到同名图（#10–12）。Dota 2 Wiki（fandom 402）与 Liquipedia（403）页面无法抓取，技能数值以 `d02` §3 为准。

## 关键结论（据此改卡）

1. **持续很短**：DotA 1、魔兽 3 ResurrectTarget、Dota 2 新旧版都在 **约 0.8–1 s** 内完成「光落下 → 冲击波 → 消失」（#1–5、#8）。上一条视频光柱亮了约 2.5–3 s，是最大的不像。→ 光柱从落下到收成一条细线消失 **约 1 秒**，贴地光浪 0.4 s。
2. **光的形状**：一道**只比目标身体宽一点的**金色光束，从天上（云隙）落到被治疗的友军身上（#4、#8、#10、#13）；不是一大片林间丁达尔光，也不是从锤头射出。→ 光束直径约 1.5 m、边缘清楚；场景里的环境光写成柔和晨光、不要林间光束，免得与技能光混在一起。
3. **伤害的形状**：落下同一瞬间，目标脚下一圈**贴地的金色冲击波**向外推到伤害半径（#2、#3、#4），外缘最亮、推完即淡出、**地面不留线**；范围内的敌人在被扫到的那一下身上各闪一下（#3）。上一条视频画成了多道同心光圈留在地上，读起来像魔法阵。→ 写成「一圈翻滚的金色热浪连着尘土」，禁止圆环线条。
4. **伤害可以致死**：DotA 1 实录里光盘范围内的敌方英雄被这一下打死倒地（#5）。→ demo 里两只残血食尸鬼被光浪打死，死法照 `m4_Ghoul/death/` 四张渐进图与 4 秒运动参考（往后仰面倒、仰躺、倒地即顺畅腐烂约 1.5 s 成白骨）。
5. **施法短促、指向目标**：原版施法只是一次短抬手（#9），治疗是瞬间的（#4 的治疗数字与光同帧）。→ 骑士把长柄战锤平平向前伸、锤头对准树人，左手按胸甲祷告一句，光随即落下；锤头不举过头顶、不往外抡。
6. **不取**：施法者头顶的天使与光翼（那是复活术施法者特效 ResurrectCaster / 守护天使的意象，#6、#7、#11）；游戏俯视机位、UI、数字、选中圈。

## follow-up 093 补充（主代理）

- 用户：洗礼改为给自己加圣光、周围食尸鬼死亡；食尸鬼攻击不要像挠痒痒，看原版。
- 下载（经 `reflog.py` 留痕，整段视频放 scratchpad 不入库，截帧拼图在 `research_093/`）：
  - `yt_yxWHNVYiKOM_ghoul_classic_reforged_226-240s_3fps.jpg`（YouTube `yxWHNVYiKOM`，WC3 不死族模型经典 / 重制对比的食尸鬼段）：经典版攻击是**后腿一蹬、上半身人立、两臂高举张开，再用全身重量把骨爪从高处劈下**，大下巴张到最大；重制版是弓背侧身、整条胳膊抡开大弧横扫。
  - `yt_dCVNcMp_EAE_*`（YouTube `dCVNcMp_EAE`）：经典 / 重制食尸鬼的站姿对比，只有待机动作，看不到攻击。
  - `yt_lnsEBuo6MTc_ghouls_vs_footmen_1fps.jpg`（YouTube `lnsEBuo6MTc`）：50 食尸鬼对 50 步兵的远景，太远看不清动作，不作依据。
  - 同一视频 3:45–5:30 的分段下载卡住未完成（不影响结论）。
- 结论：攻击写成「人立、整条胳膊从肩后抡下的重劈」，写进 `m4_Ghoul.md`「普通攻击」供全剧共用；本卡改为对自己施放，三只食尸鬼围攻骑士，被光浪打死。
