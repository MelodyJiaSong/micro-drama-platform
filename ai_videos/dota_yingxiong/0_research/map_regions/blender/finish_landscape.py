"""Natural ground cover, protected cliff smoothing and continuous outer terrain."""
from pathlib import Path
import bpy,json,math,random,base64,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';TEX=OUT/'textures'
dest=OUT/'environment_v007.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v006.blend'))
terrain=bpy.data.objects['Terrain_683d'].data;coords=np.empty(len(terrain.vertices)*3,np.float32);terrain.vertices.foreach_get('co',coords);coords=coords.reshape(1025,1025,3);z=coords[:,:,2];original=z.copy()
grid=json.loads((ROOT/'0_research/map_regions/navigation/grid.json').read_text());cells=np.frombuffer(base64.b64decode(grid['cells_base64']),np.uint8).reshape(512,512)
indices=np.minimum(np.arange(1025)//2,511);codes=cells[::-1][indices[:,None],indices[None,:]]
protected=(codes&(1|16))!=0
gy,gx=np.gradient(z,.8);steep=np.hypot(gx,gy);blur=z.copy()
for _ in range(28):
    p=np.pad(blur,1,mode='edge');blur=(p[1:-1,1:-1]*4+p[:-2,1:-1]+p[2:,1:-1]+p[1:-1,:-2]+p[1:-1,2:])/8
weight=np.clip(steep*.8,0,1)*(~protected);z[:]=z*(1-weight)+blur*weight
terrain.vertices.foreach_set('co',coords.ravel());terrain.update()
def height(x,y):
    u,v=np.clip((x+409.6)/.8,0,1023.999),np.clip((y+409.6)/.8,0,1023.999);i,j=int(u),int(v);a,b=u-i,v-j
    return float((z[j,i]*(1-a)+z[j,i+1]*a)*(1-b)+(z[j+1,i]*(1-a)+z[j+1,i+1]*a)*b)
def old_height(x,y):
    i,j=int(np.clip((x+409.6)/.8,0,1024)),int(np.clip((y+409.6)/.8,0,1024));return float(original[j,i])
for cname in ['02_Forest','03_Asset_Placement','06_Undergrowth','08_Meadow_Growth','09_Ground_Stones','13_Fallen_Timber']:
    for o in bpy.data.collections[cname].objects:o.location.z+=height(o.location.x,o.location.y)-old_height(o.location.x,o.location.y)
forest=np.zeros((1025,1025),np.float32)
for o in bpy.data.collections['02_Forest'].objects:
    x,y=o.location[:2];ix,iy=int((x+409.6)/.8),int((y+409.6)/.8);lo,hi=max(0,ix-15),min(1025,ix+16);bottom,top=max(0,iy-15),min(1025,iy+16)
    if lo>=hi or bottom>=top:continue
    yy,xx=np.mgrid[bottom:top,lo:hi];r2=((xx-ix)**2+(yy-iy)**2)*.8**2
    forest[bottom:top,lo:hi]=np.maximum(forest[bottom:top,lo:hi],np.exp(-r2/65))
attr=terrain.attributes.new('ForestFloor','FLOAT','POINT');attr.data.foreach_set('value',forest.ravel())
sources=json.loads((TEX/'sources.json').read_text());files={(r['asset'],r['map']):TEX/r['path'] for r in sources}
mat=bpy.data.materials['Continuous_ground'];nt=mat.node_tree;n,l=nt.nodes,nt.links;n.clear();out=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled');l.new(bs.outputs[0],out.inputs['Surface']);tc=n.new('ShaderNodeTexCoord')
def maps(asset,scale):
    mapping=n.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=scale;l.new(tc.outputs['Object'],mapping.inputs[0]);result={}
    for kind in ['Diffuse','Rough','Displacement']:
        node=n.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(files[(asset,kind)]),check_existing=True);node.projection='BOX';node.projection_blend=.2;l.new(mapping.outputs[0],node.inputs['Vector'])
        if kind!='Diffuse':node.image.colorspace_settings.name='Non-Color'
        result[kind]=node.outputs[0]
    return result
def attr_socket(name):
    node=n.new('ShaderNodeAttribute');node.attribute_name=name;return node.outputs['Fac']
