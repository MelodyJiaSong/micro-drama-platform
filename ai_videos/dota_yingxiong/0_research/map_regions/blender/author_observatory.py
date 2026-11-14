"""Construct the observatory as separate masonry, wood, metal and plant parts."""
from pathlib import Path
import bpy,math,random,json,hashlib,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inspect_model import look_at,material
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));SRC=WORLD/'background/map_3d/environment_sources'
a=next(a for a in json.loads((WORLD/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'))['assets'] if a['id']=='bg23')
out=ROOT/a['model_directory']/'r12/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'bg23_r12.blend'
if dest.exists():raise FileExistsError(dest)
bpy.data.batch_remove(ids=list(bpy.data.objects));coll=bpy.data.collections.new('ASSET_bg23');bpy.context.scene.collection.children.link(coll);rng=random.Random(2312)
def attach(o,name,mat=None):
    for c in list(o.users_collection):c.objects.unlink(o)
    coll.objects.link(o);o.name=name
    if mat:o.data.materials.append(mat)
    return o
def mesh(name,verts,faces,mat):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);o=bpy.data.objects.new(name,me);coll.objects.link(o);me.materials.append(mat);return o
def block(name,loc,dims,mat,angle=0,bevel=.008):
    x,y,z=[v/2 for v in dims];o=mesh(name,[(-x,-y,-z),(-x,-y,z),(-x,y,-z),(-x,y,z),(x,-y,-z),(x,-y,z),(x,y,-z),(x,y,z)],[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)],mat);o.location=loc;o.rotation_euler.z=angle
    if bevel:b=o.modifiers.new('Worn_edges','BEVEL');b.width=bevel;b.segments=3
    return o
def curve(name,points,r,mat,radii=None):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=2;cu.bevel_depth=r;cu.bevel_resolution=3;s=cu.splines.new('POLY');s.points.add(len(points)-1)
    for i,(p,co) in enumerate(zip(s.points,points)):p.co=(*co,1);p.radius=radii[i] if radii else 1
    o=bpy.data.objects.new(name,cu);coll.objects.link(o);cu.materials.append(mat);return o
def ring(name,c,r,thick,mat,axis='Z'):
    return curve(name,[(c[0]+r*math.cos(i*math.tau/128),c[1]+(r*math.sin(i*math.tau/128) if axis=='Z' else 0),c[2]+(r*math.sin(i*math.tau/128) if axis=='Y' else 0)) for i in range(129)],thick,mat)
def sphere(name,c,r,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=r,location=c);o=attach(bpy.context.object,name,mat)
    for p in o.data.polygons:p.use_smooth=True
    return o
def cylinder(name,c,r,depth,mat,vertices=64):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=depth,location=c);o=attach(bpy.context.object,name,mat);b=o.modifiers.new('Machined_lip','BEVEL');b.width=.005;b.segments=3
    for p in o.data.polygons:p.use_smooth=len(p.vertices)==4
    return o
def weathered(name,c0,c1,rough=.7,metal=0,scale=5):
    m=material(name,c0,rough);nt=m.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Metallic'].default_value=metal;tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=scale;noise.inputs['Detail'].default_value=5;nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);r=nt.nodes.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.25;r.color_ramp.elements[0].color=(*c0,1);r.color_ramp.elements[1].position=.75;r.color_ramp.elements[1].color=(*c1,1);nt.links.new(noise.outputs['Fac'],r.inputs[0]);nt.links.new(r.outputs[0],bs.inputs['Base Color']);fine=nt.nodes.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=220;fine.inputs['Detail'].default_value=3;nt.links.new(tc.outputs['Object'],fine.inputs['Vector']);bum=nt.nodes.new('ShaderNodeBump');bum.inputs['Distance'].default_value=.0025 if not metal else .0004;bum.inputs['Strength'].default_value=.5;nt.links.new(fine.outputs[0],bum.inputs['Height']);nt.links.new(bum.outputs[0],bs.inputs['Normal']);return m
