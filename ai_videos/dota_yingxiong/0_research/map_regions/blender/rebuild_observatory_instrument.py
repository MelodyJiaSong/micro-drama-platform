"""A fully spatial orrery and interwoven woody roots for all-angle filming."""
from pathlib import Path
import bpy,json,sys,math,random
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r20';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r19/inspection/bg23_r19.blend'));coll=bpy.data.collections['ASSET_bg23'];rng=random.Random(2320);bronze=bpy.data.materials['Cast_bronze_with_verdigris'];brass=bpy.data.materials['Polished_worn_brass'];silver=bpy.data.objects['Mirror_sphere_0'].data.materials[0];bark=bpy.data.materials['Pale_weathered_aerial_root_bark']
for n in bark.node_tree.nodes:
    if n.type=='VALTORGB':n.color_ramp.elements[0].color=(.025,.018,.010,1);n.color_ramp.elements[-1].color=(.18,.13,.075,1)
def curve(name,points,radius,mat):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=3;s=cu.splines.new('POLY');s.points.add(len(points)-1)
    for p,co in zip(s.points,points):p.co=(*co,1)
    o=bpy.data.objects.new(name,cu);coll.objects.link(o);cu.materials.append(mat);return o
roots=[o for o in coll.objects if o.name.startswith('Raised_pale_buttress_root')];survivors=[]
for i,o in enumerate(roots):
    if i%3==1:o.hide_render=True;continue
    survivors.append(o)
    for v in o.data.vertices:
        r=math.hypot(v.co.x,v.co.y)
        if r>3.0:v.co.z-=.02*min(1,(r-3.0)/.6)
    tex=bpy.data.textures.new('Root_bark_surface_'+str(i),type='CLOUDS');tex.noise_scale=.035;tex.noise_depth=2;dis=o.modifiers.new('Actual_bark_irregularity','DISPLACE');dis.texture=tex;dis.texture_coords='GLOBAL';dis.strength=.008
for o in coll.objects:
    if o.name.startswith('Interlaced_pale_rootlet'):o.hide_render=True
for i,o in enumerate(survivors):
    other=survivors[(i+1)%len(survivors)];a=sum((v.co for v in o.data.vertices[24*12:25*12]),Vector())/12;b=sum((v.co for v in other.data.vertices[30*12:31*12]),Vector())/12
    if (a-b).length>1.6:continue
    for shift in [0,.16]:
        pts=[]
        for j in range(45):
            t=j/44;p=a.lerp(b,t);r=math.hypot(p.x,p.y);p.x+=shift*math.sin(t*math.pi)*p.x/r;p.y+=shift*math.sin(t*math.pi)*p.y/r;p.z=.018+.028*math.sin(t*math.pi)**2+(a.z*(1-t)+b.z*t)*.35;pts.append(p)
        curve('Twisting_connected_root_web',pts,.012 if shift else .020,bark)
# Raise the low dome to the established reference silhouette. Move relief with it.
for o in coll.objects:
    if o.name.startswith(('Cast_bronze_dome','Concentric_cast_relief','Cast_spiral_relief','Fine_cast_volute')):
        if o.type=='MESH':
            for v in o.data.vertices:v.co.z=2.55+(v.co.z-2.55)*1.9
        elif o.type=='CURVE':
            for s in o.data.splines:
                for p in s.points:p.co.z=2.55+(p.co.z-2.55)*1.9
        if o.location.z>1:o.location.z=2.61+(o.location.z-2.61)*1.9
    if o.name.startswith(('Instrument_','Axis_cast_collar','Mirror_sphere_','Sphere_cup_','Connected_orbit_band_','Band_axis_join_','Central_C_meridian','Question_mark_','Orbit_band_cast_rivet')):o.hide_render=True
def attach(o,name,mat):
    for c in list(o.users_collection):c.objects.unlink(o)
    coll.objects.link(o);o.name=name;o.data.materials.append(mat);return o
def cylinder(name,loc,r,depth,mat):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=loc);o=attach(bpy.context.object,name,mat);be=o.modifiers.new('Cast_edge_rounding','BEVEL');be.width=.006;be.segments=3;return o
def beam(name,points,width=.075):
    vv=[];ff=[]
    for i,p in enumerate(points):
        tangent=(points[min(i+1,len(points)-1)]-points[max(i-1,0)]).normalized();u=tangent.cross(Vector((0,0,1))).normalized()
        if u.length<.1:u=Vector((1,0,0))
        v=tangent.cross(u).normalized()
        for a,b in [(-1,-1),(1,-1),(1,1),(-1,1)]:vv.append(tuple(p+u*a*width/2+v*b*.020))
    for j in range(len(points)-1):
        for k in range(4):ff.append((j*4+k,j*4+(k+1)%4,(j+1)*4+(k+1)%4,(j+1)*4+k))
    ff.extend([(3,2,1,0),tuple((len(points)-1)*4+k for k in range(4))]);me=bpy.data.meshes.new(name);me.from_pydata(vv,[],ff);o=bpy.data.objects.new(name,me);coll.objects.link(o);me.materials.append(bronze);be=o.modifiers.new('Rounded_cast_band','BEVEL');be.width=.005;be.segments=3;return o
cylinder('New_orrery_axis',(0,0,3.77),.075,.72,bronze);cylinder('New_orrery_base',(0,0,3.48),.23,.12,brass)
balls=[((0,0,4.18),.18),((-1.1,-.35,3.95),.35),((.95,.40,4.52),.34),((-.35,1.05,3.91),.23),((1.10,-.95,3.88),.25),((-.48,-.85,4.25),.13)]
for i,(pos,radius) in enumerate(balls):
    p=Vector(pos);bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=radius,location=p);o=attach(bpy.context.object,'Spatial_mirror_sphere',silver)
    for f in o.data.polygons:f.use_smooth=True
    cylinder('Spatial_sphere_socket',(p.x,p.y,p.z-radius-.018),radius*.32,.06,brass)
    if i:
        a=Vector((0,0,3.52));b=Vector((p.x*.45,p.y*.45,3.45));c=Vector((p.x,p.y,3.5));d=Vector((p.x,p.y,p.z-radius-.035));pts=[(1-t)**3*a+3*(1-t)**2*t*b+3*(1-t)*t*t*c+t**3*d for t in [j/100 for j in range(101)]];beam('Spatial_cast_orbit_arm',pts,.065+.012*(i%3))
# The highest support continues as a substantial, smooth hooked casting.
pts=[];center=Vector((.95,.40,4.53));rad=.49
for j in range(121):a=-math.pi/2+j/120*math.pi*1.40;pts.append(center+Vector((rad*math.cos(a),.025*math.sin(a),rad*math.sin(a))))
beam('Continuous_question_mark_casting',pts,.067)
# Engraved stone medallions gain shallow three-dimensional edge shadows.
for o in coll.objects:
    if o.hide_render:continue
    if o.name.startswith(('Carved_circular_medallion','Frieze_geometric_lines')) and o.type=='CURVE':o.data.bevel_depth*=1.7
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.camera.location=(10.5,-15,9);scene.camera.data.ortho_scale=7.5;look_at(scene.camera,(0,0,2.4));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'perspective_preview.png');bpy.ops.render.render(write_still=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r20','status':'author_preview_pending','source':'r19; fully spatial six-sphere orrery, substantial continuous question-mark casting, raised reference dome and interlaced weathered rootwork','sphere_positions_m':[p for p,r in balls],'sphere_count':6,'reference_resolution':'Raised dome follows established design views; no approval gap is assumed'},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
