"""Replace fused AI foliage with independent scanned leaves and real branches."""
from pathlib import Path
import bpy,bmesh,json,sys,hashlib,random,math,numpy as np
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));MAP=WORLD/'background/map_3d';SRC=MAP/'environment_sources'
a=next(a for a in json.loads((MAP/'asset_manifest.json').read_text(encoding='utf-8'))['assets'] if a['id']=='bg2')
out=ROOT/a['model_directory']/'r02/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'bg2_r02.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/a['model_directory']/'r01/inspection/bg2_r01.blend'))
coll=bpy.data.collections['ASSET_bg2'];obj=next(o for o in coll.objects if o.type=='MESH');mesh=obj.data;mesh.transform(obj.matrix_world);obj.matrix_world=Matrix.Identity(4)
v=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('co',v);v=v.reshape(-1,3)
uv=np.empty(len(mesh.loops)*2,np.float32);mesh.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2);vi=np.empty(len(mesh.loops),np.int32);mesh.loops.foreach_get('vertex_index',vi)
base=mesh.materials[0];image=next(n.image for n in base.node_tree.nodes if n.type=='TEX_IMAGE' and any(l.to_socket.name=='Base Color' for l in n.outputs['Color'].links));pix=np.empty(image.size[0]*image.size[1]*4,np.float32);image.pixels.foreach_get(pix);pix=pix.reshape(image.size[1],image.size[0],4)
samples=pix[(uv[:,1]*image.size[1]).astype(int).clip(0,image.size[1]-1),(uv[:,0]*image.size[0]).astype(int).clip(0,image.size[0]-1),:3];colors=np.zeros((len(v),3),np.float32);colors[vi]=samples
canopy=(v[:,2]>10.8)&(colors[:,1]>colors[:,0]*.85)&(colors.sum(1)>.7);points=v[canopy].copy()
if len(points)<10000:raise RuntimeError('Insufficient foliage points')
# Keep the photographed crown silhouette. Remove continuous leaf-shell geometry.
bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.delete(bm,geom=[p for p in bm.verts if p.co.z>10.8],context='VERTS');bm.to_mesh(mesh);bm.free();mesh.update()
with bpy.data.libraries.load(str(SRC/'tree_small_02/tree_small_02_2k.blend'),link=False) as (s,d):d.objects=[f'tree_small_02_leaves_{x}_LOD1' for x in 'abcd']
leaflibs=[]
for i,o in enumerate(d.objects):
    o.location=(0,0,0);o.hide_render=False;o.hide_viewport=False;lib=bpy.data.collections.new('bg2_Leaf_cluster_'+str(i));lib.objects.link(o);leaflibs.append(lib)
    for mat in o.data.materials:
        if mat is None:continue
        for n in mat.node_tree.nodes:
            if n.type=='BSDF_PRINCIPLED':n.inputs['Roughness'].default_value=.72
rng=random.Random(292);np_rng=np.random.default_rng(292)
indices=np_rng.choice(len(points),36000,replace=len(points)<36000)
for i,index in enumerate(indices):
    p=points[index];ob=bpy.data.objects.new('World_tree_individual_leaf_'+str(i),None);coll.objects.link(ob);ob.instance_type='COLLECTION';ob.instance_collection=leaflibs[i%4]
    ob.location=Vector(p)+Vector((rng.uniform(-.2,.2),rng.uniform(-.2,.2),rng.uniform(-.2,.2)));ob.rotation_euler=(rng.uniform(-math.pi,math.pi),rng.uniform(-math.pi,math.pi),rng.uniform(-math.pi,math.pi));ob.scale=(rng.uniform(1.1,1.8),)*3
print('LEAF_INSTANCES',len(indices),flush=True)
bark=bpy.data.materials.new('World_tree_red_brown_bark');bark.use_nodes=True;nt=bark.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.92
tc=nt.nodes.new('ShaderNodeTexCoord');tex=nt.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(next((SRC/'dead_tree_trunk_02/textures').glob('*_diff_2k.jpg'))));tex.projection='BOX';tex.projection_blend=.3;nt.links.new(tc.outputs['Object'],tex.inputs['Vector']);mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(.45,.22,.14,1);nt.links.new(tex.outputs[0],mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=30;noise.inputs['Detail'].default_value=5;bu=nt.nodes.new('ShaderNodeBump');bu.inputs['Distance'].default_value=.045;nt.links.new(noise.outputs[0],bu.inputs['Height']);nt.links.new(bu.outputs[0],bs.inputs['Normal'])
def branch(name,path,radii):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=2;cu.bevel_depth=1;cu.bevel_resolution=3;s=cu.splines.new('POLY');s.points.add(len(path)-1)
    for p,c,r in zip(s.points,path,radii):p.co=(*c,1);p.radius=r
    o=bpy.data.objects.new(name,cu);coll.objects.link(o);cu.materials.append(bark)
# Individual helical fibres retain spaces and visibly cross around the trunk.
for strand in range(6):
    path=[];radii=[]
    for j in range(80):
        t=j/79;a0=strand*math.tau/6+t*math.tau*.7;r=1.5+1.6*(1-t)**3;path.append((math.cos(a0)*r,math.sin(a0)*r,3.5+t*8.5));radii.append(.52-.25*t)
    branch('Twisted_bark_fibre_'+str(strand),path,radii)
# Connect the trunk to the actual crown lobes, using deterministic clustered tips.
centres=points[np.linspace(0,len(points)-1,12,dtype=int)].copy()
sample=points[::max(1,len(points)//12000)]
for _ in range(12):
    labels=np.argmin(((sample[:,None,:]-centres[None,:,:])**2).sum(2),axis=1)
    for k in range(12):
        if np.any(labels==k):centres[k]=sample[labels==k].mean(0)
for i,end in enumerate(centres):
    start=Vector((math.cos(i)*1.5,math.sin(i)*1.5,10.2));end=Vector(end);path=[];radii=[]
    for j in range(40):
        t=j/39;p=start.lerp(end,t);p.z-=math.sin(t*math.pi)*.4;path.append(p);radii.append(.42*(1-t)+.025)
    branch('Crown_branch_'+str(i),path,radii)
# Threadlike green aerial roots terminate at soil rather than stopping in air.
for i in range(20):
    theta=i*2.399963;r=3.8+rng.random()*2.5;x,y=math.cos(theta)*r,math.sin(theta)*r
    branch('Grounded_aerial_root_'+str(i),[(x+.12*math.sin(j),y+.09*math.cos(j*.6),11*(1-j/40)) for j in range(41)],[.028*(1-j/60) for j in range(41)])
# Resolve all appended image paths before packing.
for image in bpy.data.images:
    if image.source!='FILE' or image.packed_file:continue
    name=Path(image.filepath.replace('\\','/')).name;matches=list(SRC.glob('*/textures/'+name))
    if matches:image.filepath=str(matches[0]);image.reload()
scene=bpy.context.scene;scene.cycles.samples=24;camera=scene.camera;size=24
for name,x,y,z in [('perspective',1,-1,.7),('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22)]:
    camera.location=(x*size*3,y*size*3,10+z*size);look_at(camera,(0,0,10));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(out/'inspection.json').write_text(json.dumps({'asset_id':'bg2','revision':'r02','status':'refined_candidate_not_reviewed','source':'bg2_r01.blend','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'leaf_cluster_instances':len(indices),'source_license':'Poly Haven CC0','changes':['Replaced fused canopy with independent leaves','Connected crown branches','Twisted bark fibres','Aerial roots reaching ground'],'views':['south.png','east.png','north.png','west.png','perspective.png']},indent=2))
