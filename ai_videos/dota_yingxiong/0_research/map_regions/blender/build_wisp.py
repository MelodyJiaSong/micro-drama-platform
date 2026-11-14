"""Editable emissive-volume merchant, authored at card dimensions."""
from pathlib import Path
import bpy,sys,json,math,random,hashlib
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inspect_model import material,look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'))
manifest=json.loads((WORLD/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'));asset=next(a for a in manifest['assets'] if a['id']=='m306')
out=ROOT/asset['model_directory']/'r09/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'m306_r09.blend'
if dest.exists():raise FileExistsError(dest)
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
coll=bpy.data.collections.new('ASSET_m306');bpy.context.scene.collection.children.link(coll)
def relocate(obj):
    for c in list(obj.users_collection):c.objects.unlink(obj)
    coll.objects.link(obj);return obj
core=bpy.data.materials.new('Wisp_near_white');core.use_nodes=True;nt=core.node_tree;nt.nodes.clear();outnode=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(.82,.97,1,1);em.inputs['Strength'].default_value=12;nt.links.new(em.outputs[0],outnode.inputs['Surface'])
halo=bpy.data.materials.new('Wisp_fading_volume');halo.use_nodes=True;nt=halo.node_tree;nt.nodes.clear();outnode=nt.nodes.new('ShaderNodeOutputMaterial');vol=nt.nodes.new('ShaderNodeVolumePrincipled');vol.inputs['Color'].default_value=(.6,.88,1,1);vol.inputs['Emission Color'].default_value=(.7,.93,1,1)
tc=nt.nodes.new('ShaderNodeTexCoord');sub=nt.nodes.new('ShaderNodeVectorMath');sub.operation='SUBTRACT';sub.inputs[1].default_value=(.5,.5,.5);nt.links.new(tc.outputs['Generated'],sub.inputs[0]);length=nt.nodes.new('ShaderNodeVectorMath');length.operation='LENGTH';nt.links.new(sub.outputs[0],length.inputs[0]);ramp=nt.nodes.new('ShaderNodeMapRange');ramp.inputs['From Min'].default_value=.08;ramp.inputs['From Max'].default_value=.5;ramp.inputs['To Min'].default_value=5;ramp.inputs['To Max'].default_value=0;nt.links.new(length.outputs['Value'],ramp.inputs['Value']);nt.links.new(ramp.outputs[0],vol.inputs['Emission Strength']);nt.links.new(ramp.outputs[0],vol.inputs['Density']);nt.links.new(vol.outputs[0],outnode.inputs['Volume'])
for link in list(vol.inputs['Density'].links):nt.links.remove(link)
vol.inputs['Density'].default_value=0
square=nt.nodes.new('ShaderNodeMath');square.operation='MULTIPLY';nt.links.new(length.outputs['Value'],square.inputs[0]);nt.links.new(length.outputs['Value'],square.inputs[1])
negative=nt.nodes.new('ShaderNodeMath');negative.operation='MULTIPLY';negative.inputs[1].default_value=-240;nt.links.new(square.outputs[0],negative.inputs[0]);exponent=nt.nodes.new('ShaderNodeMath');exponent.operation='EXPONENT';nt.links.new(negative.outputs[0],exponent.inputs[0]);strength=nt.nodes.new('ShaderNodeMath');strength.operation='MULTIPLY';strength.inputs[1].default_value=300;nt.links.new(exponent.outputs[0],strength.inputs[0]);nt.links.new(strength.outputs[0],vol.inputs['Emission Strength'])
bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=.125,location=(0,0,1));obj=relocate(bpy.context.object);obj.name='Wisp_volume_25cm';obj.data.materials.append(halo)
# A separate broad, weak Gaussian supplies the cyan fringe around the hot core.
outer=halo.copy();outer.name='Cyan_atmospheric_fringe';ovn=outer.node_tree.nodes
for n in ovn:
    if n.type=='MATH' and n.operation=='MULTIPLY' and not n.inputs[1].is_linked:
        if n.inputs[1].default_value<0:n.inputs[1].default_value=-32
        elif n.inputs[1].default_value>100:n.inputs[1].default_value=6
ovn.get('Principled Volume').inputs['Emission Color'].default_value=(.18,.72,1,1)
bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=.14,location=(0,0,1));obj=relocate(bpy.context.object);obj.name='Soft_cyan_volume_fringe';obj.data.materials.append(outer)
rng=random.Random(306)
filament=core.copy();filament.name='Cyan_light_fibres';filament.node_tree.nodes.get('Emission').inputs['Color'].default_value=(.35,.80,1,1);filament.node_tree.nodes.get('Emission').inputs['Strength'].default_value=40
nt=filament.node_tree;em=nt.nodes.get('Emission');geo=nt.nodes.new('ShaderNodeNewGeometry');distance=nt.nodes.new('ShaderNodeVectorMath');distance.operation='DISTANCE';distance.inputs[1].default_value=(0,0,1);nt.links.new(geo.outputs['Position'],distance.inputs[0]);maprange=nt.nodes.new('ShaderNodeMapRange');maprange.inputs['From Min'].default_value=.015;maprange.inputs['From Max'].default_value=.18;nt.links.new(distance.outputs['Value'],maprange.inputs['Value']);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.75,.94,1,1);ramp.color_ramp.elements[1].color=(.045,.40,.75,1);nt.links.new(maprange.outputs[0],ramp.inputs[0]);nt.links.new(ramp.outputs[0],em.inputs['Color']);em.inputs['Strength'].default_value=18
curve=bpy.data.curves.new('Wisp_six_filaments_and_tail','CURVE');curve.dimensions='3D';curve.bevel_depth=.00045;curve.bevel_resolution=2
for i in range(486):
    s=curve.splines.new('POLY');s.points.add(17)
    if i<6:
        direction=Vector([(1,.3,.55),(-1,.7,-.15),(.45,1,-.7),(-.6,-1,.4),(.25,-.25,1),(-.6,-.5,-1)][i]).normalized()
    else:
        z=1-2*(i-6+.5)/480;a=i*2.399963;rr=math.sqrt(1-z*z);direction=Vector((rr*math.cos(a),rr*math.sin(a),z))
    length=rng.uniform(.20,.26) if i<6 else rng.uniform(.035,.08)
    for j,p in enumerate(s.points):
        t=j/17;curvature=.028 if i<6 else .008;co=Vector((0,0,1))+direction*length*t+Vector((math.sin(t*5+i)*curvature*t,math.sin(t*7+i)*curvature*t,math.sin(t*6+i)*curvature*t));p.co=(*co,1);p.radius=max(.02,(1-t)**1.7)*(1 if i<6 else .45)