stone=weathered('Weathered_white_limestone',(.25,.27,.23),(.59,.58,.49),.83)
stone2=weathered('Limestone_capstones',(.35,.36,.30),(.65,.64,.56),.8)
mortar=weathered('Lime_mortar',(.24,.25,.21),(.40,.40,.34),.94)
band=weathered('Grey_cyan_carved_stone',(.14,.23,.21),(.32,.39,.33),.8)
bronze=weathered('Cast_bronze_with_verdigris',(.10,.047,.014),(.022,.105,.075),.34,.83,12)
brass=weathered('Polished_worn_brass',(.20,.115,.035),(.39,.25,.075),.25,.96,18)
dark=weathered('Recessed_oxidation',(.012,.021,.014),(.038,.066,.042),.7,.4)
silver=material('Mirror_silver',(.72,.75,.80),.085);silver.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=1
wood=weathered('Oak_door_and_roots',(.035,.017,.006),(.12,.065,.022),.76,0,6)
nt=wood.node_tree;tc=next(n for n in nt.nodes if n.type=='TEX_COORD');stretch=nt.nodes.new('ShaderNodeVectorMath');stretch.operation='MULTIPLY';stretch.inputs[1].default_value=(18,18,.7);nt.links.new(tc.outputs['Object'],stretch.inputs[0])
for n in nt.nodes:
    if n.type=='TEX_NOISE':nt.links.new(stretch.outputs[0],n.inputs['Vector'])
amethyst=weathered('Unlit_dark_amethyst',(.022,.010,.038),(.095,.045,.14),.28);bs=amethyst.node_tree.nodes.get('Principled BSDF');bs.inputs['Transmission Weight'].default_value=.24;bs.inputs['IOR'].default_value=1.54
# Continuous structural core ends behind individual coursed stones.
apothem=2.18;length=2*apothem*math.tan(math.pi/8)
for side in range(8):
    phi=-math.pi/2+side*math.pi/4;n=Vector((math.cos(phi),math.sin(phi),0));t=Vector((-math.sin(phi),math.cos(phi),0))
    if side: block('Closed_masonry_core',(*tuple(n*2.0)[:2],1.22),(length,.35,2.44),mortar,phi+math.pi/2,0)
    for course in range(9):
        z0=course*2.45/9;z1=(course+1)*2.45/9;gap=0
        if side==0 and z0<2.16 and z1>.15:gap=.63 if z0<1.55 else math.sqrt(max(0,.63**2-(z0-1.55)**2))
        ranges=[(-length/2,-gap),(gap,length/2)] if gap else [(-length/2,length/2)]
        for lo,hi in ranges:
            count=max(1,round((hi-lo)/(.43 if course%2 else .5)));width=(hi-lo)/count
            for j in range(count):
                u=lo+(j+.5)*width;pos=n*apothem+t*u;block('Limestone_course',(*pos[:2],(z0+z1)/2),(width-.009,.38,z1-z0-.009),stone,phi+math.pi/2,.009)
    pos=n*apothem;block('Carved_stone_frieze',(*pos[:2],2.47),(length+.03,.46,.24),band,phi+math.pi/2,.008)
    # Round medallions and interlocking geometric recess in every face.
    for j in range(4):
        u=(j-1.5)*length/4;c=n*(apothem+.237)+t*u+Vector((0,0,2.47));points=[c+t*(.088*math.cos(k*math.tau/64))+Vector((0,0,.088*math.sin(k*math.tau/64))) for k in range(65)];curve('Carved_circular_medallion',points,.006,dark)
        for zz in [-.055,.055]:curve('Frieze_geometric_lines',[c-t*.17+Vector((0,0,zz)),c-t*.11+Vector((0,0,zz)),c+t*.11+Vector((0,0,-zz)),c+t*.17+Vector((0,0,-zz))],.005,dark)
    for k in range(4):
        u=(k-1.5)*length/4;pos=n*2.30+t*u;bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=rng.uniform(.12,.20),location=(*pos[:2],.19));o=attach(bpy.context.object,'Amethyst_raw_crystal',amethyst);o.scale=(1,.55,1.2);o.rotation_euler.z=phi
