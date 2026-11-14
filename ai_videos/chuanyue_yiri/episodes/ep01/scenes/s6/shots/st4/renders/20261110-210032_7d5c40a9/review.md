# 审核：ep1_s6_st4 · 20261110-210032_7d5c40a9

状态：已审核（保留）

Vision：见下方「看点」与独立审稿；本条是 follow-up 059 按接点、看点、真实速度、不定格修复分镜后的重出条。

## 对的

- video.subject_count：独立审稿通过
- video.no_text：独立审稿通过

## 不对的（独立多视角审稿 qc_review，原文摘要）

- video.object_continuity（fail）：[director·claude] The bright lamp point stays at her right hand, roughly at chest height, in every cell from 0.000 to 8.750 s. The lamp never drops, floats or vanishes, and no extra props show up. But the cells are too small for me to confirm the spec's lamp details: a red-ochre clay body, one spout with a single small flame, and her index finger through the ring handle. I also can't tell whether her left hand is held up shielding the outer side of the flame. In frames 0–2.0 s the light reads as a small patch of glow, and I can't rule out several flame points or a lamp of the wrong shape. Unce
- video.person_still（fail）：[director·claude·审稿兜底，待机检工具] From 0 to about 4.0 s she clearly climbs from the lower steps to near the top of the stairs. From 4.0 to 8.75 s (rows 3–5) her position in the frame hardly changes: her head stays near the top of each cell at about x≈105–125 px. At this resolution I can't tell whether she is still climbing or standing at the top. The spec's quiet beat is a stop at 2.5–4.5 s to look back, not a stop after 4.5 s. A standstill of more than 1.5 s anywhere in 4.5–8.75 s would be a mannequin moment. Uncertain, so I'm failing this. Run person_motion.py on that window and re-check.
- video.acting_natural（fail）：[Riley·codex] 关掉声音，我看到的是自己双手举在胸前附近、持着暖光沿左侧楼梯缓慢上行，能读到看点中的‘持灯爬楼’，但护火和受惊回望的表演不够明确。0–2.5秒（第1行至第2行第3格），我在逐渐升高，但手部太小、偏暗，无法确认左手持续在火苗外侧自然挡风。2.5–4.5秒（第2行第3格至第3行第3格）是规格要求我停步并朝画面右下方看的一拍，拼图中看不清明确的停步、转头和视线落点，无法确认这次反应是否完成、是否及时。4.5–8.75秒（第3行第3格至第5行第4格）我继续向楼梯上部移动，但转回后重新起步的动作分界也不清楚。关键反应与护火动作均拿不准，按要求判fail。
- video.point_landed（fail）：[director·claude] Watched with the sound off: at deep dusk with a blue-purple sky, a woman holding a small oil lamp climbs a stone staircase along a courtyard wall. The lamp lights up an orange patch of the wall, and the stairs run from lower left toward the upper middle of the frame. The main idea of the shot, 'she shields the flame and climbs the stone stairs one step at a time', partly comes across. But several required beats don't land. (1) The spec says that at 2.5–4.5 s she stops and looks back toward the lower right of the frame, with her profile lit. In cells 2.500–4.500 s she doesn't 

## 看点与表演

- 看点、表演由 qc_review 的导演视角与各角色视角判（见上）；多数「不过」是 4fps 缩略图上拿不准，真问题在用户交付说明里单列。

## 结论

先用于剪辑审看（剪辑决定里 --skip-gate 记用户原话）；是否重出由用户看片后决定。

## 怎么看的

- `python tools/qc_review.py <条目录>`：拼图按片长全覆盖（motion_check 修正后），角色视角每人一个、导演视角一个，Claude / Codex 轮换；结论写在 qc.json。
- `python tools/scene_cut.py annotate`：逐词转写定入出点。

## 重审（2026-11-14，按现行审稿规则）
状态更新：已审核（保留）。全分辨率看 _review/climb_1fps.jpg（每秒一格）与 _review/lamp.jpg（0.5/2/4.5/5.5/7.5 秒灯与手放大）：灯一直在右手掌上点着、只有一朵火苗，左手立在火苗外侧挡风；0–3 秒上楼，约 4.5–5.5 秒回头往画面右下方看一眼，6–8.75 秒继续上楼出画面上缘；没有凭空出现消失、悬空、多指、分身。看点「护着火苗一级级爬上石楼梯」落地。与现行分镜的差距：少了拐进二楼走廊、灯光沿走廊远去的尾拍（本条 9 秒，现行分镜 12 秒），分诊时归③保留；整集审看时如果觉得场尾太急再交用户定。
剪辑建议入出点：0.0–9.0 秒（全条）。
