# 审稿说明（Portal Travel · 穿越一日 · ep01 · 全量（分镜＋prompt＋出片））

所有审稿人共用，先读完。审查单目录：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1`（下文相对路径都相对它）。

## 材料
- 总索引：`materials/index.md`（场顺序、每场目的、每镜一行）。
- 每镜 `materials/shots/<场>_<镜>/`：`spec.md`（分镜规格、视频路径、成片用的区间、语音识别、剪辑理由）、`sheet4.jpg`（每秒 4 帧）、`sheet1.jpg`（每秒 1 帧）。
- 每场 `materials/scenes/<场>_bounds.jpg`（镜头接口：上一镜尾帧 | 下一镜头帧）与 `<场>_scene1.jpg`（整场剪辑每秒 1 帧）。
- 集目录：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\episodes\ep01`；系列规则：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\bible.md`；故事稿：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\episodes\ep01\story.md`；人物卡：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\2_世界观人设\characters`。
- 拼图看不清时可用 ffmpeg 另抽帧或放大裁切，**只写到你自己的目录** `work/<你的代号>/`。

## 已知、不用报告
Riley 在已出视频里是旧造型（金发、旧脸），全片将按新造型重出，发色和脸不报。

## 规则
- **只读**：不改仓库里任何文件（审查单目录下你自己的报告与 work 目录除外），不调用任何收费服务，不提交生成。
- **只管你自己那条法则**；顺手看到别的问题列在最后「其他」里，一句话。
- 拿不准写「存疑」并说明怎么核实；证据必须指到镜头、原条秒数或拼图第几格。
- 既报「这条产物出了什么错」，也报「分镜 / prompt / 规则源本身的问题」——重出时不改，同样的错会再出现。

## 输出与打勾
报告写到 `reports/<你的代号>.md`，每个问题一行，按严重度排序：

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|

- 严重度：重出 / 可剪 / 记录 / 存疑。本该哪关：② 分镜文字 / ③ prompt 或首帧 / ④ 模型随机（或「① 故事」「规则源」）。
- 全部审完没发现问题时，不写空表，写一行「结论：无问题」，下面列出你逐项核过的证据。
- 表后写「整体观察」（≤10 行）。
- **最后一步，自己打勾**：运行任务书里给的 `python tools/review_run.py tick …` 命令，看到「已打勾」才算完成；打勾失败按提示改报告再打。
- 给调用你的人回 300 字以内摘要：最严重的 5 条、报告路径、打勾结果。