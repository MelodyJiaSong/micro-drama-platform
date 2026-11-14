"""Closed pointed rock forms, exposed entry stairs and natural sky reflections."""
from pathlib import Path
import bpy,json,math,sys,hashlib,time,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import material,look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));OUT=WORLD/'background/map_3d';SRC=OUT/'environment_sources';folder=next(WORLD.glob('background/*/bg15_*/model_3d'));source=folder/'r02/inspection/bg15_r02.blend';out=folder/'r03/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'bg15_r03.blend'
if dest.exists():raise FileExistsError(dest)
while not source.exists():time.sleep(10)
bpy.ops.wm.open_mainfile(filepath=str(source));coll=bpy.data.collections['ASSET_bg15']
with bpy.data.libraries.load(str(next((SRC/'boulder_01').glob('*.blend'))),link=False) as (s,d):d.objects=['boulder_01_LOD1']
rock=d.objects[0];me=rock.data.copy();v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);low,high=v.min(0),v.max(0);v[:,:2]-=(low[:2]+high[:2])/2;v[:,2]-=low[2];v/=high-low;t=v[:,2];v[:,:2]*=(1-.32*np.clip((t-.45)/.55,0,1))[:,None];me.vertices.foreach_set('co',v.ravel());me.update()
for ob in coll.objects:
    if ob.name.startswith(('Natural_limestone_pinnacle','Rear_spire')):
        size=(ob.scale.x*4.87,ob.scale.y*3.47,ob.scale.z*4.73);ob.data=me;ob.scale=size
    if ob.name.startswith('Weathered_entry_stair'):
        radius=abs(ob.location.y);z=.53+(5.12-radius)/(.62)*(-.49) if radius>4.5 else 1.06+(radius-3.7)/.8*(-.53)
        # Linear interpolation follows the original closed mound profile.
        profile=[(3.35,1.10),(3.7,1.06),(4.5,.53),(5.12,.04)]
        for (r0,h0),(r1,h1) in zip(profile,profile[1:]):
            if r0<=radius<=r1:z=h0+(h1-h0)*(radius-r0)/(r1-r0)
        ob.location.z=z+.10
    if ob.name.startswith('Splash_drop'):ob.scale*=.65
calcite=bpy.data.materials['Pale_calcite_basin'];nt=calcite.node_tree;bs=nt.nodes.get('Principled BSDF');src=bs.inputs['Base Color'].links[0].from_socket;mix=nt.nodes.new('ShaderNodeMixRGB');mix.inputs[0].default_value=.70;mix.inputs[2].default_value=(.62,.67,.62,1);nt.links.new(src,mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
nt=bpy.data.materials['Clear_cyan_spring_water'].node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.75,.94,1,1);bs.inputs['Roughness'].default_value=.075;next(n for n in nt.nodes if n.type=='VOLUME_ABSORPTION').inputs['Density'].default_value=.16
foam=bpy.data.materials['Aerated_water_foam'];nt=foam.node_tree;bs=nt.nodes.get('Principled BSDF');output=nt.nodes.get('Material Output');tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=30;noise.inputs['Detail'].default_value=3;nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.42;ramp.color_ramp.elements[1].position=.65;nt.links.new(noise.outputs['Fac'],ramp.inputs[0]);transparent=nt.nodes.new('ShaderNodeBsdfTransparent');mix=nt.nodes.new('ShaderNodeMixShader');nt.links.new(ramp.outputs[0],mix.inputs[0]);nt.links.new(transparent.outputs[0],mix.inputs[1]);nt.links.new(bs.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],output.inputs['Surface'])
for o in coll.objects:
    if o.name.startswith('Aerated_water_thread'):o.data.bevel_depth*=.45
scene=bpy.context.scene;nt=scene.world.node_tree;bg=nt.nodes.get('Background');sky=nt.nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(38);sky.sun_rotation=math.radians(115);sky.air_density=1;sky.sun_intensity=.7;nt.links.new(sky.outputs['Color'],bg.inputs['Color']);bg.inputs['Strength'].default_value=.35;scene.view_settings.exposure=-1
for im in bpy.data.images:
    if im.source=='FILE' and not im.packed_file:
        found=list(SRC.glob('*/textures/'+Path(im.filepath.replace('\\','/')).name))
        if found:im.filepath=str(found[0]);im.reload()
scene.cycles.samples=32;camera=scene.camera
# Preserve an authoring checkpoint before the long multi-view rendering stage.
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(folder/'r03/authoring.blend'))
for name,x,y,z in [('south',0,-1,.35),('east',1,0,.35),('north',0,1,.35),('west',-1,0,.35),('perspective',1,-1,.7),('basin_detail',.3,-1,1.2)]:
    camera.location=(x*25,y*25,2.5+z*25);look_at(camera,(0,0,2.3));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(dest));report=json.loads((source.parent/'inspection.json').read_text());report.update(revision='r03',source='r02; closed irregular boulder spires, visible stairs, clear water under physical daylight and broken whitewater',sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),status='candidate_not_reviewed');(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
