# 审核：ep1_s5_st7 · 20261110-210022_03a34e9e

状态：已审核（保留，闸门未过——用户要求先剪好审看，问题随片交用户决定）

Vision：见下方「看点」与独立审稿；本条是 follow-up 059 按接点、看点、真实速度、不定格修复分镜后的重出条。

## 对的

- video.no_text：独立审稿通过

## 不对的（独立多视角审稿 qc_review，原文摘要）

- video.subject_count（fail）：[director·codex] 图1的0.00、7.00、13.75秒格均能辨认两名主角；但中间偏右、灶台后方的暗部无法可靠分辨出规格要求的两名吃喝男子，也无法逐格确认他们始终在场。人数及其连续性拿不准。
- video.object_continuity（fail）：[director·codex] 图1约11.25–12.00秒，Asellina手中出现浅色抹布并开始擦拭；此前各格无法清楚定位规格所写的“收钱碗旁叠放的抹布”，拿取过程及来源无法可靠追踪。不能排除道具凭空出现，按拿不准判fail。
- video.person_still（fail）：[director·codex·审稿兜底，待机检工具] 图1的5.00–7.50秒连续多格中，Asellina的站姿、持勺手臂和头部姿态基本不变，未见可辨认的摇头或搅拌，呈持续超过1.5秒的陪站状态。这段对应规格要求她“看着Riley摇头笑笑，用勺子搅一搅”，不属于指定的安静停顿拍。
- video.acting_natural（fail）：[Riley·codex] 静音看，我在尝过食物后满意地举杯，转向观众、抬指示意，再喝酒并望向画右；能看懂“吃得满足”，看不出“接下来还得找床”。只看 Riley：图1中0–1.25秒舔手指，1.5–3秒取杯举起，4–4.75秒转向镜头，6–7.25秒抬左手示意，动作基本连贯。但图1第5行第7格（9.5秒）至第6行第6格（11.25秒），我已把杯口持续贴在嘴前饮酒；规格此时要求7.5–10.7秒仍对镜头说第二句，10.9秒才开始喝。这使规定的说话与饮酒动作发生冲突。仅凭拼图无法确认第二句是否提前、漏说或在饮酒时继续，无法确认这段表演自然衔接，判 fail。；[Asellina·claude] Judged from my own part (Asellina, frame left) on sheet 1. The spec has me raise my ladle in a toast during 3–4 s, stir the open pot while Riley speaks, then wipe the spill by the cup and look up to smile at her. Some of this works. From 0–2.75 s I hold the ladle and watch Riley with a smile. At abo
- video.point_landed（fail）：[director·codex] 关声音看到的是：Riley舔手指、与老板娘举杯致意，转向镜头微笑并比划，随后饮酒、望向画右。满足感成立；但看不出“鱼露这一关过了”及“接下来还得找床”，只能辨认吃喝后的满足和对镜讲话。此外图1约9.25–10.75秒已举杯到嘴边饮用，侵入规格7.5–10.7秒的第二句对白拍；规格要求10.9秒后才喝酒。

## 看点与表演

- 看点、表演由 qc_review 的导演视角与各角色视角判（见上）；多数「不过」是 4fps 缩略图上拿不准，真问题在用户交付说明里单列。

## 结论

先用于剪辑审看（剪辑决定里 --skip-gate 记用户原话）；是否重出由用户看片后决定。

## 怎么看的

- `python tools/qc_review.py <条目录>`：拼图按片长全覆盖（motion_check 修正后），角色视角每人一个、导演视角一个，Claude / Codex 轮换；结论写在 qc.json。
- `python tools/scene_cut.py annotate`：逐词转写定入出点。
