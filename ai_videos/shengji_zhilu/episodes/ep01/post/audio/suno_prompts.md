# EP1 配乐与环境声 · 当前执行（2026-10-22，follow-up 114–115）

## 实际进度

- 全集需求：六场。当前可混音画面只有集级粗剪 v9 的 s1–s4（87.25 秒），未经锁片批准；s5 缺 st9–st17 正式条，s6 四镜无正式条。后两场先准备声音素材与镜头入点，不拼空画面冒充全片。
- Suno 配乐：`suno/requests_v1.json` 是 Suno 唯一请求清单，含完整 prompt、幂等键和放置依据。登录已完成，M01、M02 各点击 Create 一次但无确认歌曲；M02 检测到验证码，队列持久暂停，尚无 Suno 音乐文件。M03–M06 尚未提交。
- 当前试听配乐：follow-up 115 要求环境声小一点并加入音乐，先以本地 ACE-Step 1.5 XL Turbo 做三条纯器乐候选，原文件与生成记录在 `acestep_20261022/`。它们是临时本地配乐，未经过 Suno API，也不是 Suno 产物。最新片为 `../trial/ep01_post_v8.mp4`，相对 v6 新增环境轨降低 8 dB；v7 是同样降低环境轨但无音乐的对照。
- 环境声：当前 API 没有纯环境声后端，使用已配置的本地 MOSS-SoundEffect-v2.0。当前清单为 `ambience_20261022/gen_v2.json`（v1 前两条近静音已排除，详情见 `rejections_v1.json`），每条 WAV 旁记录 prompt、种子、模型和 SHA256。它们不是 Suno 产物。
- 本页以下旧版方案保留作历史；旧 v4 已删除，旧时间表、手工下单方法与 Extend 建议不作为本轮执行依据。

## 六场安排

| 场 | 音乐与留白 | 环境声 | 时间依据 |
|---|---|---|---|
| s1 岗哨 | M01 竖琴、木笛，盘问时靠后；穿门抬眼开始抬起 | A01 细雨与拱门滴水；脚步、纸张和对白保留原条 | 0–28 秒 |
| s2 山谷 | M01 同主题展开为弦乐、圆号，景别突然宽阔 | A02 远风、疏鸟、远河，不把远景做近景 | 28–37.625 秒 |
| s3 求助 | 呼救先留原声；约 48 秒接 M02，有紧迫感但以伸手帮人为重 | A03 路东河水、湿叶；不追加呻吟 | 37.625–65.125 秒 |
| s4 修道院 | M03 65.125 秒抵达抬起，72.875 秒问路压低；不作结局终止 | A04 屋檐滴水、庭院微风，不继续下大雨 | 65.125–87.25 秒 |
| s5 武器厅 | M04 在 st4 祈求后、st6 光柱升起展开；st8 说话前退。M05 在收徒和教他求光时短回主题，其余长对白留空间 | A05 安静石厅底；施光声、门响等按正式条另定，不与源音重复 | 未剪；按镜头锚点，不填写伪精确片内秒数 |
| s6 葡萄园 | M06 稀疏低弦；匪徒说话低伏，Hale 名字出现时抽薄而不抢谜团 | A06 柳叶和近水；蹚水、坎上脚步待画面同步 | 无正式条；按镜头锚点 |

## 混音与验收

沿用 v5 的英文字幕、地点字卡与对白提高清晰度设置。新试做版本只更换声音，不改故事、镜头、切点和对白。环境声素材不足单场长时才作接缝处理，避免明显重复；配乐待实际下载后试听选段，不能把提示词中的结构当成已生成的音乐结构。

v8 实际音乐入点为 0–38.6 秒（晨雨与山谷）、48–64.8 秒（相助）、65.125–87.25 秒（修道院），38.6–48 秒音乐静音留白。音乐按实际对白时间窗再衰减 12 dB，淡入淡出与详细增益见 `../trial/post_v8.json`。提示词中的乐器、发展和情绪是创作意图，仍待试听确认。

v7/v8 总线目标改为 -16 LUFS，峰值目标 -2 dBTP；v8 回读 -16.0 LUFS / -1.9 dBTP，87.25 秒。画面视频流与 v6 哈希相同、字幕不变，独立音乐/环境轨及无损混音保存在 `../trial/stems_v8/`。原声分轨仍含同步声，非隔离对白。机器只检查文件、信号、时长和响度，音色、空间真实感、对白可懂度和情绪效果仍待试听；当前前四场候选不标为整集终混完成。

