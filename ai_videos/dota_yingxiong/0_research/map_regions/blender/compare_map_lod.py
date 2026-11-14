"""Render the original and map LOD with identical studio, camera and pixels."""
from pathlib import Path
import bpy,json,argparse,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
p=argparse.ArgumentParser();p.add_argument('--asset',required=True);p.add_argument('--version',default='overview_v001');p.add_argument('--clay',action='store_true');args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);dest=OUT/'lod_libraries'/args.version/args.asset;report=json.loads((dest/'lod_report.json').read_text());bpy.ops.wm.open_mainfile(filepath=report['source']);coll=bpy.data.collections['ASSET_'+args.asset];source={ob.name:ob for ob in coll.all_objects if ob.type=='MESH' and not ob.hide_render};bpy.context.view_layer.update();points=[ob.matrix_world@Vector(c) for ob in source.values() for c in ob.bound_box];lo=Vector([min(v[k] for v in points) for k in range(3)]);hi=Vector([max(v[k] for v in points) for k in range(3)]);center=(lo+hi)/2;size=max(hi-lo);scene=bpy.context.scene;scene.camera.location=center+Vector((size*2,-size*3,size*1.2));look_at(scene.camera,center);scene.camera.data.type='ORTHO';scene.camera.data.ortho_scale=size*1.3;scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100;scene.cycles.device='CPU';scene.cycles.samples=32;scene.cycles.seed=683;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.use_simplify=True;scene.cycles.texture_limit_render='1024'
suffix='clay' if args.clay else 'comparison'
if args.clay:
 mat=bpy.data.materials.new('Diagnostic_opaque_clay');mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.35,.35,.35,1);bs.inputs['Roughness'].default_value=.8;bpy.context.view_layer.material_override=mat
scene.render.filepath=str(dest/f'source_{suffix}.png');bpy.ops.render.render(write_still=True)
# Keep source studio and transforms. Only replace matching source mesh data.
original_names={ob:ob.name for ob in coll.all_objects}
for ob,name in original_names.items():ob.name='HIGH_'+name
with bpy.data.libraries.load(str(dest/(args.asset+'.blend')),link=False) as (src,dst):dst.collections=['ASSET_'+args.asset]
low=dst.collections[0];lookup={ob.name:ob for ob in low.all_objects if ob.type=='MESH' and not ob.hide_render};replaced=[]
for name,ob in source.items():
 if name not in lookup:raise KeyError(('Missing LOD object',name))
 ob.data=lookup[name].data;replaced.append(name)
scene.render.filepath=str(dest/f'lod_{suffix}.png');bpy.ops.render.render(write_still=True)
(dest/(suffix+'_settings.json')).write_text(json.dumps({'status':'author_comparison_pending','resolution':[512,512],'samples':32,'texture_limit':1024,'clay_override':args.clay,'camera':list(scene.camera.location),'target':list(center),'ortho_scale':scene.camera.data.ortho_scale,'replaced_meshes':replaced,'source_blend_unchanged':True},indent=2),encoding='utf-8');print('LOD_COMPARISON_RENDERED',args.asset,flush=True)
