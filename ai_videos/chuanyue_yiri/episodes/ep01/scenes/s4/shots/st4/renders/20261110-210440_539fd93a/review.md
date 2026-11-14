# 审核：ep1_s4_st4 · 20261110-210440_539fd93a

状态：已审核（保留，闸门未过——用户要求先剪好审看，问题随片交用户决定）

Vision：见下方「看点」与独立审稿；本条是 follow-up 059 按接点、看点、真实速度、不定格修复分镜后的重出条。

## 对的

- video.subject_count：独立审稿通过
- video.no_text：独立审稿通过

## 不对的（独立多视角审稿 qc_review，原文摘要）

- video.object_continuity（fail）：[director·claude] (1) The spec's 0s beat requires a cat asleep on the stone step of the northeast corner shop, on the right of frame. In the 00:00.000–00:03.750 cells the right side shows a yellow wall, a dark doorway and a pottery jar. I could not find a cat there or in any later wide cell (for example 06.000 and 10.000), so a required prop is missing. (2) The bread cloth bundle should hang on her left hip, visible whenever she is full-body in frame. In the 0–3s full-body shots the figure is too small to tell. From 16–21s there is a beige tied lump at the front or side of her waist (for examp
- video.person_still（fail）：[director·claude·审稿兜底，待机检工具] From 00:06.000 to 00:13.750, about 8 seconds, Riley stands upright in the same spot. In every cell her arms hang at her sides, she makes no gestures, and her full-body pose barely changes. Only the camera's slow push-in changes the framing. The spec has her speaking in this stretch (4.7–13.6s: 'Okay, so… everything's closed… nap time… no idea where I am'), so it is not a scripted quiet beat. At 4fps thumbnail resolution I can't confirm her mouth is moving in sync with the lines, and her body is still well past 1.5s. She reads as a standing figurine, so I fail this 
- video.acting_natural（fail）：[Riley·codex] 静音看：我走进空路口、左右观察，面对镜头停留，随后闻袖口、在鼻前扇手，最后笑着摊手；能读出困惑和嫌弃气味，但仅凭表演不能明确读出“彻底迷路、身上还有尿味”。表演问题：图1第8行第4–8格（14.75–15.75秒），我抬臂后持续把脸埋向右臂；第9行第1–4格（16–16.75秒）还在鼻前举手、偏头，到17秒才恢复正面，闻味反应拖过规格14–16秒这一拍，挤占恢复对白的动作节奏。图1第11行第4–5格（20.75–21秒）我已双手摊开，第7格（21.5秒）收下，第8格（21.75秒）又向外摊手，同一个无奈梗出现重复起势；无法从拼图确认第二次起势是否有新的表演动机，按拿不准判fail。
- video.point_landed（fail）：[director·claude] With the sound off, here is what I see: a woman walks in from deep in a warm-coloured old street to an empty square where every door is closed. She looks left and right, stands talking to the camera for a long stretch, raises her arm and sniffs her shoulder (14.75–15.75), raises a hand by her face (16.0–16.5), then turns back, spreads her arms in a shrug and smiles (20.5–21.0). The 'stuck in an empty town' idea and the 'smelly sleeve' gag partly come through. Compared against the point and the beats: (1) 'Four identical streets' doesn't land. The camera only ever sees the nor

## 看点与表演

- 看点、表演由 qc_review 的导演视角与各角色视角判（见上）；多数「不过」是 4fps 缩略图上拿不准，真问题在用户交付说明里单列。

## 结论

先用于剪辑审看（剪辑决定里 --skip-gate 记用户原话）；是否重出由用户看片后决定。

## 怎么看的

- `python tools/qc_review.py <条目录>`：拼图按片长全覆盖（motion_check 修正后），角色视角每人一个、导演视角一个，Claude / Codex 轮换；结论写在 qc.json。
- `python tools/scene_cut.py annotate`：逐词转写定入出点。
