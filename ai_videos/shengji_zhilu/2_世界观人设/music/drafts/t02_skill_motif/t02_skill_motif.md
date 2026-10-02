# t02_skill_motif · 变奏 · 上行三音动机（「学会新本事」sting 取材）

> **status: draft（未批准）**——供试听；批准前不进 `finish_ep --bgm`、不进任何成片。**本卡即生成回执**（授权凭证），删卡＝丢证据；
> API 原样返回的响应头与 JSON 部分在 `t02_skill_motif.response.json`。生成器 `tools/gen_music_szzl.py`（请求体由它产出，本卡由它写）。

| 字段 | 值 |
|---|---|
| status | draft（未批准） |
| provider | ElevenLabs · Eleven Music API（`POST /v1/music/detailed?output_format=mp3_44100_192`） |
| model_id | `music_v2_5` |
| plan | Pro |
| date | 2026-09-30（请求 2026-09-30T20:08:01+08:00，耗时 12.6 s） |
| seed | 20260931 |
| song-id | `Ko2WUBiq9BpoenVGw8jF` |
| request-id | `50a95c56a8237c715df75c01b8faa189`（x-trace-id） |
| 音频 | `t02_skill_motif.mp3` · 44.1 kHz · 2 ch · 192 kbps · sha256 `16ade398e964c90edb44591478690a7d75dc1bdbcfcd395818720a9cd41afba0`（mp3 全局 gitignore，备份走 R2） |
| 时长 | 实测 **80.04 s**（计划 80 s = 16 小节 × 5 s） |
| 响度（原始，未归一） | 积分 **-17.4 LUFS** · 真峰值 **-2.8 dBTP** · LRA 10.8 LU |
| 成本估算 | 1.33 min × $0.15/min = **$0.20**（list 价；Pro 月包 660 min 内扣） |
| 请求的速度 / 拍号 / 调 | 84 BPM · 7/4（2+2+3）· D major（模型是否照做见「机检回读」） |

## 与立项的对应

- **G9② 上行三音动机**：D–E–A（1–2–5），末音延长；只进配乐层、只在「学会新本事」那一刻响（style_guide §9：ep01 S08、S14 各一次）。
- 计划中五次陈述：0 s 竖琴 + 钢片琴（裸奏）· 10 s 小提琴起句 · 30 s 无词女声 + 竖琴 + 钢片琴（裸奏）· 40 s 圆号 · 60 s 低音哨笛；截 sting 首选 0–4 s 与 30–34 s 两处裸奏。
- **E7 → G9②**：旧「升级音做成上行三音和弦」已改为配乐层动机、没有升级音效——本稿只作配乐素材，不当音效用。
- 当垫乐用时必须剪掉动机段（动机只在学会新本事时响）；计划与 t01 同调同速（D 大调 · 84 BPM · 7/4）以便互拼——模型实际给的速度见「机检回读」。

## 试听要点

- 听 0 / 10 / 30 / 40 / 60 s 五处有没有清楚的上行三音（任务单要求 ≥ 2 次清楚陈述）；记下最干净的一处，截 sting 用。
- 同样核：7 拍一循环、女声无吐字、克制。

| 段 | section | 计划小节（按 84 BPM） |
|---|---|---|
| 0–10 s | Motif - harp | 2 |
| 10–30 s | Theme variation - fiddle | 4 |
| 30–40 s | Motif - wordless voice | 2 |
| 40–60 s | Development - French horn | 4 |
| 60–80 s | Motif - final statement | 4 |

## 许可（Eleven Music · self-serve 计划，2026-09-30 取原文）

- Eleven Music Model-Specific Terms：Starter / Creator / **Pro** / Scale ＝ "All online and offline commercial use permitted, except film, TV, radio, & Studio Games"；Pro 有 streaming rights；付费档不要求署名。本剧主平台 YouTube 长视频属在线使用 ✅；将来上电视 / 电台 / 院线 / 游戏须另谈 Enterprise。
- 输出**不独占**（ToS："the Output … may not be unique across users"）→ **永不登记 YouTube Content ID 或任何指纹认领系统**。
- Music Terms 禁在 prompt 里写艺人 / 作曲家名、曲名、专辑名、厂牌名：生成器禁用名单闸门已拦（另加游戏 / 影视 / 厂商名，concept F5）。
- 与 concept F2（前 10–20 集非商业）/ E6（同人姿态）不冲突；本曲全原创、零魔兽原声（F5）。

