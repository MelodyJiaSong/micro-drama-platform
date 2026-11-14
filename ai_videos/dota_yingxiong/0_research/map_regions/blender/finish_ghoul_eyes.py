"""Fit small recessed amber eyes using the generated socket landmarks."""
from pathlib import Path
import bpy,json,sys,hashlib,time,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import material,look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m4_Ghoul/model_3d'));source=folder/'r08/inspection/m4_r08.blend';out=folder/'r09/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'m4_r09.blend'
if dest.exists():raise FileExistsError(dest)
while not source.exists():time.sleep(10)
bpy.ops.wm.open_mainfile(filepath=str(source));coll=bpy.data.collections['ASSET_m4'];report=json.loads((source.parent/'inspection.json').read_text());scale=report['uniform_scale'];d=np.load(folder/'r04/material_probe.npz');co=d['co'];rgb=d['colors'];base=(co[:,2]>.81)&(co[:,2]<.90)&(co[:,1]<-.36)&(rgb[:,0]<.13)
sclera=material('Ghoul_dark_sclera',(.022,.014,.007),.24);iris=material('Ghoul_amber_iris',(.30,.18,.018),.2);pupil=material('Ghoul_round_pupil',(.0005,.0005,.0003),.15)
for mat in [sclera,iris,pupil]:mat.node_tree.nodes.get('Principled BSDF').inputs['Coat Weight'].default_value=.4
nt=iris.node_tree;bs=nt.nodes.get('Principled BSDF');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=250;noise.inputs['Detail'].default_value=3;ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.08,.045,.003,1);ramp.color_ramp.elements[1].color=(.50,.31,.025,1);nt.links.new(noise.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color'])
landmarks=[]
for side in [-1,1]:
    mask=(co[:,0]*side>.025)&(co[:,0]*side<.08)&base;center=Vector(co[mask].mean(0))*scale;center.y-=.003;landmarks.append(list(center))
    for name,offset,size,mat in [('Recessed_eyeball',0,(.012,.009,.009),sclera),('Amber_iris',-.008,(.006,.002,.006),iris),('Dark_pupil',-.010,(.0022,.001,.0022),pupil)]:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=24,radius=1,location=center+Vector((0,offset,0)));o=bpy.context.object
        for c in list(o.users_collection):c.objects.unlink(o)
        coll.objects.link(o);o.name=name;o.scale=size;o.data.materials.append(mat)
        for p in o.data.polygons:p.use_smooth=True
nt=bpy.data.materials['Aged_yellow_white_enamel'].node_tree
for n in nt.nodes:
    if n.type=='HUE_SAT':n.inputs['Saturation'].default_value=.45;n.inputs['Value'].default_value=.80
scene=bpy.context.scene;scene.cycles.samples=32;camera=scene.camera
for name,x,y,z in [('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22),('perspective',1,-1,.7)]:
    camera.location=(x*4.5,y*4.5,.72+z*1.5);look_at(camera,(0,0,.72));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
camera.data.ortho_scale=.55;camera.location=(0,-2,1.25);look_at(camera,(0,-.42,1.05));scene.render.filepath=str(out/'face_detail.png');bpy.ops.render.render(write_still=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report.update(revision='r09',source='m4_r08 with fitted recessed eyes and aged enamel',sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),status='candidate_not_reviewed',eye_centres_m=landmarks,supplemental_views=['face_detail.png']);(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
