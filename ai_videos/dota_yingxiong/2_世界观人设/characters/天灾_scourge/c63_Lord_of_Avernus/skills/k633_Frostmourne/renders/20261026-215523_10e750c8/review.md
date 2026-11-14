# k633_Frostmourne · 20261026-215523_10e750c8

第 1 轮（follow-up 269）。出片后闸门 `qc.py gate` **不通过**，不交用户、不进成片。

## 结论（qc.json）
- video.slowmo：pass
- video.subject_count：pass
- video.no_text：pass
- video.timeline：fail
- video.scale：fail
- video.head_tail：fail
- video.agency：fail
- video.gaze：fail
- video.readability：fail
- video.fidelity：fail
- video.attack_contact：fail
- video.stun_visible：fail

## 主代理归因
前 5 s 镜头贴近、树人比骑手大；霜成冰白色；没有明显逃跑。处理：镜头锁侧面中景、霜压暗、负面词加特写 / 绕背 / 冰白。

`video.no_text` 若判 fail，是审稿人把拼图左上角的时间码当成画面文字（审稿兜底，待机检工具），属误报。
