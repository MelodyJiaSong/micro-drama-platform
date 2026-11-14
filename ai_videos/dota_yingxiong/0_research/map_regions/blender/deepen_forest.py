"""Layer mature canopy and varied understorey while preserving anchor positions."""
from pathlib import Path
import bpy,json,random,math,base64,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';SRC=OUT/'environment_sources';dest=OUT/'environment_v010.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v009.blend'))
def load(asset,names):
    with bpy.data.libraries.load(str(next((SRC/asset).glob('*.blend'))),link=False) as (src,dst):dst.objects=names
    for o in dst.objects:o.location=(0,0,0);o.hide_render=False;o.hide_viewport=False
    return dst.objects
island=load('island_tree_01',['island_tree_01_LOD1'])[0];jacaranda=load('jacaranda_tree',['jacaranda_tree_LOD1'])[0]
for variant,source,height in [(0,island,13),(1,jacaranda,16),(4,jacaranda,14)]:
    c=bpy.data.collections[f'LIB_Tree_{variant}'];old=list(c.objects);o=source.copy();o.data=source.data;c.objects.link(o);o.scale*=height/source.dimensions.z
    for prior in old:c.objects.unlink(prior)
ferns=load('fern_02',[f'fern_02_{v}' for v in 'abcd']);shrubs=load('shrub_02',[f'shrub_02_{v}_LOD1' for v in 'abcd'])
libraries=[]
for i,o in enumerate(ferns+shrubs):
    c=bpy.data.collections.new('SCAN_Understorey_'+str(i));c.objects.link(o);libraries.append(c)
terrain=bpy.data.objects['Terrain_683d'].data;coords=np.empty(len(terrain.vertices)*3,np.float32);terrain.vertices.foreach_get('co',coords);z=coords.reshape(1025,1025,3)[:,:,2]
def height(x,y):
    u,v=np.clip((x+409.6)/.8,0,1023.999),np.clip((y+409.6)/.8,0,1023.999);i,j=int(u),int(v);a,b=u-i,v-j
    return float((z[j,i]*(1-a)+z[j,i+1]*a)*(1-b)+(z[j+1,i]*(1-a)+z[j+1,i+1]*a)*b)
grid=json.loads((ROOT/'0_research/map_regions/navigation/grid.json').read_text());cells=np.frombuffer(base64.b64decode(grid['cells_base64']),np.uint8).reshape(512,512)
def nav(x,y):return int(cells[int(np.clip((409.6-y)/1.6,0,511)),int(np.clip((x+409.6)/1.6,0,511))])
coll=bpy.data.collections.new('16_Forest_understorey');bpy.context.scene.collection.children.link(coll);rng=random.Random(1010);count=0
for tree in bpy.data.collections['02_Forest'].objects:
    if tree.instance_collection.name.endswith(('_5','_6','_7')):continue
    for j in range(15):
        angle=rng.random()*math.tau;radius=rng.uniform(.8,5);x,y=tree.location.x+math.cos(angle)*radius,tree.location.y+math.sin(angle)*radius
        if nav(x,y)&(1|16):continue
        i=rng.randrange(8);o=bpy.data.objects.new('Forest_fern' if i<4 else 'Forest_shrub',None);coll.objects.link(o);o.instance_type='COLLECTION';o.instance_collection=libraries[i];o.location=(x,y,height(x,y)-.025);o.rotation_euler.z=rng.random()*math.tau;o.scale=(rng.uniform(.7,1.4),)*3;count+=1
# Replace abstract fern ribbons with real fronds in the pre-existing undergrowth.
undergrowth=bpy.data.collections['06_Undergrowth']
for i,o in enumerate(undergrowth.objects):
    if o.instance_type=='COLLECTION' and o.instance_collection and 'Fern' in o.instance_collection.name:
        o.instance_collection=libraries[i%4]
for image in bpy.data.images:
    if image.source!='FILE' or image.packed_file:continue
    matches=list(SRC.glob('*/textures/'+Path(image.filepath.replace('\\','/')).name))
    if matches:image.filepath=str(matches[0]);image.reload()
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V010 CANDIDATE; mature broadleaf canopy and protected understorey'
# Close reference cameras expose leaves, grass, shoreline and bark at human scale.
for name,pos,target in [('Sentinel_Forest_Eye',(-86,-78,height(-86,-78)+1.7),(-108,-105,height(-108,-105)+4)),('Sentinel_Shore_Close',(-34,-51,height(-34,-51)+1.7),(-23,-22,-3))]:
    data=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();data.lens=32;data.clip_end=3000
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report={'file':dest.name,'status':'candidate_pending_review','additional_understorey_instances':count,'tree_xy_unchanged':True,'new_sources':['island_tree_01','jacaranda_tree','fern_02','shrub_02'],'source_manifest':'environment_sources/sources.json'};(OUT/'environment_v010_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
