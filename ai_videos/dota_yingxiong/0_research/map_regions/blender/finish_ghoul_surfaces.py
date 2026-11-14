"""Refine hair response, dermal roughness and dark woven loincloth."""
from pathlib import Path
import bpy,json,numpy as np,sys,hashlib
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('characters/*/m4_Ghoul/model_3d'));out=folder/'r08/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'m4_r08.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r06/inspection/m4_r06.blend'));coll=bpy.data.collections['ASSET_m4'];ob=next(o for o in coll.objects if o.type=='MESH');me=ob.data
hair=bpy.data.materials['Black_coarse_bristles'].node_tree.nodes.get('Principled BSDF');hair.inputs['Roughness'].default_value=.9;hair.inputs['Specular IOR Level'].default_value=.08;hair.inputs['Base Color'].default_value=(.002,.0015,.001,1)
mat=me.materials[0];nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');source=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and n.image.colorspace_settings.name=='sRGB')
contrast=nt.nodes.new('ShaderNodeHueSaturation');contrast.inputs['Saturation'].default_value=1.10;contrast.inputs['Value'].default_value=1.05;nt.links.new(source.outputs['Color'],contrast.inputs['Color']);nt.links.new(contrast.outputs[0],bs.inputs['Base Color']);bs.inputs['Subsurface Weight'].default_value=.025;bs.inputs['Subsurface Radius'].default_value=(.01,.006,.003)
tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=650;noise.inputs['Detail'].default_value=3;nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.00025;bump.inputs['Strength'].default_value=.32;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
data=np.load(folder/'r04/material_probe.npz');co=data['co'];rgb=data['colors'];mask=(np.abs(co[:,0])<.17)&(co[:,2]>.26)&(co[:,2]<.66)&(co[:,1]<.06)&(rgb[:,0]<.24)&(rgb[:,1]<.22)
cloth=mat.copy();cloth.name='Ghoul_dark_woven_loincloth';nt=cloth.node_tree;cb=nt.nodes.get('Principled BSDF');src=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and n.image.colorspace_settings.name=='sRGB');mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(.22,.16,.10,1);nt.links.new(src.outputs['Color'],mix.inputs[1]);nt.links.new(mix.outputs[0],cb.inputs['Base Color'])
for link in list(cb.inputs['Roughness'].links):nt.links.remove(link)
cb.inputs['Roughness'].default_value=.92;cb.inputs['Specular IOR Level'].default_value=.12;me.materials.append(cloth);labels=np.empty(len(me.polygons),np.int32);me.polygons.foreach_get('material_index',labels);clothfaces=mask.reshape(-1,3).sum(1)>=2;labels[clothfaces]=len(me.materials)-1;me.polygons.foreach_set('material_index',labels)
scene=bpy.context.scene;scene.cycles.samples=40;camera=scene.camera
for name,x,y,z in [('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22),('perspective',1,-1,.7)]:
    camera.location=(x*4.5,y*4.5,.72+z*1.5);look_at(camera,(0,0,.72));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report=json.loads((folder/'r06/inspection/inspection.json').read_text());report.update(revision='r08',source='m4_r06; rough black bristles, differentiated dark cloth and fine skin response; preserved original albedo range',sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),status='candidate_not_reviewed',cloth_faces=int(clothfaces.sum()));(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
