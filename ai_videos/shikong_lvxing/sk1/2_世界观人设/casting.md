# 配音 casting 表 · sk1（旅行者声音锁定）

> sk1 是**游览 vlog**（用户 2026-09-14）：**全片只有旅行者开口**——对镜头说，或画外内心独白；当地人一律不开口、不接受采访，只用动作与表情；群声是没有可辨字句的环境声。
> **2026-09-15 起（系列 follow-up 012）**：① 旅行者从系列名册 `_series/characters/c1–c6` 里选（3 位说普通话、3 位说英语），**默认 c1 林问**；用户挑定后 `python tools/gen_shots_sk1.py --traveller cN` 重跑整站。② **她的台词由视频直接出声**——有台词的镜带 `声音:` 行（系列卡「声音锁定串」逐字）+ `参考:` 挂 `{名}声音(cN-2 声样)`；TTS voice_id 只用于补录与另一语种译配。③ 本站不再放旅行者卡（导入会撞键），本地沉默面孔键从 c21 起。
> 与生成器逐字一致：voice_id、声线、声音锁定串都由 `tools/gen_shots_sk1.py` 从系列卡读（卡由 `tools/gen_traveller_cards.py` 生成），本表只登记。
> 路径：人物 / 道具 / 场景行相对 `sk1/2_世界观人设/`；系列卡行相对 `ai_videos/shikong_lvxing/`。

## 发声角色：旅行者候选（一站只选一位）

| 键 | 旅行者 | 视频里说 | 视频原声 voice_id（补录用） | 译配 voice_id | 声线 |
|---|---|---|---|---|---|
| c1（默认） | 林问（Lin Wen） | 普通话 | `zh-f-vlogger-linwen-01` | `en-f-vlogger-linwen-01` | 二十九岁女声，明亮温暖的中音、带笑意，语速偏快、字字清楚，爽快不嗲 |
| c2 | 周野（Zhou Ye） | 普通话 | `zh-f-vlogger-zhouye-01` | `en-f-vlogger-zhouye-01` | 二十七岁女声，清亮偏高、脆，语速快，带一点西南口音的软尾音，笑声爽朗 |
| c3 | 许棠（Xu Tang） | 普通话 | `zh-f-vlogger-xutang-01` | `en-f-vlogger-xutang-01` | 三十一岁女声，温柔女中音带轻微沙哑气声，语速偏慢、爱停顿，江南口音的软尾音 |
| c4 | 艾拉（Ella Hart） | 英语 | `en-f-vlogger-ella-01` | `zh-f-vlogger-ella-01` | late-twenties British female, light West Country accent, bright mid-high register, fast, upward endings, self-deprecating |
| c5 | 妮娅（Nia Brooks） | 英语 | `en-f-vlogger-nia-01` | `zh-f-vlogger-nia-01` | thirty, American female, warm rich low-mid register, light Southern drawl, rhythmic, big laugh |
| c6 | 露西娅（Lucía Vega） | 英语 | `en-f-vlogger-lucia-01` | `zh-f-vlogger-lucia-01` | late-twenties Spanish female speaking English, clear Spanish accent, warm slightly grainy mid register, fast and expressive |

> 声音本体以各卡「声音锁定串」为准（音高、语速、口音、笑声都写在那里）；上表声线是短描述。

## 不开口的人（无 voice_id，不登记音色）

| 角色 | 处理 |
|---|---|
| c21 李十六 / c22 周四娘 / c23 沈十九 | 可选的沉默复现面孔：有视觉卡与参考图，**无 voice_id**；入画镜的 `台词:` 不写他们、不出配音块、不对口型、不看镜头 |
| 其余当地人 / 群像 | 不建发声卡（旧的一次性发声角色 c5–c13 作废）；群声只进环境声层，**没有可辨字句**，不走 TTS |

## 铁律

1. **一位旅行者一条声音锁定串 + 一对 id，全站不换**：换装（现代装 ↔ 宋装）不换声，不同镜只改情绪与语速。
2. **视频直接出声**：对镜句对口型；画外句（OS）嘴不动、声音照出——OS 镜同样必须有声，不能当默剧交付。`## 台词配音 prompt` 不是默认产物：视频语种那一块只在成片人声漂移时补录；另一语种那一块做整轨译配（先人声分离去掉原声、保留环境音，再用 `tools/mux_av.py` 叠译配轨）。
3. **当地人永不发声**：没有 voice_id 的人不得出现在任何 `台词:` 行或配音块里；群声不写成可读的话，连喊词也不写（写「桥上一片喊声」，不写「放桅——」）。
4. **双向一致**：系列卡「配音参考」「声音锁定串」↔ 本表 ↔ 生成器；c21–c23 卡的「配音参考」写「本片不开口·无 voice_id」。

