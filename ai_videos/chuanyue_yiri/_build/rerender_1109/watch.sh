#!/bin/sh
# 等某场的 shot_take 进程结束，给该场所有今天的新条准备审片材料，然后打印 DONE <场>
cd /c/workspace/micro-drama-platform
D=ai_videos/chuanyue_yiri/_build/rerender_1109
S=$1; PID=$2
while tasklist //FI "PID eq $PID" 2>/dev/null | grep -q "$PID"; do sleep 30; done
for t in ai_videos/chuanyue_yiri/episodes/ep01/scenes/$S/shots/*/renders/20261109-*; do
  [ -f "$t/_review/transcript.txt" ] || python $D/prep.py "$t" >> $D/prep_$S.log 2>&1
done
echo "DONE $S $(grep -c '→' $D/$S.log) 条 / 失败 $(grep -c '✗' $D/$S.log)"