## 生成请求（原样，不含 key）

*(judgment call — 不开 `force_instrumental`：它会连无词女声一起去掉（F5 要女声）；「无词」改由生成器闸门保证——唱的行只许元音音节。
不开 `store_for_inpainting` / `sign_with_c2pa`：计划档限制不明，一次失败就吃掉仅有的一次重试额度。)*

```json
{
 "composition_plan": {
  "chunks": [
   {
    "text": "[Motif - harp]\n{near silence over a soft held low string note}\n{solo Celtic harp doubled by glockenspiel plays a short rising three-note motif: D, then E, then a long held A}\n{a soft string chord answers, then stillness}",
    "duration_ms": 10000,
    "positive_styles": [
     "Celtic folk",
     "small chamber orchestra",
     "rising three-note motif",
     "clear exposed melodic statement",
     "7/4 time signature",
     "84 BPM",
     "D major",
     "hopeful",
     "understated",
     "Celtic harp",
     "glockenspiel",
     "warm intimate acoustic recording",
     "great production quality"
    ],
    "negative_styles": [
     "lyrics with words",
     "spoken word",
     "rap",
     "male vocals",
     "choir",
     "operatic vibrato",
     "epic trailer music",
     "heavy percussion",
     "drum kit",
     "electronic beats",
     "synthesizer",
     "electric guitar",
     "bagpipes",
     "East Asian instruments",
     "brass fanfare",
     "4/4 time signature"
    ]
   },
   {
    "text": "[Theme variation - fiddle]\n{a gentle groove begins in 7/4 meter, each bar grouped 2+2+3: harp ostinato, lightly strummed bouzouki, very soft bodhran}\n{fiddle plays a variation of the main theme that opens with the same rising three-note motif}",
    "duration_ms": 20000,
    "positive_styles": [
     "Celtic folk",
     "7/4 time signature",
     "fiddle melody",
     "bouzouki",
     "soft bodhran",
     "rising three-note motif",
     "hopeful"
    ],
    "negative_styles": [
     "lyrics with words",
     "spoken word",
     "rap",
     "male vocals",
     "choir",
     "operatic vibrato",
     "epic trailer music",
     "heavy percussion",
     "drum kit",
     "electronic beats",
     "synthesizer",
     "electric guitar",
     "bagpipes",
     "East Asian instruments",
     "brass fanfare",
     "4/4 time signature"
    ]
   },
   {
    "text": "[Motif - wordless voice]\n{everything drops out except one held string chord}\n{a soft solo female voice sings the rising three-note motif without words, doubled by harp and celesta, the last note held}\nAh... ah... aah...",
    "duration_ms": 10000,
    "positive_styles": [
     "exposed rising three-note motif",
     "wordless female vocalise",
     "Celtic harp",
     "celesta",
     "held string chord",
     "hushed",
     "7/4 time signature"
    ],
    "negative_styles": [
     "lyrics with words",
     "spoken word",
     "rap",
     "male vocals",
     "choir",
     "operatic vibrato",
     "epic trailer music",
     "heavy percussion",
     "drum kit",
     "electronic beats",
     "synthesizer",
     "electric guitar",
     "bagpipes",
     "East Asian instruments",
     "brass fanfare",
     "4/4 time signature"
    ]
   },
   {
    "text": "[Development - French horn]\n{solo French horn states the rising three-note motif, then warm strings and low whistle develop the theme}\n{hopeful and warm, restrained, no big drums}",
    "duration_ms": 20000,
    "positive_styles": [
     "solo French horn",
     "rising three-note motif",
     "warm strings",
     "low whistle",
     "small chamber orchestra",
     "hopeful",
     "restrained",
     "7/4 time signature"
    ],
    "negative_styles": [
     "lyrics with words",
     "spoken word",
     "rap",
     "male vocals",
     "choir",
     "operatic vibrato",
     "epic trailer music",
     "heavy percussion",
     "drum kit",
     "electronic beats",
     "synthesizer",
     "electric guitar",
     "bagpipes",
     "East Asian instruments",
     "brass fanfare",
     "4/4 time signature"
    ]
   },
   {
    "text": "[Motif - final statement]\n{the texture thins; low whistle plays the rising three-note motif one last time, answered by harp}\n{the last note is held over a soft D major chord and rings out, quiet clean ending}\nAah...",
    "duration_ms": 20000,
    "positive_styles": [
     "low whistle",
     "Celtic harp",
     "rising three-note motif",
     "wordless female vocalise",
     "gentle ending",
     "ring out",
     "7/4 time signature"
    ],
    "negative_styles": [
     "lyrics with words",
     "spoken word",
     "rap",
     "male vocals",
     "choir",
     "operatic vibrato",
     "epic trailer music",
     "heavy percussion",
     "drum kit",
     "electronic beats",
     "synthesizer",
     "electric guitar",
     "bagpipes",
     "East Asian instruments",
     "brass fanfare",
     "4/4 time signature"
    ]
   }
  ]
 },
 "model_id": "music_v2_5",
 "seed": 20260931
}
```

