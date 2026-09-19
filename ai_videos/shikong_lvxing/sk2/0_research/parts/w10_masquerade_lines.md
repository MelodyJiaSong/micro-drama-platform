---
worker_id: parent-w10-masquerade-lines
stage: 0
role: researcher
angle: masquerade-lines
status: partial
blockers:
  - "本文只登记 parent 本次亲自核到的逐字台词（来源：warcraft.wiki.gg 的 The Great Masquerade 原始 wikitext）。全场台词的完整集合须在阶段 4 写剧本前再跑一遍 raw wikitext 逐句补全，并按 I-7 新口径逐句配 source_url + quote。"
confidence: medium
---

# W10 · 《假面舞会》当庭台词（逐字原文）

> **用途**：系列 follow-up 014 把虚拟城站的 I-7 改为「**有逐字原文才能开口**」。本文登记本站唯一允许开口的当地人台词——**每句都必须是作品内逐字原文，一个字不得自编**。
> **`tag` 只能是 ✅**：有原文才有这条 fact，**没有 ⚠️ 档——推测出来的台词不存在**。
> **配套**：开口的 NPC 按 `ai_video.md` rule 12.4-H 建 `voice_id`，同一角色全剧复用一个。
> **旅行者形态不变**：艾拉仍是对镜 ≤ 40% + 画外 ≥ 60%、一路边走边讲；**她不和当地人对话**——他们在演他们自己的戏。
> **来源**：`https://warcraft.wiki.gg/index.php?title=The_Great_Masquerade&action=raw`（原始 wikitext；渲染页读不到这些引文，见 `_series/sources.md` §8.3）。

## 事实注册表

```yaml
- fact_id: stormwind.line.001
  claim: 温德索尔在王座厅当庭揭穿普瑞斯托女士的真身，这是全场的核心台词
  tag: ✅
  source: Warcraft Wiki — The Great Masquerade（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=The_Great_Masquerade&action=raw
  quote: "The masquerade is over, Lady Prestor. Or should I call you by your true name...Onyxia..."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "温德索尔立于王座厅中线，面朝王座右侧的贵族女性，抬手指向她；全厅目光随之转向"
  negative: "自编的 NPC 台词, 无出处的对白, 路人对口型, 旅行者与当地人对话"
- fact_id: stormwind.line.002
  claim: 温德索尔进城时对同行者的提醒——点明她会反抗
  tag: ✅
  source: Warcraft Wiki — The Great Masquerade（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=The_Great_Masquerade&action=raw
  quote: "On guard, friend. The lady dragon will not give in without a fight."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "温德索尔在街心停步侧头，对身侧同行者低声说话，脚步未停多久即继续前行"
  negative: "自编的 NPC 台词, 无出处的对白, 路人对口型"
- fact_id: stormwind.line.003
  claim: 温德索尔宣告此行的来由，回指卡拉赞的旧事
  tag: ✅
  source: Warcraft Wiki — The Great Masquerade（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=The_Great_Masquerade&action=raw
  quote: "As was fated a lifetime ago in Karazhan, monster - I come - and with me I bring justice."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "温德索尔正面朝前，全身板甲，步伐不停，声音压过街市的环境声"
  negative: "自编的 NPC 台词, 无出处的对白, 路人对口型"
- fact_id: stormwind.line.004
  claim: 现真身前后温德索尔对同行者的两句警示与最后的呼喊
  tag: ✅
  source: Warcraft Wiki — The Great Masquerade（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=The_Great_Masquerade&action=raw
  quote: "Be brave, friends. The reptile will thrash wildly. It is an act of desperation." / "You will not escape your fate, Onyxia." / "DO NOT LET HER ESCAPE!"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "王座厅内温德索尔转身面向厅门方向抬臂呼喊；厅内人影向两侧散开"
  negative: "自编的 NPC 台词, 无出处的对白, 路人对口型"
- fact_id: stormwind.line.005
  claim: 普瑞斯托的反应链——先令卫兵拿下他，再宣告将以叛国罪审判处决
  tag: ✅
  source: Warcraft Wiki — The Great Masquerade（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=The_Great_Masquerade&action=raw
  quote: "She initially orders guards to seize Windsor... She declares he'll be tried for treason and executed."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "王座右侧的贵族女性抬手示意，两名披甲卫兵自两侧上前；她下颌微抬、目光平视前方"
  negative: "自编的 NPC 台词, 无出处的对白, 她先动手, 她慌乱后退"
- fact_id: stormwind.line.006
  claim: 王座厅事件链——安杜因逃向安全处；皇家卫队现出龙人原形；伯瓦尔的徽章碎裂；温德索尔被普瑞斯托以爪重创后，向伯瓦尔道歉而死，她随即传送离开
  tag: ✅
  source: Warcraft Wiki — The Great Masquerade（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=The_Great_Masquerade&action=raw
  quote: "Anduin Wrynn flees to safety. Royal guards reveal themselves as dragonspawn. Combat erupts. Bolvar's medallion shatters. Windsor dies after apologizing to Bolvar."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "台基上的男孩自座上起身向侧门跑去；厅内数名披甲卫兵的轮廓变形拉长；伯瓦尔胸前一枚徽章裂开"
  negative: "血迹, 伤口特写, 尸体特写, 断肢, 近景搏斗, 旅行者参战, 旅行者被卷入"
- fact_id: stormwind.line.007
  claim: 温德索尔护送路线：自暴风城城门起步，穿城至暴风要塞入口，再入王座厅
  tag: ✅
  source: Warcraft Wiki — The Great Masquerade（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=The_Great_Masquerade&action=raw
  quote: "Windsor escorts the party from the gates of Stormwind through the city to the keep's entrance, then inside to the throne room."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "全身板甲的男子自城门方向沿主街步行向要塞，沿途行人驻足回头，队列在他身后拉长"
  negative: "骑马, 乘车, 奔跑, 被押送, 队伍喧哗"
```

