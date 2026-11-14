"""Natural branch anatomy, source-height protection, instanced ground vegetation."""
from pathlib import Path
import bpy,bmesh,json,math,base64,numpy as np
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';SRC=OUT/'environment_sources'
dest=OUT/'environment_v009.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v008.blend'))
terrain=bpy.data.objects['Terrain_683d'].data
def xyz(mesh):
    v=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('co',v);return v.reshape(1025,1025,3)
co=xyz(terrain);before=co[:,:,2].copy()
with bpy.data.libraries.load(str(OUT/'environment_v003.blend'),link=False) as (src,dst):dst.objects=['Terrain_683d']
original_object=dst.objects[0];original=xyz(original_object.data)[:,:,2].copy();bpy.data.objects.remove(original_object)
grid=json.loads((ROOT/'0_research/map_regions/navigation/grid.json').read_text());cells=np.frombuffer(base64.b64decode(grid['cells_base64']),np.uint8).reshape(512,512)
ix=np.minimum(np.arange(1025)//2,511);codes=cells[::-1][ix[:,None],ix[None,:]];protect=(codes&(1|16))!=0
# Restore traversable surface to the source mesh; diffuse correction outside it.
delta=np.where(protect,original-before,0)
for _ in range(20):
    p=np.pad(delta,1,mode='edge');smooth=(p[:-2,1:-1]+p[2:,1:-1]+p[1:-1,:-2]+p[1:-1,2:])/4
    delta=np.where(protect,original-before,smooth)
co[:,:,2]+=delta;terrain.vertices.foreach_set('co',co.ravel());terrain.update();z=co[:,:,2]
def height(x,y,arr=z):
    u,v=np.clip((x+409.6)/.8,0,1023.999),np.clip((y+409.6)/.8,0,1023.999);i,j=int(u),int(v);a,b=u-i,v-j
    return float((arr[j,i]*(1-a)+arr[j,i+1]*a)*(1-b)+(arr[j+1,i]*(1-a)+arr[j+1,i+1]*a)*b)
anchor_xy={o.name:tuple(o.location[:2]) for o in bpy.data.collections['02_Forest'].objects}
for cname in ['02_Forest','03_Asset_Placement','06_Undergrowth','07_Cliff_Relief','08_Meadow_Growth','09_Ground_Stones','13_Fallen_Timber']:
    for o in bpy.data.collections[cname].objects:
        x,y=o.location[:2];o.location.z+=height(x,y)-height(x,y,before)
def source(asset,name):
    with bpy.data.libraries.load(str(next((SRC/asset).glob('*.blend'))),link=False) as (src,dst):dst.objects=[name]
    o=dst.objects[0];o.location=(0,0,0);o.hide_render=False;o.hide_viewport=False;return o
tree=source('tree_small_02','tree_small_02_LOD1');fir=source('fir_tree_01','fir_tree_01_a_LOD1')
for source_obj,remove in [(tree,'leaves'),(fir,'twig')]:
    bm=bmesh.new();bm.from_mesh(source_obj.data);slots=[i for i,m in enumerate(source_obj.data.materials) if remove in m.name]
    bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.material_index in slots],context='FACES');bm.to_mesh(source_obj.data);bm.free();source_obj.data.update()
for variant in range(5,8):
    c=bpy.data.collections[f'LIB_Tree_{variant}'];old=list(c.objects);src=tree if variant<7 else fir
    o=src.copy();o.data=src.data;c.objects.link(o);scale=(11.5+(variant-5)*1.2)/(4.564 if variant<7 else 18.955);o.scale=(scale*(.8 if variant==6 else 1),scale,scale)
    for old_obj in old:c.objects.unlink(old_obj)
print('RESTORED_WALK_HEIGHTS_AND_BRANCHES',flush=True)
# Shared small clumps at LOD2: many real blades without unique full meshes.
grasslib=bpy.data.collections.new('SCAN_Ground_grass_LOD2')
for v in 'abc':
    o=source('grass_medium_01',f'grass_medium_01_large_{v}_LOD2');grasslib.objects.link(o)
attributes={}
for name in ['Grass','Blight','ForestFloor','Paving']:
    a=np.empty(len(terrain.vertices),np.float32);terrain.attributes[name].data.foreach_get('value',a);attributes[name]=a.reshape(1025,1025)
