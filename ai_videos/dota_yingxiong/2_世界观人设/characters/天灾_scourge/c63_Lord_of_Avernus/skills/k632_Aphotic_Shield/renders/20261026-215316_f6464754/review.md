# k632_Aphotic_Shield · 20261026-215316_f6464754

第 1 轮（follow-up 269）。出片后闸门 `qc.py gate` **不通过**，不交用户、不进成片。

## 结论（qc.json）
- video.slowmo：pass
- video.onetake_cuts：fail
- video.subject_count：fail
- video.no_text：pass
- video.timeline：fail
- video.scale：fail
- video.head_tail：pass
- video.agency：fail
- video.gaze：fail
- video.readability：fail
- video.fidelity：fail
- video.attack_contact：fail
- video.stun_visible：fail

## 主代理归因
3.88 s 硬切到「盾里出剑」参考帧的取景；开场砍中处橙红光；放盾晚约 2 s。处理：撤掉取景不同的参考帧、负面词加橙红 / 火光。

`video.no_text` 若判 fail，是审稿人把拼图左上角的时间码当成画面文字（审稿兜底，待机检工具），属误报。
