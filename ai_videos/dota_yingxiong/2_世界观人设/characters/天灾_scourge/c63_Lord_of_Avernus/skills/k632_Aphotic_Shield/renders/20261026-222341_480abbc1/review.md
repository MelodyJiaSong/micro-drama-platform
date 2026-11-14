# k632_Aphotic_Shield · 20261026-222341_480abbc1

第 2 轮（follow-up 269）。出片后闸门 `qc.py gate` **不通过**，不交用户、不进成片。

## 结论（qc.json）
- video.slowmo：pass
- video.onetake_cuts：pass
- video.subject_count：fail
- video.no_text：pass
- video.timeline：fail
- video.scale：fail
- video.head_tail：pass
- video.agency：fail
- video.gaze：fail
- video.readability：pass
- video.fidelity：fail
- video.attack_contact：fail

## 主代理归因
一镜到底、冷蓝色都对了；但树人偏大把骑手围住看不见，护盾 4.25 s 才成形且把树人也罩进去，砍中与视线看不清。

`video.no_text` 若判 fail，是审稿人把拼图左上角的时间码当成画面文字（审稿兜底，待机检工具），属误报。