rng=np.random.default_rng(9009);n=650000;x=rng.uniform(-408,408,n);y=rng.uniform(-408,408,n);i=np.clip(((x+409.6)/.8).astype(int),0,1023);j=np.clip(((y+409.6)/.8).astype(int),0,1023)
gy,gx=np.gradient(z,.8);g=attributes['Grass'][j,i];f=attributes['ForestFloor'][j,i];b=attributes['Blight'][j,i];p=attributes['Paving'][j,i]
probability=g*(.32+.40*f)*(1-b);valid=(rng.random(n)<probability)&(p<.25)&(z[j,i]>-5.7)&(np.hypot(gx[j,i],gy[j,i])<.65)
x,y,i,j=x[valid],y[valid],i[valid],j[valid];u=(x+409.6)/.8-i;v=(y+409.6)/.8-j;zz=(z[j,i]*(1-u)+z[j,i+1]*u)*(1-v)+(z[j+1,i]*(1-u)+z[j+1,i+1]*u)*v
verts=np.column_stack((x,y,zz-.015));me=bpy.data.meshes.new('Ground_vegetation_points');me.from_pydata(verts.tolist(),[],[]);ob=bpy.data.objects.new('Living_ground_grass',me);c=bpy.data.collections.new('15_Ground_vegetation');bpy.context.scene.collection.children.link(c);c.objects.link(ob)
scale=rng.uniform(1.1,2.1,len(verts));a=me.attributes.new('clump_scale','FLOAT_VECTOR','POINT');a.data.foreach_set('vector',np.repeat(scale,3).astype(np.float32))
rot=np.zeros((len(verts),3),np.float32);rot[:,2]=rng.uniform(0,math.tau,len(verts));a=me.attributes.new('clump_rotation','FLOAT_VECTOR','POINT');a.data.foreach_set('vector',rot.ravel())
ng=bpy.data.node_groups.new('Instanced_scanned_ground_cover','GeometryNodeTree');ng.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');ng.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');nodes,links=ng.nodes,ng.links
inp=nodes.new('NodeGroupInput');out=nodes.new('NodeGroupOutput');collection=nodes.new('GeometryNodeCollectionInfo');collection.inputs['Collection'].default_value=grasslib;collection.inputs['Separate Children'].default_value=True;collection.inputs['Reset Children'].default_value=True
inst=nodes.new('GeometryNodeInstanceOnPoints');inst.inputs['Pick Instance'].default_value=True;links.new(inp.outputs['Geometry'],inst.inputs['Points']);links.new(collection.outputs['Instances'],inst.inputs['Instance']);links.new(inst.outputs['Instances'],out.inputs['Geometry'])
for name,target in [('clump_scale','Scale'),('clump_rotation','Rotation')]:
    node=nodes.new('GeometryNodeInputNamedAttribute');node.data_type='FLOAT_VECTOR';node.inputs['Name'].default_value=name;links.new(node.outputs['Attribute'],inst.inputs[target])
randomnode=nodes.new('FunctionNodeRandomValue');randomnode.data_type='INT';randomnode.inputs['Min'].default_value=0;randomnode.inputs['Max'].default_value=2;links.new(randomnode.outputs['Value'],inst.inputs['Instance Index'])
ob.modifiers.new('Scanned grass instances','NODES').node_group=ng
# Metre-scale variation breaks the uniform, flat-shaded ground response.
nt=bpy.data.materials['Continuous_ground'].node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=.45;noise.inputs['Detail'].default_value=4;noise.inputs['Roughness'].default_value=.7;nt.links.new(tc.outputs['Object'],noise.inputs['Vector'])
old=bs.inputs['Base Color'].links[0].from_socket;mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.36;nt.links.new(old,mix.inputs[1]);nt.links.new(noise.outputs['Fac'],mix.inputs[2]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
previous=bs.inputs['Normal'].links[0].from_socket;bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.12;bump.inputs['Strength'].default_value=.6;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(previous,bump.inputs['Normal']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
for image in bpy.data.images:
    if image.source!='FILE' or image.packed_file:continue
    matches=list(SRC.glob('*/textures/'+Path(image.filepath.replace('\\','/')).name))
    if matches:image.filepath=str(matches[0]);image.reload()
assert all(tuple(o.location[:2])==anchor_xy[o.name] for o in bpy.data.collections['02_Forest'].objects)
bpy.context.scene['production_status']='ENVIRONMENT V009 CANDIDATE; original walk heights restored, natural leafless branches and scanned grass'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
report={'file':dest.name,'status':'candidate_pending_review','tree_xy_unchanged':True,'tree_anchor_count':len(anchor_xy),'walk_ramp_height_error_vs_v003_m':float(np.max(np.abs(z-original)[protect])),'max_restoration_m':float(np.max(np.abs(delta))),'ground_grass_instances':len(verts),'ground_grass_source':'CC0 PolyHaven grass_medium_01 LOD2','bare_tree_source':'CC0 PolyHaven tree_small_02 and fir_tree_01; foliage geometry removed','sources':'environment_sources/sources.json'}
(OUT/'environment_v009_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
