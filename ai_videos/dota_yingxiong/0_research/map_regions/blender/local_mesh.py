from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import time
import urllib.error
import urllib.request
from pathlib import Path


DRAMA = Path(__file__).resolve().parents[3]
WORLD = next(DRAMA.glob('2_*'))
MANIFEST = WORLD / 'background/map_3d/asset_manifest.json'
COMFY = Path('C:/workspace/ComfyUI')
SERVER = 'http://127.0.0.1:8188'


def api(path: str, body: dict | None = None) -> dict:
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(SERVER + path, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def node(name: str, **inputs) -> dict:
    return {'class_type': name, 'inputs': inputs}


def build(asset: dict, revision: str, resolution: str, multiview: bool, profile: str = 'wrapper', mesh_profile: str = 'baseline', max_tokens: int = 32768) -> dict:
    graph = {'1': node('LoadTrellis2Models', resolution=resolution, precision='bf16', attn_backend='sdpa')}
    source_views = asset['views'] if multiview and asset['views'] else {'front': asset['views'].get('front') or asset['anchor']}
    inputs = {}
    for i, (view, ref) in enumerate(source_views.items()):
        src = DRAMA / ref['path']
        filename = f'dota287_{asset["id"]}_{view}_{ref["sha256"][:10]}.png'
        shutil.copy2(src, COMFY / 'input' / filename)
        load, mask = str(10 + i * 2), str(11 + i * 2)
        graph[load] = node('LoadImage', image=filename)
        graph[mask] = node('Trellis2RemoveBackground', image=[load, 0], low_vram=True)
        direction = 'right' if view == 'side' else view
        inputs[f'{direction}_image'] = [mask, 0]
        inputs[f'{direction}_mask'] = [mask, 1]
    graph['20'] = node('Trellis2GetConditioning', model_config=['1', 0], image=inputs['front_image'],
                       mask=inputs['front_mask'], background_color='black')
    sampling = {'model_config': ['1', 0], 'seed': 28723, 'ss_sampling_steps': 12,
                'shape_sampling_steps': 12, 'max_tokens': max_tokens}
    texture_sampling = {}
    if profile == 'official':
        # Verified against Microsoft TRELLIS.2 app.py and installed pipeline.json.
        # Set explicitly: the wrapper's optional defaults override these values.
        config = json.loads((COMFY / 'models/trellis2/pipeline.json').read_text(encoding='utf-8'))['args']
        for prefix, stage in [('ss', 'sparse_structure_sampler'), ('shape', 'shape_slat_sampler')]:
            for key in ['guidance_strength', 'guidance_rescale']:
                sampling[prefix + '_' + key] = config[stage]['params'][key]
        for key in ['guidance_strength', 'guidance_rescale']:
            texture_sampling['tex_' + key] = config['tex_slat_sampler']['params'][key]
    if multiview and len(source_views) > 1:
        graph['21'] = node('Trellis2MultiViewImageToShape', **sampling, **inputs,
                           front_axis='z', blend_temperature=2.0, background_color='black')
    else:
        graph['21'] = node('Trellis2ImageToShape', **sampling, conditioning=['20', 0])
    prefix = f'dota287/{asset["id"]}_{revision}'
    graph['22'] = node('Trellis2ExportTrimesh', trimesh=['21', 0], filename_prefix=prefix + '_raw', file_format='glb')
    graph['23'] = node('Trellis2ShapeToTexturedMesh', model_config=['1', 0], conditioning=['20', 0],
                       shape_slat=['21', 1], subs=['21', 2], seed=28723, tex_sampling_steps=12, **texture_sampling)
    graph['24'] = node('Trellis2ProcessMesh', trimesh=['21', 0], remesh='on', target_face_count=1000000 if resolution != '512' else 500000,
                       **{'remesh.remesh_band': 1.0, 'remesh.remove_inner_faces': False},
                       floater_threshold=0.0, weld_vertices=True, weld_digits=5,
                       chart_cone_angle=90.0, chart_refine_iterations=0, chart_global_iterations=1,
                       chart_smooth_strength=1)
    graph['25'] = node('Trellis2RasterizePBR', trimesh=['24', 0], voxelgrid=['23', 0],
                       texture_size=4096 if resolution != '512' else 2048, original_mesh=['21', 0])
    graph['26'] = node('Trellis2ExportTrimesh', trimesh=['25', 0], filename_prefix=prefix + '_pbr', file_format='glb')
    graph['27'] = node('Trellis2ExportTrimesh', trimesh=['24', 0], filename_prefix=prefix + '_processed', file_format='glb')
    if mesh_profile=='preserve':
        # The installed wrapper's remesh-on branch hardcodes a 512 grid, even
        # for 1024/1536 generation. Preserve the source surface for comparison.
        graph['24']['inputs'].update(remesh='off',target_face_count=3000000)
        graph['24']['inputs'].pop('remesh.remesh_band',None)
        graph['24']['inputs'].pop('remesh.remove_inner_faces',None)
        graph['24']['inputs'].update({'remesh.fill_holes':False,'remesh.fill_holes_perimeter':.001})
    elif mesh_profile=='remesh1024':
        graph['24']['inputs']['target_face_count']=3000000
    return graph


def submit(asset_id: str, revision: str, resolution: str, multiview: bool, profile: str = 'wrapper', mesh_profile: str = 'baseline', max_tokens: int = 32768) -> None:
    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    asset = next(a for a in data['assets'] if a['id'] == asset_id)
    folder = DRAMA / asset['model_directory'] / revision
    folder.mkdir(parents=True, exist_ok=True)
    state_path = folder / 'generation.json'
    if state_path.exists():
        raise SystemExit('此版本已有请求记录；用 status 补收，不自动重提。')
    workflow = build(asset, revision, resolution, multiview, profile, mesh_profile, max_tokens)
    (folder / 'workflow_api.json').write_text(json.dumps(workflow, indent=2), encoding='utf-8')
    state = {'asset_id': asset_id, 'followups': [287, 288, 289, 290, 291], 'status': 'submitting', 'started_at': time.time(),
             'engine': 'local ComfyUI TRELLIS.2', 'hyper3d': False, 'paid_requests': 0,
             'references': {'anchor': asset['anchor'], 'views': asset['views']},
             'resolution': resolution, 'multiview': multiview,
             'sampling_profile': profile,
             'mesh_processing_profile':mesh_profile,
             'max_tokens':max_tokens,
             'pipeline_config_sha256': hashlib.sha256((COMFY / 'models/trellis2/pipeline.json').read_bytes()).hexdigest(),
             'runtime_patch_sha256': hashlib.sha256((Path(__file__).parent/'local_attention_compat.py').read_bytes()).hexdigest(),
             'runtime_patch_version': 'task-remesh-1024-for-3M-v3; verify worker installation log',
             'workflow_sha256': hashlib.sha256(json.dumps(workflow, sort_keys=True).encode()).hexdigest(),
             'license_route': 'DINOv3 本次用户授权；BiRefNet 公共模型；CuMesh + DRTK，不使用 nvdiffrast/nvdiffrec',
             'review': 'not_reviewed'}
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    try:
        receipt = api('/prompt', {'prompt': workflow, 'client_id': f'dota287_{asset_id}_{revision}'})
    except urllib.error.HTTPError as exc:
        state.update(status='rejected', error=exc.read().decode())
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
        raise SystemExit(state['error']) from exc
    state.update(status='queued', receipt=receipt, prompt_id=receipt['prompt_id'])
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'path': str(state_path), 'prompt_id': state['prompt_id']}, ensure_ascii=False))


