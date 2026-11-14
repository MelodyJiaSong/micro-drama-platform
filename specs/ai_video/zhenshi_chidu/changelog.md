
## Follow-up 001 — 2026-11-06 19:42:40
Source: user_input/follow_ups/202611.md - section 001
Summary: ep01 按肩高排名、参照人 1.75 m、分歧取值代理定

Auto-updated:
- ai_videos/zhenshi_chidu/0_research/ep01_animal_dimensions.json — 河马体长 4.0→3.5 est.（代理定，用户授权）
- ai_videos/zhenshi_chidu/0_research/ep01_animal_dimensions.md — 文末补用户决定与取舍（肩高排名、1.75 m、分歧取值）
- ai_videos/zhenshi_chidu/bible.md — D3 参照人标「1.75 m man」；§3 一期一个排序口径（ep01 肩高）；§4.3 加测量点标定 landmark_ratio
- ai_videos/zhenshi_chidu/topics.md — ep01 标题与主口径改为按肩高排名
- ai_videos/zhenshi_chidu/README.md — 已定 6–8、状态行
- ai_videos/zhenshi_chidu/_tools/scene_lineup.py — 支持 landmark_ratio（肩高标定）与 sort_value

验证: 脚本语法检查通过；肩高排名由 ep01_animal_dimensions.json 计算（冠军长颈鹿 3.31 m、并列按体重排）；文档替换逐处断言命中；未做独立审稿（文档与原型阶段）

No conflicts found in: （未单独核查）


## Follow-up 002 — 2026-11-06 19:53:11
Source: user_input/follow_ups/202611.md - section 002
Summary: 缺口物种用 Codex 参考图 + 本地 TripoSR 生成，标 AI MODEL

Auto-updated:
- ai_videos/zhenshi_chidu/bible.md（§2.4 AI MODEL 标签、§4.1 第 3 档兜底、不用近缘替代）；ai_videos/zhenshi_chidu/README.md 已定 9；.agents/references/project/paid_services.md 登记 TripoSR（允许）并注明 rembg 锁 isnet-general-use、禁 bria-rmbg（非商用）；tools/local_3d.py（TripoSR 本地入口：skimage 替 torchmcubes、glTF Y 朝上、体积为负翻面、去背景模型 sha256 校验、产物旁 .json）；ai_videos/zhenshi_chidu/_tools/scene_lineup.py（import_model、顶点色 sRGB 伽马、shoulder_ratio 自动估肩高）；0_research/toolchain_licenses.md；ep01 _build/prompts 14 份、assets/ref_images 14 张（request_log.md 已记）、_build/ref_review_v1.md；assets/models_ai/ 批量产物

验证: 权重 model.ckpt 大小 1,677,246,742 B 与 sha256 429e2c6b…70ee 代理复核一致；rembg 模型 md5 与 rembg 内置值一致；DIS 许可经 GitHub API 读回 Apache-2.0；bongo 实跑 55 s：watertight、体积为正、导入 Blender 直立头朝 +X、伽马后毛色正确、肩高线自动估 0.753 看图落在鬐甲。未过：bongo 体长比数据短约 25–30%（三分之四视角参考图深度靠猜），另开 follow-up 处理，未进成片

No conflicts found in: （未单独核查）


## Follow-up 003 — 2026-11-07 09:44:34
Source: user_input/follow_ups/202611.md - section 003
Summary: ep01 做到成片交用户审核；30 只统一走 AI 模型流程

