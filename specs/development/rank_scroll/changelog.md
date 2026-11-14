
## Follow-up 001 — 2026-11-03 15:25:35
Source: user_input/follow_ups/202611.md - section 001
Summary: rank_scroll 许可白名单加入 Pexels / Unsplash / Pixabay，补测试

Auto-updated:
- projects/rank_scroll/rank_scroll/contract.py — ACCEPTED_LICENCE_PREFIXES 加 pexels license / unsplash license / pixabay content license
- projects/rank_scroll/tests/test_rank_scroll.py — 新增 test_accepts_free_stock_licences（3 个参数）
- ai_videos/paihangbang/data_contract.md — 可接受许可列表同步

验证: pytest 17 passed（原 14 + 新 3）；NC 拒收用例仍通过

No conflicts found in: 其余校验规则未改


## Follow-up 002 — 2026-11-03 15:30:24
Source: user_input/follow_ups/202611.md - section 002
Summary: rank_scroll 卡片国旗每帧绘制、正弦飘动

Auto-updated:
- projects/rank_scroll/rank_scroll/draw.py — flag_layer / flag_waving
- projects/rank_scroll/rank_scroll/cards.py — card_image(flag_out)，_flag 辅助
- projects/rank_scroll/rank_scroll/render.py — _elem_flags，_draw_band 每帧画飘动国旗

验证: pytest 17 passed；ep02 预览 t=100/100.3/100.6 三帧对比：国旗位置正确、形状与明暗逐帧变化

No conflicts found in: 缩略图与计分板国旗未改


## Follow-up 003 — 2026-11-03 19:16:50
Source: user_input/follow_ups/202611.md - section 003
Summary: rank_scroll：签字放行的风险图不卡许可

Auto-updated:
- projects/rank_scroll/rank_scroll/contract.py — image_risk 且 allow_risk_images 时跳过许可校验
- projects/rank_scroll/tests/test_rank_scroll.py — test_unknown_licence_only_with_risk_signoff

验证: pytest 18 passed

No conflicts found in: 默认渲染行为不变


## Follow-up 007 — 2026-11-03 21:49:20
Source: user_input/follow_ups/202611.md - section 007
Summary: rank_scroll 无国旗模式（layout.flags=false）、virus 主题与 7 个新图标

Auto-updated:
- projects/rank_scroll/rank_scroll/contract.py — layout.flags（默认 true，false 时不查国旗、country_iso2 可空）；ICONS 加 virus/vaccine/skull/droplet/bug/wind/biohazard
- projects\rank_scroll\rank_scroll\cards.py — 无国旗时卡片与占位不画旗；virus 主题占位图标；署名以 Render;C:\Program Files\Git\Illustration; 开头时不加 Photo; 前缀
- projects/rank_scroll/rank_scroll/render.py — 封面与来源卡在无国旗时去掉国旗与 flagcdn 署名
- projects/rank_scroll/rank_scroll/publish.py — 无国旗时去掉 flagcdn 署名；图片署名标题去掉过时的 Wikimedia Commons 字样并说明 Render
- projects/rank_scroll/rank_scroll/theme.py — 新主题 virus
- projects/rank_scroll/assets/icons/ — Tabler 3.24.0（MIT）7 个新图标
- projects/rank_scroll/tests/test_rank_scroll.py — test_flagless_mode_skips_flags
- ai_videos/paihangbang/data_contract.md — layout.flags 说明

验证: pytest 28 passed；ep05 validate --strict OK 并渲出 1080p60 母版；默认（有国旗）期未改数据，测试覆盖原有行为

No conflicts found in: 与同时进行的 005（image_alt）、006（音乐床）只做精确替换，未动其段落


## Follow-up 004 — 2026-11-03 20:58:49
Source: user_input/follow_ups/202611.md - section 004
Summary: rank_scroll 列表模式（不排名）与公司卡（logo 牌、创始人圆形头像、右上角标签）

Auto-updated:
- projects/rank_scroll/rank_scroll/{contract,timeline,cards,render,theme}.py — mode=list、corner、logo/logo_bg、person、thumb；tech 主题；sparkles/cpu 图标（assets/icons，Tabler MIT）
projects/rank_scroll/tests/test_rank_scroll.py — 列表模式顺序/无冠军/扣下头像 + 5 个契约报错用例
projects/rank_scroll/README.md、ai_videos/paihangbang/data_contract.md — v1.3 字段说明

验证: pytest 全过（含本会话新增 6 例；与其他会话并行改动后最近一次 28 passed）；ep01/ep02 排名模式代码路径未变；ep03 列表模式两版母版渲染成功，抽帧看卡片、片尾停留与国家计分板正常

No conflicts found in: 排名模式输出不变；与 ep04/ep05 会话的 v1.4 image_alt、layout.flags 改动共存


## Follow-up 009 — 2026-11-04 00:44:21
Source: user_input/follow_ups/202611.md - section 009
Summary: rank_scroll：合成图按账本判定并披露、来源卡 Image credits、计分板分组图标 tally.icons

