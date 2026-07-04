# 分镜 prompt 索引 · 热血高校预告片

> 全片 **S01–S21 已出齐**（冷开→出手→群战→双雄→收钩）。每镜独立文件，复制其 `## 视频 prompt` 的 text 块喂 Seedance/Kling，按 Reference uploads 上传 turntable mp4 + 场景 PNG；有台词/VO 镜另按 `## 台词配音 prompt` 单独配音后期 mux。

## 分镜清单（S01–S21）
| 镜 | 文件 | 场景 | 声轨 | 一句话 |
|---|---|---|---|---|
| S01 | `shots/shot01/shot01.md` | 泳池 | VO(英) 后期mux | 黑场水声→水面波光荡开 |
| S02 | `shots/shot02/shot02.md` | 泳池(回忆闪) | 静默 | 水下旧物下沉(暗线#1) |
| S03 | `shots/shot03/shot03.md` | 泳池 | VO(英) 后期mux | 池边骤然睁眼 |
| S04 | `shots/shot04/shot04.md` | 走廊 | 廖彦廷(中) | 廖彦廷被围 |
| S05 | `shots/shot05/shot05.md` | 走廊 | 静默 | 脚步压场入画 |
| S06 | `shots/shot06/shot06.md` | 走廊 | VO(英) 后期mux | 反手扣拳·抬眼 |
| S07 | `shots/shot07/shot07.md` | 走廊 | VO(英) 后期mux | 一拳轰出(承接S06) |
| S08 | `shots/shot08/shot08.md` | 走廊 | 廖彦廷(中) | 廖彦廷呆望 |
| S09 | `shots/shot09/shot09.md` | 楼顶 bg1 | VO(英) 后期mux | 楼顶独站俯瞰(招牌气场·封面候选) |
| S10 | `shots/shot10/shot10.md` | 废厂 bg3 | 静默 | 雨夜被围·低角环绕 |
| S11 | `shots/shot11/shot11.md` | 废厂 bg3 | 静默 | 群战贴身出拳(承接S10·招牌①) |
| S12 | `shots/shot12/shot12.md` | 废厂 bg3 | 静默 | 高俯包围阵放倒两人(招牌②) |
| S13 | `shots/shot13/shot13.md` | 雨夜街 bg5 | 静默 | 街头追打·霓虹横移 |
| S14 | `shots/shot14/shot14.md` | 雨夜街 bg5 | 廖彦廷(中) | 挡棍喊话(兄弟情·成长钩) |
| S15 | `shots/shot15/shot15.md` | 楼顶(雨夜对峙) | 陈劲(中) | 拧指立威(反派首露·中文) |
| S16 | `shots/shot16/shot16.md` | 楼顶(雨夜对峙) | VO(英) 后期mux | 双雄雨中对峙(招牌·封面候选) |
| S17 | `shots/shot17/shot17.md` | 泳池(回忆闪) | 静默 | 水中伸手插帧(暗线#2·加码) |
| S18 | `shots/shot18/shot18.md` | 暗场特写 | 静默 | 攥旧金属吊牌(信物·痛) |
| S19 | `shots/shot19/shot19.md` | 废厂(战后残局) | VO(英) 后期mux | 抹血狂笑起身(招牌·封面候选) |
| S20 | `shots/shot20/shot20.md` | 对峙(楼顶雨夜) | 陈劲+姜川野(中) | 正反打狠话(高潮对白·中文) |
| S21 | `shots/shot21/shot21.md` | 黑场 | OS姜川野(中) 后期mux | 黑屏水声收钩(暗线#3·中文重锤) |

## 承接链（跨镜首帧承接）
- S06→S07（扣拳→出拳）、S10→S11（下沉蓄势→贴身出拳）；其余均硬切（快切·独立首帧）。
- 尾帧锁定（供封面/交接源）：S09 / S16 / S19。

## 声轨分工速查
- **英文 VO 镜**（S01/03/06/07/09/16/19）：视频静音（负面词已含 `no voiceover/no speech/no narration`），VO 按各镜 `## 台词配音 prompt` 用锁定 `en-trailer-vo-deep-01` 单独配音，后期 `tools/mux_av.py` 叠到对应时码。
- **中文在画对白镜**（S04/08/14/15/20）：走 Seedance/Kling 口型生成，voice_id 各取锁定值（廖彦廷 `male-youth-warm-01`／陈劲 `male-villain-cold-01`／姜川野 `male-cold-low-01`），必要时重配后 mux。S20 一镜正反打两句、两 voice_id。
- **静默镜**（S02/05/10/11/12/13/17/18）：视频静音，负面词含人声抑制串；靠动作/光影/BGM 承载。
- **片尾黑场 S21**：纯黑场，OS 姜川野中文重锤（`male-cold-low-01`）+ 一记水声回响后期叠；剧名后期叠加、prompt 不烧字。

## 音频后期（mux）说明
- 英文 VO（`en-trailer-vo-deep-01`）为锁定外部音色：相关镜视频静音，VO 单独配音后期叠到对应时码。
- 中文重锤 S21 / 中文对白镜必要时用锁定 voice_id 重配后 mux。
- BGM：冷峻低沉鼓点/弦乐，随快切递进（后期）。
- 时长合计 ≈ 32.5s 内容 + 段间黑场/呼吸 ≈ 40s；最终由 `ai_videos__时长节奏` 裁定。