## 模型返回的 song_metadata

```json
{
 "title": null,
 "description": null,
 "genres": [],
 "languages": [],
 "is_explicit": null
}
```

## 机检回读（启发式，非闸门；2026-09-30 手工跑，脚本未入库）

> 方法同 t01（librosa 拍点 / 和声周期 / pyin 旋律音高，高通 220 Hz 去掉 D3 持续低音；whisper medium.en）。**最终以耳听为准。**

| 项 | 请求 | 回读 | 判 |
|---|---|---|---|
| 时长 | 75–90 s | 80.04 s | ✅ |
| 调 | D major | D major（K-S 0.92） | ✅ |
| 速度 | 84 BPM | 拍点 ≈ 0.545 s ≈ **110 BPM**（八分音符 0.27 s 很清楚）；和 t01（≈ 99.5）也不同速，互拼要变速 | ✗ |
| 拍号 | 7/4 | 和声变化周期峰在 **16 拍**（8.7 s 0.33）与 4 拍（2.2 s 0.26）；7 拍（3.8 s）无峰 → **倾向 4/4** | ⚠ 耳听确认 |
| 上行三音 ≥ 2 次 | D–E–A（1–2–5），末音延长 | pyin 找到的上行三音：**≈ 32.9 s 与 ≈ 35.1 s D4→F♯4→G4**（无词女声段）、**≈ 61.1 s D4→F♯4→G4**（尾段）；≈ 30.0–31.1 s 有 D4→G4→A4 轮廓（中间夹一个 D4）；0–10 s 竖琴段只测到 D4 / A3 交替，**没有清楚的三音上行** | ⚠ 形状对（上行三音、≥ 2 次），音不对（1–3–4 不是 1–2–5）；耳听定 |
| 无词女声 | 30–40 s、60 s 后 | whisper：34.0–43.6 s「oh oh oh oh」、61.9–66.8 s「oh oh oh」、71.3–72.7 s「ooh」 | ✅ |
| 可疑词 | — | 5.3–6.7 s 听成 "you"（置信 0.01）＝幻听 | ⚠ 顺耳听一下 |

**sting 截取候选**（按回读排，耳听定）：① 32.9–35 s（女声 + 竖琴；计划里该段底下只留一个弦乐长和弦）② 61.1–63.5 s（尾段，末音 F♯4 延长约 0.9 s）③ 0–4 s 竖琴开头——回读不像计划那样清楚，排最后。

- 音高是 D4→F♯4→G4（1–3–4），不是计划的 D–E–A：用户若坚持 1–2–5，下一稿走 t01 卡里写的「音频锁」路线（这次锁动机），或后期自己合成 / 录这三个音。

*(judgment call — 没为「音不对」重发请求：任务单要的是「清楚地陈述 ≥ 2 次上行三音」，回读形状满足；具体音高交给早上试听。)*
