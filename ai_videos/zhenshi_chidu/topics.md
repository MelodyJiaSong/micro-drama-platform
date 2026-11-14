# 第一季选题（v0，代理起草，待用户确认）

> 2026-11-06。打分：需求（同题播放量级，【推断】为主，立项前跑 YouTube 同题实测）、数据（能否复用排行榜）、模型（§4.1 前两档能否覆盖）、商用风险。

| 期 | 题目（英文标题草案） | 主口径 | 数据来源 | 模型路线 | 风险 / 待查 | 建议 |
|---|---|---|---|---|---|---|
| **ep01** | The 30 Biggest Land Animals, Ranked by Height · True Scale 3D | **肩高排名**（用户定，follow-up 001；辅：体长、体重） | 物种集合 = 排行榜 ep04 体重前 30；尺寸见 `0_research/ep01_animal_dimensions.*`（30/30 完成） | 开放库动物模型（调研中） | 30 种是否都有可商用写实模型 | **试制** |
| ep02 | Largest Ships Ever Built | 船长 | 复用排行榜 ep11 | 程序建模简化船体（船型剖面 + 上层建筑体块） | 船型辨识度 | 第二优先 |
| ep03 | Deepest Lakes Cross-Section | 最大深度 | 复用排行榜 ep15 | 程序建模剖面 | 剖面形状需测深数据，否则用示意形状（卡上注明） | 候选 |
| ep04 | Tallest Waterfalls | 总落差 | 复用排行榜 ep20 | 程序建模崖壁 + 水体 | 水体效果的渲染成本 | 候选 |
| ep05 | Biggest Dinosaurs vs Humans | 体长 / 估计体重 | 新调研（古生物估计值差异大，必须标 est.） | 开放库恐龙模型（需核许可） | 需求高【推断】；数值争议大 | 候选 |
| ep06 | Largest Aircraft | 翼展 / 机长 | 新调研 | 开放库 / 程序简化 | 机型外观是否涉及商标与外观设计（待查） | 候选 |
| ep07 | Biggest Rockets | 高度 | 新调研 | NASA 3D（公有领域）+ 程序建模 | 不得用 NASA 标志或暗示背书 | 候选 |
| ep08 | Largest Sea Creatures | 体长 | 新调研 | 开放库 | 水下场景另做一套皮肤 | 候选 |
| — | Tallest Statues / Tallest Buildings / Largest Stadiums | 高度 / 座位 | 排行榜 ep13 / ep01 / ep16 | — | 全景自由与建筑作品版权 | **第一季不做**（bible §0） |

## 每期 topic.md 模板

```markdown
# epNN · <题目>
- 英文标题草案：
- 主口径（排序依据）与单位：
- 辅助信息：
- N 与入榜线：
- 数据来源与截至日期：
- 为什么值得做（同题 YouTube 实测、观众能得到什么）：
- 模型可得性：每条在 bible §4.1 哪一档；兜底与不收的条目
- 主题皮肤（地面 / 天空 / 配色）：
- 洞察卡草案（每 10 名一张）：
- 待用户决定：
```