## API 续跑

登录已于 2026-10-22 完成，Pro 套餐确认。M01 `11bb141ca9164b79b88825820db8dc99`、M02 `7559bb5d429a420a8c9c55480aa3384f` 各点击 Create 一次后均为 `uncertain`；M02 的错误为 `challenge`。M01 查询时余额未变不等于确认未提交；M02 后不再查询配额或重试。M03–M06 未提交。

服务 `http://127.0.0.1:8770` 仍可查询，但 `/health` 为 `automation_paused=true`。人工处理 Suno 验证并完成 `login.ps1` 的普通窗口检查后，先在账号中核对 `suno-job-<job ID>` 标题；若存在歌曲，带真实 `song_urls` 调用原任务 `/resume`，只补收。不要把 `{}` 当作重新生成许可，不换键重建。

本次未执行任何官方下载。实际歌曲页有两个 More options 控件，下载 DOM 尚须校准。只有官方 WAV 下载成功并核对完整音频后，才继续余下四条。所有请求 target 指向本集；文件经 `/v1/jobs/{id}/files/{name}` 取回并保留 SHA256，试听选段后加入新版后期决定，不覆盖 v6 环境声候选，不自动把第一首当验收通过。新 Suno 页面另有 Sounds（effects/loops/one-shots），当前 API 未实现，该集环境声候选仍来自本地 MOSS。

---

# 历史方案（2026-10-19，已被上文执行清单取代）

# EP1 配乐 · Suno prompt（英文版后期用）

写于 2026-10-19，对应集级剪辑 v9（87.25 秒）与后期 v4（只有环境声）。

## 用法

- 在 Suno 网页用 **Custom** 模式：打开 **Instrumental**（纯音乐，不要人声），**Style of Music** 填下面的 Style，**Exclude styles** 填 Exclude。
- Lyrics 框可以只填段落标签（如 `[Intro]` `[Build]` `[Climax]` `[Outro]`）。纯音乐模式下 Suno 会参考这些标签安排结构，但不保证照做。
- 每条多生成几首，挑整体情绪对的那首就行，不用管长度：我会按下面的时间表剪进片子（截哪一段、从哪一秒开始、淡入淡出、台词下压低），所以选开头 20–40 秒最好听的即可。
- **商用条件**：要在 Pro / Premier 订阅期内生成并从 Suno 官方下载（最好是 WAV），不能用 Remix 出来的版本，不能去掉水印或元数据（见 `paid_services.md`）。
- Prompt 里没写游戏名和作曲家名：Suno 会拦截这类名字，模仿受版权保护的曲子也有风险。风格靠乐器和情绪去描述。
- 下载后放到 `ai_videos/shengji_zhilu/episodes/ep01/post/audio/suno/`，文件名按 cue 编号起，例如 `m1_elwynn_dawn_a.wav`，然后告诉我，我出 v5。

## 时间表（片内时间，秒）

| cue | 片内位置 | 画面 | 对白 | 要的感觉 |
|---|---|---|---|---|
| M1 | 0 – 28 | s1 森林岗哨，清晨小雨，守卫盘问亚伦 | 3.9 – 21.3 有对白 | 安静、田园、好奇，压在对白下面 |
| M2 | 27.3 – 约 40 | s2 亚伦抬头，北郡山谷全景展开（地名字卡 30.2 起） | 无 | 全片情绪最高点：开阔、惊叹、希望 |
| M3 | 42.6 – 65.1 | s3 河边大路，伤者呼救，亚伦搀他上路 | 43.6 – 63.3 几乎全是对白 | 紧张、急迫但克制 |
| M4 | 65.1 – 87.25 | s4 修道院立在眼前，修士指路（片尾） | 72.9 – 82.2 | 松一口气、庄重、带希望，片尾收住 |

M1 和 M2 最好是同一调性、同一主题，这样从岗哨到山谷像是一段音乐抬起来，而不是换了一首曲子。可以先做 M1，挑中后用 Suno 的 **Extend** 从结尾往后续写出 M2。条款明确说 Remix 不能商用，但 Extend 是否受同样限制我没有核实，用之前先看一下条款。也可以用下面的方案 B，一首曲子做到底。