## 旅行者的脸：Seedance 人物 entity

- 脸不走选角库，走用户用系列卡建立的 **Seedance 人物 entity**（`specs/ai_video/sk1/divergence.md` #6）。脸源是选中那位的 `_series/characters/cN_{名}/cN-1.png`（立绘）+ `cN-2.mp4`（4 s 建立视频，带声样）；shot prompt 一律不写五官。
- **两个装束状态，同一张脸、同一个声音**：
  - **现代装**——系列卡 `cN-1` / `cN-2`（每位候选有自己的一套现代装）。
  - **宋装**——系列卡「站点装束变体 · sk1」的 `cN-11`（宋装立绘，挂 `cN-1` 定脸 + `props/p11_旅行者宋装/p11-1.png` 定衣服）与 `cN-12`（宋装 4 s 建立视频，带声样）。
- 换装发生在客店（bg7-2）；换装前的镜挂现代装状态，换装后的镜挂宋装状态。
- **挑人顺序**：先出 6 张 `cN-1` 立绘给用户挑 → 选定后只给那一位出 `cN-2` / `cN-11` / `cN-12`，并重跑生成器。

## 参考图清单

> 落盘只用路由键命名（rule 4b-A）；中文视图名住在各自卡里，不进文件名。**必做**＝出片前必须有；**可选**＝新大纲用到才出。

### 人物

| 文件 | 出处 | 状态 |
|---|---|---|
| `_series/characters/cN_{名}/cN-1.png` | 旅行者现代装立绘（脸的唯一标准）；**6 位候选各一张，先出这 6 张给用户挑** | 必做（最先出） |
| `_series/characters/cN_{名}/cN-2.mp4` | 选中那位的现代装 4 s 建立视频（带声样；抽帧落 `views/`） | 选定后必做 |
| `_series/characters/cN_{名}/cN-11.png` | 选中那位的 sk1 宋装立绘（挂 `cN-1` + `p11-1`） | 选定后必做 |
| `_series/characters/cN_{名}/cN-12.mp4` | 选中那位的 sk1 宋装 4 s 建立视频（带声样） | 选定后必做 |
| `characters/c21_李十六/c21-1.png` · `c21-2.mp4` | 立绘 + 4 s 建立视频（全程闭嘴） | 可选 |
| `characters/c22_周四娘/c22-1.png` · `c22-2.mp4` | 立绘 + 4 s 建立视频（全程闭嘴） | 可选 |
| `characters/c23_沈十九/c23-1.png` · `c23-2.mp4` | 立绘 + 4 s 建立视频（全程闭嘴） | 可选 |

### 道具与建筑单体

| 文件 | 出处 | 状态 |
|---|---|---|
| `props/p1_旋煎羊白肠与食摊/p1-1.png` | 州桥夜市食摊锚点 | 必做 |
| `props/p2_铜钱与钱串/p2-1.png` | 铜钱与钱串锚点 | 必做 |
| `props/p3_三件不变物/p3-1.png` | 话筒 / 采访本 / 铜片 / 胸牌平铺锚点（零参考） | 必做 |
| `props/p4_饮子摊/p4-1.png` | 汤茶药饮子摊锚点 | 必做 |
| `props/p6_太平车与独轮车/p6-1.png` · `p6-2.png` | 太平车与串车 / 平头车运酒梢桶（`p6-2` 挂 `p6-1`） | 必做 |
| `props/p7_彩楼欢门与招牌/p7-1.png` | 彩楼欢门锚点 | 必做 |
| `props/p8_虹桥单体/p8-1.png` · `p8-2.png` · `p8-3.png` · `p8-4.png` | 锚点 + 正面 / 侧面 / 俯视（image-to-3D 白模用） | 建城前必做 |
| `props/p9_桥尾脚店单元/p9-1.png` · `p9-2.png` · `p9-3.png` · `p9-4.png` | 同上 | 建城前必做 |
| `props/p10_沿河民居单元/p10-1.png` · `p10-2.png` · `p10-3.png` · `p10-4.png` | 同上 | 建城前必做 |
| `props/p11_旅行者宋装/p11-1.png` | 旅行者宋装实物锚点（一桁一凳七件；六位候选共用，宋装立绘之前出） | 选定后必做 |

