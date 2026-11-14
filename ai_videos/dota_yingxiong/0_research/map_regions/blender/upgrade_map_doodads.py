"""Replace canonical plant/rock prototypes and ground all original placements."""
from pathlib import Path
import bpy,json,math,random,numpy as np,base64
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';SRC=OUT/'environment_sources';dest=OUT/'environment_v013.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v012.blend'));rng=random.Random(13013)
def load(asset,names):
    with bpy.data.libraries.load(str(next((SRC/asset).glob('*.blend'))),link=False) as (s,d):d.objects=[n for n in s.objects if n in names]
    if not d.objects:raise ValueError((asset,names))
    for o in d.objects:o.location=(0,0,0)
    return d.objects
shrubs=load('shrub_02',[f'shrub_02_{v}_LOD1' for v in 'abcd']);blue=load('flower_heliophila',['flower_heliophila_large_LOD1','flower_heliophila_medium_LOD1']);gold=load('flower_ursinia',[f'flower_ursinia_{v}_LOD1' for v in 'abcde']);boulder=load('boulder_01',['boulder_01_LOD1'])[0]
replaced=[]
for c in list(bpy.data.collections):
    code=next((key for key in ['ZPsh','D00B','ZPfw','ARrk','CRrk'] if c.name.startswith('ENV_'+key+'_')),None)
    if not code:continue
    variant=int(c.name.rsplit('_',1)[1]);old=list(c.objects);items=shrubs if code in ['ZPsh','D00B'] else blue if code=='ZPfw' else [boulder]
    source=items[variant%len(items)];o=source.copy();o.data=source.data;c.objects.link(o);o.location=(0,0,0);o.name='Detailed_'+code;o.scale=(1,1,1);o.rotation_euler.z=variant*2.1
    if code=='D00B':
        o.data=o.data.copy()
        for i,mat in enumerate(o.data.materials):
            m=mat.copy();m.name='Blighted_'+m.name;o.data.materials[i]=m;nt=m.node_tree;bs=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
            if bs and bs.inputs['Base Color'].links:
                src=bs.inputs['Base Color'].links[0].from_socket;hue=nt.nodes.new('ShaderNodeHueSaturation');hue.inputs['Saturation'].default_value=.4;hue.inputs['Value'].default_value=.42;nt.links.new(src,hue.inputs['Color']);nt.links.new(hue.outputs[0],bs.inputs['Base Color'])
    if code=='ZPfw':
        for j in range(3):
            src=gold[(variant+j)%len(gold)];ob=src.copy();ob.data=src.data;c.objects.link(ob);ob.location=(rng.uniform(-.5,.5),rng.uniform(-.5,.5),0);ob.rotation_euler.z=rng.random()*math.tau;ob.scale=(1.5,)*3
    if code=='CRrk':
        o.data=o.data.copy()
        for i,mat in enumerate(o.data.materials):
            m=mat.copy();o.data.materials[i]=m;nt=m.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');src=bs.inputs['Base Color'].links[0].from_socket;hue=nt.nodes.new('ShaderNodeHueSaturation');hue.inputs['Value'].default_value=.35;hue.inputs['Saturation'].default_value=.2;nt.links.new(src,hue.inputs['Color']);nt.links.new(hue.outputs[0],bs.inputs['Base Color'])
    for ob in old:c.objects.unlink(ob)
    replaced.append(c.name)