for x in [-1.65,1.65]:
    for y in [-1.65,1.65]:
        for j in range(10):block('Obelisk_stone_course',(x,y,.16+j*.268),(.48-.013*j,.48-.013*j,.26),stone2,0,.009)
        block('Obelisk_base',(x,y,.18),(.65,.65,.26),stone2)
        for zz in [.77,2.49]:block('Obelisk_collar',(x,y,zz),(.56,.56,.12),stone2)
        bpy.ops.mesh.primitive_cone_add(vertices=4,radius1=.305,radius2=0,depth=.49,rotation=(0,0,math.pi/4),location=(x,y,2.96));attach(bpy.context.object,'Four_sided_obelisk_cap',stone2)
# Door: individual clipped planks and separately cast brass arch.
for j in range(10):
    x0=-.59+j*.118+.003;x1=x0+.112;top0=1.55+math.sqrt(max(0,.59**2-x0*x0));top1=1.55+math.sqrt(max(0,.59**2-x1*x1));verts=[(x0,-2.215,.16),(x1,-2.215,.16),(x1,-2.215,top1),(x0,-2.215,top0),(x0,-2.12,.16),(x1,-2.12,.16),(x1,-2.12,top1),(x0,-2.12,top0)];o=mesh('Arched_oak_door_plank',verts,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(3,2,6,7),(0,3,7,4),(1,5,6,2)],wood);b=o.modifiers.new('Timber_edge','BEVEL');b.width=.003;b.segments=2
for x in [-.69,.69]:block('Door_jamb',(x,-2.23,.86),(.22,.30,1.42),stone2)
for k in range(13):
    th0=k*math.pi/13+.004;th1=(k+1)*math.pi/13-.004;verts=[]
    for y in [-2.39,-2.10]:
        for r,th in [(.63,th0),(.84,th0),(.84,th1),(.63,th1)]:verts.append((r*math.cos(th),y,1.55+r*math.sin(th)))
    o=mesh('Arch_voussoir',verts,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],stone2);be=o.modifiers.new('Weathered_arch_edges','BEVEL');be.width=.005;be.segments=2
curve('Polished_arch_border',[(-.61,-2.405,.16),(-.61,-2.405,1.55)]+[(.61*math.cos(t),-2.405,1.55+.61*math.sin(t)) for t in [math.pi-i*math.pi/96 for i in range(97)]]+[(.61,-2.405,.16)],.018,brass)
for zz in [.22,.58,1.42]:block('Door_brass_strap',(0,-2.24,zz),(1.16,.025,.035),brass,0,.003)
coin=cylinder('Door_radial_emblem',(0,-2.26,1.05),.23,.035,brass);coin.rotation_euler.x=math.pi/2
for r in [.06,.13,.20,.23]:ring('Door_concentric_engraving',(0,-2.285,1.05),r,.004,dark,'Y')
for k in range(28):
    t=k*math.tau/28;curve('Door_emblem_radial',[(.14*math.cos(t),-2.289,1.05+.14*math.sin(t)),(.215*math.cos(t),-2.289,1.05+.215*math.sin(t))],.0035,dark)
for i in range(3):block('Entrance_stair',(0,-2.38-i*.32,.15-i*.045),(1.32+i*.15,.40,.12),stone2,0,.012)
# Low closed copper dome, with actual concentric and spiral surface relief.
profile=[(2.02,2.55),(2.02,2.59),(1.86,2.64),(1.65,2.72),(1.35,2.83),(1.0,2.92),(.55,2.98),(0,3.0)];verts=[];faces=[]
for r,z in profile:
    for k in range(192):t=k*math.tau/192;verts.append((r*math.cos(t),r*math.sin(t),z))
for j in range(len(profile)-1):
    for k in range(192):faces.append((j*192+k,j*192+(k+1)%192,(j+1)*192+(k+1)%192,(j+1)*192+k))
faces.append(tuple(range(191,-1,-1)));o=mesh('Cast_bronze_dome',verts,faces,bronze)
for p in o.data.polygons:p.use_smooth=True
def domeheight(r):
    for (r0,z0),(r1,z1) in zip(profile,profile[1:]):
        if r1<=r<=r0:return z0+(z1-z0)*(r0-r)/(r0-r1)
    return 3