Auto-updated:
- projects/rank_scroll/rank_scroll/contract.py — 可选 tally.icons（分组名 → 图标，校验图标名）；ICONS 加 paw / glass-full / hand-stop
- projects/rank_scroll/rank_scroll/render.py — 揭晓页按 tally.icons 画分组图标（缺省 globe）
- projects/rank_scroll/rank_scroll/publish.py — 合成图按账本 licence（AI-generated）或 synthetic 判定，描述框写数量注释、上传清单选 Yes；无国旗分组期署名行不重复 country_name
- projects/rank_scroll/assets/icons/ — Tabler 3.24.0 paw、glass-full、hand-stop
- projects/rank_scroll/tests/test_rank_scroll.py — test_tally_icons_and_synthetic_disclosure

验证: pytest 31 passed；ep05 validate --strict OK，publish 描述 3,370/5,000 字符、清单为 Yes；来源卡 Image credits 已由另一会话改好未重复改

No conflicts found in: 与同时进行的 intro_hold（008）等改动只做精确替换


## Follow-up 008 — 2026-11-03 23:58:21
Source: user_input/follow_ups/202611.md - section 008
Summary: rank_scroll：新增 layout.intro_hold 让第一张卡可读；章节标签按实际名次

Auto-updated:
- rank_scroll/contract.py（layout.intro_hold 0–6 s）、timeline.py（f_hold，滚动段加长）、publish.py（章节时间含 hold；章节标签按组内实际最小名次；标题年份取 period_label 最后一个四位年份，无则当年）、render.py（来源卡 Image credits；无图版本写 No images are shown in this version）、tests（test_intro_hold_keeps_band_still_then_scrolls）、ai_videos/paihangbang/data_contract.md、specs/development/rank_scroll/final_specs/spec.md

验证: python -m pytest -q：31 passed；ep06 预览帧 t=7.4 s #30 完整停在画面；第 2 轮独立审片实测 #30 可读约 3.3 s、滚动每帧 2 px

No conflicts found in: 默认 intro_hold=0，其他各期渲染行为不变；章节/标题/来源卡文字变化只在重新 publish / render 时生效


## Follow-up 012 — 2026-11-04 02:23:15
Source: user_input/follow_ups/202611.md - section 012
Summary: rank_scroll 封面：标题过长时两行换行；公司卡加 logo 牌

Auto-updated:
- projects/rank_scroll/rank_scroll/render.py render_thumb — 标题放不下时两行换行（不再省略号）；有 logo 的卡在数值药丸上方画 logo 白底牌（复用 cards._logo_plate）

验证: pytest 全过；ep03 封面重出，标题两行完整、OpenAI / Anthropic / DeepSeek 三张各带 logo，代理看图确认

No conflicts found in: 标题放得下的期（排名期）输出不变；无 logo 的期不画 logo 牌


## Follow-up 005 — 2026-11-03 21:26:21
Source: user_input/follow_ups/202611.md - section 005
Summary: rank_scroll 契约 v1.4：image_alt 顶替被扣下的风险图，许可白名单收 AI 生成图

Auto-updated:
- projects/rank_scroll/rank_scroll/contract.py（image_alt/image_alt_credit、AI-generated 白名单）、publish.py（署名按实际上屏图）、tests/test_rank_scroll.py、ai_videos/paihangbang/data_contract.md v1.4

验证: python -m pytest -q：25→31 passed；ep12/ep14/ep15/ep17 等实际用 image_alt 渲染通过 validate --strict

No conflicts found in: timeline/渲染时序未改；list 模式（follow-up 004）测试仍过


## Follow-up 010 — 2026-11-04 01:57:55
Source: user_input/follow_ups/202611.md - section 010
Summary: rank_scroll：AI 生成图卡片自动加 AI IMAGE 标记与「not a photo」署名

Auto-updated:
- rank_scroll/contract.py（Item.image_ai）、cards.py（AI IMAGE 黄标、署名「AI-generated image, not a photo」）、tests

验证: pytest 31 passed；ep14 重渲后抽帧可见标记

No conflicts found in: 实拍卡与风险版不显示；契约不变


## Follow-up 011 — 2026-11-04 02:05:36
Source: user_input/follow_ups/202611.md - section 011
Summary: rank_scroll：publish 章节在 N<50 时不再漏掉第一组

Auto-updated:
- rank_scroll/publish.py chapters()：第一组从 N 起；首组 <2 名并入下一组

验证: ep11(N=41)→Intro & #41–#31，ep15(N=35/36)、ep19(N=50) 章节正确；pytest 31 passed

No conflicts found in: N=50 输出与原来一致（ep02/ep19 对照）


## Follow-up 013 — 2026-11-04 02:25:37
Source: user_input/follow_ups/202611.md - section 013
Summary: rank_scroll publish：列表期文案与章节，头像署名

