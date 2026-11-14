"""Repair material separation on the existing, calibrated merchant mesh."""
from pathlib import Path
import bpy,json,sys,hashlib,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'))
a=next(a for a in json.loads((WORLD/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'))['assets'] if a['id']=='m300')
out=ROOT/a['model_directory']/'r04/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'m300_r04.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/a['model_directory']/'r03/inspection/m300_r03.blend'))
obj=next(o for o in bpy.data.collections['ASSET_m300'].objects if o.type=='MESH');mesh=obj.data
v=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('co',v);v=v.reshape(-1,3)
# Remove accidental cloth labels from weapons, hands and breastplate, then
# consolidate the long rear cape; preserve the original texture elsewhere.
for p in mesh.polygons:
    points=v[list(p.vertices)];x,y,z=points.mean(0)
    if p.material_index==1 and ((z<.47 and y<.035) or (abs(x)<.24 and y<.03) or (z<.78 and y<-.055)):
        p.material_index=0
    if y>.18 and .30<z<.94:p.material_index=1
cloth=mesh.materials[1];nt=cloth.node_tree;nt.nodes.clear()
outnode=nt.nodes.new('ShaderNodeOutputMaterial');bs=nt.nodes.new('ShaderNodeBsdfPrincipled');nt.links.new(bs.outputs[0],outnode.inputs['Surface'])
bs.inputs['Roughness'].default_value=.92;bs.inputs['Specular IOR Level'].default_value=.12
noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=90;noise.inputs['Detail'].default_value=3
ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.028,.0025,.005,1);ramp.color_ramp.elements[1].color=(.085,.009,.018,1);nt.links.new(noise.outputs['Fac'],ramp.inputs['Fac']);nt.links.new(ramp.outputs[0],bs.inputs['Base Color'])
fine=nt.nodes.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=1600
bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.00025;bump.inputs['Strength'].default_value=.25;nt.links.new(fine.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
steel=mesh.materials[3];bs=steel.node_tree.nodes.get('Principled BSDF')
for l in list(bs.inputs['Base Color'].links):steel.node_tree.links.remove(l)
bs.inputs['Base Color'].default_value=(.43,.46,.48,1);bs.inputs['Metallic'].default_value=.95;bs.inputs['Roughness'].default_value=.3
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_percentage=100
camera=scene.camera
for name,x,y,z in [('perspective',1,-1,.7),('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22)]:
    camera.location=(x*4.05,y*4.05,.675+z*1.35);look_at(camera,(0,0,.675));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(out/'inspection.json').write_text(json.dumps({'asset_id':'m300','revision':'r04','status':'refined_candidate_not_reviewed','source':'m300_r03.blend','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'target_height_m':1.35,'changes':['Consolidated cape material segmentation','Physical dark wool shader','Uniform steel cheek and helmet shader'],'views':['south.png','east.png','north.png','west.png','perspective.png']},indent=2))
