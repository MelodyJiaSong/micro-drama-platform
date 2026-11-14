"""Checkpoint bounded continuation and all available LOD visual decisions."""
from pathlib import Path
import ast,collections,datetime,json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
AUDIT=ROOT.parents[1]/'.audit/adhoc_agents/2026-10-27/dota-local-3d-287'
lod=OUT/'lod_libraries/overview_v004';counts=collections.Counter();decisions={};before=after=0
for path in lod.glob('*/lod_report.json'):
 r=json.loads(path.read_text(encoding='utf-8'));check=path.parent/'comparison_author_check.json'
 status=json.loads(check.read_text(encoding='utf-8'))['status'] if check.exists() else 'geometry_unchanged' if not r['changes'] else 'unreviewed'
 counts[status]+=1;decisions[path.parent.name]=status
 before+=r['visible_unique_faces_before'];after+=r['visible_unique_faces_after'] if status in ('usable_for_map_preview','geometry_unchanged') else r['visible_unique_faces_before']
scripts=['build_map_lod_batch.py','finish_map_lod_preview.py','save_map_with_lod_libraries.py']
for name in scripts:ast.parse((Path(__file__).parent/name).read_text(encoding='utf-8'))
state=json.loads((lod/'map_preview_state.json').read_text(encoding='utf-8'))
reportpath=OUT/'assembly_working_v022_lod_v004_report.json'
report=json.loads(reportpath.read_text(encoding='utf-8')) if reportpath.exists() else None
record={'at':datetime.datetime.now().astimezone().isoformat(),'followup':297,'status':'partial_not_deliverable','accepted_fine_families':1,'total_families':59,'lod_decisions':decisions,'lod_counts':dict(counts),'all_library_faces_before':before,'all_library_faces_after_latest_visual_fallbacks':after,'map_state_snapshot':state,'pipeline_pid':36936,'map_saved':(OUT/'assembly_working_v022_lod_v004.blend').exists(),'map_report_sha256':hashlib.sha256(reportpath.read_bytes()).hexdigest() if report else None,'unloaded_alternative_families':report.get('unloaded_alternative_families') if report else None,'policy':'Per asset/step 20 minute maximum; resource wait 2 minutes; only own process terminated. Skip failed camera and continue. Unreviewed or rejected LOD uses original. Whole-map save/profile are dependencies; failures preserve partial output.','validation':{'AST':scripts,'runtime':'Shared-mesh bg26 generation succeeded, but LOD visual result rejected. New map save succeeded after allowing only audited unused camp alternatives to be absent. Reopen/render pipeline remains in progress.'},'limitations':['Visual comparison is a single studio perspective, not independent fine asset QC.','Latest per-asset decisions may postdate the saved map selection; its report pins actual chosen libraries.','Full map visual acceptance still pending.']}
(AUDIT/'manual_work_r26.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
p=json.loads((OUT/'authoring_checkpoint.json').read_text(encoding='utf-8'));p.update(at=record['at'],followup=297)
p['runtime']['latest_author_evidence']=str((AUDIT/'manual_work_r26.json').relative_to(ROOT.parents[1]));p['runtime']['pending_trials']={'map_pipeline_pid':36936};p['runtime']['bounded_continuation']=record
(OUT/'authoring_checkpoint.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'counts':dict(counts),'map_state':state,'faces_before':before,'faces_with_fallbacks':after},ensure_ascii=False))
