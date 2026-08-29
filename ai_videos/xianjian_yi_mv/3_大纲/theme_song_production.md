# 主题曲制作流程 ·《一生逍遥，半世离散》

> 姊妹档：`theme_song.md`（**词 + 段落时间轴 + 曲风 prompt**，v5 定稿 5:20/320s）。
> 本档只管**怎么把它做出来**：Suno / Mureka 的分工、抽卡策略、评分门、拼接定长、与 `structure.md` 的时间轴回填。
> 工具前提：Suno 会员 + Mureka 会员 + Seedance。零音乐版权风险（词曲全原创；仙剑为致敬向，成片标注「AI 概念重制」）。

---

## 0. 一句话方案

**Suno 出骨架（人声 + 副歌 hook） → Mureka 做 A/B 竞标与器乐补段 → DAW/ffmpeg 定长到片长 → 用成品的真实时间轴回填 `structure.md`。**

三条错误路线，先排掉：

| 反模式 | 为什么不行 |
|---|---|
| 一次生成 5:20 整首就当定稿 | 长曲后半段（副歌2 之后）质量断崖是所有 AI 音乐模型的通病；且时长必然不是 320s |
| 先按 320s 剪好画面，再让歌去凑 | 顺序反了。歌是不可控变量，画是可控变量——**永远让画迁就歌** |
| 一个平台抽到满意为止 | Suno 和 Mureka 的失败模式不重叠（见 §7）。单平台死磕 30 次，不如双平台各 10 次 |

---

## 1. 工具分工

| 工具 | 在本项目里干什么 | 不要用它干什么 |
|---|---|---|
| **Suno** | 主力。人声质感 / 副歌爆发力 / Persona 锁音色 / Extend 续写 / Stems 分轨 | 不要指望它精确执行 `[Intro] 18s` 这类时长指令 |
| **Mureka** | ① 中文咬字对照组（中文语料权重更高，「模样」「没过」这类多音字更稳）② 「以曲生曲」——把 Suno 选中的骨架当参考音频，换配器/换人声出变体 ③ 纯器乐段（前奏/间奏/尾奏）单独生成 | 不要用它当唯一主力抽整首——副歌张力通常弱于 Suno |
| **ffmpeg / Reaper（免费档 Audacity 也够）** | 拼接、交叉淡化、定长到 320s、导出段落 marker | — |
| **Seedance** | 阶段 5–6 出片。**只在歌定稿后启动**，按成品真实时间轴切镜 | 不要在歌没定稿前批量出镜（时间轴一改全废） |
| `tools/mux_av.py` | 最后把成片视频 + 主题曲 MP3 合轨 | — |

---

## 2. 流程总览（S0 → S8）

```
S0 歌词净化（多音字/断句）
  ↓
S1 只抽副歌，锁 hook 旋律        ← 门1：hook 不抓人就重来，不要往下走
  ↓
S2 锁人声 Persona（男/女 AB）    ← 门2：音色定了就不许再换
  ↓
S3 Suno 整首抽卡 ×10            ┐
S4 Mureka 平行抽卡 ×8           ┘ 并行
  ↓
S5 盲听评分 → 选 1 条骨架        ← 门3：8 维评分 ≥ 55/80 才进入精修
  ↓
S6 精修：坏段替换 / Extend / 器乐段单独生成
  ↓
S7 Stems 分轨 → 定长到片长 → 母带
  ↓
S8 落盘 + 用真实时间轴回填 structure.md / shotlist.md
```

**迭代上限**（沿用 CLAUDE.md § Iteration bounds）：单个门最多 3 轮。S1 三轮抽不出满意 hook → 停下改**歌词**或**曲风 prompt**，不要继续抽卡。

---

## S0 · 歌词净化（先做，5 分钟，省掉后面十次重抽）

AI 唱错字最常见的两个来源：**多音字**和**断句**。本首歌的雷点已逐条排出：

