# -*- coding: utf-8 -*-
"""ep06 配乐底轨：Suno 任务 a5d954a2 的两首（A 2:55、B 1:33）手工拼成一条与成片等长的 WAV。

为什么不用渲染器默认的 4 s 交叉淡化（独立音频审片 _build/qc_audio_independent.md）：
A 的最后约 4 s 是收尾停顿 + 几下重击、2:53.5 硬停，4 s 叠化正好叠在上面，造成约 4.5 s 的响度凹陷（-15 → -18.3 LUFS），
且 A≈154 BPM、B≈159 BPM，重叠时鼓点错位。改为：A 放到硬停后（173.757 s），0.4 s 等功率交叉淡化接 B，
B 从 48.69 s 的一下鼓击开始，放到自己的结尾，总长正好 = 视频 217.467 s。

    python ai_videos/paihangbang/episodes/ep06_best_selling_manga/_build/08_music_bed.py
    python -m rank_scroll render <ep> [--allow-risk-images] --music <ep>/assets/music/ep06_music_bed.wav
"""
import subprocess
from pathlib import Path

M = Path(__file__).resolve().parents[1] / "assets" / "music"
A = M / "5a56b2fa-a6ff-4b9b-a0ac-d4ad197490a3.mp3"
B = M / "88a650ad-4708-4def-a68e-053ea1afca1f.mp3"
A_END, B_START, XFADE = 173.757, 48.69, 0.4

subprocess.run([
    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(A), "-i", str(B), "-filter_complex",
    f"[0:a]atrim=0:{A_END},asetpts=PTS-STARTPTS[a];[1:a]atrim=start={B_START},asetpts=PTS-STARTPTS[b];"
    f"[a][b]acrossfade=d={XFADE}:c1=qsin:c2=qsin[out]",
    "-map", "[out]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(M / "ep06_music_bed.wav"),
], check=True)
print(M / "ep06_music_bed.wav")
