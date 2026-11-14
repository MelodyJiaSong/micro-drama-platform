"""Use a point emitter, Gaussian halo and separate visible dust particles."""
from pathlib import Path
import bpy,json,sys,math,random,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m306_*/model_3d'));out=folder/'r19';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r17/authoring.blend'));coll=bpy.data.collections['ASSET_m306'];center=Vector((0,0,1));rng=random.Random(30618)
for ob in coll.objects:
 if ob.type=='LIGHT':
  ob.data.energy=70 if ob.data.type=='POINT' else 0;ob.data.color=(.24,.74,1);ob.data.shadow_soft_size=.09
 if ob.name in ['Six_curving_light_fibres','Tapered_particle_wake','Soft_particle_wake_volume']:ob.hide_render=True
 if ob.name=='Visible_organic_Fuzz':
  for i,s in enumerate(list(ob.data.splines)):
   if i%2:ob.data.splines.remove(s)
  ob.data.bevel_depth=.000085
nt=bpy.data.materials['Cyan_atmospheric_fringe'].node_tree;volume=next(n for n in nt.nodes if n.type=='PRINCIPLED_VOLUME');volume.inputs['Emission Color'].default_value=(.035,.55,1,1);volume.inputs['Color'].default_value=(.2,.65,.9,1);volume.inputs['Anisotropy'].default_value=.2
exponent=next(n for n in nt.nodes if n.type=='MATH' and n.operation=='EXPONENT')
for n in nt.nodes:
 if n.type=='MATH' and n.operation=='MULTIPLY' and not n.inputs[1].is_linked:
  if n.inputs[1].default_value<0:n.inputs[1].default_value=-38
  elif n.inputs[1].default_value>0:n.inputs[1].default_value=9
density=nt.nodes.new('ShaderNodeMath');density.operation='MULTIPLY';density.inputs[1].default_value=.2;nt.links.new(exponent.outputs[0],density.inputs[0]);nt.links.new(density.outputs[0],volume.inputs['Density'])
def emission(name,color,power):
 m=bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;nt.nodes.clear();e=nt.nodes.new('ShaderNodeEmission');e.inputs[0].default_value=(*color,1);e.inputs[1].default_value=power;o=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(e.outputs[0],o.inputs['Surface']);return m
mat=emission('Irregular_cyan_star_filaments',(.10,.65,1),25);nt=mat.node_tree;tc=nt.nodes.new('ShaderNodeTexCoord');dist=nt.nodes.new('ShaderNodeVectorMath');dist.operation='DISTANCE';dist.inputs[1].default_value=(0,0,1);nt.links.new(tc.outputs['Object'],dist.inputs[0]);fade=nt.nodes.new('ShaderNodeMapRange');fade.inputs['From Min'].default_value=.025;fade.inputs['From Max'].default_value=.28;fade.inputs['To Min'].default_value=25;fade.inputs['To Max'].default_value=0;nt.links.new(dist.outputs['Value'],fade.inputs[0]);nt.links.new(fade.outputs[0],nt.nodes.get('Emission').inputs[1]);cu=bpy.data.curves.new('Six_irregular_star_filaments','CURVE');cu.dimensions='3D';cu.bevel_depth=.00012;cu.bevel_resolution=2;cu.materials.append(mat)
directions=[(.45,.15,1),(-.7,-.1,.42),(.95,.35,.12),(.25,.75,-.65),(-.35,.15,-.48),(.55,-.6,.48)];lengths=[.27,.14,.20,.12,.10,.15]
for i,(direction,length) in enumerate(zip(directions,lengths)):
 d=Vector(direction).normalized();u=d.cross(Vector((0,1,0))).normalized();c1=center+d*length*.25+u*length*rng.uniform(-.18,.18);c2=center+d*length*.7+u*length*rng.uniform(-.25,.25);end=center+d*length+u*length*rng.uniform(-.1,.1);s=cu.splines.new('POLY');s.points.add(64)
 for j,p in enumerate(s.points):
  t=j/64;co=(1-t)**3*center+3*(1-t)**2*t*c1+3*(1-t)*t*t*c2+t**3*end;p.co=(*co,1);p.radius=max(.002,(1-t)**1.6)
ob=bpy.data.objects.new(cu.name,cu);coll.objects.link(ob)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1);tmp=bpy.context.object;unit=[v.co.copy() for v in tmp.data.vertices];faces=[tuple(p.vertices) for p in tmp.data.polygons];bpy.data.objects.remove(tmp,do_unlink=True);verts=[];polys=[];colors=[]
for i in range(700):
 t=rng.betavariate(1.05,1.25);spread=.002+.026*t;pos=Vector((.025*math.sin(t*math.pi*1.5),.36*t,1-.09*t))+Vector((rng.gauss(0,spread),rng.gauss(0,spread*.4),rng.gauss(0,spread*.65)));radius=rng.uniform(.0004,.0014)*(1-.35*t);fade=(1-t)**1.5*.85+.015;start=len(verts)
 for v in unit:verts.append(tuple(pos+v*radius));colors.append((.12*fade,.65*fade,fade,1))
 polys.extend(tuple(start+j for j in f) for f in faces)
me=bpy.data.meshes.new('Sparse_resolvable_cyan_light_dust');me.from_pydata(verts,[],polys);attr=me.attributes.new('DustFade','FLOAT_COLOR','POINT');attr.data.foreach_set('color',np.array(colors,np.float32).ravel());mat=emission('Sparse_cyan_light_dust',(.1,.65,1),18);nt=mat.node_tree;att=nt.nodes.new('ShaderNodeAttribute');att.attribute_name='DustFade';nt.links.new(att.outputs['Color'],nt.nodes.get('Emission').inputs[0]);me.materials.append(mat);ob=bpy.data.objects.new(me.name,me);coll.objects.link(ob)
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=900;scene.render.resolution_y=900;scene.camera.data.ortho_scale=.72;scene.camera.location=(1.1,-1.6,1.25);look_at(scene.camera,(0,.05,1));bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'revision':'r19','status':'author_preview_pending','source':'r17','changes':['Single 70 W point emitter; spot emitters disabled','Balanced Gaussian cyan emission and light scattering halo; r18 oversized halo rejected','No continuous wake volume; 700 separate dust grains resolvable at medium distance','Asymmetric six fine star filaments; 300 shorter fuzz strands'],'main_filaments':6,'short_fuzz_filaments':300,'dust_particles':700,'tail_length_m':.38,'remaining':['All-view lighting and translated-instance checks pending']},indent=2),encoding='utf-8');scene.render.filepath=str(out/'close_preview.png');bpy.ops.render.render(write_still=True)
