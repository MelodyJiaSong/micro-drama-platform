"""Material separation and real beard fibres on the reviewed merchant candidate."""
from pathlib import Path
import bpy,json,numpy as np,random,math,sys,hashlib
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inspect_model import look_at

ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'))
manifest=json.loads((WORLD/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'));asset=next(a for a in manifest['assets'] if a['id']=='m300')
folder=ROOT/asset['model_directory']/'r03';out=folder/'inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'m300_r03.blend'
if dest.exists():raise FileExistsError(dest)
source=ROOT/asset['model_directory']/'r01/inspection/m300_r01.blend';bpy.ops.wm.open_mainfile(filepath=str(source))
coll=bpy.data.collections['ASSET_m300'];obj=next(o for o in coll.objects if o.type=='MESH');mesh=obj.data
mesh.transform(obj.matrix_world);obj.matrix_world=Matrix.Identity(4)
v=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('co',v);v=v.reshape(-1,3)
norm=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('normal',norm);norm=norm.reshape(-1,3)
uv=np.empty(len(mesh.loops)*2,np.float32);mesh.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2)
vi=np.empty(len(mesh.loops),np.int32);mesh.loops.foreach_get('vertex_index',vi)
base=mesh.materials[0];tex=next(n for n in base.node_tree.nodes if n.type=='TEX_IMAGE' and any(l.to_socket.name=='Base Color' for l in n.outputs['Color'].links))
img=tex.image;pix=np.empty(img.size[0]*img.size[1]*4,np.float32);img.pixels.foreach_get(pix);pix=pix.reshape(img.size[1],img.size[0],4)
samples=pix[(uv[:,1]*img.size[1]).astype(int).clip(0,img.size[1]-1),(uv[:,0]*img.size[0]).astype(int).clip(0,img.size[0]-1),:3]
colors=np.zeros((len(v),3),np.float32);colors[vi]=samples
def variant(name,tint=None,metal=None,rough=.65):
    mat=base.copy();mat.name=name;nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF')
    if tint:
        original=bs.inputs['Base Color'].links[0].from_socket;mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);nt.links.new(original,mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
    if metal is not None:
        for link in list(bs.inputs['Metallic'].links):nt.links.remove(link)
        bs.inputs['Metallic'].default_value=metal
    for link in list(bs.inputs['Roughness'].links):nt.links.remove(link)
    bs.inputs['Roughness'].default_value=rough
    noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1300;noise.inputs['Detail'].default_value=2
    coord=nt.nodes.new('ShaderNodeTexCoord');nt.links.new(coord.outputs['Object'],noise.inputs['Vector']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.00045;bump.inputs['Strength'].default_value=.35;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
    mesh.materials.append(mat);return len(mesh.materials)-1
cloth=variant('m300_Dark_burgundy_wool',(.35,.075,.11),0,.88)
hairbase=variant('m300_Golden_beard_undercoat',(.85,.60,.20),0,.8)
steel=variant('m300_Aged_steel',None,.92,.32)
skin=variant('m300_Skin',(.92,.73,.65),0,.48)
bs=mesh.materials[skin].node_tree.nodes.get('Principled BSDF');bs.inputs['Subsurface Weight'].default_value=.08;bs.inputs['Subsurface Radius'].default_value=(1,.38,.2)
beard=(np.abs(v[:,0])<np.clip((v[:,2]-.68)*.6+.035,.035,.155))&(v[:,1]<-.15)&(v[:,2]>.71)&(v[:,2]<1.065)
clothmask=(colors[:,0]>colors[:,1]*1.04)&(colors[:,2]>colors[:,1]*.96)&(v[:,2]<1.08)&((np.abs(v[:,0])>.15)|(v[:,1]>.01))
helmet=(v[:,2]>1.155)|((np.abs(v[:,0])>.085)&(np.abs(v[:,0])<.145)&(v[:,2]>1.025)&(v[:,2]<1.155)&(v[:,1]<.07)&~beard)
face=(v[:,2]>1.05)&(v[:,2]<1.15)&(np.abs(v[:,0])<.087)&(v[:,1]<-.06)&~helmet
labels=np.zeros(len(v),np.int32);labels[clothmask]=cloth;labels[beard]=hairbase;labels[helmet]=steel;labels[face]=skin
polys=np.empty(len(mesh.polygons),np.int32)
for p in mesh.polygons:
    labels_p=labels[list(p.vertices)];polys[p.index]=np.bincount(labels_p,minlength=5).argmax()
mesh.polygons.foreach_set('material_index',polys)
# Preserve the macro silhouette while layering actual fibres over the rough beard.
rng=random.Random(300);candidates=np.flatnonzero(beard);rng.shuffle(candidates)
curve=bpy.data.curves.new('m300_Groomed_beard_fibres','CURVE');curve.dimensions='3D';curve.resolution_u=2;curve.bevel_depth=.00042;curve.bevel_resolution=1
for idx in candidates[:25000]:
    p=Vector(v[idx])+Vector(norm[idx])*.002;length=rng.uniform(.035,.085);spline=curve.splines.new('POLY');spline.points.add(5)
    phase=rng.uniform(0,math.tau);curl=rng.uniform(.001,.004)
    for j,point in enumerate(spline.points):
        t=j/5;co=p+Vector((math.sin(t*8+phase)*curl,-.003*t,-length*t));point.co=(*co,1);point.radius=(1-t)*.9+.06
hairmat=bpy.data.materials.new('m300_Individual_gold_hair');hairmat.use_nodes=True;nt=hairmat.node_tree;nt.nodes.clear();outnode=nt.nodes.new('ShaderNodeOutputMaterial');hair=nt.nodes.new('ShaderNodeBsdfHairPrincipled');hair.parametrization='COLOR';hair.inputs['Color'].default_value=(.37,.15,.027,1);hair.inputs['Roughness'].default_value=.36;nt.links.new(hair.outputs[0],outnode.inputs['Surface']);curve.materials.append(hairmat)
hair_obj=bpy.data.objects.new('Beard_individual_fibres',curve);coll.objects.link(hair_obj)
# Preserve original hammer and cloak geometry; the broad spatial selection used
# in r02 intersected the cloak hem and has been discarded.
mesh.vertices.foreach_set('co',v.ravel());mesh.update()
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.threads=8
camera=scene.camera;size=1.35
for name,x,y,z in [('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22),('perspective',1,-1,.7)]:
    camera.location=(x*size*3,y*size*3,.675+z*size);look_at(camera,(0,0,.675));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
sha=hashlib.sha256(dest.read_bytes()).hexdigest()
(out/'inspection.json').write_text(json.dumps({'asset_id':'m300','revision':'r03','status':'refined_candidate_not_reviewed','source':source.name,'sha256':sha,'target_height_m':1.35,'faces':len(mesh.polygons),'hair_strands':len(curve.splines),'changes':['Refined hue and geometry masks for cloth and beard','Burgundy wool and golden hair colour correction','Individual hair fibre geometry','Original hammer/hem geometry preserved'],'views':['south.png','east.png','north.png','west.png','perspective.png']},indent=2),encoding='utf-8')
print('SAVED',dest,flush=True)
