# t01_main_theme · 主题曲 · 7/4（凯尔特民谣 + 小编制管弦 + 无词女声）

> **status: draft（未批准）**——供试听；批准前不进 `finish_ep --bgm`、不进任何成片。**本卡即生成回执**（授权凭证），删卡＝丢证据；
> API 原样返回的响应头与 JSON 部分在 `t01_main_theme.response.json`。生成器 `tools/gen_music_szzl.py`（请求体由它产出，本卡由它写）。

| 字段 | 值 |
|---|---|
| status | draft（未批准） |
| provider | ElevenLabs · Eleven Music API（`POST /v1/music/detailed?output_format=mp3_44100_192`） |
| model_id | `music_v2_5` |
| plan | Pro |
| date | 2026-09-30（请求 2026-09-30T20:07:44+08:00，耗时 12.3 s） |
| seed | 20260930 |
| song-id | `xOrLk3uKxlz6w4tSdBdm` |
| request-id | `6bd6120f912c45e0a7884e92c395d90a`（x-trace-id） |
| 音频 | `t01_main_theme.mp3` · 44.1 kHz · 2 ch · 192 kbps · sha256 `53504e54f2b59de448e18486da2c1bcd3de545256e36bf521da8e7f9974cae04`（mp3 全局 gitignore，备份走 R2） |
| 时长 | 实测 **85.03 s**（计划 85 s = 17 小节 × 5 s） |
| 响度（原始，未归一） | 积分 **-13.4 LUFS** · 真峰值 **-1.3 dBTP** · LRA 12.0 LU |
| 成本估算 | 1.42 min × $0.15/min = **$0.21**（list 价；Pro 月包 660 min 内扣） |
| 请求的速度 / 拍号 / 调 | 84 BPM · 7/4（2+2+3）· D major（模型是否照做见「机检回读」） |

## 与立项的对应

- **E3 片头曲试 7/4**：本稿就是这次尝试——按 2+2+3 分组、84 BPM，一小节正好 5 s。耳听若数不齐 7 拍，按 E3 退 4/4、改下一稿的 plan，不在本稿上修。
- **F5 配乐语汇**：凯尔特民谣（竖琴 / 低音哨笛 / 小提琴 / 布祖基 / 宝思兰鼓）+ 小编制管弦（弦乐 + 圆号）+ 无词女声；请求里零作品名、零作曲家名（生成器禁用名单闸门）。
- **G9②**：本稿**不含**上行三音动机——动机只留给「学会新本事」那一刻（t02 供料），主题里先用掉就不稀罕了。
- **E5 BGM 走生成**：本稿即生成件。用途候选：S01 冷开场切黑后的片名卡 *JUST ENOUGH LIGHT*（style_guide §8）与片尾卡。

## 试听要点

- 段落起点 0 / 10 / 30 / 50 / 70 s（v2.5 硬执行段长）。数拍：跟着听到的拍子数，数到 7 回到强拍＝7/4，数到 4 或 8＝4/4。
- 听三件事：① 是不是 7 拍一循环（E3 成败）② 女声只有 a / u 元音、没有吐字 ③ 克制，不是史诗。

