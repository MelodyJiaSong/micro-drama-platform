"""Record images actually inspected this work segment, without independent approval."""
from pathlib import Path
import json,hashlib,datetime
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));OUT=WORLD/'background/map_3d';AUDIT=ROOT.parents[1]/'.audit/adhoc_agents/2026-10-27/dota-local-3d-287';now=datetime.datetime.now().astimezone().isoformat()
def evidence(path):return {'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
def record(folder,names,status,notes):
 data={'at':now,'review_type':'author_visual_check_not_independent_QC','status':status,'notes':notes,'images':[evidence(folder/n) for n in names]};(folder/'author_visual_check.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');return data
rows={}
folder=next(WORLD.glob('characters/*/m26_*/model_3d/r11'));rows['m26:r11']=record(folder,['head_detail.png','back_detail.png','author_preview.png'],'partial_improvement_not_accepted',['金色眼睛已位于实测眼窝，红色口腔内收后不再像外突光滑红团。','背棘和角质仍有不自然凹孔与斑驳，近景扫描表面不足；未启动重复的完整独立审稿。'])
folder=next(WORLD.glob('characters/*/m303_*/model_3d/r08'));rows['m303:r08']=record(folder,['face_detail.png'],'rejected',['MeshFix 仅连通性处理和小孔填充产生大量重叠补面，脸部出现灰色碎片边缘；不得替换候选。','实测额头、下巴、鼻旁及左领口射线已击中前表面，但右领口仍穿透到背面。','下一试验 r09 保留主体连通分量、填孔后清理自交；尚无结果，不能认定成功。'])
rows['map:v020']={'status':'draft_author_viewed_not_accepted','images':[evidence(OUT/f'assembly_working_v020_{n}.png') for n in ['Map_Overview','Sentinel_Forest_Eye']],'notes':['分机位进程、88 GiB 空闲门槛成功恢复两张图。','52 类实际实例化、59 类载入、97 布置，7 类是可替换野怪组合；此前环境独立 fail 6 仍适用。']}
rows['environment:v032']={'status':'author_viewed_not_accepted','images':[evidence(OUT/'environment_v032_Map_Overview.png')],'water_audit':json.loads((OUT/'environment_v032_water_footprint_audit.json').read_text()),'notes':['高度和水位统一，但岸线仍方折，地表与边界不自然。']}
rows['environment:v033']={'status':'author_viewed_not_accepted','images':[evidence(OUT/f'environment_v033_{n}.png') for n in ['Map_Overview','River_Eye_Level']],'notes':['河岸轮廓有所软化，三条湿岸材质分支改用局部水位上方高度。','崖壁仍过平，石块成串，地图外边界仍方形；未作为成品验收。']}
(AUDIT/'manual_work_r17.json').write_text(json.dumps({'at':now,'author_checks':rows,'running_trials':{'m303_r09_geometry_repair_pid':34936,'bg23_r37_author_pid':34912},'independent_review':'bg23 r36 fail 4; no additional accepted family','dependency':'pymeshfix 0.18.1 installed only into this audit task python_deps; no shared Comfy environment modification'},ensure_ascii=False,indent=2),encoding='utf-8');print('AUTHOR_CHECKS_R17_RECORDED')
