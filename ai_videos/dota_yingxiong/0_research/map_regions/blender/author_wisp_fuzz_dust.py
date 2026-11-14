"""Organic asymmetric light fibres and a descending particulate light trail."""
from pathlib import Path
import bpy,json,sys,math,random,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m306_*/model_3d'));out=folder/'r12';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r11/inspection/m306_r11.blend'));coll=bpy.data.collections['ASSET_m306'];rng=random.Random(30612)
for ob in coll.objects:
    if ob.name.startswith(('Wisp_light_filaments','Wisp_light_dust','Curved_volumetric_light_wake')):ob.hide_render=True
for name,strength,color in [('Wisp_fading_volume',125,(.82,.96,1,1)),('Cyan_atmospheric_fringe',5,(.48,.80,1,1))]:
    nt=bpy.data.materials[name].node_tree
    for n in nt.nodes:
        if n.type=='MATH' and n.operation=='MULTIPLY' and not n.inputs[1].is_linked and n.inputs[1].default_value>0:n.inputs[1].default_value=strength
        if n.type=='PRINCIPLED_VOLUME':n.inputs['Emission Color'].default_value=color
def emissive(name,color,strength,fade=False):
    m=bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;nt.nodes.clear();output=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=color;em.inputs['Strength'].default_value=strength;nt.links.new(em.outputs[0],output.inputs['Surface'])
    if fade:
        tc=nt.nodes.new('ShaderNodeTexCoord');dist=nt.nodes.new('ShaderNodeVectorMath');dist.operation='DISTANCE';dist.inputs[1].default_value=(0,0,1);nt.links.new(tc.outputs['Object'],dist.inputs[0]);r=nt.nodes.new('ShaderNodeMapRange');r.inputs['From Min'].default_value=.025;r.inputs['From Max'].default_value=.25;r.inputs['To Min'].default_value=strength;r.inputs['To Max'].default_value=0;nt.links.new(dist.outputs['Value'],r.inputs['Value']);nt.links.new(r.outputs[0],em.inputs['Strength'])
    return m
mainmat=emissive('Organic_fading_light_filaments',(.44,.82,1,1),7,True);fuzzmat=emissive('Fine_white_cyan_fuzz',(.70,.93,1,1),26);center=Vector((0,0,1))
for kind,count,bevel,mat in [('Primary',6,.00022,mainmat),('Fuzz',750,.00012,fuzzmat)]:
    cu=bpy.data.curves.new('Organic_'+kind,'CURVE');cu.dimensions='3D';cu.bevel_depth=bevel;cu.bevel_resolution=2;cu.materials.append(mat)
    directions=[(-.8,.1,.4),(.2,.7,.7),(.75,.3,-.1),(.1,-.7,-.6),(-.3,-.7,.4),(.45,-.2,.8)]
    for i in range(count):
        d=Vector(directions[i]).normalized() if kind=='Primary' else Vector((rng.gauss(0,1),rng.gauss(0,1),rng.gauss(0,1))).normalized();u=d.cross(Vector((0,1,0))).normalized();v=d.cross(u);length=rng.uniform(.16,.255) if kind=='Primary' else rng.uniform(.025,.095);bend=rng.uniform(-.6,.6);c1=center+d*length*.30+u*length*bend*.7;c2=center+d*length*.66-u*length*bend*.5+v*length*rng.uniform(-.3,.3);end=center+d*length+u*length*bend*.2;steps=40 if kind=='Primary' else 12;s=cu.splines.new('POLY');s.points.add(steps)
        for j,p in enumerate(s.points):t=j/steps;co=(1-t)**3*center+3*(1-t)**2*t*c1+3*(1-t)*t*t*c2+t**3*end;p.co=(*co,1);p.radius=max(.002,(1-t)**1.55)*(1 if kind=='Primary' else rng.uniform(.65,1.0))
    ob=bpy.data.objects.new('Visible_organic_'+kind,cu);coll.objects.link(ob)
# Join tiny real icospheres into one emissive mesh, retaining a smooth density fade.
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1);tmp=bpy.context.object;unit=[v.co.copy() for v in tmp.data.vertices];faces=[tuple(p.vertices) for p in tmp.data.polygons];bpy.data.objects.remove(tmp,do_unlink=True);verts=[];polys=[];colors=[]
for i in range(6500):
    t=rng.betavariate(.9,1.55);y=.38*t;spread=.002+.027*t**1.5;pos=Vector((.012*math.sin(t*math.pi)+rng.gauss(0,spread),y+rng.gauss(0,spread*.4),1-.12*t+rng.gauss(0,spread*.65)));radius=rng.uniform(.00018,.00085)*(1-.3*t);fade=(1-t)**1.6*.8+.025;start=len(verts)
    for v in unit:verts.append(tuple(pos+v*radius));colors.append((.50*fade,.82*fade,fade,1))
    polys.extend(tuple(start+j for j in f) for f in faces)
me=bpy.data.meshes.new('Volumetric_fine_light_dust');me.from_pydata(verts,[],polys);attr=me.attributes.new('DustFade','FLOAT_COLOR','POINT');attr.data.foreach_set('color',np.asarray(colors,np.float32).ravel());mat=emissive('Particulate_light_trail',(.5,.82,1,1),12);nt=mat.node_tree;attribute=nt.nodes.new('ShaderNodeAttribute');attribute.attribute_name='DustFade';nt.links.new(attribute.outputs['Color'],nt.nodes.get('Emission').inputs['Color']);me.materials.append(mat);ob=bpy.data.objects.new('Descending_individual_light_particles',me);coll.objects.link(ob)
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=720;scene.render.resolution_y=720;glow=next(n for n in scene.compositing_node_group.nodes if n.type=='GLARE');glow.inputs['Strength'].default_value=.65;glow.inputs['Size'].default_value=.25;glow.inputs['Threshold'].default_value=.8;camera=scene.camera;camera.data.ortho_scale=.72;camera.location=(1.1,-1.6,1.25);look_at(camera,(0,.05,1));bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'close_preview.png');bpy.ops.render.render(write_still=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r12','status':'author_preview_pending','source':'r11 instance-local optics with asymmetric soft filaments, visible fuzz and descending dust','main_filaments':6,'short_fuzz_filaments':750,'dust_particles':6500,'tail_length_m':.398},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
