"""Revision 20: curved light fibres and additive dust, preserving revision 19."""
from pathlib import Path
import bpy, json, math, random, sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3]
folder=next(next(ROOT.glob('2_*')).glob('characters/*/m306_*/model_3d'))
out=folder/'r20';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r19/authoring.blend'))
coll=bpy.data.collections['ASSET_m306'];center=Vector((0,0,1));rng=random.Random(30620)
for ob in coll.objects:
    if ob.name.startswith(('Six_irregular_star_filaments','Sparse_resolvable_cyan_light_dust')):ob.hide_render=True
    if ob.type=='LIGHT':
        ob.data.energy=18 if ob.data.type=='POINT' else 0
        ob.data.color=(.63,.87,1)
nt=bpy.data.materials['Cyan_atmospheric_fringe'].node_tree
vol=next(n for n in nt.nodes if n.type=='PRINCIPLED_VOLUME')
vol.inputs['Emission Color'].default_value=(.38,.76,1,1)
vol.inputs['Color'].default_value=(.6,.8,1,1)
def additive(name,strength,color):
    m=bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;nt.nodes.clear()
    e=nt.nodes.new('ShaderNodeEmission');e.inputs[0].default_value=(*color,1);e.inputs[1].default_value=strength
    transparent=nt.nodes.new('ShaderNodeBsdfTransparent');add=nt.nodes.new('ShaderNodeAddShader')
    nt.links.new(transparent.outputs[0],add.inputs[0]);nt.links.new(e.outputs[0],add.inputs[1])
    output=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(add.outputs[0],output.inputs['Surface'])
    return m
mat=additive('White_cyan_curving_fibres',22,(.55,.85,1))
cu=bpy.data.curves.new('Six_organic_bent_light_filaments','CURVE');cu.dimensions='3D';cu.bevel_depth=.00022;cu.bevel_resolution=3;cu.materials.append(mat)
directions=[(.45,.1,1),(-.8,-.15,.4),(1,.35,.1),(.15,.75,-.7),(-.55,.25,-.4),(.55,-.6,.4)]
lengths=[.18,.13,.17,.12,.14,.13]
for i,(direction,length) in enumerate(zip(directions,lengths)):
    d=Vector(direction).normalized();u=d.cross(Vector((0,1,0))).normalized();v=d.cross(u).normalized()
    bend=(1 if i%2 else -1)*(.42+.12*(i%3));s=cu.splines.new('POLY');s.points.add(95)
    for j,p in enumerate(s.points):
        t=j/95
        # A substantial three-dimensional arc with a slight S bend at the tip.
        co=center+d*length*t+u*length*bend*math.sin(t*math.pi*.95)+v*length*.22*math.sin(t*math.pi*1.5)
        p.co=(*co,1);p.radius=max(.001,(1-t)**1.9*(.75+.25*math.sin(t*math.pi)))
ob=bpy.data.objects.new(cu.name,cu);coll.objects.link(ob)
# Transparent + emission prevents dim distant dust from becoming dark opaque specks.
# Smooth icospheres avoid flat square fragments in close views.
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1)
tmp=bpy.context.object;unit=[v.co.copy() for v in tmp.data.vertices];faces=[tuple(p.vertices) for p in tmp.data.polygons]
bpy.data.objects.remove(tmp,do_unlink=True)
verts=[];polys=[];indices=[]
for i in range(1000):
    t=rng.betavariate(.85,1.8);spread=.0015+.020*t
    pos=Vector((.028*math.sin(t*math.pi*1.5),.37*t,1-.10*t))+Vector((rng.gauss(0,spread),rng.gauss(0,spread*.4),rng.gauss(0,spread*.6)))
    radius=rng.uniform(.00013,.00048)*(1-.75*t);offset=len(verts)
    verts.extend(tuple(pos+v*radius) for v in unit)
    polys.extend(tuple(offset+j for j in f) for f in faces)
    indices.extend([min(15,int(t*16))]*len(faces))
me=bpy.data.meshes.new('Additive_fine_light_dust');me.from_pydata(verts,[],polys)
for i in range(16):
    fade=(1-(i+.5)/16)**2
    me.materials.append(additive('White_dust_fade_%02d'%i,45*fade,(.68,.90,1)))
for p,idx in zip(me.polygons,indices):p.material_index=idx;p.use_smooth=True
ob=bpy.data.objects.new(me.name,me);coll.objects.link(ob)
data=bpy.data.lights.new('Soft_local_ground_pool','SPOT');data.energy=32;data.color=(.65,.87,1);data.spot_size=1.05;data.spot_blend=1;data.shadow_soft_size=.18
ob=bpy.data.objects.new(data.name,data);coll.objects.link(ob);ob.location=center
scene=bpy.context.scene;scene.cycles.samples=32;scene.render.resolution_x=900;scene.render.resolution_y=900
scene.camera.data.ortho_scale=.72;scene.camera.location=(1.1,-1.6,1.25);look_at(scene.camera,(0,.05,1))
bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'revision':'r20','status':'author_preview_pending','source':'r19','changes':['Shorter explicitly curved 3D filaments','1000 smaller smooth dust grains with additive transparency and nonlinear brightness fade','Whiter halo and soft local downward light pool'],'remaining':['All-view appearance and translated-instance checks pending']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'close_preview.png');bpy.ops.render.render(write_still=True)
