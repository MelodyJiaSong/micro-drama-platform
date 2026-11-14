"""Physical fountain: solid hillside, scanned rock, clear basin, falling water."""
from pathlib import Path
import bpy,math,random,json,hashlib,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import material,look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));OUT=WORLD/'background/map_3d';SRC=OUT/'environment_sources';folder=next(WORLD.glob('background/*/bg15_*/model_3d'));out=folder/'r02/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'bg15_r02.blend'
if dest.exists():raise FileExistsError(dest)
bpy.data.batch_remove(ids=list(bpy.data.objects));coll=bpy.data.collections.new('ASSET_bg15');bpy.context.scene.collection.children.link(coll);rng=random.Random(1502)
def attach(o,name,mat=None):
    for c in list(o.users_collection):c.objects.unlink(o)
    coll.objects.link(o);o.name=name
    if mat:o.data.materials.append(mat)
    return o
def mesh(name,v,f,mat):
    me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);o=bpy.data.objects.new(name,me);coll.objects.link(o);me.materials.append(mat)
    for p in me.polygons:p.use_smooth=True
    return o
def block(name,loc,dim,mat,bevel=.015):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=attach(bpy.context.object,name,mat);o.scale=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:m=o.modifiers.new('Worn_edges','BEVEL');m.width=bevel;m.segments=3
    return o
def source(asset,names):
    with bpy.data.libraries.load(str(next((SRC/asset).glob('*.blend'))),link=False) as (s,d):d.objects=[n for n in s.objects if n in names]
    if not d.objects:raise ValueError((asset,names))
    for o in d.objects:o.location=(0,0,0)
    return d.objects
rock=source('rock_face_02',['rock_face_02'])[0];ferns=source('fern_02',['fern_02_a','fern_02_b','fern_02_c','fern_02_d']);shrubs=source('shrub_02',['shrub_02_a_LOD1','shrub_02_b_LOD1','shrub_02_c_LOD1','shrub_02_d_LOD1'])
def copy_scaled(src,name,loc,size,rotation=0):
    ob=src.copy();ob.data=src.data;coll.objects.link(ob);ob.name=name;ob.location=loc;ob.rotation_euler=(0,0,rotation);ob.scale=size;return ob
