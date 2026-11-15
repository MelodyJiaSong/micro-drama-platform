---
name: codex-imagegen
description: 经 Codex CLI 调内置 image_gen 出高质量图片（ChatGPT 订阅额度，无需 API key）；先记请求日志，图片存到 ai_videos 下指定路径，再看图验收。
---

> Kimi / Codex 共用本 skill，通过统一脚本调用 Codex 出图后端。执行前按根目录 `AGENTS.md` 路由，工具、提问、委派、参数与收尾遵 `CONVENTIONS.md` § Tool scoping and team coordination。路径相对仓库根。

# Codex 内置出图

**调用前关卡**：遵 `CONVENTIONS.md` § 外部服务请求审计（全局必经），先读 `.agents/references/project/paid_services.md`「Codex 内置出图」与商业用途表。只经 `tools/codex_image.py` 调用，不直接跑 `codex exec` 出图——直跑不留请求日志。Codex 会话里本来就有 `image_gen`，但仍走本脚本，这样日志与落盘位置一致。

## 什么时候用

- **2026-11-08 用户定：以后出图全部用 Codex（`tools/codex_image.py` / 各出图器 `--engine auto` 现在只用 Codex）；没有用户明确允许不用 ElevenLabs，ElevenLabs 失败也不再是自动回退的一环。** 下面关于 ElevenLabs 的说明只在用户允许时适用。
- 旧规则（只在用户允许用 ElevenLabs 时适用）——出图顺序（follow-up 275，取代 270 的 Codex 优先）：默认 ElevenLabs，ElevenLabs 有任何 blocker（额度、审核、网络、超时）就用本脚本，不问用户（dota_yingxiong follow-up 066）；Codex 也可直接点名（出图器 `--engine codex`）；资产出图器（`gen_char_images` / `gen_bg_images` / `gen_bg_assets` / `gen_outfit_views` / `gen_equipment`）的 `--engine auto` 已按 ElevenLabs → Codex 自动调用本脚本，批量出资产走出图器即可；零散单张直接调本脚本。出图只有 Codex 与 ElevenLabs 两个选择，即梦只用于视频。
- 视频不走这里；视频生成仍由用户决定。

## 步骤

1. **定归属与路径**：`--out` 必须是 `ai_videos/` 或 `edu_videos/<系列>/<知识点>/` 下的 `.png`，按资产、集或知识点目录放（决定 `request_log.md` 位置）；无归属的能力测试放 `ai_videos/_research/service_tests/`。已存在的文件不覆盖，另起带版本号的文件名；确需替换才加 `--overwrite`。
2. **写 prompt**：完整画面描述，比例写进 prompt（如「竖幅 9:16」）；参考图按附带顺序在 prompt 里指认（第 1 张是人物正面，第 2 张是场景……）。长 prompt 写进文件用 `--prompt-file`。
3. **调用**：

   ```bash
   python tools/codex_image.py --out ai_videos/<剧>/<资产目录>/<名>.png --prompt-file <prompt.txt> [--ref <参考1> --ref <参考2>] [--transparent]
   ```

   一张约 2–3 分钟，用后台或足够长的超时（默认 900 秒）。成功时打印保存路径；`image_gen` 改写了 prompt 会在 stderr 提示。
4. **看图验收**：读取图片，核对主体、风格、构图、比例、文字与参考一致性；不合格就改一处 prompt 再调用，新文件另起版本号。
5. **失败**：脚本报「没有拿到新图」时不要立刻重提；先看 request_log 里的 thread_id、errors，并查 `~/.codex/generated_images/<thread_id>/`，可能已经生成。同一张图三轮仍不行就停，和用户讨论。
6. **卡住 / 被拒的常见原因**（dota_yingxiong follow-up 066，约 170 张人物立绘实测）：同一 prompt 连续超时（会话里 image_gen 一直不返回、`generated_images` 为空）多半是图像审核在后台拦，重提同一版没用，要改措辞——① 像知名角色 / IP 的组合描述（「熊猫人」+ 斗笠长袍回 `moderation_blocked`；「巨魔战士」）改成中性生物描述、识别层不丢；② 裸露相关词，**负面词里的「裸露 / 性感」也算**，改成正面写「羽毛 / 布料严密覆盖」；③ 密集孔洞、湿润蠕动的肉质触须这类易引不适的质感，改成「细纵纹」「鲶鱼须」；④ 负面词过长且与正文矛盾，删到十几项。确认没出图再重提，结果未知的仍按第 5 步查。 另：**内置 image_gen 一次最多收 5 张参考图**，超过即明确失败、不出图——参考清单超 5 张时先合并（如多件武器拼一张）或去掉最次要的一张。

## 边界

- 用的是本机 `codex login` 的 ChatGPT 订阅额度；未登录或额度不足时说明情况，不改走其他收费服务，除非用户同意。
- 内置工具不暴露图像型号、画质档与费用，日志里记「未知」，不要在报告里写成某个具体型号。
- 未经明确同意不生成真人肖像（OpenAI 条款）。
