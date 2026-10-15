---
name: codex-imagegen
description: 经 Codex CLI 调内置 image_gen 出高质量图片（ChatGPT 订阅额度，无需 API key）；先记请求日志，图片存到 ai_videos 下指定路径，再看图验收。
metadata:
  claude:
    argument-hint: '<目标 .png 路径> <画面描述或 prompt 文件> [参考图…]'
---

> Claude / Codex 共用正文。执行前按根目录 `AGENTS.md` 路由，工具、提问、委派、参数与收尾遵 `CONVENTIONS.md` § Tool scoping and team coordination。路径相对仓库根。

# Codex 内置出图

**调用前关卡**：遵 `CONVENTIONS.md` § 外部服务请求审计（全局必经），先读 `.agents/references/project/paid_services.md`「Codex 内置出图」与商业用途表。只经 `tools/codex_image.py` 调用，不直接跑 `codex exec` 出图——直跑不留请求日志。Codex 会话里本来就有 `image_gen`，但仍走本脚本，这样日志与落盘位置一致。

## 什么时候用

- 默认出图方式（follow-up 238）：人物、背景、道具、装备、概念图都先用它；资产出图器（`gen_char_images` / `gen_bg_images` / `gen_bg_assets` / `gen_outfit_views` / `gen_equipment`）的 `--engine auto` 已按 Codex → ElevenLabs → 即梦 自动调用本脚本，批量出资产走出图器即可；零散单张直接调本脚本。即梦是最低选项，前面都不行才用。
- 视频不走这里；视频生成仍由用户决定。

## 步骤

1. **定归属与路径**：`--out` 必须是 `ai_videos/` 下的 `.png`，按资产或集目录放（决定 `request_log.md` 位置）；无归属的能力测试放 `ai_videos/_research/service_tests/`。已存在的文件不覆盖，另起带版本号的文件名；确需替换才加 `--overwrite`。
2. **写 prompt**：完整画面描述，比例写进 prompt（如「竖幅 9:16」）；参考图按附带顺序在 prompt 里指认（第 1 张是人物正面，第 2 张是场景……）。长 prompt 写进文件用 `--prompt-file`。
3. **调用**：

   ```bash
   python tools/codex_image.py --out ai_videos/<剧>/<资产目录>/<名>.png --prompt-file <prompt.txt> [--ref <参考1> --ref <参考2>] [--transparent]
   ```

   一张约 2–3 分钟，用后台或足够长的超时（默认 900 秒）。成功时打印保存路径；`image_gen` 改写了 prompt 会在 stderr 提示。
4. **看图验收**：读取图片，核对主体、风格、构图、比例、文字与参考一致性；不合格就改一处 prompt 再调用，新文件另起版本号。
5. **失败**：脚本报「没有拿到新图」时不要立刻重提；先看 request_log 里的 thread_id、errors，并查 `~/.codex/generated_images/<thread_id>/`，可能已经生成。同一张图三轮仍不行就停，和用户讨论。

## 边界

- 用的是本机 `codex login` 的 ChatGPT 订阅额度；未登录或额度不足时说明情况，不改走其他收费服务，除非用户同意。
- 内置工具不暴露图像型号、画质档与费用，日志里记「未知」，不要在报告里写成某个具体型号。
- 未经明确同意不生成真人肖像（OpenAI 条款）。
