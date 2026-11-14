"""Organic asymmetric light fibres and a descending particulate light trail."""
from pathlib import Path
import bpy,json,sys,math,random,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m306_*/model_3d'));out=folder/'r15';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r11/inspection/m306_r11.blend'));coll=bpy.data.collections['ASSET_m306'];rng=random.Random(30612)
for ob in coll.objects:
    if ob.name.startswith(('Wisp_light_filaments','Wisp_light_dust','Curved_volumetric_light_wake')):ob.hide_render=True
for name,strength,color in [('Wisp_fading_volume',125,(.82,.96,1,1)),('Cyan_atmospheric_fringe',12,(.48,.80,1,1))]:
    nt=bpy.data.materials[name].node_tree
    for n in nt.nodes:
        if n.type=='MATH' and n.operation=='MULTIPLY' and not n.inputs[1].is_linked and n.inputs[1].default_value>0:n.inputs[1].default_value=strength
        if n.type=='PRINCIPLED_VOLUME':n.inputs['Emission Color'].default_value=color
def emissive(name,color,strength,fade=False):
    m=bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;nt.nodes.clear();output=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=color;em.inputs['Strength'].default_value=strength;nt.links.new(em.outputs[0],output.inputs['Surface'])
    if fade:
        tc=nt.nodes.new('ShaderNodeTexCoord');dist=nt.nodes.new('ShaderNodeVectorMath');dist.operation='DISTANCE';dist.inputs[1].default_value=(0,0,1);nt.links.new(tc.outputs['Object'],dist.inputs[0]);r=nt.nodes.new('ShaderNodeMapRange');r.inputs['From Min'].default_value=.025;r.inputs['From Max'].default_value=.145;r.inputs['To Min'].default_value=strength;r.inputs['To Max'].default_value=0;nt.links.new(dist.outputs['Value'],r.inputs['Value']);nt.links.new(r.outputs[0],em.inputs['Strength'])
    return m
mainmat=emissive('Organic_fading_light_filaments',(.25,.76,1,1),26,True);fuzzmat=emissive('Fine_white_cyan_fuzz',(.35,.78,1,1),17);center=Vector((0,0,1))
for kind,count,bevel,mat in [('Primary',6,.00011,mainmat),('Fuzz',600,.00009,fuzzmat)]:
    cu=bpy.data.curves.new('Organic_'+kind,'CURVE');cu.dimensions='3D';cu.bevel_depth=bevel;cu.bevel_resolution=2;cu.materials.append(mat)
    directions=[(-.8,.1,.4),(.2,.7,.7),(.75,.3,-.1),(.1,-.7,-.6),(-.3,-.7,.4),(.45,-.2,.8)]
    for i in range(count):
        d=Vector(directions[i]).normalized() if kind=='Primary' else Vector((rng.gauss(0,1),rng.gauss(0,1),rng.gauss(0,1))).normalized();u=d.cross(Vector((0,1,0))).normalized();v=d.cross(u);length=rng.uniform(.12,.18) if kind=='Primary' else rng.uniform(.018,.068);bend=rng.choice([-1,1])*rng.uniform(.25,.45);c1=center+d*length*.30+u*length*bend*.7;c2=center+d*length*.66-u*length*bend*.5+v*length*rng.uniform(-.3,.3);end=center+d*length+u*length*bend*.2;steps=40 if kind=='Primary' else 12;s=cu.splines.new('POLY');s.points.add(steps)
        for j,p in enumerate(s.points):t=j/steps;co=(1-t)**3*center+3*(1-t)**2*t*c1+3*(1-t)*t*t*c2+t**3*end;p.co=(*co,1);p.radius=max(.002,(1-t)**1.55)*(1 if kind=='Primary' else rng.uniform(.65,1.0))
    ob=bpy.data.objects.new('Visible_organic_'+kind,cu);coll.objects.link(ob)
