# k633_Frostmourne · 20261026-222241_7ad6ea6a

第 2 轮（follow-up 269）。出片后闸门 `qc.py gate` **不通过**，不交用户、不进成片。

## 结论（qc.json）
- video.slowmo：pass
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

## 主代理归因
逃跑与追砍做到；但开头仍贴近、树人比骑手大，霜仍偏冰白，10.55 s 疑似切镜，多剑看不清是否砍中。

`video.no_text` 若判 fail，是审稿人把拼图左上角的时间码当成画面文字（审稿兜底，待机检工具），属误报。