| 原句 | 风险 | 处理 |
|---|---|---|
| 塔门在身后合上 **只进不还** | 「还」正读 huán，模型八成唱成 hái | 改 **「只进不出」**（意思不变，零歧义） |
| **野草没过腰间** | 「没」正读 mò，模型必唱 méi | 改 **「野草漫过腰间」** |
| 我不做谁的**模样** | 正读 mú，易唱成 mó | 保留，但若唱错就在 Mureka 版取该句 |
| 十里坡上山神庙 **三更** | 正读 gēng，易唱 gèng | 保留（上下文强，实测多数正确）；备选写作「半夜三更」 |
| 婶娘一嗓子 把我从梦里**劈成两半** | 断句易被切成「劈成/两半」拖长 | 保留，靠 `[Verse]` 内换行控制 |

**净化后的两处硬改，写进送生成的歌词文本**（`theme_song.md` 的文学母版不动）：

```
塔门在身后合上 只进不出
密道漏下一线月光 野草漫过腰间
```

> 其余断句规则：**一行 = 一个乐句**，行内用空格分气口，**不要用逗号句号**（标点会被模型当停顿或读出来）。`theme_song.md` § Suno 两框直贴版 已按此规范排好，直接复制即可。

---

## S1 · 只抽副歌，先锁 hook（最关键的一步）

**全曲只有一个记忆点：「我以为逍遥…／原来逍遥…」。** 这四句立不住，后面全是白费。所以第一步不生成整首，只生成副歌区。

**Suno · Custom Mode**

Title
```
一生逍遥 - hook test
```

Lyrics 框（只填这一段，前后各留一个器乐标签让它有起落）
```
[Instrumental build: taiko roll, strings rising, 4 bars]

[Chorus]
我以为逍遥 是一剑挑开青冥的光
是一壶酒 换三千里路的斜阳
原来逍遥 是石门落下的那一响
是我拍碎了掌心 也喊不回的姑娘

烟尘里她还笑着 还是那样张狂
说你快走啊 别回头看这一场
落石砸成了雨 火光吞掉那身紫裳
最后是一只白蝶 掠过断墙

[Outro: strings decay]
```

Styles 框
```
soaring symphonic Chinese ballad chorus, xianxia film score, airy slightly husky female vocal with restrained crying tone, full string orchestra, driving taiko drums, pipa tremolo, erhu soaring counter-line, bamboo flute, pentatonic minor, 74 BPM, 4/4, huge cathartic climax, wide cinematic reverb, melancholic and heroic
```

Exclude Styles 框
```
edm, trap, autotune, dubstep, electric guitar, rap, lo-fi, synth pop, distorted bass, heavy metal, spoken word, chiptune
```

**门 1 判定（三问，全过才走 S2）**
1. 关掉画面只听，「原来逍遥」那一句有没有**往上顶**？（副歌必须比主歌高至少四度，平着走就是废卡）
2. 听完能不能哼出来？哼不出来 = 没 hook。
3. 「是我拍碎了掌心 也喊不回的姑娘」那句有没有**咬住**？这是全曲情绪最低点转最高点的枢纽。

抽 6–8 条，留 2 条。**三轮不过就回去改词或降 BPM 到 70**，别硬抽。

---

## S2 · 锁人声（Persona）

副歌选定后，用 Suno 的 **Persona / Cover** 功能把那条的人声固化，后续所有段落都挂同一个 Persona——这是保证 5 分钟里音色不漂移的唯一可靠手段。

**默认女声**（`theme_song.md` 已定：空灵微哑 + 克制哭腔）。

**男声 AB 版**（更贴逍遥第一人称，建议也做一条对照）：Styles 框把
```
airy slightly husky female vocal with restrained crying tone
```
换成
```
warm male tenor vocal, husky and weathered, restrained emotional delivery, slight vocal fry on sustained notes
```
并把调性从 `D pentatonic minor` 降到 `A pentatonic minor`。

> 门 2：**Persona 一旦选定，S3 之后不许再换**。换音色 = 前面所有抽卡作废。

---

## S3 · Suno 整首抽卡（×10）

直接用 `theme_song.md` § C「Suno 两框直贴版」的三框内容（记得套用 S0 的两处硬改），挂 S2 的 Persona，连抽 10 条。

**抽卡纪律**
- 每条只听三个位置：**00:00–00:20（前奏气质）、副歌1 首句、终副歌清唱转全奏**。这三处对了，中间基本不会太差。
- 不要边听边改 prompt。**十条抽完再统一评**——中途改参数会让样本没法横向比。
- 编号存盘：`_audio/candidates/suno_01.mp3` … `suno_10.mp3`。

---

