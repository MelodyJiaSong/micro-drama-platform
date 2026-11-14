# k633_Frostmourne · 20261027-085146_c446ae86

第 3 轮（follow-up 279）。出片后闸门 `qc.py gate` **不通过**，不交用户、不进成片。三轮已满，带证据找用户。

## 结论（qc.json）
- video.slowmo：fail
- video.subject_count：pass
- video.no_text：fail
- video.timeline：fail
- video.scale：fail
- video.head_tail：fail
- video.agency：fail
- video.gaze：fail
- video.readability：fail
- video.fidelity：fail
- video.attack_contact：fail
- video.attack_tempo：fail
- video.slow_visible：fail

## 主代理归因
霜寒仍呈浅蓝白冰壳而非压暗深蓝；中招后树人移动没有明显变慢；开头镜头偏近、树人偏大；多剑接触看不清。

`video.no_text` 判 fail 是审稿人把拼图时间码当画面文字（审稿兜底，待 OCR 机检工具），属误报。首次 `motion_check` 在后台因中文路径编码报错，`video.slowmo` 曾被误记 pass，已用 UTF-8 重跑更正。