Auto-updated:
- ai_videos/zhenshi_chidu/episodes/ep01_largest_land_animals（data.json、sources.md、licenses.csv、topic.md、publish.md、qc.md、review_for_user.md、scene/ep.blend、render/）；ai_videos/zhenshi_chidu/_tools/*；bible.md；README.md；0_research/toolchain_licenses.md

验证: 成片 render/ep_master.mp4（4:08，−14.1 LUFS）；_tools/gate.py PASS（licenses 31 行白名单、scale_check 30/30 ≤0.5%、人 1.75 m）；独立审片 3 轮（qc.md），第 3 轮可交用户审核、无阻塞；交审说明 review_for_user.md；未上传（用户亲手）
费用: Codex 出图 18 次（16 只 v2 + 长颈鹿 v3 + 北极熊 v3）；Suno 1 个任务

No conflicts found in: （未单独核查）


## Follow-up 004 — 2026-11-07 22:19:37
Source: user_input/follow_ups/202611.md - section 004
Summary: ep01 第 2 版：AI 写实图抠像 + CC0 真实环境（2.5D），替代 TripoSR 3D 模型

Auto-updated:
- ep01 第 2 版成片 render/ep_master.mp4（2.5D：AI 写实图抠像 + Poly Haven CC0 环境）、thumb_A/B、preview.json、data.json、licenses.csv（34 条）、publish.md（标题去 3D）、review_for_user.md、qc.md 第 4–5 轮；新工具 _tools/cutouts.py、build_cutout.py，改 render_ep.py、cards.py、gate.py、make_ep01_data.py、make_ep01_meta.py、make_preview.py；bible §2.3 2.5D 段、README 决定 #11、toolchain_licenses；第 1 版备份 _build/v1_3d/

验证: gate.py PASS（许可 34 条白名单、比例机检 30/30、参照人 1.75 m）；成片 248.2 s、−14.1 LUFS、真峰值 −2.0 dBFS；第 4 轮独立审片「可交审」无阻塞；第 5 轮独立复核「需要先修」（非阻塞：地面无草纹理与硬地平线、蹄下阴影只剩细线、钩子天空偏灰），已如实写入 review_for_user.md 交用户定；白犀翻向导致放大约 11% 的错误已修并经复核确认
费用: Codex 出图 2 次（1 次网络不通未出图，1 次参照人成功），记 request_log.md；Poly Haven CC0 免费下载

No conflicts found in: （未单独核查）


## Follow-up 005 — 2026-11-08 01:05:43
Source: user_input/follow_ups/202611.md - section 005
Summary: ep01 第 3 版：远景板 + 中景树 + 3D 草的精细草原环境

Auto-updated:
- ep01 第 3 版精细环境：scene_env.py（远景板、金合欢/灌木抠像、Poly Haven 3D 草与石块、前景草按 0.0284×距离限高、合影机位一侧铺草）；build_cutout.py（抠像平面不投影、合影人移最左、构图下移）；cards.py（标题/洞察卡移到脚线下）；render_ep/compose/make_preview/gate/make_ep01_meta 相应更新；全片重渲 render/ep_master.mp4、封面、preview.json；qc.md 第 6 轮与作者修复记录；review_for_user.md、bible.md、publish.md、SOURCES.md、toolchain_licenses.md

验证: gate.py GATE PASS（许可 42 条、比例 30/30）；成片 248.2 s、−14.1 LUFS、真峰值 −2.0 dB，三段帧数齐（300/210/6486）；作者抽帧确认细黑线消失、蹄子未被前景草挡、卡片不压主体；第 6 轮独立审片（Sonnet）结论需要先修，4 条应修已改并重渲；第 7 轮独立复核进行中，结论写入 qc.md
费用: Codex 出图 4 次（远景板、两种金合欢、灌木），均记 request_log.md；Poly Haven CC0 免费下载；本地 Blender 渲染两遍全片约 6 小时

No conflicts found in: （未单独核查）


## Follow-up 006 — 2026-11-08 11:57:41
Source: user_input/follow_ups/202611.md - section 006
Summary: ep01 第 3 版出中英两版：英文成片沿用 ep_master.mp4；中文版只换叠加文字（无旁白），新增 cards_zh.py、compose --cards、thumbnail --lang zh；publish.md 写中英两套标题、描述、标签、置顶评论

Auto-updated:
- ai_videos/zhenshi_chidu/_tools/{cards_zh.py(新),compose.py,thumbnail.py,make_preview.py}; episodes/ep01_largest_land_animals/{publish.md,qc.md,review_for_user.md,render/ep_master_zh.mp4,render/thumb_*_zh.jpg,_build/pinned_comment_zh.txt}; README.md

验证: 中文成片 248.2 s、−14.1 LUFS、峰值 −2.0 dB；抽帧看卡片与封面；Sonnet 独立审片结论可交付，4 条应修（标题身高→肩高、括号嵌套、并列措辞）已改并记 qc.md
费用: 无收费调用（本地字体 Noto Sans SC OFL，无新出图）

No conflicts found in: （未单独核查）


## Follow-up 007 — 2026-11-08 14:01:29
Source: user_input/follow_ups/202611.md - section 007
Summary: ep01：英文版经 YouTube API 传成私享（剧级适配器 _tools/upload.py，公开由用户在 Studio 点）；封面改为 Blender 高清静帧合成，中英 × A/B × 16:9 / YouTube / 4:3 / 3:4，写 render/covers/；publish.md 补各平台（TikTok、抖音、快手、B站、视频号、小红书）文案与封面对照

Auto-updated:
- ai_videos/zhenshi_chidu/_tools/{upload.py(新),thumbnail.py(重写),render_ep.py(--still),cards_zh.py(中文置顶评论去外链)}; episodes/ep01_largest_land_animals/{publish.md(按平台分节+封面对照),qc.md,uploads.json,render/covers/{en,zh}/*,render/thumb_*.jpg,_build/cover_stills/*}; README.md

验证: YouTube 私享上传成功 https://youtu.be/gXIryNL5fp4（标题/描述/标签/合成内容声明/封面 A），封面重设后仍为 private；封面两轮 Sonnet 独立审片：第 1 轮需要先修（5 条应修已处理），第 2 轮可交付，比例实测三尺寸均 2.63；upload.py --dry-run 通过、gate.py 通过
费用: YouTube API 配额约 1,700 单位（传片 1,600 + 封面 2×50），非收费服务；无新出图

No conflicts found in: （未单独核查）

