# 出片

状态：基础版。把编译好的 prompt 和它的全部参考一起交给生成服务，结果作为该镜头的条保存，供剪辑选条。不能只用文字 prompt 提交。

## 资料包（每镜标准流程）

每个镜头目录下一个 `资料包/`：prompt 参考的**全部文件各复制一份**（运动参考 overhead 图或 previz 视频、每人三视图、背景图、每人声样），加 `prompt.txt` 与 `manifest.json`。文件名带上传顺序与 key_id，`01_图片1_ep1_s4_st2_overhead.png`、`02_图片2_c14_Brother_Sammuel.png` …；资料包里的 prompt.txt 已把「参考：」行的 `key=>@` 填成 `key=>@图片1`…，与上传顺序一致。资料包是派生缓存（gitignored），整个拿去上传即可。管理 UI 的每镜 prompt 页下方显示资料包：状态（一致 / 等待更新 / 已失效 / 还没建）、每个文件的缩略图或播放器、副本与源文件链接、填好编号的 prompt.txt（follow-up 229）。

| 情况 | 资料包怎样 |
|---|---|
| 刚编译完 / 还没有资料包 | 建：复制全部参考，manifest 记每个源文件的路径与 sha256 |
| 源文件内容变了、prompt 不用变（重画背景图、换声样、重画同一份 overhead） | **更新**：重新复制，manifest 记新指纹 |
| prompt 要重编译才对得上（编译器升版；分镜编译后改过；参考文件不在了；overhead.toml 改了没重画；previz 判定变了） | **失效**：清空，只留 `_失效.md` 写明原因；修好、重新编译后再建 |

```
python tools/shot_pack.py sync <集目录> [镜头key]   # 建 / 更新 / 失效
python tools/shot_pack.py sync --all --quiet         # 全仓（Claude Stop hook 每回合跑）
python tools/shot_pack.py check <集目录>             # 只报告
python tools/shot_pack.py cmd <集目录> <镜头key>     # 资料包最新时打印提交命令
```

## 提交

| 规则 | 说明 |
|---|---|
| 人工审核 | 每次生成由用户决定后才提交（「生成永远人点」） |
| 先记日志再请求 | `cmd` 打印的命令经 `tools/service_call.py` 写请求日志，见[外部服务](../../../references/project/paid_services.md)；上传的是资料包里的文件，`--image / --video / --audio` 按资料包顺序 |
| 模型与分辨率 | 剧 `workflow.json` 的 `prompt.model`（本剧 `seedance2.5`）与 `prompt.resolution`（默认 **720p**：用户定，1080p 太耗积分）；超过该模型的参考上限，资料包失效 |
| 只用可商用的工具 | 条款不明确允许商业用途的服务不用 |
| 结果落盘：每次生成一个条目录 | `renders/{YYYYMMDD-HHMMSS}_{submit_id 前 8 位}/`：视频（文件名带镜头 key）、`generation.json`（submit_id、模型、时长、比例、分辨率、积分、参考清单与 sha256）、`prompt.txt`（提交时的原文）、`review.md`（审核）。CLI 出片用 `python tools/shot_take.py poll <集目录> <镜头key> <submit_id> --credits N` 查询、下载并建目录；网页下载的文件经导入也各自进一个目录。一镜可以有多条（follow-up 230） |
| 重试与搁置 | 同一镜重试（含改写后重出）到上限（CONVENTIONS「Iteration bounds」默认 3 轮）仍不成功就**搁置**：该镜最新一条的 `review.md` 写「状态：搁置」、每次失败的表现与已试过的改法，交给用户共同讨论（改设计、换镜头、剪辑绕过或接受瑕疵）；不无限重试，也不为一次随机失败加规则（2026-10-11 用户定） |
| 审核（每条必写） | `review.md` 写「Vision / 对的 / 不对的 / 结论 / 怎么看的」，Vision 一项回答这条是否给出全剧 Vision 要的体验（编译是固定转换，不另做 Vision 判断）：逐秒抽帧看整体、与参考图并排看人、听或测声音；**判断「没有」某样东西之前先看全分辨率局部**（2026-10-10 在缩略图上把卫兵的长戟误判为没有）。管理 UI 每镜 prompt 页的「生成记录」显示每条的视频与审核 |

## 将来改为自动

人工审核以后可切换为自动，切换前须具备：每集或每场的积分上限；生成后的自动看片质检；同一镜的重试上限与「原因相同就换方案」；同一场多角度的一致性检查；请求日志照常记录。具备之前保持人工审核。
