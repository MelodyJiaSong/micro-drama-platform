"""Independently inspect a hash-bound map draft without releasing its asset library."""
from pathlib import Path
import argparse,json,sys,hashlib,tempfile,datetime,time
ROOT=Path(__file__).resolve().parents[3];REPO=ROOT.parents[1];OUT=next(ROOT.glob('2_*'))/'background/map_3d';sys.path.insert(0,str(REPO/'tools'));import qc_review
p=argparse.ArgumentParser();p.add_argument('--blend',required=True);args=p.parse_args();blend=OUT/args.blend;stem=blend.stem;reportpath=OUT/(stem+'_environment_review.json')
if reportpath.exists():raise FileExistsError(reportpath)
refs=[ROOT/'0_research/base_layout_refs/map_683d_original.png'];views=['Map_Overview','Sentinel_Forest_Eye','Mid_River','Sentinel_Base','Scourge_Base'];renders=[OUT/f'{stem}_{name}.png' for name in views];deadline=time.monotonic()+3600
while not all(p.exists() for p in renders):
 if time.monotonic()>deadline:raise TimeoutError('Missing map views')
 time.sleep(20)
summary=json.loads((OUT/(stem+'_report.json')).read_text(encoding='utf-8'));settings_files=[OUT/f'{stem}_{name}_render_settings.json' for name in views if (OUT/f'{stem}_{name}_render_settings.json').exists()];settings={p.name:json.loads(p.read_text(encoding='utf-8')) for p in settings_files};evidence=[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in refs+renders+settings_files];blend_hash=hashlib.sha256(blend.read_bytes()).hexdigest()
water_audit=None;drafts=json.loads((OUT/'draft_refresh_state.json').read_text(encoding='utf-8')).get('drafts',[])
selected=next((d for d in drafts if d.get('file')==args.blend),None)
if selected:
 water_path=OUT/(Path(selected['environment']).stem+'_water_footprint_audit.json')
 if not water_path.exists():water_path=OUT/'original_water_footprint_audit.json'
 if water_path.exists():
  candidate=json.loads(water_path.read_text(encoding='utf-8'))
  if selected['environment']==candidate.get('current_environment'):
   water_audit=candidate;evidence.append({'path':str(water_path.relative_to(ROOT)),'sha256':hashlib.sha256(water_path.read_bytes()).hexdigest()})
prompt=f'''你是独立三维环境审稿人。目标是以 DotA 6.83d 地图为布局基础，搭建精细、真实、可拍电影的完整 Blender 地图。第一张是原版游戏布局参考，后五张是当前地图的总览、近卫林地人眼视角、中路河流、近卫基地、天灾基地。原版卡通渲染只用于空间布局和阵营识别，不是目标材质风格。
请逐图检查：地形和河岸是否自然、有真实尺度和厚度；植被、道路、水面、岩壁及地表是否达到写实镜头需要；两个阵营环境是否可辨；是否有明显漂浮、穿插、重复图案、方块轮廓、断层、空洞；近景、中景与总览分别有什么具体缺陷。不要把“有真实3D网格”当作外观合格。有限图像不能证明导航、碰撞、拓扑、布置坐标一致，明确列出未验证。
这是内部工作图，尚缺 {len(summary['missing_assets'])} 类模型，已装入 {summary['asset_library_count']} 类候选；单体建筑和NPC另有独立审稿。本轮请主要审环境与空间整合，缺少的单体和单体细节无需逐个重复，但若单体尺度、地基接地或遮挡环境有明显问题仍应报告。本轮通过也不代表整图可交付。
渲染设置覆盖（有记录的视角）：{json.dumps(settings,ensure_ascii=False)}。2048 贴图采样上限仅用于 1200×900 环境预览，源贴图与几何保持原件；不能据此验证原贴图近摄精度。
原版 W3E 与当前环境的水域抽样核对：{json.dumps(water_audit,ensure_ascii=False)}。如有数据，请同时考虑主河道与分离水域的实际范围，不预设主河道必须连续到地图边缘。抽样也记录了当前缺失和多出的湿点，不能据此认定岸线、导航或外观已通过；仍请报告可见问题。
只输出JSON，字段verdict(pass/fail)、suitable_use、blockers、refinements、unverified、evidence（逐图依据）。给出具体可见位置和原因，不推断无法看到的幕后实现。不要修改文件或执行代码。'''
audit=REPO/'.audit/adhoc_agents'/datetime.date.today().isoformat()/'map_environment_review'/stem;audit.mkdir(parents=True,exist_ok=True);(audit/'request.json').write_text(json.dumps({'prompt':prompt,'images':evidence,'blend_sha256':blend_hash},ensure_ascii=False,indent=2),encoding='utf-8');errors=[]
for who in qc_review.pick('auto'):
 try:
  with tempfile.TemporaryDirectory(prefix='dota_map_review_') as tmp:raw=qc_review.run_reviewer(who,prompt,refs+renders,Path(tmp),600)
  (audit/(who+'_response.txt')).write_text(raw,encoding='utf-8');result=json.loads(raw[raw.find('{'):raw.rfind('}')+1]);assert result.get('verdict') in ['pass','fail'];result.update(reviewer=who,blend_sha256=blend_hash,evidence_files=evidence,scope='environment_visual_only_not_final_map_acceptance',prior_errors=errors);reportpath.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(result['verdict'],len(result.get('blockers',[])),flush=True);break
 except Exception as exc:errors.append({'reviewer':who,'error':str(exc)})
else:reportpath.write_text(json.dumps({'verdict':'not_reviewed','errors':errors},indent=2),encoding='utf-8')
