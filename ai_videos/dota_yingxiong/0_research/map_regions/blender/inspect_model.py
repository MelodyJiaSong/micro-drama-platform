"""导入候选 GLB、按米制标定、保存可编辑 Blender 和多视角检查图。"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

DRAMA = Path(__file__).resolve().parents[3]
WORLD = next(DRAMA.glob('2_*'))


def material(name, color, roughness=.7):
    result = bpy.data.materials.new(name)
    result.use_nodes = True
    bsdf = result.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Roughness'].default_value = roughness
    return result


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def main(args):
    manifest = json.loads((WORLD / 'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'))
    asset = next(a for a in manifest['assets'] if a['id'] == args.asset)
    folder = DRAMA / asset['model_directory'] / args.revision
    candidates = sorted(folder.glob('*_pbr_*.glb'))
    if not candidates:
        raise FileNotFoundError('等待 PBR 场景模型；原始高模保留归档，不默认导入检查场景。')
    source = candidates[-1]
    out = folder / 'inspection'
    out.mkdir(exist_ok=True)
    blend = out / f'{args.asset}_{args.revision}.blend'
    if blend.exists():
        raise FileExistsError(blend)
    # Keep the generator export immutable. Some wrapper versions rotate custom
    # normals twice while converting Z-up vertices to glTF Y-up coordinates.
    # Repair a retained copy only if geometric dot products identify that defect.
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from check_glb_normals import repair_exported_normals
    original_source=source
    source=out/'normalized_source.glb'
    shutil.copy2(original_source,source)
    normal_repair=repair_exported_normals(source)
    (out/'normal_repair.json').write_text(json.dumps(normal_repair,indent=2),encoding='utf-8')
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.ops.import_scene.gltf(filepath=str(source))
    imported = list(bpy.context.scene.objects)
    meshes = [o for o in imported if o.type == 'MESH']
    # A verified m5 export contained a 94-face fragment 5.4 cm below the body,
    # making bbox-based grounding float. UV seam splits must be welded in the
    # analysis copy before identifying physical disconnected components.
    ground_fragments=[]
    if args.asset.startswith('m') and args.asset!='m306':
        from check_ground_fragments import inspect_and_remove
        ground_fragments=[inspect_and_remove(o,True) for o in meshes]
        bpy.context.view_layer.update()
    points = [o.matrix_world @ Vector(p) for o in meshes for p in o.bound_box]
    low = Vector([min(p[i] for p in points) for i in range(3)])
    high = Vector([max(p[i] for p in points) for i in range(3)])
    original_bounds = [list(low), list(high)]
    calibration_path=WORLD/'background/map_3d/model_calibration.json'
    calibration=json.loads(calibration_path.read_text(encoding='utf-8'))
    basis=calibration.get('scale_basis',{}).get(args.asset,{'axis':'Z','metres':args.height,'status':'height_bound_requires_pose_review'})
    axis='XYZ'.index(basis['axis']);factor=basis['metres']/(high[axis]-low[axis])
    center = Vector(((low.x + high.x)/2, (low.y + high.y)/2, low.z))
    transform = Matrix.Scale(factor, 4) @ Matrix.Translation(-center)
    for obj in imported:
        if obj.parent is None:
            obj.matrix_world = transform @ obj.matrix_world
    asset_coll = bpy.data.collections.new(f'ASSET_{args.asset}')
    bpy.context.scene.collection.children.link(asset_coll)
    for obj in imported:
        for coll in list(obj.users_collection):
            coll.objects.unlink(obj)
        asset_coll.objects.link(obj)
        obj['asset_id'] = args.asset
        obj['candidate_status'] = 'not_reviewed'
    clay = material('Inspection_clay', (.38, .40, .42))
    for obj in meshes:
        if not obj.data.materials:
            obj.data.materials.append(clay)
    bpy.context.view_layer.update()
    scaled_height=(high.z-low.z)*factor
    width = max(high.x-low.x, high.y-low.y) * factor
    size = max(width, scaled_height)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = args.samples
    scene.cycles.use_denoising = True
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = 8
    scene.render.resolution_x = 960
    scene.render.resolution_y = 960
    scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = 'AgX'
    scene.world = bpy.data.worlds.new('Inspection_studio')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes.get('Background').inputs[0].default_value = (.12,.14,.17,1)
    scene.world.node_tree.nodes.get('Background').inputs[1].default_value = .4
    floor_mat = material('Studio_floor', (.16,.17,.18))
    bpy.ops.mesh.primitive_plane_add(size=size*200, location=(0,0,0))
    bpy.context.object.name = 'Studio_floor'
    bpy.context.object.data.materials.append(floor_mat)
    for name, pos, power, color in [
        ('Key',(-1.5,-2,2.5),1600,(1,.90,.77)),
        ('Fill',(1.8,-.4,1.4),700,(.73,.84,1)),
        ('Rim',(.6,1.5,2),1900,(1,.96,.87)),
    ]:
        data = bpy.data.lights.new(name, 'AREA')
        data.energy = power*size*size/4
        data.color = color
        data.shape = 'DISK'
        data.size = size*1.4
        obj = bpy.data.objects.new(name,data)
        scene.collection.objects.link(obj)
        obj.location = Vector(pos)*size
        look_at(obj,(0,0,scaled_height*.5))
    data = bpy.data.cameras.new('Inspection_camera')
    camera = bpy.data.objects.new('Inspection_camera',data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    data.type = 'ORTHO'
    data.ortho_scale = size*1.28
    data.clip_end = size*1000
    report = {'asset_id':args.asset,'revision':args.revision,'status':'candidate_not_reviewed',
              'source':source.name,'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
              'original_export':original_source.name,'normal_repair_applied':normal_repair['applied'],
              'normal_geometry_alignment':normal_repair.get('after',normal_repair.get('before',{})).get('results',[]),
              'original_bounds':original_bounds,'target_height_m':args.height,
              'ground_fragment_cleanup':ground_fragments,
              'uniform_scale':factor,'meshes':len(meshes),
              'calibration_basis':basis,'calibration_sha256':hashlib.sha256(calibration_path.read_bytes()).hexdigest(),
              'calibrated_dimensions_m':list((high-low)*factor),
              'vertices':sum(len(o.data.vertices) for o in meshes),
              'faces':sum(len(o.data.polygons) for o in meshes),
              'materials':[m.name for m in bpy.data.materials],
              'images':[{'name':i.name,'size':list(i.size)} for i in bpy.data.images],
              'views':[]}
    # 标签为世界坐标观察方向；是否对应参考正面由看图确认。
    views = [('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),
             ('west',-1,0,.22),('perspective',1,-1,.7)]
    for name,x,y,z in views:
        camera.location=(x*size*3,y*size*3,scaled_height*.5+z*size)
        look_at(camera,(0,0,scaled_height*.5))
        scene.render.filepath=str(out/f'{name}.png')
        bpy.ops.render.render(write_still=True)
        report['views'].append(f'{name}.png')
        print('RENDERED',scene.render.filepath,flush=True)
    scene['production_status']='CANDIDATE_NOT_REVIEWED'
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    (out/'inspection.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('asset')
    parser.add_argument('--revision',default='r03')
    parser.add_argument('--height',type=float,required=True)
    parser.add_argument('--samples',type=int,default=32)
    main(parser.parse_args(sys.argv[sys.argv.index('--')+1:]))
