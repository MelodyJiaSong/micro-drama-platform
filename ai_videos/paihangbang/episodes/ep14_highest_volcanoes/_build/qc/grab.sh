#!/bin/sh
# usage: grab.sh <mp4> <tag>
V=$1; T=$2; O=_build/qc/frames
for t in 2 4.5 $(seq 9 9 342) 347 350 354 357.5 360 366 378 ; do
  n=$(printf "%s_%06.1f" $T $t)
  ffmpeg -v error -y -ss $t -i "$V" -frames:v 1 -q:v 3 "$O/$n.jpg"
done