## S4 · Mureka 平行抽卡（×8，与 S3 同时进行）

Mureka 走两条线：

### 线 A · 中文 prompt 直生（咬字对照组）

歌词框：同 S0 净化后的完整歌词。
风格描述框（中文，Mureka 对中文描述解析更好）：
```
中文古风悲情流行抒情曲，仙侠电影主题曲质感。女声空灵微哑，克制的哭腔，咬字温柔清晰。
编曲：竹笛+古筝+琵琶+二胡+弦乐群+钢琴；主歌稀疏亲密只留古筝与笛，副歌加大鼓与弦乐全奏爆发，桥段A鼓点渐入半唱，终副歌前四句仅钢琴清唱、后四句全奏收峰，尾奏笛声渐远伴风声。
速度 74 BPM，4/4 拍，五声小调。
情绪：从温暖少年感走向辽阔悲怆，最后释然余痛。
```
排除：
```
电子舞曲，说唱，电吉他，重金属，自动调音，Lo-Fi，合成器流行
```

### 线 B · 以曲生曲（把 Suno 骨架当参考音频）

等 S3 出结果后，挑 Suno 最好的 1–2 条上传到 Mureka 的**参考音频 / 参考歌曲**入口，配同一份歌词，让它**换配器重演**。用途有二：
1. Suno 版编曲太满时，Mureka 常给出更留白的版本，主歌段更好听；
2. 抽出一条**换人声但同旋律**的版本，做男女对唱的素材（终副歌可以女声起、男声接，情绪杀伤力翻倍）。

### 线 C · 纯器乐段（Mureka 的强项，专供四个器乐段）

四段器乐（前奏 18s / 间奏 22s / 尾奏 22s，以及副歌前的 build）单独生成，比从整首里剪更干净。开 **Instrumental / 纯音乐**模式：

**前奏（18s，暖·晨光·顽皮前的宁静）**
```
中国古风器乐前奏，独奏竹笛引入，古筝分解和弦铺底，极简，无鼓无人声，
清晨水乡的空气感，温暖明亮但带一丝隐约的怅惘，74 BPM，五声小调，18 秒，
结尾停在半终止不解决，留给人声进入
```

**间奏（22s，低回·十年·婴儿啼声混入）**
```
中国古风器乐间奏，二胡独奏悲歌，持续弦乐垫底，古筝泛音稀疏点缀，无打击乐，
72 BPM 自由速度，深沉悲怆，电影配乐质感，末尾渐弱留白，22 秒
```

**尾奏（22s，余韵·风雪·消散）**
```
中国古风器乐尾奏，独奏竹笛在弦乐长音上远去，风声环境音，无鼓，
极简，苦涩释然，逐渐溶解进寂静，72 BPM，22 秒
```

---

## S5 · 盲听评分 → 选骨架（门 3）

18 条候选（Suno 10 + Mureka 8）**去掉文件名盲听**，按下表打分，每项 0–10：

| # | 维度 | 判据 | 权重 |
|---|---|---|---|
| 1 | **Hook 记忆度** | 听完能否哼出「原来逍遥」那一句 | ×2 |
| 2 | 人声质感 | 有没有「人味」——气声、咬字轻重、哭腔是否克制不做作 | ×2 |
| 3 | 中文咬字 | 有无唱错字、吞字、洋腔洋调 | ×1 |
| 4 | 编曲层次 | 主歌是否够稀疏、副歌是否真的炸开（动态差 ≥ 12dB 观感） | ×1 |
| 5 | 情绪弧 | 暖 → 骤紧 → 悲恸 → 释然，四个拐点是否听得出来 | ×1 |
| 6 | 后半段不塌 | 副歌2 与终副歌的质量 vs 前半段 | ×1 |
| 7 | 收束 | 结尾是消散得漂亮，还是硬切/循环感 | ×1 |
| 8 | 仙剑味 | 笛/筝/二胡的中式色彩是否成立，有没有变成「泛亚洲风」 | ×1 |

**满分 80。门槛：总分 ≥ 55 且第 1 项 ≥ 8**（hook 不达标一票否决，不许靠其他项凑）。

选出 **1 条主骨架 + 2 条备件**（备件用来替换主骨架的坏段）。

---

## S6 · 精修（把「好听」做成「精彩」）

