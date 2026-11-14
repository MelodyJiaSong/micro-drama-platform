"""Persist inspected LOD comparisons and the latest independent result."""
from pathlib import Path
import datetime, hashlib, json, ast
ROOT=Path(__file__).resolve().parents[3]
WORLD=next(ROOT.glob('2_*'));OUT=WORLD/'background/map_3d'
AUDIT=ROOT.parents[1]/'.audit/adhoc_agents/2026-10-27/dota-local-3d-287'
now=datetime.datetime.now().astimezone().isoformat()
review_path=next(WORLD.glob('background/*/bg23_*/model_3d/r49/inspection/independent_review.json'))
review=json.loads(review_path.read_text(encoding='utf-8'))
lod=OUT/'lod_libraries/overview_v004'
checks={p.parent.name:json.loads(p.read_text(encoding='utf-8')) for p in lod.glob('*/comparison_author_check.json')}
scripts=['build_map_lod_library.py','build_map_lod_batch.py','compare_map_lod.py','record_lod_comparison.py','finish_map_lod_preview.py','save_map_with_lod_libraries.py','record_author_trials_r25.py']
for name in scripts:ast.parse((Path(__file__).parent/name).read_text(encoding='utf-8'))
record={'at':now,'followup':293,'status':'in_progress_not_deliverable','accepted_families':1,'total_families':59,
 'latest_independent_review':{'asset':'bg23','revision':'r49','verdict':review['verdict'],'blockers':len(review['blockers']),'path':str(review_path.relative_to(ROOT.parents[1])),'sha256':hashlib.sha256(review_path.read_bytes()).hexdigest()},
 'lod_comparisons':checks,'running_at_record':{'lod_batch_pid':9896,'lod_map_pipeline_pid':23988},
 'memory':'Last measured physical free 92.51 GiB / commit free 23.52 GiB. 24 GiB batch threshold unmet. openweb not stopped; explicit permission question still unanswered.',
 'repair':'bg26 failed because modifier_apply rejected shared mesh data. Builder now copies for modifier application then restores shared instance references. Syntax checked; Blender runtime validation pending resource availability. Old waiting batch 30356 stopped and resumed as 9896; completed libraries preserved.',
 'validation':{'ast_passed':scripts},'remaining':'All fine model quality defects remain tracked; LOD comparison is not final asset acceptance. Latest bg23 review still fail 4. No final map QC pass.'}
(AUDIT/'manual_work_r25.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
p=json.loads((OUT/'authoring_checkpoint.json').read_text(encoding='utf-8'))
p.update(at=now,followup=293)
p['assets']['bg23'].update(authoring='r49 石框 UV 已补，作者图已看；完整独立审稿仍 fail 4：根网不可见、水晶像规则镜片、土壤硬边、植被稀疏。',candidate='r49 未验收，仍需返工。')
p['runtime']['latest_author_evidence']=str((AUDIT/'manual_work_r25.json').relative_to(ROOT.parents[1]))
p['runtime']['pending_trials']=record['running_at_record']
p['runtime']['map_lod_latest']={'comparisons':{k:v['status'] for k,v in checks.items()},'repair':record['repair'],'memory':record['memory']}
(OUT/'authoring_checkpoint.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
print('R25_CHECKPOINT_RECORDED; AST passed:',len(scripts))
