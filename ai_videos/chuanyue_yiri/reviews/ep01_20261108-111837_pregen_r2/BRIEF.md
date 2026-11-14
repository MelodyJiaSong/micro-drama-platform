# 审稿说明（Portal Travel · 穿越一日 · ep01 · 出片前（故事＋分镜＋prompt＋首帧/故事板） · 第 2 轮）

所有审稿人共用，先读完。审查单目录：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-111837_pregen_r2`（下文相对路径都相对它）。

## 材料
- 总索引：`materials/index.md`。
- 每镜 `materials/shots/<场>_<镜>/spec.md`：分镜规格、送给模型的 prompt 与参考清单路径、俯视图 / 首帧图路径；镜组板与镜组 prompt 路径在索引里。
- 出片前审查看的是**文字与参考图**：做不到、会出错、前后矛盾的写法都要报，因为它们一定会变成画面错误。
- 这是第 2 轮（最多 3 轮）。上一轮的问题在 `previous.md`，这轮改了什么在 `changes.md`；必查项 R 要逐条复核。
- 集目录：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\episodes\ep01`；系列规则：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\bible.md`；故事稿：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\episodes\ep01\story.md`（结构化版 `story.json`）；人物卡：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\2_世界观人设\characters`；场景卡：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\2_世界观人设\background`。
- 需要时可用 ffmpeg 另抽帧或放大裁切，**只写到你自己的目录** `work/<你的代号>/`。

## 已知、不用报告
1) 维苏威：按用户 2026-11-06「只入画、全片不提」。第 1 轮 era 审稿人指出：从海门外朝东看，画右那座绿山其实是南面的 Monti Lattari，维苏威在画左身后、出画；山本身不用再报，冒烟或 prompt 写火山词仍要报。2) 场一之外的场不在本单范围。

## 规则
- **只读**：不改仓库里任何文件（本审查单目录下你自己的报告与 work 目录除外），不调用任何收费服务，不提交生成。
- **只管你自己那条法则**；顺手看到别的问题列在最后「其他」里，一句话。
- 拿不准写「存疑」并说明怎么核实；证据必须指到镜头、秒数、拼图第几格或文件行。
- 既报产物的错，也报「分镜 / prompt / 规则源本身的问题」。

## 报告格式（缺一不能打勾）
1. `## 必查项`：任务书里每个必查项编号一行，写 ✓（查过、没问题）或 ✗（有问题，见表）加一句说明，例如 `- P1 ✗ s3_st2 自拍却双手掰面包`。
2. 问题表，每个问题一行，按严重度排序：

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|

   严重度：重出 / 可剪 / 记录 / 存疑。本该哪关：① 故事 / ② 分镜文字 / ③ prompt 或首帧 / ④ 模型随机 / 规则源。
   建议改动要标「便宜」（改文字、出图、改工具即可）或「要积分」（必须重出视频）。
   全部没问题时不写空表，写一行「结论：无问题」。
3. 「整体观察」（≤10 行）。
4. **最后一步自己打勾**：运行任务书里的 `tick` 命令，看到「已打勾」才算完成；被拒就按提示改报告再打。
5. 给调用你的人回 300 字以内摘要：最严重的 5 条、报告路径、打勾结果。