def status(asset_id: str, revision: str) -> None:
    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    asset = next(a for a in data['assets'] if a['id'] == asset_id)
    folder = DRAMA / asset['model_directory'] / revision
    state_path = folder / 'generation.json'
    state = json.loads(state_path.read_text(encoding='utf-8'))
    prompt_id = state.get('prompt_id')
    if not prompt_id:
        raise SystemExit('没有 prompt_id；保留状态，不重提。')
    history = api('/history/' + prompt_id).get(prompt_id)
    if history:
        (folder / 'history.json').write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding='utf-8')
        state['status'] = 'generated_pending_review' if history['status']['status_str'] == 'success' else 'failed'
        state['history_status'] = history['status']
        state['outputs'] = []
        for path in (COMFY / 'output/dota287').glob(f'{asset_id}_{revision}_*.glb'):
            dest = folder / path.name
            if not dest.exists():
                shutil.copy2(path, dest)
            state['outputs'].append({'path': dest.name, 'bytes': dest.stat().st_size,
                                     'sha256': hashlib.sha256(dest.read_bytes()).hexdigest()})
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
        errors = [message[1] for message in history['status']['messages'] if message[0] == 'execution_error']
        print(json.dumps({'status': state['status'], 'outputs': state['outputs'],
                          'errors': [{'node':e['node_id'],'type':e['exception_type'],
                                      'message':e['exception_message'][:600]} for e in errors]}, ensure_ascii=False))
    else:
        queue = api('/queue')
        running = any(item[1] == prompt_id for item in queue['queue_running'])
        pending = any(item[1] == prompt_id for item in queue['queue_pending'])
        print(json.dumps({'status': 'running' if running else 'queued' if pending else 'unknown',
                          'elapsed_seconds': round(time.time() - state['started_at']),
                          'raw_files': [p.name for p in (COMFY / 'output/dota287').glob(f'{asset_id}_{revision}_*.glb')]}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['submit', 'status'])
    parser.add_argument('asset_id')
    parser.add_argument('--revision', default='r01')
    parser.add_argument('--resolution', default='1024_cascade')
    parser.add_argument('--multiview', action='store_true')
    parser.add_argument('--profile', choices=['wrapper', 'official'], default='wrapper')
    parser.add_argument('--mesh-profile',choices=['baseline','preserve','remesh1024'],default='baseline')
    parser.add_argument('--max-tokens',type=int,default=32768)
    args = parser.parse_args()
    if args.command == 'submit':
        submit(args.asset_id, args.revision, args.resolution, args.multiview, args.profile,args.mesh_profile,args.max_tokens)
    else:
        status(args.asset_id, args.revision)
