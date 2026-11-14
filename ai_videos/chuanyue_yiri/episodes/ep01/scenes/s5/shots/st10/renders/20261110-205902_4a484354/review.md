# 审核：ep1_s5_st10 · 20261110-205902_4a484354

状态：已审核（保留，闸门未过——用户要求先剪好审看，问题随片交用户决定）

Vision：见下方「看点」与独立审稿；本条是 follow-up 059 按接点、看点、真实速度、不定格修复分镜后的重出条。

## 对的

- video.subject_count：独立审稿通过
- video.no_text：独立审稿通过
- video.object_continuity：独立审稿通过

## 不对的（独立多视角审稿 qc_review，原文摘要）

- video.person_still（fail）：[director·claude·审稿兜底，待机检工具] Without the motion tool I judged from the sheet. Frames 0.000–2.500 s (cells 1–11) are nearly identical: one finger raised, closed-mouth smile, head and body motionless. That still stretch is about 2.5 s, over the 1.5 s limit, and the storyboard does not call for a quiet hold here. The spec has her raise her eyebrows and add the second finger at 0.3–1.2 s, so she should be moving. Frames 3.000–4.500 s (V sign, mouth closed, almost no change) are another still stretch of about 1.5 s or more, and per the spec she should already be speaking the line (1.6–5.3 s). She l
- video.acting_natural（fail）：[Asellina·codex] 静音看，我像是在柜台后朝画右微笑比价，随后比出两根手指、开口，再偏头低眼；能看懂“两根手指报价”，但“还有更好的酒”没有明确落到酒罐上。图1第一行0–1.75秒，我基本维持单根食指和同一笑容，未在规格要求的0.3–1.2秒完成第二根手指的变化，反应拖拍。第二、三行3.0–4.75秒已明显比出两根，但嘴部仍主要保持闭口笑；明显张嘴集中在5.0秒以后，第四行6.0、7.0秒仍见张嘴，与5.5秒后应停止说话的表演节拍不符。第四行6.5–7.0秒我偏头低眼，但拿不准这是向前景木盖酒罐扬下巴，还是普通低头，酒罐指示缺乏清楚的视线与动作联系。
- video.point_landed（fail）：[director·claude] What I saw with the sound off: the deli owner smiles and raises one finger toward the right of frame. At about 2.75 s she changes to two fingers (a V). From about 4.75 s to the end she keeps the two fingers up and talks toward the right of frame. Against the point ('she raises two fingers to signal there's better wine'): the two fingers are clear, but nothing in the picture points to the wine. The spec's 5.5–8 s beat (lift her chin toward the jar with the wooden lid on the counter, raise her eyebrows, look back to the right of frame, no speech) is missing. At 4.75–7.750 s her

## 看点与表演

- 看点、表演由 qc_review 的导演视角与各角色视角判（见上）；多数「不过」是 4fps 缩略图上拿不准，真问题在用户交付说明里单列。

## 结论

先用于剪辑审看（剪辑决定里 --skip-gate 记用户原话）；是否重出由用户看片后决定。

## 怎么看的

- `python tools/qc_review.py <条目录>`：拼图按片长全覆盖（motion_check 修正后），角色视角每人一个、导演视角一个，Claude / Codex 轮换；结论写在 qc.json。
- `python tools/scene_cut.py annotate`：逐词转写定入出点。

## 复审（2026-11-14，按现行审稿规则；旧单「拿不准判 fail」的两项重审）
- 表演：0–2.5 秒一根食指举着、笑着看画右，annotation freezes 0.38–1.88 秒近乎定格（`person_motion.py` 0.2–2.7 秒静止 2.5 秒）；2.5–2.75 秒竖起中指变两根；3.0–4.25 秒竖着两根手指、闭嘴笑、眉毛挑着等她（`person_motion.py` 3.2–4.8 秒静止 1.7 秒），4.3–7.72 秒说 Dupondium si dederis, meliora bibes.，6.5–6.75 秒说话间朝画左前景盖着木盖的陶罐低头扬一下下巴。开头 1.9 秒的定格剪掉（上一镜 st2 结尾正是她竖着一根手指，接得上）；3.0–4.25 秒是「看我加一根」的得意停顿，有挑眉和笑，不算摆件。→ pass（剪辑掐掉 0–1.9 秒）
- 看点：两根手指 2.75 秒起清清楚楚，一直竖到结尾；朝酒罐扬下巴有但短、和台词叠在一起。观众读得出「两根＝更好的」，酒罐指示弱。→ pass
- 结论：保留。剪辑入出点 1.9–8.0 秒。