curve.materials.append(filament);obj=bpy.data.objects.new('Wisp_light_filaments',curve);coll.objects.link(obj)
taildir=Vector((.4,.8,-.25)).normalized()
tail=bpy.data.curves.new('Tapering_luminous_tail','CURVE');tail.dimensions='3D';tail.bevel_depth=.0008;tail.bevel_resolution=2;tail.materials.append(filament)
for i in range(2):
    spline=tail.splines.new('POLY');spline.points.add(30);phase=rng.random()*math.tau
    for j,p in enumerate(spline.points):
        t=j/30;spread=.007*math.sin(math.pi*t)*(1-t);co=Vector((0,0,1))+taildir*.26*t+Vector((math.cos(phase+t*9)*spread,math.sin(phase+t*7)*spread,.035*math.sin(math.pi*t*.7)));p.co=(*co,1);p.radius=max(.005,(1-t)**2*.8)
o=bpy.data.objects.new('Wisp_tapered_light_tail',tail);coll.objects.link(o)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1);particle=relocate(bpy.context.object);particle.name='Wisp_light_dust_000';particle_mat=filament.copy();particle_mat.name='Fading_light_dust';info=particle_mat.node_tree.nodes.new('ShaderNodeObjectInfo');particle_mat.node_tree.links.new(info.outputs['Color'],particle_mat.node_tree.nodes.get('Emission').inputs['Color']);particle.data.materials.append(particle_mat)
for i in range(900):
    t=rng.uniform(0,1.1);spread=.003+.025*t*t
    p=particle if i==0 else bpy.data.objects.new('Wisp_light_dust_'+str(i),particle.data)
    if i:coll.objects.link(p)
    fade=max(.025,(1-t*.85)**1.4);p.location=Vector((0,0,1))+taildir*.38*t+Vector((rng.gauss(0,spread),rng.gauss(0,spread),.035*math.sin(math.pi*t)+rng.gauss(0,spread)));p.scale=(rng.uniform(.00035,.0010)*(1.1-t*.4),)*3;p.color=(.25*fade,.75*fade,fade,1)
