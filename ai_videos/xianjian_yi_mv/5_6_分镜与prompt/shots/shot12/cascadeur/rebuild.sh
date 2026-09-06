#!/usr/bin/env bash
# shot12 Cascadeur 全量重建：落地段 → 第一幕各 STAGE → 第二幕各 STAGE → 存盘 → 拷回 shot 目录 → 导 FBX。
# 每个 STAGE 单独投递（脚本服务器 30s 超时）。脚本先拷到 ASCII 临时目录再 exec（Cascadeur 读不了中文路径）。
# 用法（仓库根目录）：bash "ai_videos/xianjian_yi_mv/5_6_分镜与prompt/shots/shot12/cascadeur/rebuild.sh" [scratch_dir]
# 前置：Cascadeur 已开且脚本服务器在 127.0.0.1:8765（否则先 bash tools/cascadeur/casc_restart.sh）。
set -u
ROOT="C:/workspace/micro-drama-platform"
D="$ROOT/ai_videos/xianjian_yi_mv/5_6_分镜与prompt/shots/shot12/cascadeur"
S="${1:-$LOCALAPPDATA/Temp/casc_shot12}"
mkdir -p "$S"
SW=$(cygpath -w "$S")
LIB="C:\\workspace\\micro-drama-platform\\tools\\cascadeur\\casc_lib.py"
RUN="python $ROOT/tools/cascadeur/casc_run.py"

# 脚本服务器不在线就先拉起（Cascadeur 常在空闲一段时间后自己退出）
if ! curl -s -m 3 http://127.0.0.1:8765/ >/dev/null 2>&1; then echo "== cascadeur not answering, restarting =="; bash "$ROOT/tools/cascadeur/casc_restart.sh" 2>&1 | tail -1; fi

cp "$D"/shot12_cascadeur_*.py "$S/"
for f in jianzhi_l_cascy.json hands_lr_cascy.json relax_lr.json base_points.json; do
  [ -f "$S/$f" ] || cp "$D/act1_0-15s/$f" "$S/$f" 2>/dev/null || true
done
: > "$S/build.log"

COMMON="LIB=r'$LIB'; JZ_L=r'$SW\\jianzhi_l_cascy.json'; FALL_SCRIPT=r'$SW\\shot12_cascadeur_fall.py'; ACT1_SCRIPT=r'$SW\\shot12_cascadeur_act1.py'; OUT_DIR=r'$SW'; HANDS_JSON_IN=r'$SW\\hands_lr_cascy.json'; CUBE_NATIVE=100.0"

run_stage() {  # $1 = script basename, $2 = STAGE
  local out
  [ "$2" = "wrists" ] || [ "$2" = "wrists2" ] && sleep 5     # 插值改完后台重算时间轴，等它落定再做逐帧校直
  out=$($RUN -c "$COMMON; STAGE='$2'
exec(open(r'$SW\\$1', encoding='utf-8').read())" 2>&1)
  if echo "$out" | grep -qE "Traceback|Error"; then
    echo "!! $1 / $2 failed:"; echo "$out" | grep -E "Traceback|Error|File " | head -8; return 1
  fi
  echo "ok  $1 / $2   $(tail -1 "$S/build.log" 2>/dev/null | cut -c1-70)"
}

echo "== load Cascy =="
out=$($RUN -c "LIB=r'$LIB'; exec(open(LIB, encoding='utf-8').read()); reload_scene(r'C:\Program Files\Cascadeur\samples\Cascy.casc'); print('loaded')" 2>&1)
echo "$out" | grep -q loaded || { echo "!! load Cascy failed"; echo "$out" | tail -4; exit 1; }
echo "== fall =="
out=$($RUN -c "$COMMON; SKIP_RELOAD=True; NO_SAVE=True
exec(open(FALL_SCRIPT, encoding='utf-8').read())" 2>&1)
echo "$out" | grep -qE "Traceback|Error" && { echo "!! fall failed"; echo "$out" | grep -E "Traceback|Error|File " | head -8; exit 1; }
echo "ok  fall   $(echo "$out" | grep -o 'check:.*' | cut -c1-80)"

for st in hands body1 body2 body3 gourd interp wrists finish; do run_stage shot12_cascadeur_act1.py $st || exit 1; done
for st in body2a body2b sword interp wrists2 finish; do run_stage shot12_cascadeur_act2.py $st || exit 1; done

newest=$(ls -t "$S"/shot12_full_*.casc | head -1)
cp "$newest" "$D/full_0-27s/shot12_full.casc" && echo "casc -> full_0-27s/shot12_full.casc ($(basename "$newest"))"
$RUN -c "LIB=r'$LIB'; exec(open(LIB, encoding='utf-8').read())
print('frames', scene.layers_viewer().frames_count()); print('fbx ->', export_fbx(r'$SW\\shot12_full.fbx', 'export_all_objects'))" 2>&1 | grep -E "frames|fbx|Error"
cp "$S/shot12_full.fbx" "$D/full_0-27s/shot12_full.fbx" && echo "fbx  -> full_0-27s/shot12_full.fbx"
