"""Use scanned plant/rock geometry while retaining map anchors and ramp clearance."""
from pathlib import Path
import bpy,json,sys,math,random,base64,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';SRC=OUT/'environment_sources'
dest=OUT/'environment_v006.blend'
if dest.exists():raise FileExistsError(dest)
plan=json.loads((SRC/'download_plan.json').read_text())
missing=[r['path'] for r in plan['jobs'] if not (SRC/r['path']).exists()]
if missing:raise RuntimeError({'missing_sources':missing})
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v005.blend'))
print('LOADED_MAP',flush=True)
def load_objects(asset,names):
    path=next((SRC/asset).glob('*.blend'))
    with bpy.data.libraries.load(str(path),link=False) as (src,dst):
        dst.objects=[n for n in src.objects if n in names]
    if len(dst.objects)!=len(names):raise ValueError((asset,names))
    for ob in dst.objects:
        ob.location=(0,0,0);ob.hide_render=False;ob.hide_viewport=False
    return dst.objects
tree=load_objects('tree_small_02',['tree_small_02_LOD1'])[0]
firs=load_objects('fir_tree_01',[f'fir_tree_01_{v}_LOD1' for v in 'abc'])
rock=load_objects('rock_face_02',['rock_face_02'])[0]
grasses=load_objects('grass_medium_01',[f'grass_medium_01_large_{v}_LOD0' for v in 'abc'])
trunk=load_objects('dead_tree_trunk_02',['dead_tree_trunk_02_LOD1'])[0]
print('LOADED_SOURCES',flush=True)
def proto(name,source,scale=1):
    c=bpy.data.collections.new(name);o=source.copy();o.data=source.data;c.objects.link(o);o.scale=tuple(x*scale for x in source.scale);return c
original_xy={o.name:tuple(o.location[:2]) for o in bpy.data.collections['02_Forest'].objects}
# Replace only the shared source geometry, leaving all original tree positions.
for variant in range(5):
    c=bpy.data.collections[f'LIB_Tree_{variant}'];old=list(c.objects)
    source=tree if variant<3 else firs[variant-3]
    o=source.copy();o.data=source.data;o.location=(0,0,0);o.scale*=((12.5+variant*.65)/source.dimensions.z);c.objects.link(o)
    for old_obj in old:c.objects.unlink(old_obj)
# Scanned bark gives the dead branch forms physical surface detail.
bark=bpy.data.materials.get('Dead_bark');nt=bark.node_tree;bs=nt.nodes.get('Principled BSDF');tc=nt.nodes.new('ShaderNodeTexCoord')
for kind,target in [('diff','Base Color'),('rough','Roughness')]:
    f=next((SRC/'dead_tree_trunk_02/textures').glob('*_'+kind+'_2k.*'));n=nt.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(f),check_existing=True);n.projection='BOX';n.projection_blend=.4
    if kind!='diff':n.image.colorspace_settings.name='Non-Color'
    nt.links.new(tc.outputs['Object'],n.inputs['Vector']);nt.links.new(n.outputs['Color'],bs.inputs[target])
# Group real grass clumps in a metre-scale patch, then reuse the existing scatter.
for variant in range(5):
    c=bpy.data.collections[f'ENV_GRASS_{variant}'];old=list(c.objects);rng=random.Random(906+variant)
    for j in range(10):
        src=grasses[j%3];o=src.copy();o.data=src.data;c.objects.link(o);o.location=(rng.uniform(-.55,.55),rng.uniform(-.55,.55),0);o.rotation_euler.z=rng.random()*math.tau;o.scale*=rng.uniform(.8,1.5)
    for old_obj in old:c.objects.unlink(old_obj)