data=bpy.data.lights.new('Wisp_actual_light','POINT');data.energy=65;data.color=(.65,.9,1);data.shadow_soft_size=.10;obj=bpy.data.objects.new('Wisp_actual_light',data);obj.location=(0,0,1);coll.objects.link(obj)
for i,(angle,power) in enumerate([(.42,8),(.8,22),(1.25,18)]):
    data=bpy.data.lights.new('Core_ground_emission_'+str(i),'SPOT');data.energy=power;data.color=(.65,.9,1);data.spot_size=angle;data.spot_blend=1;data.shadow_soft_size=.09;lamp=bpy.data.objects.new('Core_ground_emission_'+str(i),data);lamp.location=(0,0,1);coll.objects.link(lamp)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=64;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=960;scene.render.resolution_y=960;scene.view_settings.view_transform='AgX'
scene.cycles.volume_biased=True;scene.cycles.volume_step_rate=.1;scene.cycles.volume_max_steps=4096
scene.world=bpy.data.worlds.new('Grey_studio');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.25
key=bpy.data.lights.new('Soft_studio','AREA');key.energy=60;key.size=3;ob=bpy.data.objects.new('Soft_studio',key);scene.collection.objects.link(ob);ob.location=(1,-2,3);look_at(ob,(0,0,.7))
bpy.ops.mesh.primitive_plane_add(size=200);bpy.context.object.name='Studio_floor';bpy.context.object.data.materials.append(material('Floor',(.45,.45,.45)))
data=bpy.data.cameras.new('Inspection_camera');camera=bpy.data.objects.new('Inspection_camera',data);scene.collection.objects.link(camera);scene.camera=camera;data.type='ORTHO';data.ortho_scale=1.7
nt=bpy.data.node_groups.new('Optical_bloom','CompositorNodeTree');scene.compositing_node_group=nt;nt.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');rl=nt.nodes.new('CompositorNodeRLayers');glow=nt.nodes.new('CompositorNodeGlare');glow.inputs['Type'].default_value='Fog Glow';glow.inputs['Quality'].default_value='High';glow.inputs['Threshold'].default_value=1.0;glow.inputs['Size'].default_value=.25;glow.inputs['Strength'].default_value=.35;nt.links.new(rl.outputs['Image'],glow.inputs['Image']);output=nt.nodes.new('NodeGroupOutput');nt.links.new(glow.outputs['Image'],output.inputs['Image'])
for name,x,y,z in [('south',0,-1,1.0),('east',1,0,1.0),('north',0,1,1.0),('west',-1,0,1.0),('perspective',.7,-.7,2.8)]:
    camera.location=(x*4,y*4,1+z);look_at(camera,(0,0,.65));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
data.ortho_scale=.72;camera.location=(1.1,-1.6,1.25);look_at(camera,(0,.05,1));scene.render.filepath=str(out/'close.png');bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(dest))
report={'asset_id':'m306','revision':'r09','source':'procedural_authoring_from_asset_card','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'status':'candidate_not_reviewed','diameter_m':.25,'hover_height_m':1,'tail_length_m':.38,'dust_particles':900,'main_filaments':6,'short_fuzz_filaments':480,'ground_illumination':'point emitter plus three smoothly blended spot lobes at the same luminous core; no ground decal','volume_sampling':'step rate 0.1, biased ray marching; separated nested boundaries','views':['south.png','east.png','north.png','west.png','perspective.png'],'supplemental_views':['close.png']}
(out/'inspection.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SAVED',dest,flush=True)
