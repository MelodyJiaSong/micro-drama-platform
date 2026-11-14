"""Local StableGen Klein reference workflow; inspect output before any projection."""
from pathlib import Path
import ast,json,shutil,urllib.request,time,datetime
ROOT=Path(__file__).resolve().parents[3]
WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('characters/*/m303_*/model_3d'))
out=folder/'texture_trial_klein_r01';out.mkdir(exist_ok=True)
receipt=out/'request.json'
if receipt.exists():raise FileExistsError('Preserve existing request; query its receipt instead')
template=Path('C:/Users/light/AppData/Roaming/Blender Foundation/Blender/5.2/extensions/user_default/stablegen/util/workflow_templates.py')
tree=ast.parse(template.read_text(encoding='utf-8'))
value=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='prompt_text_flux2_klein' for t in n.targets))
prompt=json.loads(value)
prompt.pop('16')
prompt['13']={'class_type':'SaveImage','inputs':{'images':['12',0],'filename_prefix':'dota_m303_texture_klein_r01'}}
prompt['4']['inputs']['text']='Edit image 1 into a detailed photorealistic texture reference of the same head. Preserve the exact image 1 camera angle, head silhouette, face orientation, eye and mouth positions, proportions, crop and background. Image 2 shows the identity and materials: a friendly stout European merchant aged around forty, warm natural skin, short dark brown buzz cut, subtle stubble, brown eyes, muted taupe linen collar. Replace the waxy surface with natural skin pores, subtle warm skin colour variation, fine eyebrows and individual short hairs. The eyes have natural irises and sclera without dark artificial rings. Keep lighting soft, neutral and diffuse. One single head in the exact pose of image 1. No text or additional objects.'
for node in ('6','7'):prompt[node]['inputs'].update(width=768,height=768)
prompt['7']['inputs']['steps']=50;prompt['10']['inputs']['cfg']=4.0;prompt['9']['inputs']['noise_seed']=3031401
input_dir=Path('C:/workspace/ComfyUI/input/dota_texture_trial');input_dir.mkdir(exist_ok=True)
sources=[folder/'r10/face_detail.png',folder.parent/'m303_Gateway_Relics.png']
for index,(node,source) in enumerate(zip(('14','15'),sources)):
    target=input_dir/f'm303_klein_ref_{index+1}.png';shutil.copyfile(source,target)
    prompt[node]['inputs']['image']='dota_texture_trial/'+target.name
    scale=str(700+index*4);enc=str(701+index*4);pos=str(702+index*4);neg=str(703+index*4)
    prompt[scale]={'class_type':'ImageScaleToTotalPixels','inputs':{'image':[node,0],'upscale_method':'lanczos','megapixels':0.6}}
    prompt[enc]={'class_type':'VAEEncode','inputs':{'pixels':[scale,0],'vae':['3',0]}}
    prompt[pos]={'class_type':'ReferenceLatent','inputs':{'conditioning':prompt['10']['inputs']['positive'],'latent':[enc,0]}}
    prompt[neg]={'class_type':'ReferenceLatent','inputs':{'conditioning':prompt['10']['inputs']['negative'],'latent':[enc,0]}}
    prompt['10']['inputs'].update(positive=[pos,0],negative=[neg,0])
def api(path,data=None):
    req=urllib.request.Request('http://127.0.0.1:8188'+path,data=None if data is None else json.dumps(data).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=60) as response:return json.load(response)
nodes=api('/object_info')
missing=sorted({n['class_type'] for n in prompt.values()}-nodes.keys())
if missing:raise RuntimeError(missing)
now=lambda:datetime.datetime.now().astimezone().isoformat()
record={'at':now(),'status':'prepared_before_submit','service':'local_ComfyUI','paid_service':False,'template':str(template),'model':'flux-2-klein-base-4b-fp8.safetensors','sources':[str(p) for p in sources],'purpose':'Author-only front texture feasibility test. Not applied to mesh, not accepted.','official_settings_source':'https://github.com/black-forest-labs/flux2/blob/main/README.md','workflow':prompt}
receipt.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
try:
    result=api('/prompt',{'prompt':prompt,'client_id':'dota-local-texture-303-r01'})
    record.update(status='submitted',response=result,prompt_id=result.get('prompt_id'));receipt.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    print('SUBMITTED',result,flush=True)
    deadline=time.monotonic()+3600
    while time.monotonic()<deadline:
        history=api('/history/'+record['prompt_id']).get(record['prompt_id'])
        if history:
            record['history']=history;record['status']='completed_unreviewed' if history['status']['status_str']=='success' else 'failed';record['finished_at']=now()
            for item in history.get('outputs',{}).get('13',{}).get('images',[]):
                src=Path('C:/workspace/ComfyUI/output')/item['subfolder']/item['filename'];shutil.copyfile(src,out/src.name)
            receipt.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8');print(record['status'],flush=True);break
        time.sleep(10)
    else:raise TimeoutError('Request remains live; inspect receipt and queue before retrying')
except Exception as exc:
    record['error']=repr(exc);receipt.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8');raise