| 段 | section | 计划小节（按 84 BPM） |
|---|---|---|
| 0–10 s | Intro | 2 |
| 10–30 s | Theme A - low whistle | 4 |
| 30–50 s | Theme A - wordless voice | 4 |
| 50–70 s | Lift - small orchestra | 4 |
| 70–85 s | Outro | 3 |

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
    "text": "[Intro]\n{solo Celtic harp alone, a gentle fingerpicked ostinato in 7/4 meter, each bar grouped 2+2+3}\n{a soft low string drone underneath, quiet early-morning stillness}",
    "duration_ms": 10000,
    "positive_styles": [
     "Celtic folk",
     "small chamber orchestra",
     "gentle main title theme",
     "7/4 time signature",
     "84 BPM",
     "D major",
     "hopeful",
     "understated",
     "Celtic harp",
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
    "text": "[Theme A - low whistle]\n{low whistle states the main melody: simple, singable, mostly stepwise, gently arching}\n{harp ostinato continues, lightly strummed bouzouki, very soft bodhran on the first beat of each bar}",
    "duration_ms": 20000,
    "positive_styles": [
     "Celtic folk",
     "7/4 time signature",
     "low whistle melody",
     "bouzouki",
     "soft bodhran",
     "hopeful",
     "understated"
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
    "text": "[Theme A - wordless voice]\n{a soft, breathy solo female voice sings the melody without words, open vowels only}\n{fiddle adds a gentle countermelody, warm chamber strings enter underneath}\nAah... aah... aah...\nOoh... ooh... aah...",
    "duration_ms": 20000,
    "positive_styles": [
     "wordless female vocalise",
     "soft breathy solo female voice",
     "fiddle countermelody",
     "warm chamber strings",
     "7/4 time signature",
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
    "text": "[Lift - small orchestra]\n{the small orchestra lifts the theme: solo French horn and warm strings join the voice and the whistle}\n{fuller and hopeful, but restrained, no big drums, no epic climax}\nAah... aah... aah...",
    "duration_ms": 20000,
    "positive_styles": [
     "small chamber orchestra",
     "solo French horn",
     "warm strings",
     "wordless female vocalise",
     "hopeful swell",
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
    "text": "[Outro]\n{the texture thins back to Celtic harp and the wordless voice}\n{the last phrase settles on D major and rings out, quiet clean ending}\nOoh... aah...",
    "duration_ms": 15000,
    "positive_styles": [
     "Celtic harp",
     "wordless female vocalise",
     "gentle ending",
     "ring out",
     "understated",
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
 "seed": 20260930
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

> 方法：librosa（`.venv-post`）量拍点周期与和声变化周期，whisper medium.en（CPU）听有没有词。和声周期法先在合成的 7/4 与 4/4 素材上验过能分开（7/4 → 7 / 14 拍峰 0.63 / 0.70；4/4 → 4 / 8 拍峰 0.71 / 0.61）。**最终以耳听为准。**

| 项 | 请求 | 回读 | 判 |
|---|---|---|---|
| 时长 | 75–90 s | 85.03 s | ✅ |
| 调 | D major | D major（K-S 相关 0.97） | ✅ |
| 速度 | 84 BPM | 拍点间隔 ≈ 0.60 s ≈ **99.5 BPM**；84 BPM 的 0.714 s 在主体段（10–70 s）无峰 | ✗ 没照做 |
| 拍号 | 7/4（2+2+3） | 和声变化周期峰在 **8 / 16 拍**（4.8 s 0.30 · 9.6 s 0.26）；7 拍（4.2 s）0.21、14 拍无峰；拍点重音自相关也是 8 拍最高（0.37）、7 拍为负 → **倾向 4/4**（两种测法一致） | ⚠ 大概率没照做，耳听确认 |
| 无词女声 | 30 s 起 | whisper 只听到元音：30.0–60.0 s「ah」、60.0–84.2 s「mmm」 | ✅ |
| 可疑词 | — | 28.6–30.0 s 听成 "I'm not sure what to say."（逐词置信 0.07–0.38，avg_logprob −1.73）＝典型的乐声幻听 | ⚠ 试听这 1.4 s |
| 模型自报 | — | `song_metadata.languages = []`（plan 是我们写的，弱证据） | — |

**E3 下一步（未执行，本批只准两首）**：
- 耳听确认是 4/4 → 按 E3 原文「退 4/4，片头用别的方式建立辨识度」，本稿直接当 4/4 主题候选。
- 还想再试 7/4：两首都说明文字写拍号不管用。下一稿改用**音频锁拍号**：自己做一段原创 7/4 竖琴 ostinato（约 10 s），`POST /v1/music/upload` 拿 `song_id`（按时长计价，上传会过版权检测），放进第一段 `conditioning_ref` + `condition_strength: high`。

*(judgment call — 没发第三个请求：任务单写死「exactly two sketches」、合计 ≤ 3 min；拍号交给早上的耳朵和用户定。)*
