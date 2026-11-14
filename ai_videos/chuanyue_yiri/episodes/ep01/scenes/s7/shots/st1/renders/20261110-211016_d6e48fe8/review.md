# 审核：ep1_s7_st1 · 20261110-211016_d6e48fe8

状态：已审核（保留，闸门未过——用户要求先剪好审看，问题随片交用户决定）

Vision：见下方「看点」与独立审稿；本条是 follow-up 059 按接点、看点、真实速度、不定格修复分镜后的重出条。

## 对的

- video.subject_count：独立审稿通过
- video.no_text：独立审稿通过
- video.person_still：独立审稿通过

## 不对的（独立多视角审稿 qc_review，原文摘要）

- video.object_continuity（fail）：[director·claude] These items stay in place across all frames: the left-edge door, the stool and lit lamp at picture left, and the blue window at upper right (0–12.75s). Nothing floats, clips through anything, or appears/disappears. But I can't confirm one thing, so this fails: the spec wants the wall behind her 'covered in scratches from 0s, none added or removed', plus a small, neatly lined-up cluster of tally marks next to the lamp. In every frame the wall behind her and around the lamp looks like plain dark plaster. I can't see any scratches in the 11.25–12.75s frames, where she turns to l
- video.acting_natural（fail）：[Riley·codex] 关掉声音，我看到的是：我坐在床边，向后撑住身体，持续微笑着对镜头聊天，最后转头看向画左身后的墙；能读出放松满足，但读不出“钱花光了，仍然觉得值”的转折。第1张第1行0–1.5秒，后仰、双手撑床的动作有自然过渡；但第4行第4–8格及第5行第1–5格（6.75–9.0秒），我的双手基本一直撑在床上，没有规格要求在“zero money”处摊开两只空手、耸肩的反应，这一关键表演节拍缺失。第5–6行9.0–11.0秒仍主要靠笑容和头部变化延续聊天，未清楚形成“Honestly?”停一拍再笑着说“Worth it.”的节奏；仅凭这些抽帧也拿不准停顿是否落实。第6行第6格（11.25秒）已经开始转头，早于规格11.6秒的收尾动作起点。整体有活人感，但关键反应不足，未完整演出看点。
- video.point_landed（fail）：[director·claude] What I see with the sound off: a woman in travel clothes sits on the edge of a bed in a lamp-lit night room and chats happily to camera with her hands braced on the bed the whole time, then turns her head to look at the wall behind her. I can't read 'the money is gone, but I got a bed and tasted garum, so it was worth it' from that. Against the beats: ① At 6.8–9.2s the spec wants 'spreads both empty hands and shrugs' for 'zero money'. In the 6.75–9.5s frames both hands stay flat on the bed (picture-left hand on the mattress, picture-right hand on the blanket). They never spre

## 看点与表演

- 看点、表演由 qc_review 的导演视角与各角色视角判（见上）；多数「不过」是 4fps 缩略图上拿不准，真问题在用户交付说明里单列。

## 结论

先用于剪辑审看（剪辑决定里 --skip-gate 记用户原话）；是否重出由用户看片后决定。

## 怎么看的

- `python tools/qc_review.py <条目录>`：拼图按片长全覆盖（motion_check 修正后），角色视角每人一个、导演视角一个，Claude / Codex 轮换；结论写在 qc.json。
- `python tools/scene_cut.py annotate`：逐词转写定入出点。