> 判断：`p5` 是空号。阶段 2 立卡时没有用这个编号；路由键一经发出就不重排（重排会让已下载的图对不上目录），所以保留空号。

### 场景主体

| 文件 | 出处 | 状态 |
|---|---|---|
| `scenes/bianjing/bg1_虹桥/bg1-1.png` | 虹桥地点锚点（挂世界锚点 `bg0-1` + 两张北宋原本局部） | 必做（`bg0-1` 之后） |
| `scenes/bianjing/bg2_东水门城门/bg2-1.png` | 东水门锚点 | 必做 |
| `scenes/bianjing/bg3_汴河码头/bg3-1.png` | 汴河码头锚点 | 必做 |
| `scenes/bianjing/bg4_州桥御街/bg4-1.png` | 州桥御街锚点 | 必做 |
| `scenes/bianjing/bg5_正店酒楼/bg5-1.png` | 正店门首锚点 | 必做 |
| `scenes/bianjing/bg6_瓦子勾栏/bg6-1.png` | 瓦子勾栏锚点 | 必做（用户 2026-09-14 点名瓦子） |
| `scenes/bianjing/bg7_坊巷民居/bg7-1.png` · `bg7-2.png` | 坊巷外观 / 客店房间内景（`bg7-2` 挂 `bg7-1`） | 必做 |
| `scenes/bianjing/bg8_郊外清明踏青路/bg8-1.png` | 踏青路锚点 | 必做 |
| `scenes/bianjing/bg9_今日州桥遗址/bg9-1.png` | 今天的开封州桥考古遗址（现代；不挂世界锚点） | 可选实验 |
| `scenes/bianjing/bg0_汴京全城/bg0-1.png` · `bg0-2.png` | **世界锚点**（`bg0-1`，最先出；只挂历史参考图）· 全城斜俯瞰（S02）/ 汴河低空迎虹桥（S01 首帧）；几何由 `bianjing.blend` 航拍白模给 | 必做 |
| `scenes/bianjing/bg10_赵太丞家/bg10-1.png` · `bg10-2.png` | 赵太丞家门面（匾与立招不出字，后期加）/ 铺内看诊 | 必做 |
| `scenes/bianjing/bg11_开封府/bg11-1.png` · `bg11-2.png` | 开封府府门 / 院内正厅（⚠️ 类比宋代州府格局） | 必做 |
| `scenes/bianjing/bg12_宣德楼/bg12-1.png` · `bg12-2.png` | 宣德楼正面（绿琉璃瓦、朱漆金钉，唯一例外）/ 宣德门内大庆殿殿庭 | 必做 |
| `scenes/bianjing/bg13_相国寺/bg13-1.png` · `bg13-2.png` | 相国寺东门书铺街 / 资圣门前书画市 | 必做 |
| `scenes/bianjing/bg14_客店房间夜/bg14-1.png` · `bg14-2.png` | 客房三更油灯 / 五更天光（挂 `bg7-2`） | 必做 |
| `scenes/bianjing/bg15_园林雅集/bg15-1.png` | 园池边文士雅集（S23） | 必做 |
| `scenes/bianjing/bg16_汴京全城五更/bg16-1.png` | 全城五更天亮（S36，与 bg0-1 同机位） | 必做 |
| `scenes/bianjing/bg17_州桥夜市/bg17-1.png` · `bg17-2.png` | 州桥南望夜市 / 包子与羊白肠摊面（S30） | 必做 |

> 2026-09-14 更新：医馆（bg10）、开封府（bg11）、宣德楼（bg12）、相国寺（bg13）、园林雅集（bg15）、全城航拍（bg0 / bg16）、客房夜态（bg14）、州桥夜市（bg17）的场景卡均已建成，上表已补齐。**出图顺序**：先 `bg0-1` 世界锚点（2026-09-14 由 `bg1-1` 改，follow-up 003），再各场景锚点，最后派生视图与时间态（时间态挂母主体锚点）。
