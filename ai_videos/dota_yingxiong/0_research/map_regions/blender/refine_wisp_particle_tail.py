"""Separate the particulate wake from its soft volume, with a generous domain."""
from pathlib import Path
import bpy,sys,json,math,random,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3]
folder=next(next(ROOT.glob('2_*')).glob('characters/*/m306_*/model_3d'))
out=folder/'r16';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r15/authoring.blend'))
coll=bpy.data.collections['ASSET_m306'];rng=random.Random(30616)
for ob in coll.objects:
    if ob.name.startswith(('Visible_organic_Primary','Descending_individual_light_particles','Curved_volumetric_light_wake')):ob.hide_render=True

def emission(name,color,power):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;n.clear()
    e=n.new('ShaderNodeEmission');e.inputs[0].default_value=color;e.inputs[1].default_value=power
    o=n.new('ShaderNodeOutputMaterial');l.new(e.outputs[0],o.inputs['Surface']);return m

mat=emission('Pale_cyan_tapering_fibres',(.64,.89,1,1),24)
n=mat.node_tree.nodes;l=mat.node_tree.links;tc=n.new('ShaderNodeTexCoord');dist=n.new('ShaderNodeVectorMath');dist.operation='DISTANCE';dist.inputs[1].default_value=(0,0,1);l.new(tc.outputs['Object'],dist.inputs[0]);fade=n.new('ShaderNodeMapRange');fade.inputs['From Min'].default_value=.025;fade.inputs['From Max'].default_value=.29;fade.inputs['To Min'].default_value=24;fade.inputs['To Max'].default_value=0;l.new(dist.outputs['Value'],fade.inputs[0]);l.new(fade.outputs[0],n.get('Emission').inputs[1])
cu=bpy.data.curves.new('Six_asymmetric_soft_light_fibres','CURVE');cu.dimensions='3D';cu.bevel_depth=.00010;cu.bevel_resolution=2;cu.materials.append(mat)
center=Vector((0,0,1))
directions=[(-.8,.1,.4),(.12,.25,1),(.75,.3,-.1),(.1,-.7,-.6),(-.3,-.7,.4),(.45,-.2,-.8)]
lengths=[.19,.28,.22,.16,.135,.205]
for i,(direction,length) in enumerate(zip(directions,lengths)):
    d=Vector(direction).normalized();u=d.cross(Vector((0,1,0))).normalized();v=d.cross(u)
    bend=(-1 if i%2 else 1)*(.55+.1*i)
    c1=center+d*length*.24+u*length*bend*.5
    c2=center+d*length*.66-u*length*bend*.55+v*length*.15
    end=center+d*length+u*length*bend*.15
    s=cu.splines.new('POLY');s.points.add(64)
    for j,p in enumerate(s.points):
        t=j/64;co=(1-t)**3*center+3*(1-t)**2*t*c1+3*(1-t)*t*t*c2+t**3*end;p.co=(*co,1);p.radius=max(.002,(1-t)**1.4)
ob=bpy.data.objects.new('Six_curving_light_fibres',cu);coll.objects.link(ob)

def centerline(t):return Vector((.025*math.sin(t*math.pi*1.5),.36*t,1-.11*t-.012*math.sin(t*math.pi)))
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1);tmp=bpy.context.object;unit=[v.co.copy() for v in tmp.data.vertices];faces=[tuple(p.vertices) for p in tmp.data.polygons];bpy.data.objects.remove(tmp,do_unlink=True)
verts=[];polys=[];colors=[]
for i in range(1900):
    t=rng.betavariate(.8,1.5);spread=.001+.014*t**1.1;pos=centerline(t)+Vector((rng.gauss(0,spread),rng.gauss(0,spread*.5),rng.gauss(0,spread*.6)))
    r=rng.uniform(.00009,.00035)*(1-.45*t);a=(1-t)**1.2*.85+.015;start=len(verts)
    for v in unit:verts.append(tuple(pos+v*r));colors.append((.60*a,.87*a,a,1))
    polys.extend(tuple(start+j for j in f) for f in faces)
