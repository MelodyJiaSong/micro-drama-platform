"""Unify cape panels and groom undercoat after material-mask diagnostics."""
from pathlib import Path
import bpy,json,sys,hashlib,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'))
a=next(a for a in json.loads((WORLD/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'))['assets'] if a['id']=='m300')
out=ROOT/a['model_directory']/'r05/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'m300_r05.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/a['model_directory']/'r04/inspection/m300_r04.blend'))
coll=bpy.data.collections['ASSET_m300'];obj=next(o for o in coll.objects if o.type=='MESH');mesh=obj.data
v=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('co',v);v=v.reshape(-1,3)
for p in mesh.polygons:
    x,y,z=v[list(p.vertices)].mean(0)
    if (y>.12 and .12<z<1.02) or (abs(x)>.30 and y>-.035 and .17<z<1.02) or (abs(x)>.17 and y>-.11 and .96<z<1.08):p.material_index=1
cloth=mesh.materials[1];ramp=next(n for n in cloth.node_tree.nodes if n.type=='VALTORGB');ramp.color_ramp.elements[0].color=(.003,.0003,.0006,1);ramp.color_ramp.elements[1].color=(.012,.0012,.0025,1)
hairbase=mesh.materials[2];bs=hairbase.node_tree.nodes.get('Principled BSDF')
for link in list(bs.inputs['Base Color'].links):hairbase.node_tree.links.remove(link)
bs.inputs['Base Color'].default_value=(.07,.025,.005,1);bs.inputs['Roughness'].default_value=.9
hair=next(o for o in coll.objects if o.type=='CURVE');hair.location.y-=.005
steel=mesh.materials[3];bs=steel.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.43;bs.inputs['Base Color'].default_value=(.26,.28,.29,1)
noise=steel.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=40
mix=steel.node_tree.nodes.new('ShaderNodeValToRGB');mix.color_ramp.elements[0].color=(.12,.13,.14,1);mix.color_ramp.elements[1].color=(.40,.43,.45,1);steel.node_tree.links.new(noise.outputs[0],mix.inputs[0]);steel.node_tree.links.new(mix.outputs[0],bs.inputs['Base Color'])
scene=bpy.context.scene;scene.cycles.samples=24;camera=scene.camera
for name,x,y,z in [('perspective',1,-1,.7),('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22)]:
    camera.location=(x*4.05,y*4.05,.675+z*1.35);look_at(camera,(0,0,.675));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(out/'inspection.json').write_text(json.dumps({'asset_id':'m300','revision':'r05','status':'refined_candidate_not_reviewed','source':'m300_r04.blend','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'target_height_m':1.35,'changes':['Unified cape panels','Dark wool reflectance correction','Dark hair undercoat and fibre offset','Worn steel variation'],'views':['south.png','east.png','north.png','west.png','perspective.png']},indent=2))
