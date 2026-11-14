"""Rebuild the observatory's thin metal assembly as connected hard surfaces."""
from pathlib import Path
import bpy,bmesh,math,json,sys,hashlib,random
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'))
a=next(a for a in json.loads((WORLD/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'))['assets'] if a['id']=='bg23')
out=ROOT/a['model_directory']/'r09/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'bg23_r09.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/a['model_directory']/'r08/inspection/bg23_r08.blend'))
coll=bpy.data.collections['ASSET_bg23'];obj=next(o for o in coll.objects if o.type=='MESH');obj.data.transform(obj.matrix_world);obj.matrix_world=Matrix.Identity(4)
bm=bmesh.new();bm.from_mesh(obj.data)
remove=[v for v in bm.verts if v.co.z>3.12 or (v.co.z>2.47 and math.hypot(v.co.x,v.co.y)<1.7)]
bmesh.ops.delete(bm,geom=remove,context='VERTS');bm.to_mesh(obj.data);bm.free();obj.data.update()
def relocate(o,name,mat):
    for c in list(o.users_collection):c.objects.unlink(o)
    coll.objects.link(o);o.name=name;o.data.materials.append(mat)
    if o.type=='MESH':
        for p in o.data.polygons:p.use_smooth=True
    return o
def metal(name,dark,light,metallic,rough):
    mat=bpy.data.materials.new(name);mat.use_nodes=True;nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Metallic'].default_value=metallic;bs.inputs['Roughness'].default_value=rough
    noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=14;noise.inputs['Detail'].default_value=4
    ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*dark,1);ramp.color_ramp.elements[1].color=(*light,1);nt.links.new(noise.outputs[0],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color'])
    fine=nt.nodes.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=240;bum=nt.nodes.new('ShaderNodeBump');bum.inputs['Distance'].default_value=.001;bum.inputs['Strength'].default_value=.25;nt.links.new(fine.outputs[0],bum.inputs['Height']);nt.links.new(bum.outputs[0],bs.inputs['Normal']);return mat
bronze=metal('Patinated_structural_bronze',(.025,.075,.060),(.14,.20,.13),.78,.38)
brass=metal('Warm_brass_edges',(.16,.075,.018),(.42,.26,.07),.93,.28)
polished=metal('Polished_astronomical_spheres',(.31,.23,.10),(.57,.48,.25),1,.12)
stone=metal('Foundation_limestone',(.13,.15,.12),(.32,.34,.27),0,.9)
def tube(name,points,radius,mat):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=3;s=cu.splines.new('POLY');s.points.add(len(points)-1)
    for p,c in zip(s.points,points):p.co=(*c,1)
    o=bpy.data.objects.new(name,cu);coll.objects.link(o);cu.materials.append(mat);return o
def ring(name,c,r,thick,mat,plane='XY'):
    points=[]
    for i in range(129):
        t=i*math.tau/128
        points.append((c[0]+r*math.cos(t),c[1]+r*math.sin(t),c[2]) if plane=='XY' else (c[0]+r*math.cos(t),c[1],c[2]+r*math.sin(t)))
    return tube(name,points,thick,mat)
def sphere(name,c,r,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=r,location=c);return relocate(bpy.context.object,name,mat)
def cylinder(name,c,r,depth,mat):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=r,depth=depth,location=c);o=relocate(bpy.context.object,name,mat);bev=o.modifiers.new('Machined_edge','BEVEL');bev.width=.009;bev.segments=3;return o
# A closed stone foundation fills the minor reconstruction gap at ground level.
cylinder('Stone_foundation_contact',(0,0,.075),2.02,.15,stone)
profile=[(1.73,2.42),(1.73,2.47),(1.62,2.49),(1.50,2.57),(1.32,2.66),(1.08,2.76),(.75,2.84),(.37,2.89),(.12,2.91)]
verts=[];faces=[]
for r,z in profile:
    for i in range(192):
        t=i*math.tau/192;verts.append((r*math.cos(t),r*math.sin(t),z))
for j in range(len(profile)-1):
    for i in range(192):faces.append((j*192+i,j*192+(i+1)%192,(j+1)*192+(i+1)%192,(j+1)*192+i))
faces.append(tuple(range(192-1,-1,-1)));faces.append(tuple((len(profile)-1)*192+i for i in range(192)))
me=bpy.data.meshes.new('Engraved_dome');me.from_pydata(verts,[],faces);o=bpy.data.objects.new('Engraved_dome',me);coll.objects.link(o);me.materials.append(bronze)
for p in me.polygons:p.use_smooth=True
for i,(r,z) in enumerate(profile[1:-1]):ring('Dome_latitude_'+str(i),(0,0,z+.008),r,.012,brass)
def dome_z(r):
    for (r0,z0),(r1,z1) in zip(profile,profile[1:]):
        if r1<=r<=r0:return z0+(z1-z0)*(r0-r)/(r0-r1)
    return 2.91
