# 审核：ep1_s2_st1 · 20261110-205108_1bfc9fa8

状态：已审核（保留，闸门未过——用户要求先剪好审看，问题随片交用户决定）

Vision：见下方「看点」与独立审稿；本条是 follow-up 059 按接点、看点、真实速度、不定格修复分镜后的重出条。

## 对的

- video.subject_count：独立审稿通过
- video.no_text：独立审稿通过
- video.object_continuity：独立审稿通过
- video.person_still：独立审稿通过
- video.acting_natural：独立审稿通过

## 不对的（独立多视角审稿 qc_review，原文摘要）

- video.point_landed（fail）：[director·claude] With the sound off, this shot shows a low camera filming the legs of a woman in khaki trousers and brown boots. She steps from the raised kerb on the left onto three stone blocks and crosses to the right, while water splashes up around the stones and runs past them. That broadly matches the point "cross the street on stepping stones, boots stay dry." It still fails for these reasons. (1) The timing is about a second behind the spec. The spec has her stepping onto the right pavement at 1.5–2s, with the camera stopping at 2s on stone 3 and the right kerb. In the frames she is s

## 看点与表演

- 看点、表演由 qc_review 的导演视角与各角色视角判（见上）；多数「不过」是 4fps 缩略图上拿不准，真问题在用户交付说明里单列。
- 主会话补充：主会话看了 4fps 全条：约 1.5 秒连跨三块干石头（每步约 0.5 秒），满街流水绕过石头、漂着菜叶，落脚处不溅水；水比分镜写的浅、颜色偏灰，看点基本读得出。

## 结论

先用于剪辑审看（剪辑决定里 --skip-gate 记用户原话）；是否重出由用户看片后决定。

## 怎么看的

- `python tools/qc_review.py <条目录>`：拼图按片长全覆盖（motion_check 修正后），角色视角每人一个、导演视角一个，Claude / Codex 轮换；结论写在 qc.json。
- `python tools/scene_cut.py annotate`：逐词转写定入出点。