terrain=bpy.data.objects['Terrain_683d'].data;coords=np.empty(len(terrain.vertices)*3,np.float32);terrain.vertices.foreach_get('co',coords);coords=coords.reshape(1025,1025,3);z=coords[:,:,2];gy,gx=np.gradient(z,.8)
grid=json.loads((ROOT/'0_research/map_regions/navigation/grid.json').read_text());cells=np.frombuffer(base64.b64decode(grid['cells_base64']),np.uint8).reshape(512,512)
def nav(x,y):return int(cells[int(np.clip((409.6-y)/1.6,0,511)),int(np.clip((x+409.6)/1.6,0,511))])
def height(x,y):
    u,v=np.clip((x+409.6)/.8,0,1023.999),np.clip((y+409.6)/.8,0,1023.999);i,j=int(u),int(v);a,b=u-i,v-j
    return float((z[j,i]*(1-a)+z[j,i+1]*a)*(1-b)+(z[j+1,i]*(1-a)+z[j+1,i+1]*a)*b)
cliffs=bpy.data.collections['07_Cliff_Relief']
bpy.data.batch_remove(ids=list(cliffs.objects))
print('REPLACED_FOLIAGE_CLEARED_CLIFFS',flush=True)
rockproto=proto('SCAN_Cliff_face',rock);rng=random.Random(606);used=set();blocked_near_ramp=0
for j,i in np.argwhere(np.hypot(gx,gy)>.9)[::3]:
    x,y,zz=map(float,coords[j,i]);cell=(int(x/3.5),int(y/3.5))
    if cell in used:continue
    code=nav(x,y)
    if not code&2 or code&16:continue
    # Keep the rock footprint clear of verified walk/ramp cells, including edges.
    if any(nav(x+dx,y+dy)&(1|16) for dx,dy in [(0,0),(1.5,0),(-1.5,0),(0,1.5),(0,-1.5)]):blocked_near_ramp+=1;continue
    used.add(cell);o=bpy.data.objects.new('Scanned_cliff_strata',None);cliffs.objects.link(o);o.instance_type='COLLECTION';o.instance_collection=rockproto;o.location=(x,y,zz-2.0)
    o.rotation_euler.z=math.atan2(float(gy[j,i]),float(gx[j,i]))+rng.uniform(-.25,.25);o.scale=(rng.uniform(.75,1.05),rng.uniform(.45,.7),rng.uniform(.65,.95))
stones=bpy.data.collections['09_Ground_Stones']
for o in stones.objects:o.instance_collection=rockproto;o.scale=(rng.uniform(.1,.22),)*3
# Add fallen timber only in forest interiors, outside traversable cells.
logs=bpy.data.collections.new('13_Fallen_Timber');bpy.context.scene.collection.children.link(logs);logproto=proto('SCAN_Fallen_log',trunk)
for i,anchor in enumerate(bpy.data.collections['02_Forest'].objects):
    if i%23:continue
    x,y=anchor.location[:2];x+=2;y+=1
    if nav(x,y)&(1|16):continue
    o=bpy.data.objects.new('Fallen_tree',None);logs.objects.link(o);o.instance_type='COLLECTION';o.instance_collection=logproto;o.location=(x,y,height(x,y)-.12);o.rotation_euler.z=rng.random()*math.tau
assert all(tuple(o.location[:2])==original_xy[o.name] for o in bpy.data.collections['02_Forest'].objects)
print('PLACED_SCANNED_DETAIL',len(cliffs.objects),flush=True)
# Resolve image paths explicitly before packing appended source libraries.
for image in bpy.data.images:
    if image.source!='FILE' or image.packed_file:continue
    name=Path(image.filepath.replace('\\','/')).name
    matches=list(SRC.glob('*/textures/'+name))
    if matches:image.filepath=str(matches[0]);image.reload()
    elif not Path(bpy.path.abspath(image.filepath)).exists():raise FileNotFoundError(image.filepath)
bpy.context.scene['production_status']='ENVIRONMENT V006 CANDIDATE; scanned foliage and rocks; ramp clearance filter applied'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(OUT/'environment_v006_report.json').write_text(json.dumps({'file':dest.name,'status':'candidate_pending_visual_review','tree_anchor_count':len(original_xy),'tree_xy_unchanged':True,'scanned_cliff_instances':len(cliffs.objects),'excluded_near_walk_or_ramps':blocked_near_ramp,'fallen_logs':len(logs.objects),'license':'CC0','source_manifest':'environment_sources/sources.json'},indent=2))
print('SAVED',dest,flush=True)