## 平台合规与系列铁律的落点（写进本场每一镜的负向）

本场结局有死亡。**系列 I-1「灾变日只做前一日、远景无血」与平台合规在此合并为一条硬约束**：

- **远景处理**：现真身与战斗一律**远景 / 长焦压缩大全景**，人占画高 ≤ 1/6；**不给近景搏斗、不给伤口、不给尸体特写、不给血**。
- **旅行者不参战、不被卷入**（I-5 三铁律）：她站在厅门内侧靠墙，全程只看、只讲。
- **她不揭穿、不预警、不评论对错**——她只描述看见了什么。

**固定负向组**：`血迹, 伤口特写, 尸体特写, 断肢, 近景搏斗, 旅行者参战, 旅行者被卷入, 旅行者出手, 旅行者呼喊示警`

## 未查 / Open questions

1. **全场台词未穷尽**。本文只登记 parent 本次核到的 7 条。**阶段 4 写剧本前必须再跑一遍 raw wikitext**，把伯瓦尔、普瑞斯托、卫兵的每一句逐字补全——凡要进片的句子，一句一条 fact、一句一个 `source_url` + `quote`。
2. **步行时长未查实**。W8 记为「约十分钟」，但本次 raw wikitext 的返回里 `The exact duration isn't specified in the text`。**口播不要报分钟数**，除非另有出处。
3. **路线的逐段细节未查实**——只确证「自城门 → 穿城 → 要塞入口 → 王座厅」。途经哪几个区、在哪里停顿，须另查或标 ⚠️ 自设。
4. **`voice_id` 未建**。温德索尔、普瑞斯托、伯瓦尔三人各需锁一个；本站还须决定**当地人说英语原文时，中文轨怎么处理**（字幕 / 译配），属阶段 2 casting 的活。