for r in [.45,.60,.95,1.1,1.53,1.7,1.89]:ring('Concentric_cast_relief',(0,0,domeheight(r)+.01),r,.008,brass)
for sector in range(12):
    points=[]
    for k in range(121):
        t=k/120*math.tau*1.7;radius=.20*(1-k/145);u=1.30+radius*math.cos(t);v=radius*math.sin(t);a0=sector*math.tau/12;x=u*math.cos(a0)-v*math.sin(a0);y=u*math.sin(a0)+v*math.cos(a0);points.append((x,y,domeheight(math.hypot(x,y))+.009))
    curve('Cast_spiral_relief',points,.009,brass)
# Connected flat bronze bands, riveted collars and six true mirror spheres.
cylinder('Instrument_pedestal',(0,0,3.04),.22,.10,bronze);cylinder('Instrument_axis',(0,0,3.55),.065,1.04,bronze)
for zz in [3.1,3.22,3.48,3.78,3.99]:cylinder('Axis_cast_collar',(0,0,zz),.103,.05,brass)
def beam(name,controls,width=.085):
    controls=[Vector(x) for x in controls];points=[]
    for i in range(97):
        t=i/96;p=controls;points.append((1-t)**3*p[0]+3*t*(1-t)**2*p[1]+3*t*t*(1-t)*p[2]+t**3*p[3])
    vv=[]
    for i,v in enumerate(points):
        tangent=(points[min(i+1,96)]-points[max(i-1,0)]).normalized();normal=tangent.cross(Vector((0,1,0))).normalized()
        for s,y in [(-1,-1),(-1,1),(1,1),(1,-1)]:vv.append(tuple(v+normal*(s*width/2)+Vector((0,y*.027,0))))
    ff=[(i*4+j,i*4+(j+1)%4,(i+1)*4+(j+1)%4,(i+1)*4+j) for i in range(96) for j in range(4)]+[(3,2,1,0),(384,385,386,387)];o=mesh(name,vv,ff,bronze);b=o.modifiers.new('Rounded_cast_edges','BEVEL');b.width=.006;b.segments=3
    for side in [-1,1]:curve(name+'_polished_edge',[tuple(v+Vector((0,-.030,0))) for i,v in enumerate(points) if i%1==0],.006,brass)
balls=[((0,0,4.18),.17),((-1.17,-.04,3.72),.35),((.94,.08,4.50),.34),((-.61,.40,3.57),.19),((1.40,.34,3.57),.24),((-.32,-.17,3.92),.105)]
for i,(c,r) in enumerate(balls):
    sphere('Mirror_sphere_'+str(i),c,r,silver);cylinder('Sphere_cup_'+str(i),(c[0],c[1],c[2]-r-.025),r*.35,.065,brass)
    if i:beam('Connected_orbit_band_'+str(i),[(0,0,3.18),(c[0]*.65,c[1],3.02),(c[0],c[1],3.16),(c[0],c[1],c[2]-r-.03)])
    if i:curve('Band_axis_join_'+str(i),[(0,0,3.18),(0,c[1],3.18)],.055,bronze)
beam('Central_C_meridian',[(0,.03,3.32),(1.25,.03,3.14),(1.28,.03,4.16),(0,.03,3.99)],.075)
c=Vector((.94,.08,4.50));arc=[tuple(c+Vector((.43*math.cos(t),0,.43*math.sin(t)))) for t in [.15+i*2.6/96 for i in range(97)]];curve('Question_mark_crown',arc,.022,bronze);curve('Question_mark_mount',[(.94,.08,4.13),(1.27,.08,4.27),arc[0]],.027,bronze);sphere('Question_mark_terminal',arc[-1],.035,brass)
# Subtle roots and true fern fronds, avoiding the doorway.
for i in range(26):
    t=i*math.tau/26
    if math.sin(t)<-.9:continue
    points=[]
    for j in range(31):
        f=j/30;r=1.92+.77*f;angle=t+.07*math.sin(f*6+i);points.append((r*math.cos(angle),r*math.sin(angle),.07+.15*(1-f)**2+.025*math.sin(f*9+i)))
    curve('Surface_root',points,.025,wood,[max(.08,1-j/33) for j in range(31)])