def mix(a,b,t):
    node=n.new('ShaderNodeMixRGB');l.new(a,node.inputs[1]);l.new(b,node.inputs[2]);l.new(t,node.inputs[0]);return node.outputs[0]
soil=maps('brown_mud_02',.5);grass=maps('grass_ground',.45);leaves=maps('leafy_grass',.4);rock=maps('mossy_rock',.3)
g,b,r,f=[attr_socket(x) for x in ['Grass','Blight','Rock','ForestFloor']]
colour=mix(soil['Diffuse'],grass['Diffuse'],g);colour=mix(colour,leaves['Diffuse'],f)
ash=n.new('ShaderNodeHueSaturation');ash.inputs['Saturation'].default_value=.25;ash.inputs['Value'].default_value=.23;l.new(soil['Diffuse'],ash.inputs['Color']);colour=mix(colour,ash.outputs[0],b);colour=mix(colour,rock['Diffuse'],r);l.new(colour,bs.inputs['Base Color'])
l.new(grass['Rough'],bs.inputs['Roughness']);bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.05;bump.inputs['Strength'].default_value=.65;l.new(mix(soil['Displacement'],grass['Displacement'],g),bump.inputs['Height']);l.new(bump.outputs[0],bs.inputs['Normal'])
# Extend the physical land outside the playable square, rather than showing a slab.
coll=bpy.data.collections.new('14_Distant_Landscape');bpy.context.scene.collection.children.link(coll);verts=[];faces=[];steps=128
for layer in range(31):
    radius=409.6+layer*20;t=min(1,layer/12)
    for side in range(4):
        for i in range(steps):
            u=-1+2*i/steps
            x,y=[(radius*u,-radius),(radius,radius*u),(-radius*u,radius),(-radius,-radius*u)][side]
            edge=height(np.clip(x,-409.6,409.6),np.clip(y,-409.6,409.6));hills=10+18*math.sin(x*.006)*math.cos(y*.009)+9*math.sin((x+y)*.013)
            verts.append((x,y,edge*(1-t)+hills*t))
    if layer:
        for i in range(4*steps):faces.append(((layer-1)*4*steps+i,(layer-1)*4*steps+(i+1)%(4*steps),layer*4*steps+(i+1)%(4*steps),layer*4*steps+i))
me=bpy.data.meshes.new('Continuous_outer_land');me.from_pydata(verts,[],faces);ob=bpy.data.objects.new('Continuous_outer_land',me);coll.objects.link(ob);me.materials.append(mat)
for p in me.polygons:p.use_smooth=True
for name,value in [('Grass',.65),('ForestFloor',.65),('Blight',0),('Rock',0)]:
    a=me.attributes.new(name,'FLOAT','POINT');a.data.foreach_set('value',np.full(len(verts),value,np.float32))
# Outside-world planting has its own collection; original tree anchors stay intact.
rng=random.Random(7007)
for i in range(1400):
    side=i%4;radius=rng.uniform(421,650);u=rng.uniform(-1,1);x,y=[(radius*u,-radius),(radius,radius*u),(-radius*u,radius),(-radius,-radius*u)][side];t=min(1,(radius-409.6)/240)
    edge=height(np.clip(x,-409.6,409.6),np.clip(y,-409.6,409.6));zz=edge*(1-t)+(10+18*math.sin(x*.006)*math.cos(y*.009)+9*math.sin((x+y)*.013))*t
    o=bpy.data.objects.new('Distant_forest_tree',None);coll.objects.link(o);o.instance_type='COLLECTION';o.instance_collection=bpy.data.collections[f'LIB_Tree_{i%5}'];o.location=(x,y,zz);o.rotation_euler.z=rng.random()*math.tau;o.scale=(rng.uniform(.85,1.35),)*3
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V007 CANDIDATE; terrain outside playable boundary is authored extension'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(OUT/'environment_v007_report.json').write_text(json.dumps({'file':dest.name,'status':'candidate_pending_review','protected_walk_ramp_max_height_change_m':float(np.max(np.abs(z-original)[protected])),'blocked_cliff_max_height_change_m':float(np.max(np.abs(z-original))),'outside_trees':1400,'sources':'textures/sources.json','scope':'Authored naturalistic land outside canonical playable boundary; no changes to in-map XY anchors'},indent=2))
print('SAVED',dest,flush=True)
