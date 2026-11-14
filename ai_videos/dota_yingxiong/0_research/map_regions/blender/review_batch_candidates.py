"""Review each generated candidate once in an independent review process."""
import json,time,sys,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
OUT=next(ROOT.glob('2_*'))/'background/map_3d'
manifest=json.loads((OUT/'asset_manifest.json').read_text(encoding='utf-8'))
while True:
    state=json.loads((OUT/'batch_full_models_v1.json').read_text(encoding='utf-8'))
    for record in state['results']:
        if record['status']!='candidate_pending_review':continue
        a=next(a for a in manifest['assets'] if a['id']==record['asset'])
        folder=ROOT/a['model_directory']/record['revision']/'inspection'
        if (folder/'independent_review.json').exists():continue
        print('REVIEW',a['id'],record['revision'],flush=True)
        with (folder/'independent_review_process.log').open('w',encoding='utf-8') as log:
            result=subprocess.run([sys.executable,'-X','utf8',str(HERE/'review_model_asset.py'),a['id'],'--revision',record['revision']],stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
        print('REVIEW_DONE',a['id'],result.returncode,flush=True)
        if result.returncode:raise RuntimeError('Review process failed; inspect log')
    if state['status']=='candidates_generated_pending_review':break
    time.sleep(30)
