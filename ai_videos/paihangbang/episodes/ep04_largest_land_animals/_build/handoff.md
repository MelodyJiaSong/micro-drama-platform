# ep04 交接（2026-11-04 夜间自主推进，follow-up 039）

## 现在能看的
- **默认母版**（可商用图）：`render/ep04_largest_land_animals_master.mp4`，4:16，**带正式配乐**（Suno 任务 101bce70 两首纯音乐 B→A，4 s 交叉淡化、片尾随曲子自然收尾，−16 LUFS；2026-11-04 用 `_build/add_music.py` 补音轨，视频流原样复制，没重渲）。
- **风险图版**：`render/ep04_largest_land_animals_master_with-risk-images.mp4`，爪哇犀 #7、野牦牛 #11 用许可未知的野外照，同一配乐。
- 原曲在 `assets/music/`；描述框已加 Music 署名。临时配乐审片版（借 ep12 曲）已删除。
- 缩略图 `render/thumbnail.png`；上传文案 `publish.md`（风险版 `publish_with-risk-images.md`）；审片记录 `qc.md`。
- 审片：三轮独立审片 + 第 4 轮独立复核（画面「可发布」）+ 配乐独立审片（`qc.md` 末尾）。

## 配乐备注
- 顺序 B→A（第 1 轮配乐审片 AU-M1：原 A→B 让 A 的尾声落在前 10 名中段，形成约 17 s 能量洞）。现在 B 播 0–149.73 s，A 从 71.8 s（乐句重新进入处）切入、播到自身结尾，正好对齐片尾；接点约 2:26–2:30，紧挨前 10 名开始。
- 分段响度：#30–21 −19.0、#20–11 −15.8、前 10 名前半 −15.9 / 后半 −14.0、冠军 −14.1、计分板与片尾 −18.9 LUFS（全片 −16.0，真峰值约 −5 dBFS）。
- 建议你人耳听：2:24–2:32 接点（两首速度不同）、3:40 前后冠军揭晓。
- 不满意可重混，约 5 秒、不重渲：`python _build/add_music.py <母版> --fit end "B.mp3@:149.73" A.mp3`（`@IN:OUT` 指定入出点）。
- 原任务 `51842da5…` 提交超时 → 库里按标题认领 1.5 小时没找到，判为没生成，所以另建了 v2（判断记在 `qc.md`「配乐记录」）。

## 发布前要你定
1. 爪哇犀、野牦牛两张野外照许可未知（WWF Italia / Stephen Belcher；Coke Smith）。默认版用博物馆标本图（Commons，CC BY-SA 4.0 / CC BY 2.0，你特许的例外）。选风险版就用 `publish_with-risk-images.md`（取得授权后按对方要求改署名）。
2. 非洲森林象取 2,000 kg（Larramendi 2016，唯一给出方法的来源；卡上标「Estimate: none weighed」）。取 4,500 kg 会升到第 3–4 名。
3. 低可信度的国旗归属：长颈鹿、巨羚、邦戈、普通大羚羊、欧洲野牛（`topic.md`）。
4. 邦戈照片是美国动物园圈养个体（找不到可商用野外照），账本已注明。
5. Gaur 的雄性范围 588–1500 kg 出自 Walker's，经维基转读（tier=secondary），找不到一手出处；卡上首位标「Estimates: 650–1,500 kg」，描述框也写明是估计值。
6. 时长 4:16，比 bible 建议的 5–8 分钟短（Top 30 是你定的）。