Auto-updated:
- projects/rank_scroll/rank_scroll/publish.py — 列表期：首句「N entries one by one, in order (not a ranking)」、章节按出场公司每 6 家一段 + 计分板 + 来源、标签去 #Ranking、序号不带 #；所有期：进片头像列入署名（简版 + 完整版）；data.json youtube_title 优先
projects/rank_scroll/rank_scroll/cards.py — 公司卡 AI 图署名不加 Photo: 前缀；名称与创始人说明间距 40 px

验证: pytest 31 passed；ep03 两版 publish 重出：标题 41 字符、5 段公司章节、默认版 10 条 / 签字版 30 条头像署名；排名期测试不变

No conflicts found in: 排名期文案与章节输出不变


## Follow-up 006 — 2026-11-03 21:31:35
Source: user_input/follow_ups/202611.md - section 006
Summary: 配乐改为先做音乐床：每首可设入点出点、末首对齐片尾自然结束、loudnorm 两遍线性

Auto-updated:
- projects/rank_scroll/rank_scroll/render.py; __main__.py; tests/test_rank_scroll.py; README.md; specs/development/rank_scroll/final_specs/spec.md FR9

验证: pytest 29 passed（新增 parse_track、music bed fit=end＋linear loudnorm、ai-generated 许可三项）；实渲两期四版，日志 music bed chain 362.8/383.8 s → -16 LUFS linear，成片 ebur128 I=-16.0

No conflicts found in: contract.py 的 ai-generated 前缀由另一会话已加，本次未改


## Follow-up 014 — 2026-11-04 04:47:06
Source: user_input/follow_ups/202611.md - section 014
Summary: 配乐拼接改为等功率交叉淡化（qsin），消除接缝处约 2 秒的音量下陷

Auto-updated:
- projects/rank_scroll/rank_scroll/render.py（build_music_bed acrossfade c1/c2 tri→qsin）

验证: pytest 31 passed；两期四版重渲中，第 6 轮独立审片测接缝响度

No conflicts found in: 只改曲线参数；其他剧集用 --music 的渲染不受影响以外的行为不变


## Follow-up 016 — 2026-11-07 00:00:20
Source: user_input/follow_ups/202611.md - section 016
Summary: 卡片主图新增 image_fit=contain（同图虚化填充）

Auto-updated:
- projects/rank_scroll/rank_scroll/draw.py — 新增 draw_contain（整图放入 + 同图 cover 放大模糊压暗填空，focus 决定放入位置）与 draw_photo（按 image_fit 分派）；draw_fit_portrait 改为调用 draw_contain
- projects/rank_scroll/rank_scroll/contract.py — Item.image_fit（默认 cover）；卡级可选字段 image_fit 校验，只允许 cover / contain
- projects/rank_scroll/rank_scroll/cards.py、styles.py — 卡片主图改经 D.draw_photo，未设 image_fit 的卡行为不变

验证: pytest projects/rank_scroll/tests 35 passed；用真实渲染器 card_image 出 ep18 的 7 张 contain 卡目检：整车完整、模糊填充正常，焦点 y=0.15 时车身在国旗与车名数值块之间；ep20 用默认 cover 重渲后抽帧正常

No conflicts found in: （未单独核查）


## Follow-up 017 — 2026-11-07 00:06:42
Source: user_input/follow_ups/202611.md - section 017
Summary: draw.wrap() 支持中日韩文字逐字断行（英文单词仍按词，不在行首放中文标点），修中文版洞察卡等多行文字溢出。

Auto-updated:
- rank_scroll/draw.py：wrap() 遇中日韩文字改走 wrap_cjk（逐字断行，拉丁词与数字不拆，中文标点不放行首）；英文断行不变

验证: pytest 35 passed；ep21 中文版 21 s 洞察卡预览帧四行正常换行不出框

No conflicts found in: 与同时进行的 016 image-fit-contain（另一会话）只同改 draw.py 不同函数，未触碰其改动


## Follow-up 018 — 2026-11-07 10:34:32
Source: user_input/follow_ups/202611.md - section 018
Summary: SPEED 3 px/帧；匀速段余数并入缓动段

Auto-updated:
- projects/rank_scroll/rank_scroll/timeline.py — SPEED 2→3 px/帧；Timeline.ease_dist = EASE_DIST + 匀速段余数，缓动帧数 2·ease_dist/SPEED（速度衔接不变），去掉「距离须整除」断言

验证: pytest 35 passed；17 期 timeline 全部构建（如 ep15 282.9→202.8 s、ep16/17 383→269.2 s）；6 期重渲抽帧目检卡片滚动正常、文字无闪烁

No conflicts found in: （未单独核查）


## Follow-up 015 — 2026-11-04 16:49:18
Source: user_input/follow_ups/202611.md - section 015
Summary: rank_scroll 中文版本地化（--lang zh）

Auto-updated:
- i18n.py（含 ai_credit）、draw.py（思源黑体按字重）、contract.py（lang、tally_labels、TW/HK/MO 全语言禁用）、render/cards/__main__ --lang

验证: pytest 35 passed；zh 渲染抽帧核对
费用: 无

No conflicts found in: 无

