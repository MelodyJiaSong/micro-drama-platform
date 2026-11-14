# m4 食尸鬼 · 原版声音参考（WC3 语音组 `Ghoul`）

> 暴雪娱乐版权素材：不进成片、不上传任何第三方生成服务。**例外（用户 2026-10-21 follow-up 044 决定，自担风险）**：本卡 `m4` 的台词声音可用这些文件作参考，在本地模型（MOSS-TTS-Local-Transformer-v1.5）做声音克隆，产出可对外使用；只限本地、只限 `m4`。正式发行前建议确认授权。2026-10-19 follow-up 038 下载（warcraft.wiki.gg 公开文件，免费，未调用收费服务）。同一组文件也在 `c70_Lifestealer/ref/audio/original/`。
> wiki 只收了下面 7 个；无词的应答（What1/3、Yes、YesAttack）、死亡与攻击音效没有公开文件（按常见文件名逐个试过，404）；YouTube 原声合集下架或要求登录，未取。

| 文件 | 内容 | 时长 | f0 中位数 | 频谱质心 | sha256 前 12 位 |
|---|---|---|---|---|---|
| GhoulWhat2.wav | "Wuzzap." | 1.17 s | 54.5 Hz | 1397 Hz | 665258168829 |
| GhoulWhat4.wav | "Must feed!" | 1.95 s | 53.0 Hz | 1321 Hz | 4c3d19cbcc07 |
| GhoulPissed1.wav | "Me eat dead people!" | 2.86 s | 58.4 Hz | 1276 Hz | 69c4b2e0e5c6 |
| GhoulPissed2.wav | "Me scary." | 2.16 s | 61.7 Hz | 1398 Hz | 5432027c7dc8 |
| GhoulPissed3.wav | "Me eat brains!" | 2.44 s | 57.9 Hz | 1398 Hz | f44a4ded7e1d |
| GhoulPissed4.wav | "No guts, no gory." | 3.09 s | 57.8 Hz | 1423 Hz | b94dca172770 |
| GhoulDinner.wav | 进食声（咀嚼撕扯，无人声） | 1.57 s | — | 1688 Hz | d72c94ee5987 |

URL：`https://warcraft.wiki.gg/images/{文件名}`。测量：librosa pyin（50–600 Hz，16 kHz），WC3 原声有变调与失真处理，f0 只作量级参考。

**结论**：原版是**极低（约 55–60 Hz）、粗砺带喉音颤（vocal fry）的蛙鸣式嗓音**，含糊的破碎英语、贪吃又蠢；不是尖利的嘶叫。旧卡写的「嘶哑尖利的喉音嘶叫」方向错（首条建立视频的声音即按此出，用户 follow-up 038 退回）。

## 拼接试听（2026-10-20，follow-up 042）

`m4_Ghoul_game_original_4s_不进成片_不挂建立视频.mp3`：GhoulWhat4（"Must feed!"）+ 0.2 s + GhoulDinner（啃食），48 kHz 单声道，响度归一到 −18 LUFS，补静音到 4.00 s。用户要「跟游戏原声一样」的 4 秒声音，按原声拼的试听片；仍是暴雪素材：不进成片、不上传生成服务（文件名带「不挂建立视频」，`gen_turntable_videos.py` 不会挂）。
