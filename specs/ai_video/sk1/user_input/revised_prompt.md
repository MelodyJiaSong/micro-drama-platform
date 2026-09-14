# sk1 · 合并后的完整意图（raw_prompt + 全部 follow-ups）

> 派生文件，由 `raw_prompt.md` + `follow_ups/*.md` 按时序拼成。改动请改源文件后重生成。

# sk1 · 《时空旅行》第 1 站 · 汴京 · 1120 · 清明日 — 原始请求

> **task_type**：`ai_video` · **sub_type**：`short`（单站独立成片，系列嵌套于 `ai_videos/shikong_lvxing/`）
> 系列级意图在 `specs/ai_video/shikong_lvxing/`；本目录只装 sk1 单站的。

## 用户意图（2026-09-13）

按系列提案 `ai_videos/shikong_lvxing/proposal.md` C §sk1 概念卡开工第一站：**北宋汴京 · 宣和二年（1120）· 清明日**。
先跑「阶段 0 史料调研 → 出 prompt」小闭环，看效果再选下一站。

阶段 0 参数（用户确认，2026-09-13）：严格度＝科普向娱乐（画面可截图指认的东西只允许 ✅ / ⚠️，❌ 只进纠错单元）；系列公共库本站新建；每个资产 ≥ 8 张历史参考图。

---

# sk1 · 后续指令日志 · 2026-09

> 单站意图的落点；系列级意图见 `specs/ai_video/shikong_lvxing/`。

---

## 001 — 2026-09-14 08:26:14 — sk1 另起片名：系列名不作单片标题

> target_stage: 1
> target_artifacts:
>   - ai_videos/shikong_lvxing/sk1/README.md
>   - ai_videos/shikong_lvxing/sk1/1_立项/concept.md
> severity: low

### 指令

sk1 在剧目管理界面上显示的标题不能是《时空旅行》——那是系列名。为本站另起一个片名，README 首行等处统一。

### 一行摘要

片名由 Claude 自定并记判断；系列名只作前缀，与《荒野生活 · 深雪第一夜》同构。