选中的骨架几乎不会 12 段全好。逐段过一遍，标出坏段，按下表处理：

| 症状 | 处理手段 |
|---|---|
| 某一段唱错字 / 情绪不对 | 从**备件**里剪同段替换（同 Persona 同 BPM，交叉淡化 0.3s 基本听不出） |
| 结尾收得仓促 | Suno **Extend**，只给 `[Outro: bamboo flute fading over wind, no vocals]`，续 20–30s 再剪 |
| 主歌编曲太满 | 用 Mureka 线 B 出的留白版替换主歌区 |
| 器乐段太短/太长 | 直接用 S4 线 C 单独生成的器乐段整段替换 |
| 整体混音闷/糊 | Suno **Remaster**（若可用），或 S7 分轨后自己修 |
| 终副歌清唱段没做出来 | 分轨后手动：把人声轨保留、伴奏轨在前四句压到 -20dB 只留钢琴，第五句全奏推回 |

**精修的判据不是「有没有瑕疵」，是「这一段有没有服务它对位的画面」**——对照 `structure.md` 全片对位表：副歌1 对的是塔崩月如断后（悲情第一峰），这一段如果听着不揪心，就是废段，必须换。

---

## S7 · 分轨 → 定长 → 母带

### 7.1 分轨
Suno / Mureka 会员均可导出 Stems（人声 / 鼓 / 贝斯 / 其他）。**务必导出**——后面 MV 混音要用：画面强奇观段（月下剑舞、塔崩、御剑）常需要单独压人声、放大器乐。

### 7.2 拼接与定长

段落拼接（交叉淡化 1s，避免硬切爆音）：
```bash
ffmpeg -i seg_a.wav -i seg_b.wav -filter_complex \
  "[0][1]acrossfade=d=1:c1=tri:c2=tri" -c:a pcm_s24le out_ab.wav
```

多段串联（把 12 段依次接起来，逐段两两 acrossfade 即可；或写进 concat 列表后统一处理）：
```bash
ffmpeg -f concat -safe 0 -i seglist.txt -c:a pcm_s24le theme_raw.wav
# seglist.txt 每行： file 'C:/workspace/spec_coding/ai_videos/xianjian_yi_mv/_audio/seg/01_intro.wav'
```

导出段落时间点（拼完之后查真实边界，用于回填 structure.md）：
```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 theme_raw.wav
```

### 7.3 母带
目标：**-14 LUFS 整体响度**（B站/YouTube 标准），峰值 -1 dBTP。副歌与主歌的响度差不要压死，留 ≥ 6 LU 的动态。

```bash
# 两遍 loudnorm（第一遍测量，第二遍套用），比单遍准得多
ffmpeg -i theme_raw.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null -
# 把上一步输出的 measured_* 填进来
ffmpeg -i theme_raw.wav -af \
  loudnorm=I=-14:TP=-1:LRA=11:measured_I=<M_I>:measured_TP=<M_TP>:measured_LRA=<M_LRA>:measured_thresh=<M_TH>:linear=true \
  -ar 48000 -c:a pcm_s24le theme_master.wav
ffmpeg -i theme_master.wav -c:a libmp3lame -b:a 320k theme_master.mp3
```

---

## S8 · 落盘 + 时间轴回填（不能跳过）

### 8.1 目录
```
ai_videos/xianjian_yi_mv/_audio/
├── candidates/   suno_01..10.mp3, mureka_01..08.mp3   （抽卡原始，留档）
├── seg/          01_intro.wav … 12_outro.wav          （精修后的分段）
├── stems/        vocal.wav, drums.wav, other.wav
└── master/       theme_master.wav, theme_master.mp3, sections.md
```

### 8.2 回填（**方向不可反**）

成品歌曲极少正好 320s。**以成品的真实时长为准**，反向修改 `structure.md` 和 `shotlist.md`：

1. 在 DAW 里逐段读出真实边界，写成 `_audio/master/sections.md`：

   | # | 段 | 真实起 | 真实止 | 时长 | 计划时长 | 差 |
   |---|---|---|---|---|---|---|
   | 1 | 前奏 | 00:00 | 00:16.8 | 16.8s | 18s | −1.2 |
   | … | | | | | | |

