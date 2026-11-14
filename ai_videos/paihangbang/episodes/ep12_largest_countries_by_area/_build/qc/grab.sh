#!/bin/sh
# QC 抽帧：$1 = 视频，$2 = 输出前缀，其余 = 时间点（秒）
v=$1; p=$2; shift 2
for t in "$@"; do ffmpeg -v error -y -ss "$t" -i "$v" -frames:v 1 "_build/qc/frames/${p}_t$(printf '%06.2f' $t).png"; done