with bpy.data.libraries.load(str(next((SRC/'fern_02').glob('*.blend'))),link=False) as (s,d):d.objects=['fern_02_a','fern_02_b','fern_02_c','fern_02_d']
ferns=d.objects
for i in range(38):
    t=rng.random()*math.tau
    if math.sin(t)<-.9:continue
    src=ferns[i%4];o=src.copy();o.data=src.data;coll.objects.link(o);r=rng.uniform(2.2,2.55);o.location=(r*math.cos(t),r*math.sin(t),.02);o.scale=(rng.uniform(.45,.75),)*3;o.rotation_euler.z=rng.random()*math.tau;o.name='Base_fern'
with bpy.data.libraries.load(str(next((SRC/'tree_small_02').glob('*.blend'))),link=False) as (s,d):d.objects=['tree_small_02_leaves_a_LOD1']
leaf=d.objects[0]
if leaf:
    for i in range(8):
        angle=i*math.tau/8+.23;n=Vector((math.cos(angle),math.sin(angle),0));t=Vector((-n.y,n.x,0));points=[]
        for j in range(31):
            f=j/30;co=n*(2.34+.03*math.sin(f*7))+t*(.14*math.sin(f*11+i))+Vector((0,0,2.55*f));points.append(co)
            if j%2==0:
                o=leaf.copy();o.data=leaf.data;coll.objects.link(o);o.name='Climbing_leaf_cluster';o.location=co;o.scale=(.35,)*3;o.rotation_euler=(rng.uniform(-.3,.3),rng.uniform(-.3,.3),angle+rng.uniform(-1,1))
        curve('Climbing_vine',points,.006,wood)
for image in bpy.data.images:
    if image.source!='FILE' or image.packed_file:continue
    matches=list(SRC.glob('*/textures/'+Path(image.filepath.replace('\\','/')).name))
    if matches:image.filepath=str(matches[0]);image.reload()
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=48;scene.cycles.use_denoising=True;scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1200;scene.render.resolution_y=1200;scene.view_settings.view_transform='AgX'
scene.world=bpy.data.worlds.new('Natural_forest_reflections');scene.world.use_nodes=True;nt=scene.world.node_tree;nt.nodes.clear();env=nt.nodes.new('ShaderNodeTexEnvironment');env.image=bpy.data.images.load(str(SRC/'forest_slope_2k.hdr'));bg=nt.nodes.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.6;nt.links.new(env.outputs['Color'],bg.inputs['Color']);output=nt.nodes.new('ShaderNodeOutputWorld');nt.links.new(bg.outputs[0],output.inputs[0])
floor=material('Neutral_ground',(.18,.19,.18),.9);bpy.ops.mesh.primitive_plane_add(size=1000,location=(0,0,-.01));bpy.context.object.name='Studio_floor';bpy.context.object.data.materials.append(floor)
key=bpy.data.lights.new('Soft_daylight','AREA');key.energy=1500;key.size=7;lamp=bpy.data.objects.new('Soft_daylight',key);scene.collection.objects.link(lamp);lamp.location=(-5,-8,10);look_at(lamp,(0,0,2.3))
data=bpy.data.cameras.new('Inspection_camera');camera=bpy.data.objects.new('Inspection_camera',data);scene.collection.objects.link(camera);scene.camera=camera;data.type='ORTHO';data.ortho_scale=6.7
for name,x,y,z in [('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22),('perspective',1,-1,.7)]:
    camera.location=(x*15,y*15,2.5+z*5);look_at(camera,(0,0,2.5));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
scene['production_status']='DETAILED_AUTHORED_CANDIDATE_NOT_REVIEWED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
report={'asset_id':'bg23','revision':'r12','status':'candidate_not_reviewed','source':'manual component authoring from asset card and views; no image projection','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'wall_height_m':2.45,'door_height_m':2,'total_height_m':4.965,'wall_diameter_m':4.74,'mirror_spheres':6,'objects':len(coll.objects),'editable_parts':['masonry courses','door planks and arch','brass radial emblem','frieze geometric carving','dome relief','connected orbit bands','silver spheres','fern fronds','vine leaf clusters','roots'],'views':['south.png','east.png','north.png','west.png','perspective.png']};(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