# Physically shaped caps, stalks and gills replace flattened ellipsoids.
def mushroom_mesh(c,variant):
    mats=[bpy.data.materials['Pale_fungus'],bpy.data.materials['Mushroom_cap']];v=[];f=[];mi=[]
    def revolution(cx,cy,profile,index,seed):
        offset=len(v);N=64
        for radius,z in profile:
            for k in range(N):
                a=k*math.tau/N;rr=radius*(1+.045*math.sin(a*5+seed));v.append((cx+rr*math.cos(a)+.025*z,cy+rr*math.sin(a),z+.004*math.sin(a*9+seed)))
        for j in range(len(profile)-1):
            for k in range(N):a=offset+j*N+k;b=offset+j*N+(k+1)%N;f.append((a,b,b+N,a+N));mi.append(index)
    for j in range(9):
        x,y=rng.uniform(-.55,.55),rng.uniform(-.55,.55);h=rng.uniform(.15,.58);r=h*.58;revolution(x,y,[(0,0),(.06*h,.01),(.10*h,h*.15),(.055*h,h*.72),(.11*h,h*.85)],0,j)
        profile=[(0,h*1.03),(r*.18,h*1.02),(r*.42,h*.99),(r*.7,h*.92),(r*.94,h*.80),(r,h*.73),(r*.92,h*.70),(r*.65,h*.73),(r*.25,h*.78),(0,h*.80)];revolution(x,y,profile,1,j)
        for k in range(44):
            a=k*math.tau/44;cu=bpy.data.curves.new('Mushroom_gill','CURVE');cu.dimensions='3D';cu.bevel_depth=.0007;cu.bevel_resolution=1;s=cu.splines.new('POLY');s.points.add(7)
            for n,p in enumerate(s.points):t=.14+.8*n/7;p.co=(x+r*t*math.cos(a),y+r*t*math.sin(a),h*(.79-.09*t),1)
            cu.materials.append(mats[0]);ob=bpy.data.objects.new('Fine_radial_gill',cu);c.objects.link(ob)
    me=bpy.data.meshes.new('Mushroom_anatomy');me.from_pydata(v,[],f)
    for m in mats:me.materials.append(m)
    me.polygons.foreach_set('material_index',mi)
    for p in me.polygons:p.use_smooth=True
    ob=bpy.data.objects.new('Natural_mushroom_cluster',me);c.objects.link(ob)
for c in list(bpy.data.collections):
    if c.name.startswith(('ENV_APms_','ENV_CPms_')):
        old=list(c.objects);mushroom_mesh(c,int(c.name.rsplit('_',1)[1]));replaced.append(c.name)
        for ob in old:c.objects.unlink(ob)
# Canonical XY/facing remain exact; ground heights follow the refined terrain.
terrain=bpy.data.objects['Terrain_683d'].data;co=np.empty(len(terrain.vertices)*3,np.float32);terrain.vertices.foreach_get('co',co);co=co.reshape(1025,1025,3);z=co[:,:,2]
def height(x,y):
    u,v=np.clip((x+409.6)/.8,0,1023.999),np.clip((y+409.6)/.8,0,1023.999);i,j=int(u),int(v);a,b=u-i,v-j;return float((z[j,i]*(1-a)+z[j,i+1]*a)*(1-b)+(z[j+1,i]*(1-a)+z[j+1,i+1]*a)*b)
details=bpy.data.collections['04_Environment_Details'];before={o.name:tuple(o.location[:2]) for o in details.objects};maxshift=0
for o in details.objects:
    code=o.get('source_rawcode');x,y=o.location[:2]
    if code in ['AWfs','ZWfs','ZWsf','CPlp']:continue
    new=height(x,y)+(4 if code in ['AObd','NObt'] else 0);maxshift=max(maxshift,abs(o.location.z-new));o.location.z=new
assert all(before[o.name]==tuple(o.location[:2]) for o in details.objects)
# Use a full footprint check for new large river-bank rocks, keeping paths open.
grid=json.loads((ROOT/'0_research/map_regions/navigation/grid.json').read_text());cells=np.frombuffer(base64.b64decode(grid['cells_base64']),np.uint8).reshape(512,512)
def nav(x,y):return int(cells[int(np.clip((409.6-y)/1.6,0,511)),int(np.clip((x+409.6)/1.6,0,511))])
excluded=0
for o in bpy.data.collections['17_River_bank_detail'].objects:
    if o.name.startswith('Broken_shore_outcrop'):
        x,y=o.location[:2];r=max(o.scale.x*4.87,o.scale.y*3.47)/2+.25
        if any(nav(x+r*math.cos(a),y+r*math.sin(a))&(1|16) for a in np.linspace(0,math.tau,16,endpoint=False)):o.hide_render=True;excluded+=1
for im in bpy.data.images:
    if im.source=='FILE' and not im.packed_file:
        found=list(SRC.glob('*/textures/'+Path(im.filepath.replace('\\','/')).name))
        if found:im.filepath=str(found[0]);im.reload()
bpy.context.scene['production_status']='ENVIRONMENT V013 CANDIDATE; canonical shrubs/flowers/rocks replaced and ground contact repaired';bpy.data.orphans_purge(do_recursive=True);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report={'file':dest.name,'status':'candidate_pending_review','replaced_prototypes':replaced,'canonical_xy_unchanged':True,'canonical_instances':len(details.objects),'max_grounding_correction_m':maxshift,'bank_outcrops_excluded_by_full_footprint':excluded,'limitations':['Statues, bones, water effects and small fauna still require close-up refinement and independent review']};(OUT/'environment_v013_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
