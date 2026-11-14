"""Record Oct 30 recovery without overwriting earlier evidence or claiming acceptance."""
from pathlib import Path
import json,datetime,hashlib
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));OUT=WORLD/'background/map_3d';AUDIT=ROOT.parents[1]/'.audit/adhoc_agents/2026-10-27/dota-local-3d-287'
now=datetime.datetime.now().astimezone().isoformat()
def evidence(path):return {'path':str(path.relative_to(ROOT.parents[1])),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
bg=next(WORLD.glob('background/*/bg23_*/model_3d'));lizard=next(WORLD.glob('characters/*/m26_*/model_3d'))
review=json.loads((bg/'r45/inspection/independent_review.json').read_text(encoding='utf-8'))
uv=json.loads((lizard/'r13/uv_transfer_progress.json').read_text(encoding='utf-8'))
report={'at':now,'followup':293,'accepted_families':1,'total_families':59,'status':'in_progress_not_deliverable',
 'bg23_r45':{'verdict':review['verdict'],'blockers':len(review['blockers']),'evidence':evidence(bg/'r45/inspection/independent_review.json'),'summary':'水晶偏小暗、根网被遮挡且偏橙、孤立尖根、土层融地不清、藤苔覆盖不足。'},
 'm26_r12':{'status':'terminated_task_owned_process','pid':12572,'reason':'内置 UV Data Transfer 运行约 20 小时、CPU 持续工作但无候选文件。已保留日志和 r11 高模；不再重复同一不透明计算。'},
 'm26_r13':{'pid':26936,'status':'UV_transfer_complete_author_renders_in_progress','uv_progress':uv,'geometry_preserved':True,'viewed_images':[evidence(lizard/'r13/back_detail.png')],'author_observation':'背部鳞片贴图清晰度恢复；背刺边缘仍有碎片、凹坑和模糊色斑，未达到精细验收。'},
 'bg23_r46':{'pid':23008,'status':'author_renders_in_progress','changes':'重建 99 条从墙内生长、末端入土的分枝根，减小外移蕨类；35 水晶露出石面并调整大小；新增 1512 聚簇藤叶和 404 真实尺度苔藓簇。尚未看图验收。'},
 'map':{'latest_saved':'assembly_working_v022.blend','latest_complete_preview':'v021','v022_resume_pid':34440,'v022_resume_status':'timed_out_after_memory_wait','openweb_pid':13652,'openweb_private_commit_gib_at_recheck':266.84,'openweb_action':'未终止；用户确认仍未收到。','environment':'v036 总装底图；v039–v041 局部岩层仍未接受。'},
 'validation':{'followup_check':'2026-10-30 已运行通过；283/286 为其他会话历史未收尾提示；293 本会话进行中。'}}
(AUDIT/'manual_work_r22.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
p=json.loads((OUT/'authoring_checkpoint.json').read_text(encoding='utf-8'));p.update(at=now,followup=293,status='in_progress_not_deliverable');p['map']='v022 总装保存但全景内存分配失败；恢复等待也已超时。最新完整可看预览为 v021。openweb 未获关闭授权，继续模型工作。';p['assets']['bg23'].update(authoring=report['bg23_r46']['changes'],candidate='r45 完整独立 fail 5；r46 作者渲染中，未验收。');p['assets']['m26'].update(authoring='r12 内置 UV 转移运行约 20 小时无产出后终止；r13 分块 BVH 转移 8765718 面完成于 207.7 秒，高模不变。背部已看：纹理恢复但背刺仍有缺陷。',candidate='r13 作者渲染中，无新独立通过。');p['runtime']['latest_author_evidence']=str((AUDIT/'manual_work_r22.json').relative_to(ROOT.parents[1]));p['runtime']['pending_trials']={'m26_r13_author_pid':26936,'bg23_r46_author_pid':23008};(OUT/'authoring_checkpoint.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8');print('R22_CHECKPOINT_RECORDED')
