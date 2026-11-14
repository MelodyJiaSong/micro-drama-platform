"""Resumable local modeling queue; every result remains pending visual review."""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
import local_mesh as lm

BLENDER = 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
HERE = Path(__file__).resolve().parent


def save(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')


def main(args):
    manifest=json.loads(lm.MANIFEST.read_text(encoding='utf-8'))
    heights=json.loads((lm.MANIFEST.parent/'model_calibration.json').read_text(encoding='utf-8'))['heights']
    selected=[a for a in manifest['assets'] if a['id'] in args.ids.split(',')]
    if len(selected)!=len(args.ids.split(',')):raise ValueError('Unknown/duplicate IDs')
    state={'started_at':time.time(),'ids':[a['id'] for a in selected],'status':'running','results':[],'resolution':args.resolution}
    audit=lm.MANIFEST.parent/f'batch_{args.name}.json'
    if audit.exists():state=json.loads(audit.read_text(encoding='utf-8'));state['status']='resuming'
    state.update(sampling_profile_for_new_requests=args.profile,view_mode_for_new_requests=args.view_mode,mesh_processing_profile_for_new_requests=args.mesh_profile)
    state.pop('hold_reason',None);state.pop('hold_at',None)
    for index,asset in enumerate(selected):
        folder=lm.DRAMA/asset['model_directory']/args.revision
        prior=next((r for r in state['results'] if r['asset']==asset['id'] and r.get('revision')==args.revision and r['status']=='candidate_pending_review'),None)
        if prior and (lm.DRAMA/prior['blend']).exists():
            print('EXISTING_CANDIDATE',asset['id'],flush=True);continue
        generation=folder/'generation.json'
        state['active_asset']=asset['id'];save(audit,state)
        print('START',asset['id'],flush=True)
        if not generation.exists():
            lm.submit(asset['id'],args.revision,args.resolution,args.view_mode=='auto' and len(asset['views'])>1,args.profile,args.mesh_profile)
        request=json.loads(generation.read_text(encoding='utf-8'))
        if not request.get('prompt_id'):
            state['status']='blocked_unknown_request_receipt';save(audit,state);raise RuntimeError(str(generation))
        while request['status'] not in ('generated_pending_review','failed'):
            history=lm.api('/history/'+request['prompt_id']).get(request['prompt_id'])
            if history:
                lm.status(asset['id'],args.revision)
                request=json.loads(generation.read_text(encoding='utf-8'))
            else:
                queue=lm.api('/queue')
                if not any(r[1]==request['prompt_id'] for r in queue['queue_running']+queue['queue_pending']):
                    state['status']='blocked_request_missing_from_server';save(audit,state);raise RuntimeError(request['prompt_id'])
                time.sleep(10)
        if request['status']=='failed':
            state['results']=[r for r in state['results'] if not (r['asset']==asset['id'] and r.get('revision')==args.revision)]
            state['results'].append({'asset':asset['id'],'status':'generation_failed','revision':args.revision});save(audit,state);continue
        # Once this GPU request is complete, the next one can overlap CPU inspection.
        # Existing receipts are always reused; never resubmit a pending/failed receipt.
        if args.prefetch and index+1<len(selected):
            upcoming=selected[index+1]
            receipt=lm.DRAMA/upcoming['model_directory']/args.revision/'generation.json'
            if not receipt.exists():
                print('PREFETCH_NEXT_GPU_REQUEST',upcoming['id'],flush=True)
                lm.submit(upcoming['id'],args.revision,args.resolution,args.view_mode=='auto' and len(upcoming['views'])>1,args.profile,args.mesh_profile)
                state['prefetched_asset']=upcoming['id'];save(audit,state)
        inspection=folder/'inspection'/f'{asset["id"]}_{args.revision}.blend'
        if not inspection.exists():
            heights=json.loads((lm.MANIFEST.parent/'model_calibration.json').read_text(encoding='utf-8'))['heights']
            with (folder/'inspection.log').open('w',encoding='utf-8') as log:
                result=subprocess.run([BLENDER,'--factory-startup','--background','--python-exit-code','1','--python',str(HERE/'inspect_model.py'),'--',asset['id'],'--revision',args.revision,'--height',str(heights[asset['id']]),'--samples','16'],stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode:raise RuntimeError(f'Inspection failed: {asset["id"]}')
        state['results']=[r for r in state['results'] if r['asset']!=asset['id']]
        state['results'].append({'asset':asset['id'],'status':'candidate_pending_review','revision':args.revision,'blend':str(inspection.relative_to(lm.DRAMA))})
        save(audit,state)
        current=json.loads(lm.MANIFEST.read_text(encoding='utf-8'))
        item=next(a for a in current['assets'] if a['id']==asset['id'])
        item.update(status='candidate_pending_review',current_revision=args.revision,review='not_reviewed')
        save(lm.MANIFEST,current)
        print('CANDIDATE_SAVED',asset['id'],flush=True)
    state['status']='candidates_generated_pending_review';state['finished_at']=time.time();save(audit,state)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--ids',required=True);p.add_argument('--revision',default='r01');p.add_argument('--name',required=True);p.add_argument('--resolution',default='1024_cascade');p.add_argument('--profile',choices=['wrapper','official'],default='wrapper');p.add_argument('--view-mode',choices=['auto','single'],default='auto');p.add_argument('--mesh-profile',choices=['baseline','preserve'],default='baseline');p.add_argument('--prefetch',action='store_true',help='Overlap one next GPU generation with current CPU inspection');main(p.parse_args())