def scanned(name,asset,tint,scale):
    m=material(name,(.3,.3,.3),.8);nt=m.node_tree;bs=nt.nodes.get('Principled BSDF');tc=nt.nodes.new('ShaderNodeTexCoord');mp=nt.nodes.new('ShaderNodeVectorMath');mp.operation='SCALE';mp.inputs[3].default_value=scale;nt.links.new(tc.outputs['Object'],mp.inputs[0]);tex=nt.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(next((OUT/'textures').glob(asset+'_diff_2k.*'))),check_existing=True);tex.projection='BOX';tex.projection_blend=.3;nt.links.new(mp.outputs[0],tex.inputs['Vector']);mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);nt.links.new(tex.outputs['Color'],mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.025;bump.inputs['Strength'].default_value=.5;nt.links.new(tex.outputs['Color'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal']);return m
earth=scanned('Fountain_mossy_hill','forest_ground_04',(.6,.65,.38),.7);stone=scanned('Pale_calcite_basin','white_sandstone_blocks_02',(.85,.83,.72),.6);wood=scanned('Dark_oak_lantern','wood_planks',(.18,.12,.065),1)
iron=material('Lantern_aged_metal',(.09,.065,.033),.34);iron.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=.85
# Closed mound: no floating shell. Central depression is a genuine basin.
profile=[(0,.47),(.8,.48),(2.4,.53),(3.0,.73),(3.35,1.10),(3.7,1.06),(4.5,.53),(5.12,.04)];verts=[];faces=[];N=192
for r,z in profile:
    for k in range(N):
        a=k*math.tau/N;rr=r*(1+.025*math.sin(a*7)+.018*math.sin(a*13));verts.append((rr*math.cos(a),rr*math.sin(a),z+.03*math.sin(a*11)*(r/5)))
for j in range(len(profile)-1):
    for k in range(N):faces.append((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k))
faces.append(tuple((len(profile)-1)*N+k for k in range(N-1,-1,-1)));hill=mesh('Solid_grounded_hillside_and_basin',verts,faces,earth);hill.data.materials.append(stone)
for p in hill.data.polygons:
    if p.index<3*N:p.material_index=1
def ground(r):
    for (r0,z0),(r1,z1) in zip(profile,profile[1:]):
        if r0<=r<=r1:return z0+(z1-z0)*(r-r0)/(r1-r0)
    return .04
# Pillars around the reservoir, leaving the stairs and the central waterfall open.
for i in range(28):
    a=i*math.tau/28;nx,ny=math.sin(a),math.cos(a)
    if ny<-.92:continue
    r=rng.uniform(3.35,4.0);h=1.0+2.4*max(0,ny)**2+rng.uniform(-.15,.3)
    if abs(nx)<.18 and ny>.9:continue
    copy_scaled(rock,'Natural_limestone_pinnacle',(nx*r,ny*r,ground(r)-.35),(rng.uniform(.18,.30),rng.uniform(.17,.27),h/4.73),rng.uniform(0,math.tau))
for x,y,h in [(-.65,3.75,4.35),(.75,3.7,3.65),(-1.45,3.5,2.75),(1.55,3.55,3.1)]:copy_scaled(rock,'Rear_spire',(x,y,.65),(.28,.24,h/4.73),rng.uniform(0,math.tau))
for i in range(95):
    a=rng.random()*math.tau;r=rng.uniform(3.35,5.0)
    if math.sin(a)<-.9 and abs(r*math.cos(a))<1.2:continue
    s=rng.uniform(.055,.13);copy_scaled(rock,'Ground_embedded_rock',(r*math.cos(a),r*math.sin(a),ground(r)-.15),(s,s*.85,s*.75),rng.uniform(0,math.tau))
for i in range(170):
    a=rng.random()*math.tau;r=rng.uniform(3.5,4.95)
    if math.sin(a)<-.88 and abs(r*math.cos(a))<1.3:continue
    src=ferns[i%4] if i%4 else shrubs[i%4];s=rng.uniform(1.0,2.0) if i%4 else rng.uniform(.4,.75);copy_scaled(src,'Living_fern_and_bank_foliage',(r*math.cos(a),r*math.sin(a),ground(r)-.015),(s,s,s),rng.uniform(0,math.tau))
# Light-coloured pebbles remain visible under the transmissive water.
pebble=rock.copy();pebble.data=rock.data.copy();pebble.data.materials.clear();pebble.data.materials.append(stone)
for p in pebble.data.polygons:p.material_index=0
for i in range(270):
    r=math.sqrt(rng.random())*2.85;a=rng.random()*math.tau;s=rng.uniform(.012,.045);copy_scaled(pebble,'Submerged_calcite_pebble',(r*math.cos(a),r*math.sin(a),ground(r)-.03),(s,s,s*.45),rng.random()*math.tau)
water=material('Clear_cyan_spring_water',(.86,.965,.99),.055);bs=water.node_tree.nodes.get('Principled BSDF');bs.inputs['Transmission Weight'].default_value=1;bs.inputs['IOR'].default_value=1.333
nt=water.node_tree;absorb=nt.nodes.new('ShaderNodeVolumeAbsorption');absorb.inputs['Color'].default_value=(.18,.75,.90,1);absorb.inputs['Density'].default_value=.22;nt.links.new(absorb.outputs[0],nt.nodes.get('Material Output').inputs['Volume'])
v=[(0,0,1.04)];f=[]
for j in range(1,41):
    r=3.23*j/40
    for k in range(N):
        a=k*math.tau/N;x,y=r*math.cos(a),r*math.sin(a);d=math.hypot(x,y-1.7);zz=1.04+.004*math.sin(d*30)*math.exp(-d*.35)+.003*math.sin(x*11+y*7);v.append((x,y,zz))
for k in range(N):f.append((0,1+k,1+(k+1)%N))
for j in range(39):
    for k in range(N):a=1+j*N+k;b=1+j*N+(k+1)%N;f.append((a,b,b+N,a+N))
topcount=len(v)
for k in range(N):a=k*math.tau/N;v.append((3.23*math.cos(a),3.23*math.sin(a),.48))
for k in range(N):f.append((1+39*N+k,topcount+k,topcount+(k+1)%N,1+39*N+(k+1)%N))
f.append(tuple(topcount+k for k in range(N-1,-1,-1)));mesh('Refractive_reservoir_water',v,f,water)
# Water sheet leaves the rear crevice and lands in the pool, with physical thickness.
v=[];f=[]
for j in range(81):
    t=j/80;y=3.10-1.32*t;z=3.45-2.41*t**1.35
    for k in range(17):
        u=k/16-.5;v.append((u*(.42+.20*t)+.015*math.sin(t*28+k),y+.012*math.sin(t*39+k*.7),z))
for j in range(80):
    for k in range(16):a=j*17+k;f.append((a,a+1,a+18,a+17))
fall=mesh('Continuous_falling_water_sheet',v,f,water);solid=fall.modifiers.new('Water_sheet_thickness','SOLIDIFY');solid.thickness=.008
foam=material('Aerated_water_foam',(.88,.94,.94),.32);nt=foam.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Subsurface Weight'].default_value=.06
for i in range(36):
    cu=bpy.data.curves.new('Falling_whitewater_filament','CURVE');cu.dimensions='3D';cu.bevel_depth=rng.uniform(.002,.006);cu.bevel_resolution=2;cu.materials.append(foam);s=cu.splines.new('POLY');s.points.add(60);u=rng.uniform(-.22,.22)
    for j,p in enumerate(s.points):t=j/60;p.co=(u*(1+.4*t)+.018*math.sin(t*29+i),3.08-1.32*t,3.45-2.41*t**1.35,1);p.radius=.3+.7*abs(math.sin(t*7+i))
    o=bpy.data.objects.new('Aerated_water_thread',cu);coll.objects.link(o)
for i in range(210):
    t=rng.random();a=rng.random()*math.tau;r=rng.uniform(.03,.65)*t;bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=rng.uniform(.006,.018),location=(math.cos(a)*r,1.78+math.sin(a)*r,1.05+(.35*t*(1-t))*rng.random()));o=attach(bpy.context.object,'Splash_drop',foam if i%3 else water);o.scale.z=rng.uniform(.5,2)
# Entry steps and two practical stone lanterns.
for j in range(5):block('Weathered_entry_stair',(0,-4.9+j*.32,.09+j*.15),(1.75,.40,.18),stone,.025)
flame=material('Candle_flame',(.8,.22,.015),.3);fb=flame.node_tree.nodes.get('Principled BSDF');fb.inputs['Emission Color'].default_value=(1,.26,.015,1);fb.inputs['Emission Strength'].default_value=12
for x in [-1.35,1.35]:
    y=-4.15;base=ground(math.hypot(x,y));block('Lantern_stone_plinth',(x,y,base+.42),(.48,.48,.84),stone,.04);block('Lantern_stone_cap',(x,y,base+.86),(.62,.62,.12),stone,.02)
    for dx in [-.22,.22]:
        for dy in [-.22,.22]:block('Lantern_timber_post',(x+dx,y+dy,base+1.14),(.045,.045,.5),wood,.005)
    block('Lantern_lower_frame',(x,y,base+.94),(.53,.53,.07),wood,.01)
    roof=mesh('Four_sided_oak_lantern_roof',[(x-.39,y-.39,base+1.40),(x+.39,y-.39,base+1.40),(x+.39,y+.39,base+1.40),(x-.39,y+.39,base+1.40),(x,y,base+1.70)],[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(0,3,2,1)],wood)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.035,location=(x,y,base+1.15));o=attach(bpy.context.object,'Lantern_candle_flame',flame);o.scale.z=2.4
    data=bpy.data.lights.new('Lantern_warm_light','POINT');data.energy=12;data.color=(1,.48,.18);data.shadow_soft_size=.06;o=bpy.data.objects.new('Lantern_warm_light',data);coll.objects.link(o);o.location=(x,y,base+1.18)
for im in bpy.data.images:
    if im.source=='FILE' and not im.packed_file:
        matches=list(SRC.glob('*/textures/'+Path(im.filepath.replace('\\','/')).name))
        if matches:im.filepath=str(matches[0]);im.reload()
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=40;scene.cycles.use_denoising=True;scene.cycles.transmission_bounces=10;scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1200;scene.render.resolution_y=1200;scene.view_settings.view_transform='AgX'
scene.world=bpy.data.worlds.new('Natural_fountain_daylight');scene.world.use_nodes=True;nt=scene.world.node_tree;env=nt.nodes.new('ShaderNodeTexEnvironment');env.image=bpy.data.images.load(str(SRC/'forest_slope_2k.hdr'));nt.links.new(env.outputs['Color'],nt.nodes.get('Background').inputs['Color']);nt.nodes.get('Background').inputs['Strength'].default_value=.65
bpy.ops.mesh.primitive_plane_add(size=1000,location=(0,0,0));bpy.context.object.name='Studio_floor';bpy.context.object.data.materials.append(material('Neutral_floor',(.25,.25,.25),.85));data=bpy.data.lights.new('Daylight_key','AREA');data.energy=2500;data.size=8;ob=bpy.data.objects.new('Daylight_key',data);scene.collection.objects.link(ob);ob.location=(-6,-9,12);look_at(ob,(0,0,2))
data=bpy.data.cameras.new('Inspection_camera');camera=bpy.data.objects.new('Inspection_camera',data);scene.collection.objects.link(camera);scene.camera=camera;data.type='ORTHO';data.ortho_scale=12.5
for name,x,y,z in [('south',0,-1,.35),('east',1,0,.35),('north',0,1,.35),('west',-1,0,.35),('perspective',1,-1,.7),('basin_detail',.3,-1,1.2)]:
    camera.location=(x*25,y*25,2.5+z*10);look_at(camera,(0,0,2.3));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report={'asset_id':'bg15','revision':'r02','source':'Component authoring from established fountain design; CC0 rock and plant source manifest','status':'candidate_not_reviewed','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'water_surface_height_m':1.04,'reservoir_radius_m':3.23,'waterfall_drop_m':2.41,'editable_water_and_lanterns':True,'objects':len(coll.objects),'views':['south.png','east.png','north.png','west.png','perspective.png'],'supplemental_views':['basin_detail.png']};(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
