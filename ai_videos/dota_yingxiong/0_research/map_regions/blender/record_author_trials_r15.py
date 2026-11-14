"""Persist inspected trial failures without promoting them to independent passes."""
from pathlib import Path
from datetime import datetime
import json,hashlib
ROOT=Path(__file__).resolve().parents[3];W=next(ROOT.glob('2_*'));OUT=W/'background/map_3d';AUDIT=ROOT.parents[1]/'.audit/adhoc_agents/2026-10-27/dota-local-3d-287'
checks=[
 ('m303','r04',['face_detail.png','face_side.png'],'partial_improvement_not_accepted',['MPFB lids and actual iris improve eye readability versus r02.','Patch boundaries remain visible at nose and cheek; expression still sleepy/frowning.','Source black mesh holes remain on face, ears, neck and shirt.','Hair still reads grey despite black material trial; inspect actual shader and masks.']),
 ('m26','r09',['head_detail.png'],'not_accepted',['12mm inward shell avoids r08 sieve-like surface across the whole head.','Head still has pitted surface, missing readable yellow eye, weak mouth interior and washed green keratin.','Zero boundary/nonmanifold edges is not visual acceptance; current mesh is 8.77M faces.']),
]
records=[]
for asset,revision,views,status,findings in checks:
 folder=next(W.glob(f'characters/*/{asset}_*/model_3d'))/revision
 row={'at':datetime.now().astimezone().isoformat(),'review_type':'author_visual_check_not_independent','asset_id':asset,'revision':revision,'status':status,'findings':findings,'images':[{'path':name,'sha256':hashlib.sha256((folder/name).read_bytes()).hexdigest()} for name in views]}
 (folder/'author_visual_check.json').write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf-8');records.append(row)
camp=OUT/'camp_K8_RAO_v001_report.json';data=json.loads(camp.read_text(encoding='utf-8'));data['author_visual_check']={'status':'view_rejected_for_occlusion','image':'camp_K8_RAO_v001.png','finding':'Foreground trunks and branches obscure the three units. Sampled navigation pass does not establish visible contact/collision acceptance.','next':'Unchanged geometry overhead diagnostic rendering'};camp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
record={'at':datetime.now().astimezone().isoformat(),'followup':292,'status':'in_progress_not_deliverable','author_trial_checks':records,'merchant_placement_research':{'asset':'m309','host':'bg12','evidence':'m309 card: merchant is part of original building mesh, on right raised platform. Two u010 host instances exist in v019.','platform_probe':'bg12 r08 inspection/platform_anchor_probe.json','anchor_trial':'side_shop_merchant_fit_v001.blend','status':'contact_render_pending; not integrated into map'},'gateway_retry':{'first_error':'Hidden viewport source had no evaluated mesh for ray_cast','fix':'Temporarily enable source for ray casting and colour transfer, hide again before saving/rendering','retry_pid':17272,'result':'Saved and both face views inspected; not accepted'},'syntax_checks':9,'followup_check':'Passed; other owner 283/286 remain untouched'}
(AUDIT/'manual_work_r15.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8');print('Recorded author trial checks; no independent acceptance changed.')