me=bpy.data.meshes.new('Tapered_individual_light_dust');me.from_pydata(verts,[],polys);attr=me.attributes.new('DustFade','FLOAT_COLOR','POINT');attr.data.foreach_set('color',np.asarray(colors,np.float32).ravel())
mat=emission('Pale_cyan_fading_dust',(.64,.89,1,1),22);nt=mat.node_tree;att=nt.nodes.new('ShaderNodeAttribute');att.attribute_name='DustFade';nt.links.new(att.outputs['Color'],nt.nodes.get('Emission').inputs[0]);me.materials.append(mat);ob=bpy.data.objects.new('Tapered_particle_wake',me);coll.objects.link(ob)
# The previous narrow domain could clip a changed centerline. This box is well
# outside the nonzero field; positions are baked to local coordinates.
verts=[(x,y,z) for z in (.72,1.16) for y in (-.08,.46) for x in (-.18,.18)]
faces=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
me=bpy.data.meshes.new('Unclipped_wake_domain');me.from_pydata(verts,[],faces);ob=bpy.data.objects.new('Soft_particle_wake_volume',me);coll.objects.link(ob)
mat=bpy.data.materials.new('Tapered_local_volume');mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;n.clear();o=n.new('ShaderNodeOutputMaterial');v=n.new('ShaderNodeVolumePrincipled');v.inputs['Density'].default_value=0;v.inputs['Emission Color'].default_value=(.64,.89,1,1);l.new(v.outputs[0],o.inputs['Volume']);tc=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Object'],sep.inputs[0])
def calc(op,a,b=None):
    q=n.new('ShaderNodeMath');q.operation=op
    for i,x in enumerate((a,b)):
        if x is None:continue
        if isinstance(x,(int,float)):q.inputs[i].default_value=x
        else:l.new(x,q.inputs[i])
    return q.outputs[0]
t=calc('DIVIDE',sep.outputs['Y'],.36);cx=calc('MULTIPLY',calc('SINE',calc('MULTIPLY',t,math.pi*1.5)),.025);cz=calc('SUBTRACT',calc('SUBTRACT',1,calc('MULTIPLY',t,.11)),calc('MULTIPLY',calc('SINE',calc('MULTIPLY',t,math.pi)),.012));dx=calc('SUBTRACT',sep.outputs['X'],cx);dz=calc('SUBTRACT',sep.outputs['Z'],cz);r2=calc('ADD',calc('MULTIPLY',dx,dx),calc('MULTIPLY',dz,dz));width=calc('MAXIMUM',calc('SUBTRACT',.009,calc('MULTIPLY',t,.007)),.002);g=calc('EXPONENT',calc('MULTIPLY',calc('DIVIDE',r2,calc('MULTIPLY',width,width)),-2));fade=calc('POWER',calc('MAXIMUM',calc('SUBTRACT',1,t),0),4);gate=calc('MULTIPLY',calc('GREATER_THAN',t,0),calc('LESS_THAN',t,1));strength=calc('MULTIPLY',calc('MULTIPLY',g,calc('MULTIPLY',fade,gate)),28);l.new(strength,v.inputs['Emission Strength']);me.materials.append(mat)
light=bpy.data.lights['Core_ground_emission_0'];light.energy=17;light.spot_size=.67;light.spot_blend=1;light.shadow_soft_size=.10
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=800;scene.render.resolution_y=800
scene.camera.data.ortho_scale=.8;scene.camera.location=(1.1,-1.6,1.25);look_at(scene.camera,(0,.05,1))
bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'revision':'r16','status':'author_preview_pending','source':'r15','main_filaments':6,'short_fuzz_filaments':600,'dust_particles':1900,'tail_length_m':.38,'tail_vertical_drop_m':.11,'volume_domain':'baked local coordinates, oversized closed box','ground_spot_watts':17,'ground_spot_radians':.67},indent=2))
scene.render.filepath=str(out/'close_preview.png');bpy.ops.render.render(write_still=True)
print('PREVIEW',scene.render.filepath,flush=True)