---

## 方案 A：四段分开做

### M1 · Elwynn Dawn（岗哨晨雨）

- **Style**：
  `pastoral orchestral fantasy, gentle Celtic folk, solo wooden flute melody, soft harp arpeggios, warm sustained strings, distant french horn, quiet rainy dawn in a forest, calm, curious, slightly melancholic, sparse, underscore, 72 BPM, D major`
- **Exclude**：`vocals, choir, drums, percussion, electronic, synth, epic, trailer`
- **Lyrics（结构标签）**：
  ```
  [Intro: solo harp]
  [Verse: flute melody over soft strings]
  [Verse: horn answers the flute]
  [Outro: strings hold, fade]
  ```

### M2 · Northshire Reveal（山谷展开）

- **Style**：
  `majestic orchestral fantasy swell, soaring strings and french horns, harp glissando, soft wordless choir pad, gentle timpani roll, wonder and awe, a vast green valley revealed at sunrise, hopeful, cinematic adventure, 72 BPM, D major`
- **Exclude**：`vocals with lyrics, electronic, synth, rock drums, dubstep, trailer hits`
- **Lyrics（结构标签）**：
  ```
  [Intro: strings rise from silence]
  [Build: horns enter]
  [Climax: full orchestra, choir pad, timpani]
  [Outro: settles to warm strings]
  ```
- 片里只用 10–13 秒：从开始上扬的地方切进来，最高点对准山谷全景（约 31–36 秒），再自然收进 s3。

### M3 · Road Peril（路上的伤者）

- **Style**：
  `tense fantasy underscore, low tremolo strings, pulsing cellos and double basses, soft low frame drum, muted dark brass swells, sense of danger on a forest road, urgent but restrained, leaves room for dialogue, minor key, 96 BPM`
- **Exclude**：`vocals, choir, electronic, synth, rock, heavy percussion, horror stingers`
- **Lyrics（结构标签）**：
  ```
  [Intro: low string tremolo]
  [Verse: pulsing cellos, soft drum]
  [Build: brass swells, tension rises]
  [Outro: tension holds unresolved]
  ```

### M4 · Abbey Arrival（抵达修道院）

- **Style**：
  `solemn hopeful orchestral fantasy, warm low strings, gentle pipe organ, soft wordless choir pad, noble french horn theme slowly rising, relief and reverence, ancient stone abbey, peaceful resolution, 66 BPM, D major`
- **Exclude**：`vocals with lyrics, electronic, synth, drums, rock, epic trailer`
- **Lyrics（结构标签）**：
  ```
  [Intro: organ and low strings]
  [Verse: horn theme over choir pad]
  [Outro: final chord, gentle fade]
  ```
- 曲子的收尾要落在片尾 87 秒附近；挑结尾干净、有一个完整终止和弦的那首。

---

## 方案 B：一首做完整集（约 90 秒）

- **Style**：
  `cinematic orchestral fantasy score, pastoral Celtic opening with solo flute and harp, swelling to soaring strings and french horns, then a tense section of low tremolo strings and pulsing cellos, resolving into a solemn hopeful finale with organ and soft wordless choir, one recurring main theme, D major, 72 BPM`
- **Exclude**：`vocals with lyrics, electronic, synth, rock drums, dubstep, trailer hits`
- **Lyrics（结构标签，按片内时间排）**：
  ```
  [Intro: solo harp, gentle rain mood]
  [Verse: flute melody, soft strings, quiet]
  [Build: strings rise]
  [Climax: full orchestra, horns, choir pad — valley revealed]
  [Break: low tremolo strings, tense pulse]
  [Bridge: urgent cellos, dark brass]
  [Outro: organ and choir, hopeful resolution, final chord]
  ```
- 一首曲子各段的时长不一定和片子对得上，所以我可能会在段落之间剪几刀、加交叉淡化。方案 A 更好控制，方案 B 主题更统一。

---

## 以后：主题曲 / 片尾曲

需要带人声的版本时，可以用同一个主题（D 大调、长笛加圆号的旋律），在 Suno 里关掉 Instrumental、写歌词；或者交给本地 ACE-Step 1.5（MIT 许可，模型已下载）生成。