for sector in range(16):
    a0=sector*math.tau/16;points=[]
    for j in range(65):
        t=j*math.tau/64;r=1.20+.18*math.cos(t);a1=a0+.11*math.sin(t);points.append((r*math.cos(a1),r*math.sin(a1),dome_z(r)+.015))
    tube('Dome_celestial_engraving',points,.009,brass)
cylinder('Main_instrument_pedestal',(0,0,2.96),.23,.14,bronze)
cylinder('Central_axis',(0,0,3.57),.074,1.16,bronze)
for z in [3.0,3.16,3.58,3.72,4.02,4.14]:cylinder('Axis_brass_collar',(0,0,z),.105,.035,brass)
balls=[((0,0,4.30),.16),((-1.02,-.06,3.88),.31),((.94,.08,4.56),.33),((-.57,.35,3.56),.18),((1.40,.28,3.67),.22),((-.33,-.14,4.02),.115)]
def beam(name,controls,width=.08):
    p=[Vector(x) for x in controls];points=[]
    for i in range(81):
        t=i/80;points.append((1-t)**3*p[0]+3*t*(1-t)**2*p[1]+3*t*t*(1-t)*p[2]+t**3*p[3])
    vs=[]
    for i,v in enumerate(points):
        tangent=(points[min(i+1,80)]-points[max(i-1,0)]).normalized();normal=Vector((-tangent.z,0,tangent.x)).normalized()
        for s,y in [(-1,-1),(-1,1),(1,1),(1,-1)]:vs.append(tuple(v+normal*(s*width/2)+Vector((0,y*.027,0))))
    fs=[]
    for i in range(80):
        for j in range(4):fs.append((i*4+j,i*4+(j+1)%4,(i+1)*4+(j+1)%4,(i+1)*4+j))
    fs.extend([(3,2,1,0),(320,321,322,323)])
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);ob=bpy.data.objects.new(name,me);coll.objects.link(ob);me.materials.append(bronze);be=ob.modifiers.new('Brass_band_bevel','BEVEL');be.width=.006;be.segments=3
    for side in [-1,1]:
        edge=[]
        for i,v in enumerate(points):
            tangent=(points[min(i+1,80)]-points[max(i-1,0)]).normalized();normal=Vector((-tangent.z,0,tangent.x)).normalized();edge.append(tuple(v+normal*(side*width/2)+Vector((0,-.03,0))))
        tube(name+'_edge',edge,.006,brass)
for i,(c,r) in enumerate(balls):
    sphere('Astronomical_sphere_'+str(i+1),c,r,polished)
    cylinder('Sphere_socket_'+str(i+1),(c[0],c[1],c[2]-r-.018),.063,.065,brass)
    if i:
        end=(c[0],c[1],c[2]-r)
        beam('Connected_orbit_arm_'+str(i),[(0,c[1],3.15),(c[0]*.65,c[1],3.02),(c[0],c[1],3.20),end],.085 if i in [1,2] else .06)
beam('Central_meridian',[(0,.04,3.26),(1.08,.04,3.1),(1.1,.04,4.27),(0,.04,4.15)],.065)
# The upper arch visibly attaches to the large sphere's mounting assembly.
arch=[(.94+.43*math.cos(t),.08,4.56+.43*math.sin(t)) for t in [i*2.6/80+.12 for i in range(81)]]
tube('Attached_top_arc',arch,.025,bronze);tube('Top_arc_mount',[arch[0],(.94,.08,4.56)],.02,brass);sphere('Arc_terminal',arch[-1],.045,brass)
scene=bpy.context.scene;scene.cycles.samples=24;camera=scene.camera
for name,x,y,z in [('perspective',1,-1,.7),('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22)]:
    camera.location=(x*15,y*15,2.5+z*5);look_at(camera,(0,0,2.5));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(out/'inspection.json').write_text(json.dumps({'asset_id':'bg23','revision':'r09','status':'refined_candidate_not_reviewed','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source':'bg23_r08.blend','changes':['Removed disconnected reconstructed orrery','Connected metal arms, six polished spheres, collars and top arch','Closed engraved bronze dome','Stone foundation contact'],'views':['south.png','east.png','north.png','west.png','perspective.png']},indent=2))