2. 差值 **≤ ±1.5s** → 段内最长的那一镜吸收，`shotlist.md` 不动结构。
3. 差值 **> ±1.5s** → 改 `structure.md` 对位表的时间轴列 + 该段镜数/单镜时长，并按 CLAUDE.md § Follow-up prompt handling 跑受影响范围的 `ai_videos__审查总编排`（重点 `ai_videos__时长节奏`）+ 追加 `specs/ai_video/xianjian_yi_mv/changelog.md`。
4. **副歌区（S 档：段6b 塔崩 / 段8b 决战）宁可加镜也不要拉长单镜**——密集短切是这两段的情绪机制，单镜超过 6s 就泄气。

### 8.3 合轨
成片视频出来后：
```bash
python tools/mux_av.py --video <ep_or_mv>.mp4 --audio _audio/master/theme_master.mp3
```

---

## 7. 常见失败模式与对策

| 失败模式 | 平台 | 根因 | 对策 |
|---|---|---|---|
| 后半段（3:30 之后）质量断崖 | Suno 尤甚 | 长上下文衰减 | 分段生成 + 拼接（S6），不要指望一次整首 |
| 副歌不炸，平着走 | 两者都有 | style prompt 没给动态指令 | Styles 加 `sparse intimate verses building to soaring orchestral choruses`、`huge cathartic climax`；主歌段 Exclude 里加 `drums` |
| 中文唱成洋腔 / 咬字含混 | Suno | 英文语料权重 | 走 Mureka 线 A 取该段；或歌词行内加空格拆气口 |
| 多音字唱错 | 两者都有 | 无上下文消歧 | S0 已排雷；仍错就换同义词，不要试图用标注纠正 |
| 器乐段被塞进人声 | 两者都有 | 器乐标签被当歌词提示 | 器乐段**单独生成**（S4 线 C），Instrumental 模式 |
| 音色中途漂移 | Suno | 未挂 Persona | S2 锁 Persona，全程不换 |
| 变成「泛亚洲风」（三味线/尺八味） | 两者都有 | 乐器写得太笼统 | 乐器必须点名：`guzheng`（不写 zither）、`dizi/bamboo flute`、`erhu`、`pipa`；Exclude 加 `shakuhachi, koto, shamisen, gamelan` |
| 结尾硬切或有循环感 | 两者都有 | 生成边界 | Extend 续 20–30s 再手动淡出 |
| 主歌鼓点太早进来 | Suno | 默认编曲惯性 | 主歌段 Exclude 框加 `drums, percussion` |

---

## 8. 抽卡预算参考

| 阶段 | 条数 | 说明 |
|---|---|---|
| S1 hook | 6–8 | 门 1 不过最多再来两轮 |
| S3 Suno 整首 | 10 | |
| S4 Mureka 线 A | 5 | 咬字对照 |
| S4 线 B 以曲生曲 | 3 | 等 S3 出结果后 |
| S4 线 C 器乐段 | 4 段 × 3 = 12 | 器乐便宜，多抽 |
| S6 精修补段 | 8–12 | 按坏段数定 |
| **合计** | **≈ 45–50 次** | 两个会员并行，半天到一天可完成 |

---

## 9. 与 MV 主线的衔接

- **歌不定稿，Seedance 不批量出镜。** 目前 `5_6_分镜与prompt/shots/` 已有 shot01–，这些是按计划 320s 轴排的；S8 回填后若时间轴变动 > ±1.5s，对应段的镜头需按 §8.2 调整。
- 歌定稿后，把 `_audio/master/sections.md` 的真实时间轴写回 `structure.md` 表头注释，并在 `specs/ai_video/xianjian_yi_mv/changelog.md` 记一条（含 9 项维度通过矩阵）。
- MV 混音阶段用 stems：奇观镜（月下剑舞 shot15–16、塔崩 shot25–31、御剑、决战）可短暂压低人声轨 3–5dB 放大器乐与音效，让画面的音效（剑鸣/落石/浪涌）有位置。

---

## 10. 版权

词曲全部原创，人声为 AI 生成，**歌曲本身零版权风险**。仙剑奇侠传 IP（软星/大宇）归权利人所有，本片为致敬向非商业二创，发布物须标注「AI 概念重制 / 致敬《仙剑奇侠传》」，且生成块内零真人演员名（沿用 `1_立项/concept.md` § 版权与人设策略）。商用前需取得 IP 授权。
