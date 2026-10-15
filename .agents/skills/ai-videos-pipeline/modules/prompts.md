# Prompt 编译与出片

输入：已确定的分镜（episodes/epNN/filming.json）。输出：每镜的 overhead（复杂镜另有 previz 视频）、episodes/epNN/prompts.json（每镜一条视频 prompt 与按上传顺序的参考清单）；出片后各镜头的条落在 renders/，交给剪辑选条。

不能只用文字 prompt 生成视频：每一镜都带参考上传——运动参考（overhead 图，复杂镜换成 previz 视频）、每个出场人物的三视图与声样、背景图——prompt 第一段「参考：」一行列出全部参考并写明每个管什么（follow-up 227、228）。

## 步骤

| 步 | 做什么 | 产物 | 工具 |
|---|---|---|---|
| 1 | 每镜写 overhead：机位、人物站位与走位、朝向、物件、时刻 | `shots/stN/planning/overhead.toml` | 手写（代理或人），见 [Overhead](prompts-overhead.md) |
| 2 | 画 overhead、判要不要 previz | `stN_overhead.png`（给人审）、`stN_overhead_ref.png`（给模型）、`previz.json` | `python tools/shot_overhead.py --all <集目录>` |
| 3 | 每镜出静帧核对取景（几十秒）；复杂镜渲 previz 视频 | `previz/frames/stN_stills.png`；`previz/stN_previz.mp4` | `python tools/overhead_previz.py <镜头目录> --force --stills`；`--render`，见 [Previz](prompts-previz.md) |
| 4 | 编译：分镜字段 + 参考 + 固定规则 → prompt | `prompts.json`、各镜 `prompt.txt` | 管理 UI「编译」；参考缺一镜就拒绝编译。也可只编一场（API `scene`），只查这一场的参考，其它场原样保留、仍标过期（follow-up 259） |
| 5 | 每镜资料包：把 prompt 参考的全部文件复制一份，源文件变了自动更新、prompt 要重编译时失效；用户决定后提交 | `shots/stN/资料包/` | `python tools/shot_pack.py sync <集目录>`（Stop hook 每回合跑），见[出片](prompts-generate.md) |

| 子页 | 讲什么 |
|---|---|
| [Prompt 结构](prompts-structure.md) | 一条 prompt 有哪几行，每行从哪个字段来、起什么作用 |
| [固定规则](prompts-rules.md) | 编译器自动加的规则：镜头 key、参考用法、声音、连续镜头、防分身、版本与参考门禁 |
| [Seedance 写法](prompts-seedance.md) | 官方指南与实践：结构、长度、运镜、动作、台词、参考、负向、常见失败 |
| [参考](prompts-references.md) | 每镜上传哪些参考、什么顺序、从哪个资产取、怎样说明用法 |
| [Overhead](prompts-overhead.md) | 俯视站位图：画什么、怎么写 overhead.toml、两张图、取景核对 |
| [Previz](prompts-previz.md) | 绿幕小人偶预演：哪些镜要、怎么做、怎样交给模型 |
| [出片](prompts-generate.md) | 资料包、提交、记日志、落盘；现为人工审核 |

## 分镜要给什么

每个镜头编译成一条独立的 prompt，生成模型看不到前后镜。所以分镜要让每一镜自给自足：

| 字段 | 应该 | 不应该 |
|---|---|---|
| `cast` | 画面里每个人的资产键：换装阶段 `c1-1`，没有换装的用人物卡 `c14`；空镜留空列表 | 漏掉画面里的人；用名字代替资产键 |
| `action` | 每个人是谁、在做什么；本镜的环境与陈设 | 写「他」「同上」「接上一镜」 |
| `blocking` | 每个人站在哪、面朝谁、视线落在哪、怎么移动；有人物就必填 | 只写「两人对话」；与 overhead 矛盾 |
| `beats` | 按秒分拍：`0–3秒 …；3–5秒 …`，区间连续、覆盖整镜；动作写到身体部位、幅度与速度 | 一句话概括整镜；用时间戳控制眨眼这类高频小动作 |
| `camera` | 按[镜头](filming-shots.md)写功能、景别与裁切、取景、机位与焦点；一镜只写一种运镜 | 只写「近景」；推、拉、摇、移叠在一起 |
| `lighting` | 光从哪来、什么性格、有没有火光等禁项 | 只写「好看的光」 |
| `dialogue` | 本镜实际说出口的话，标明谁说；无对白留空 | 把旁白、心理活动或画面说明写进对白 |

时长要够念台词、做完动作；一镜塞不下就拆镜。

## 落盘与导入

派生文件写 episodes/epNN/scenes/sN/shots/stN/prompt.txt；生成的媒体导入该镜 renders/，保留原文件名。完整 key 优先于参考资产 key；截断、未知或有歧义的 key 留在下载目录并报告，不猜测。

## 当前边界

- 上游未确定或版本变化时拒绝编译；任何一镜缺 overhead、该有 previz 却没渲、人物三视图或声样或「Shot prompt 外观」缺失、场次没绑背景或背景卡缺「Shot prompt 场景」，都拒绝编译并列出是哪几镜；单场编译只看这一场的镜头。
- 编译只写本模块，不回写故事和分镜；overhead 与 previz 也属于本模块，改走位只改 overhead，不改分镜文字——两者矛盾时回分镜改。
- 编译不等于验收：画面是否符合分镜、声音是否守规则，出片后对照核对。
