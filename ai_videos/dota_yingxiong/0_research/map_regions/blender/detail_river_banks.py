"""Add navigable small shore rubble and broken rock outcrops on blocked banks."""
from pathlib import Path
import bpy,json,numpy as np,math,base64,random
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v012.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v011.blend'));terrain=bpy.data.objects['Terrain_683d'].data;co=np.empty(len(terrain.vertices)*3,np.float32);terrain.vertices.foreach_get('co',co);co=co.reshape(1025,1025,3);z=co[:,:,2];gy,gx=np.gradient(z,.8)
grid=json.loads((ROOT/'0_research/map_regions/navigation/grid.json').read_text());cells=np.frombuffer(base64.b64decode(grid['cells_base64']),np.uint8).reshape(512,512)
def nav(x,y):return int(cells[int(np.clip((409.6-y)/1.6,0,511)),int(np.clip((x+409.6)/1.6,0,511))])
def height(x,y):
    u,v=np.clip((x+409.6)/.8,0,1023.999),np.clip((y+409.6)/.8,0,1023.999);i,j=int(u),int(v);a,b=u-i,v-j;return float((z[j,i]*(1-a)+z[j,i+1]*a)*(1-b)+(z[j+1,i]*(1-a)+z[j+1,i+1]*a)*b)
c=bpy.data.collections.new('17_River_bank_detail');bpy.context.scene.collection.children.link(c);proto=bpy.data.collections['SCAN_Cliff_face'];rng=random.Random(12012);used=set();large=small=0
for j,i in np.argwhere((z>-7.2)&(z<-2.5)&(np.hypot(gx,gy)>.18))[::2]:
    x,y,zz=map(float,co[j,i]);key=(int(x/1.8),int(y/1.8))
    if key in used or nav(x,y)&16:continue
    used.add(key);code=nav(x,y);radius=.9
    clear=not any(nav(x+dx,y+dy)&(1|16) for dx,dy in [(0,0),(radius,0),(-radius,0),(0,radius),(0,-radius)])
    if clear and rng.random()<.75:
        ob=bpy.data.objects.new('Broken_shore_outcrop',None);c.objects.link(ob);ob.instance_type='COLLECTION';ob.instance_collection=proto;ob.location=(x,y,zz-.6);ob.scale=(rng.uniform(.24,.47),rng.uniform(.20,.35),rng.uniform(.23,.39));ob.rotation_euler=(rng.uniform(-.15,.15),rng.uniform(-.2,.2),math.atan2(gy[j,i],gx[j,i])+rng.uniform(-1,1));large+=1
    else:
        for k in range(rng.randrange(2,7)):
            px,py=x+rng.uniform(-.75,.75),y+rng.uniform(-.75,.75)
            if nav(px,py)&16:continue
            ob=bpy.data.objects.new('Shore_pebble',None);c.objects.link(ob);ob.instance_type='COLLECTION';ob.instance_collection=proto;ob.location=(px,py,height(px,py)-.04);s=rng.uniform(.018,.055);ob.scale=(s,s*.8,s*.38);ob.rotation_euler.z=rng.uniform(0,math.tau);small+=1
# Wet earth and moss have finer normals than the terrain grid itself.
nt=bpy.data.materials['Continuous_ground'].node_tree;n,l=nt.nodes,nt.links;bs=next(no for no in n if no.type=='BSDF_PRINCIPLED');tc=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=.5;l.new(tc.outputs['Object'],mapping.inputs[0]);tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(OUT/'textures/brown_mud_02_nor_gl_2k.jpg'),check_existing=True);tex.image.colorspace_settings.name='Non-Color';tex.projection='BOX';tex.projection_blend=.3;l.new(mapping.outputs[0],tex.inputs['Vector']);normal=n.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.55;l.new(tex.outputs['Color'],normal.inputs['Color'])
# Existing relief remains; the scan normal is an additional small-scale layer.
existing=bs.inputs['Normal'].links[0].from_node
if existing.type=='BUMP':l.new(normal.outputs['Normal'],existing.inputs['Normal'])
pave=n.new('ShaderNodeAttribute');pave.attribute_name='Paving';pavetex=n.new('ShaderNodeTexImage');pavetex.image=bpy.data.images.load(str(next((OUT/'textures').glob('white_sandstone_blocks_02_diff_2k.*'))),check_existing=True);pavetex.projection='BOX';l.new(mapping.outputs[0],pavetex.inputs['Vector']);tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.45,.43,.36,1);l.new(pavetex.outputs[0],tint.inputs[1]);old=bs.inputs['Base Color'].links[0].from_socket;mix=n.new('ShaderNodeMixRGB');l.new(pave.outputs['Fac'],mix.inputs[0]);l.new(old,mix.inputs[1]);l.new(tint.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],bs.inputs['Base Color'])
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V012 CANDIDATE; blocked bank outcrops, small shore rubble, paving restored';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report={'file':dest.name,'status':'candidate_pending_review','bank_rock_instances':large,'shore_pebbles':small,'large_rocks_exclude_walk_and_ramp_5point_radius_m':.9,'small_rubble_max_height_m':.10,'terrain_geometry_changed':False,'canonical_xy_unchanged':True};(OUT/'environment_v012_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
