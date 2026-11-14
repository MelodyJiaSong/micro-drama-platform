"""Record verified rejected trials and current serialized continuation work."""
from pathlib import Path
import json,hashlib,datetime
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));OUT=WORLD/'background/map_3d';AUDIT=ROOT.parents[1]/'.audit/adhoc_agents/2026-10-27/dota-local-3d-287';now=datetime.datetime.now().astimezone().isoformat()
def evidence(path):return {'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
rows={}
for glob,names,status,notes in [
 ('characters/*/m303_*/model_3d/r09',['author_preview.png'],'rejected',['MeshFix 自交清理误删大部分身体，五处面部/领口射线全部未击中。作者全身图证实只剩局部小腿、眼眶和头发。禁止用于地图，原 r07 保留。']),
 ('characters/*/m309_*/model_3d/r03',['face_detail.png','back_detail.png','author_preview.png'],'partial_improvement_not_accepted',['紫色衣料比 r02 改善，但肤色偏浅、白色碎片仍在。','清除 89098 个游离毛发顶点后，后脑暴露大块缺失；须先重建头部表面，不能以更多毛发遮盖。']),
 ('background/*/bg23_*/model_3d/r38',['hook_side_detail.png','perspective_preview.png'],'independent_fail_3',['作者已查看接头与透视。独立复检仍有根须/土丘自然度、石带纹样可读性、弯钩圆管与薄扁带不一致三项阻断。'])]:
 folder=next(WORLD.glob(glob));data={'at':now,'review_type':'author_visual_check_not_independent_QC','status':status,'notes':notes,'images':[evidence(folder/n) for n in names]};(folder/'author_visual_check.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');rows[str(folder.relative_to(ROOT))]=data
report={'at':now,'author_checks':rows,'map':'v021 已保存，环境 v033，52 类实际实例化、59 类载入、97 布置、30 线兵；渲染尚未验收。','render_resume':'原 88 GiB 门槛持续等待；确认自有等待进程无渲染锁后停止，改以 84 GiB 起始门槛及 1024 纹理上限渲染已保存文件。源几何和贴图不改写；需检查输出和内存。','queued':'v034 连续崖壁在 v021 两机位结束后取得独占内存锁；m303 r10 局部补孔、bg23 r39 扁带弯臂/根/石带代码已准备，尚未执行。','accepted_families':1,'total_families':59}
(AUDIT/'manual_work_r18.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
path=OUT/'authoring_checkpoint.json';p=json.loads(path.read_text(encoding='utf-8'));p['at']=now;p['assets']['m303'].update(authoring='r09 清理误删大部分身体，作者全身图确认拒绝。r10 改为五处实测小孔局部补面脚本，尚未执行。',remaining='局部孔洞、头发帽状轮廓、皮肤眼眶真实度、服装配色。');p['assets']['bg23'].update(candidate='r38 独立 fail 3',authoring='r38 接头平滑和石色修正已查看。r39 改回连续扁带问号弯臂、较粗抬升根冠、浅灰青深刻石带，脚本已准备，尚未执行。');p['assets']['m309']={'candidate':'r01 独立 fail 4','authoring':'r02/r03 三图均已查看，紫色衣料改善；后脑大片缺失，毛发和肤色不合格。','remaining':'后脑表面重建、附着白色扫描残片、皮肤/眼睛/衣领颜色、完整检查。'};p['map']=report['map'];p['runtime']['map_resume']=report['render_resume'];p['runtime']['cliff_relief_trial']='v034 细分岩面数组已准备，原地形及导航几何不变；位移最大 .54364 m，源点距保护通路至少 1.6 m，不代表新表面的实际净距。等待 v021 预览结束后运行。';path.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8');print('R18_AUTHOR_EVIDENCE_RECORDED')