# Join tiny real icospheres into one emissive mesh, retaining a smooth density fade.
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1);tmp=bpy.context.object;unit=[v.co.copy() for v in tmp.data.vertices];faces=[tuple(p.vertices) for p in tmp.data.polygons];bpy.data.objects.remove(tmp,do_unlink=True);verts=[];polys=[];colors=[]
for i in range(1100):
    t=rng.betavariate(.9,1.55);y=.38*t;spread=.002+.027*t**1.5;pos=Vector((.012*math.sin(t*math.pi)+rng.gauss(0,spread),y+rng.gauss(0,spread*.4),1-.025*t+rng.gauss(0,spread*.40)));radius=rng.uniform(.00009,.00035)*(1-.3*t);fade=(1-t)**1.6*.8+.025;start=len(verts)
    for v in unit:verts.append(tuple(pos+v*radius));colors.append((.20*fade,.67*fade,fade,1))
    polys.extend(tuple(start+j for j in f) for f in faces)
me=bpy.data.meshes.new('Volumetric_fine_light_dust');me.from_pydata(verts,[],polys);attr=me.attributes.new('DustFade','FLOAT_COLOR','POINT');attr.data.foreach_set('color',np.asarray(colors,np.float32).ravel());mat=emissive('Particulate_light_trail',(.5,.82,1,1),20);nt=mat.node_tree;attribute=nt.nodes.new('ShaderNodeAttribute');attribute.attribute_name='DustFade';nt.links.new(attribute.outputs['Color'],nt.nodes.get('Emission').inputs['Color']);me.materials.append(mat);ob=bpy.data.objects.new('Descending_individual_light_particles',me);coll.objects.link(ob)

trail=bpy.data.objects['Curved_volumetric_light_wake'];trail.hide_render=False
mat=trail.data.materials[0];nt=mat.node_tree;n,l=nt.nodes,nt.links;n.clear();output=n.new('ShaderNodeOutputMaterial');vol=n.new('ShaderNodeVolumePrincipled');vol.inputs['Density'].default_value=0;vol.inputs['Emission Color'].default_value=(.25,.78,1,1);l.new(vol.outputs[0],output.inputs['Volume']);tc=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Object'],sep.inputs[0])
def calc(op,a,b=None):
    node=n.new('ShaderNodeMath');node.operation=op
    for i,v in enumerate([a,b]):
        if v is None:continue
        if isinstance(v,(float,int)):node.inputs[i].default_value=v
        else:l.new(v,node.inputs[i])
    return node.outputs[0]
y=sep.outputs['Y'];t=calc('DIVIDE',y,.38);cx=calc('MULTIPLY',calc('SINE',calc('MULTIPLY',t,math.pi)),.012);cz=calc('SUBTRACT',1,calc('MULTIPLY',t,.025));dx=calc('SUBTRACT',sep.outputs['X'],cx);dz=calc('SUBTRACT',sep.outputs['Z'],cz);r2=calc('ADD',calc('MULTIPLY',dx,dx),calc('MULTIPLY',dz,dz));width=calc('ADD',.010,calc('MULTIPLY',t,.018));g=calc('EXPONENT',calc('MULTIPLY',calc('DIVIDE',r2,calc('MULTIPLY',width,width)),-2));fade=calc('POWER',calc('MAXIMUM',calc('SUBTRACT',1,t),0),2.5);gate=calc('MULTIPLY',calc('GREATER_THAN',y,0),calc('LESS_THAN',y,.38));strength=calc('MULTIPLY',calc('MULTIPLY',g,calc('MULTIPLY',fade,gate)),80);l.new(strength,vol.inputs['Emission Strength'])
bpy.data.lights['Core_ground_emission_0'].energy=70;bpy.data.lights['Core_ground_emission_0'].spot_size=1.0;bpy.data.lights['Core_ground_emission_0'].spot_blend=1
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=720;scene.render.resolution_y=720;glow=next(n for n in scene.compositing_node_group.nodes if n.type=='GLARE');glow.inputs['Strength'].default_value=.8;glow.inputs['Size'].default_value=.25;glow.inputs['Threshold'].default_value=.8;camera=scene.camera;camera.data.ortho_scale=.72;camera.location=(1.1,-1.6,1.25);look_at(camera,(0,.05,1));bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'close_preview.png');bpy.ops.render.render(write_still=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r15','status':'author_preview_pending','source':'r11 instance-local optics with asymmetric soft filaments, visible fuzz and descending dust','main_filaments':6,'short_fuzz_filaments':600,'dust_particles':1100,'tail_length_m':.381,'tail_vertical_drop_m':.025,'volume_and_particle_centerline':'shared x=.012 sin(pi*t), z=1-.025*t'},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
