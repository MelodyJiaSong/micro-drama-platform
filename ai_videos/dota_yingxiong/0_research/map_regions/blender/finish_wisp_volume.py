"""Continuous volumetric light trail and fading optical filaments."""
from pathlib import Path
import bpy,json,math,sys,hashlib,random
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at,material
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m306_Enchanted_Artifacts/model_3d'));out=folder/'r10/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'m306_r10.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r09/inspection/m306_r09.blend'));coll=bpy.data.collections['ASSET_m306'];center=Vector((0,0,1));rng=random.Random(30610)
cu=bpy.data.objects['Wisp_light_filaments'].data
for i,s in enumerate(cu.splines):
    direction=(Vector(s.points[-1].co[:3])-center).normalized();length=.18 if i<6 else rng.uniform(.025,.065);bend=direction.cross(Vector((0,0,1)))*.009
    for j,p in enumerate(s.points):
        t=j/(len(s.points)-1);p.co=(*(center+direction*length*t+bend*math.sin(t*math.pi)),1);p.radius=(1-t)**2*(1 if i<6 else .20)
nt=bpy.data.materials['Cyan_light_fibres'].node_tree;em=nt.nodes.get('Emission');dist=next(n for n in nt.nodes if n.type=='VECT_MATH' and n.operation=='DISTANCE');fade=nt.nodes.new('ShaderNodeMapRange');fade.inputs['From Min'].default_value=.025;fade.inputs['From Max'].default_value=.18;fade.inputs['To Min'].default_value=14;fade.inputs['To Max'].default_value=0;nt.links.new(dist.outputs['Value'],fade.inputs['Value']);nt.links.new(fade.outputs[0],em.inputs['Strength'])
for n in bpy.data.materials['Cyan_atmospheric_fringe'].node_tree.nodes:
    if n.type=='MATH' and n.operation=='MULTIPLY' and not n.inputs[1].is_linked:
        if n.inputs[1].default_value<0:n.inputs[1].default_value=-55
        elif n.inputs[1].default_value>0:n.inputs[1].default_value=45
taildir=Vector((0,1,-.18)).normalized();oldtail=Vector((.4,.8,-.25)).normalized();rotate=oldtail.rotation_difference(taildir)
for ob in coll.objects:
    if ob.name.startswith('Wisp_light_dust'):
        delta=ob.location-center;ob.location=center+rotate@delta;ob.scale*=rng.uniform(.3,.7)
        if rng.random()<.55:ob.hide_render=True
    if ob.name=='Wisp_tapered_light_tail':ob.hide_render=True
# An ellipsoidal emitter has a Gaussian radial falloff and fades longitudinally.
bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,radius=1,location=center+taildir*.14);trail=bpy.context.object
for c in list(trail.users_collection):c.objects.unlink(trail)
coll.objects.link(trail);trail.name='Continuous_soft_light_trail';trail.scale=(.019,.019,.17);trail.rotation_euler=taildir.to_track_quat('Z','Y').to_euler()
m=bpy.data.materials.new('Gaussian_tail_volume');m.use_nodes=True;nt=m.node_tree;n,l=nt.nodes,nt.links;n.clear();output=n.new('ShaderNodeOutputMaterial');vol=n.new('ShaderNodeVolumePrincipled');vol.inputs['Density'].default_value=0;vol.inputs['Emission Color'].default_value=(.30,.82,1,1);l.new(vol.outputs[0],output.inputs['Volume']);tc=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Generated'],sep.inputs[0])
def mathnode(op,a,b=None):
    no=n.new('ShaderNodeMath');no.operation=op
    if isinstance(a,(float,int)):no.inputs[0].default_value=a
    else:l.new(a,no.inputs[0])
    if b is not None:
        if isinstance(b,(float,int)):no.inputs[1].default_value=b
        else:l.new(b,no.inputs[1])
    return no.outputs[0]
x=mathnode('SUBTRACT',sep.outputs['X'],.5);y=mathnode('SUBTRACT',sep.outputs['Y'],.5);r2=mathnode('ADD',mathnode('MULTIPLY',x,x),mathnode('MULTIPLY',y,y));radial=mathnode('EXPONENT',mathnode('MULTIPLY',r2,-60));along=mathnode('POWER',mathnode('SUBTRACT',1,sep.outputs['Z']),2);intensity=mathnode('MULTIPLY',mathnode('MULTIPLY',radial,along),500);l.new(intensity,vol.inputs['Emission Strength']);trail.data.materials.append(m)
bpy.data.lights['Wisp_actual_light'].energy=8
for i,power in enumerate([30,8,0]):bpy.data.lights['Core_ground_emission_'+str(i)].energy=power
scene=bpy.context.scene;scene.cycles.samples=96;scene.cycles.use_denoising=True
glow=next(n for n in scene.compositing_node_group.nodes if n.type=='GLARE');glow.inputs['Strength'].default_value=1.0;glow.inputs['Size'].default_value=.35;glow.inputs['Threshold'].default_value=.7
# Scale reference is a separate inspection prop, never part of the asset collection.
bpy.ops.mesh.primitive_cube_add(size=.1,location=(.38,0,.05));bpy.context.object.name='Inspection_10cm_scale_cube';bpy.context.object.data.materials.append(material('Scale_cube_grey',(.2,.2,.2),.8))
camera=scene.camera;camera.data.ortho_scale=1.7
for name,x,y,z in [('south',0,-1,1),('east',1,0,1),('north',0,1,1),('west',-1,0,1),('perspective',.7,-.7,2.8)]:
    camera.location=(x*4,y*4,1+z);look_at(camera,(0,0,.65));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
for name,loc,target,size in [('close',(1.1,-1.6,1.25),(0,.05,1),.72),('top',(0,0,4),(0,.05,1),.8),('bottom',(0,0,.2),(0,.05,1),.8)]:
    camera.data.ortho_scale=size;camera.location=loc;look_at(camera,target);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(dest));report=json.loads((folder/'r09/inspection/inspection.json').read_text());report.update(revision='r10',sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),source='r09 refined with Gaussian volume tail, smoothly fading filaments, reduced particle dust',status='candidate_not_reviewed',supplemental_views=['close.png','top.png','bottom.png'],scale_reference_m=.1,tail_direction=[0,1,-.18],ground_illumination='8W point plus compact blended spot, no ground decal');(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
