# changelog · xingji_yingjiu

## 建项 — 2026-09-06 10:36:12
Source: user_input/raw_prompt.md
Summary: 新建 AI 军事科幻短片《幽灵撤离》，走 ai_videos__全流程编排 阶段 1→3。

新建：
- ai_videos/xingji_yingjiu/1_立项/concept.md — 立项策划单
- ai_videos/xingji_yingjiu/2_世界观人设/world.md — 世界观 + 七条核心规则 + bg 索引
- ai_videos/xingji_yingjiu/2_世界观人设/style_guide.md — 渲染样式串 + 三段色调曲线 + 固定负面词块
- ai_videos/xingji_yingjiu/2_世界观人设/casting.md — voice_id 全片锁定
- ai_videos/xingji_yingjiu/2_世界观人设/relationships.md — 人物网
- ai_videos/xingji_yingjiu/2_世界观人设/units/u1–u7 — 单位卡 ×7 + 正典参考图 35 张
- ai_videos/xingji_yingjiu/2_世界观人设/characters/c1–c3 — 人物卡 ×3（含 12 维人物灵魂）
- ai_videos/xingji_yingjiu/2_世界观人设/scenes/bg1–bg4 — 场景档 ×4
- ai_videos/xingji_yingjiu/2_世界观人设/props/p1_数据核心舱 — 关键道具卡
- ai_videos/xingji_yingjiu/3_大纲/arc_outline.md — 六段结构 + 36 镜细纲
- ai_videos/xingji_yingjiu/README.md — 项目门面（中文）

QC 记录：
- 阶段 1（人工确认）：主角诉求 / 反派动机 / 长线伏笔 / 正向立意 四项齐全 → PASS
- 阶段 2（ai_videos__格式契约 机械项）：0 hex · 24 个 text prompt 块全部 ≤2000 字（最大 639）· 「字幕」仅出现于负向词块 · 路径 ASCII 前缀 + 中文后缀 → PASS
- 阶段 3（ai_videos__剧情连贯 + ai_videos__全剧序列）：初稿 3 处 blocker，已当场修复 →
  1. 段落时长与逐镜之和不符（段五声明 42s 实计 52s，全片实为 197s 而非声明的 185s）→ 重配全部逐镜时长，六段逐段对账一致，全片 180s。
  2. shot03「三人短暂显形」与 world.md 规则 1「迷彩失效全片只有一种表现、只在 shot17」冲突 → 改为迷彩开启态的折射轮廓被逆光勾边，不解除迷彩。
  3. 露脸镜编号串号（shot21 误标为渡鸦露脸镜②）→ 增设「露脸镜台账」与人物卡对账，c1=shot12/35、c3=shot21/34、c2 全片零露脸。
  复核后 → PASS

divergence note（相对 BLUEPRINT §4 全局默认）：
- 画幅 **16:9**（非 9:16 母版）—— 用户明确选择，理由：战场纵深 / 虫潮压迫感 / 机甲与战舰体量需要横向画幅。
- 赛道为军事科幻（非古风仙侠），故「藏锋·无外放」特效规则不适用，改用 world.md 七条核心规则约束特效边界。

遗留风险（不静默）：
- 单位造型高度还原《星际争霸》正典（用户指定"参考星际单位"），存在版权风险；当前定位为同人致敬、非商业发行。公开商用前须重新裁定。
