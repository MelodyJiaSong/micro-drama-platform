"""Close the octagonal cornice and rebuild staggered stone, plinth and roots."""
from pathlib import Path
import bpy,json,math,random,sys,hashlib
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inspect_model import look_at,material
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r16/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'bg23_r16.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r15/inspection/bg23_r15.blend'));coll=bpy.data.collections['ASSET_bg23'];rng=random.Random(2316)
for o in list(coll.objects):
    if o.name.startswith(('Limestone_course','Closed_masonry_core','Carved_stone_frieze','Obelisk_','Exposed_obelisk','Four_sided_obelisk','Surface_root','Natural_root_trunk','Root_fine_branch','Amethyst_raw_crystal')):o.hide_render=True;o.hide_viewport=True
stone=bpy.data.materials['Weathered_white_limestone'];cap=bpy.data.materials['Limestone_capstones'];band=bpy.data.materials['Grey_cyan_carved_stone'];purple=bpy.data.materials['Unlit_dark_amethyst']
mortar=material('Pale_lime_pointing',(.41,.40,.34),.95)
def mesh(name,verts,faces,mat,bevel=0,uvscale=1):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);coll.objects.link(o);me.materials.append(mat)
    uv=me.uv_layers.new(name='Stone_individual_metres');offset=(rng.uniform(-20,20),rng.uniform(-20,20))
    for p in me.polygons:
        axis=max(range(3),key=lambda i:abs(p.normal[i]));axes=[(1,2),(0,2),(0,1)][axis]
        for li in p.loop_indices:
            v=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]]*uvscale+offset[0],v[axes[1]]*uvscale+offset[1])
    if bevel:b=o.modifiers.new('Soft_worn_stone_edges','BEVEL');b.width=bevel;b.segments=3
    return o
F=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def wedge(name,phi,inner,outer,lo,hi,z0,z1,mat,bevel=.006):
    # lo/hi are angular offsets; adjacent pieces share the exact miter plane.
    verts=[];n=Vector((math.cos(phi),math.sin(phi),0));t=Vector((-n.y,n.x,0))
    for z in [z0,z1]:
        for radius,a in [(inner,lo),(outer,lo),(outer,hi),(inner,hi)]:verts.append(tuple(n*radius+t*(radius*math.tan(a))+Vector((0,0,z))))
    return mesh(name,verts,F,mat,bevel)
def block(name,center,dim,mat,bevel=.006):
    x,y,z=[v/2 for v in dim];cx,cy,cz=center;return mesh(name,[(cx+a*x,cy+b*y,cz+c*z) for c in [-1,1] for a,b in [(-1,-1),(1,-1),(1,1),(-1,1)]],F,mat,bevel)
for side in range(8):
    phi=-math.pi/2+side*math.pi/4;extent=2.37*math.tan(math.pi/8)
    for course in range(9):
        z0=course*2.35/9+.005;z1=(course+1)*2.35/9-.005
        gap=.64 if side==0 and z0<1.55 else math.sqrt(max(0,.66**2-(z0-1.55)**2)) if side==0 and z0<2.21 else 0
        intervals=[(-extent,-gap),(gap,extent)] if gap else [(-extent,extent)]
        for lo,hi in intervals:
            if hi-lo<.015:continue
            wedge('Continuous_lime_backing',phi,2.06,2.355,math.atan(lo/2.37),math.atan(hi/2.37),z0-.005,z1+.005,mortar,0)
            cuts=[lo];step=.47;pos=-extent+(step*.5 if course%2 else step)
            while pos<hi:
                if pos>lo+.12 and hi-pos>.12:cuts.append(pos)
                pos+=step
            cuts.append(hi)
            for l,h in zip(cuts,cuts[1:]):
                relief=rng.uniform(-.004,.008);wedge('Staggered_limestone_block',phi,2.16,2.37+relief,math.atan((l+.004)/2.37),math.atan((h-.004)/2.37),z0,z1,stone,rng.uniform(.006,.011))
    wedge('Mitered_continuous_frieze',phi,1.98,2.42,-math.pi/8,math.pi/8,2.35,2.59,band,.004)
    for z0,z1,rad in [(.08,.14,2.44),(.47,.52,2.46)]:
        ranges=[(-math.pi/8,math.atan(-.72/rad)),(math.atan(.72/rad),math.pi/8)] if side==0 else [(-math.pi/8,math.pi/8)]
        for lo,hi in ranges:wedge('Continuous_plinth_moulding',phi,2.26,rad,lo,hi,z0,z1,cap,.008)
    for k in range(5):
        u=(k-2)*.36
        if side==0 and abs(u)<.73:continue
        n=Vector((math.cos(phi),math.sin(phi),0));t=Vector((-n.y,n.x,0));center=n*2.385+t*u+Vector((0,0,.30))
        # Faceted inset slabs, surrounded by a pale stone socket.
        verts=[]
        for depth in [-.025,.025]:
            for dx,dz in [(-.13,-.13),(.10,-.13),(.145,-.03),(.11,.125),(-.09,.14),(-.15,.01)]:verts.append(tuple(center+t*dx+n*depth+Vector((0,0,dz))))
        o=mesh('Inset_amethyst_plinth_slab',verts,[tuple(range(5,-1,-1)),tuple(range(6,12))]+[(j,(j+1)%6,(j+1)%6+6,j+6) for j in range(6)],purple,.012)
        for j in range(6):
            p0=Vector(verts[j+6]);p1=Vector(verts[(j+1)%6+6]);mid=(p0+p1)/2
            cu=bpy.data.curves.new('Plinth_socket','CURVE');cu.dimensions='3D';cu.bevel_depth=.014;cu.bevel_resolution=2;s=cu.splines.new('POLY');s.points.add(1);s.points[0].co=(*p0,1);s.points[1].co=(*p1,1);ob=bpy.data.objects.new('Stone_amethyst_socket',cu);coll.objects.link(ob);cu.materials.append(cap)
# Four continuous obelisks sit outside the diagonal wall planes.
for x in [-1.88,1.88]:
    for y in [-1.88,1.88]:
        block('Obelisk_independent_foot',(x,y,.18),(.59,.59,.36),cap)
        for j in range(10):
            z0=.32+j*.285;z1=z0+.28;w0=.46-.12*j/10;w1=.46-.12*(j+1)/10
            vv=[(x+sx*w/2,y+sy*w/2,z) for w,z in [(w0,z0),(w1,z1)] for sx,sy in [(-1,-1),(1,-1),(1,1),(-1,1)]];mesh('Unbroken_tapered_obelisk',vv,F,cap,.005)
        mesh('Obelisk_pyramid_point',[(x-.18,y-.18,3.17),(x+.18,y-.18,3.17),(x+.18,y+.18,3.17),(x-.18,y+.18,3.17),(x,y,3.59)],[(0,3,2,1),(0,1,4),(1,2,4),(2,3,4),(3,0,4)],cap,.003)
# Low branching woody roots with cylindrical UVs, not upward pointed hooks.
bark=material('Branching_root_bark',(.12,.065,.026),.88);nt=bark.node_tree;bs=nt.nodes.get('Principled BSDF');tc=nt.nodes.new('ShaderNodeTexCoord');mult=nt.nodes.new('ShaderNodeVectorMath');mult.operation='MULTIPLY';mult.inputs[1].default_value=(85,2.5,1);nt.links.new(tc.outputs['UV'],mult.inputs[0]);noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1;noise.inputs['Detail'].default_value=5;noise.inputs['Roughness'].default_value=.8;nt.links.new(mult.outputs[0],noise.inputs['Vector']);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.04,.02,.008,1);ramp.color_ramp.elements[1].color=(.22,.14,.065,1);nt.links.new(noise.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.005;bump.inputs['Strength'].default_value=.6;nt.links.new(noise.outputs[0],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
def root_mesh(name,points,radius):
    vertices=[];faces=[];arclength=[0]
    for j,p in enumerate(points):
        if j:arclength.append(arclength[-1]+(p-points[j-1]).length)
        tangent=(points[min(j+1,len(points)-1)]-points[max(j-1,0)]).normalized();u=tangent.cross(Vector((0,0,1))).normalized();v=tangent.cross(u).normalized();r=radius*(1-j/len(points))**.7+.001
        for k in range(10):a=k*math.tau/10;vertices.append(tuple(p+r*(u*math.cos(a)+v*math.sin(a))))
    for j in range(len(points)-1):
        for k in range(10):faces.append((j*10+k,j*10+(k+1)%10,(j+1)*10+(k+1)%10,(j+1)*10+k))
    ob=mesh(name,vertices,faces,bark);uv=ob.data.uv_layers.active
    for p in ob.data.polygons:
        p.use_smooth=True
        for li in p.loop_indices:idx=ob.data.loops[li].vertex_index;uv.data[li].uv=(idx%10/10,arclength[idx//10])
for k in range(28):
    angle=rng.random()*math.tau
    if math.sin(angle)<-.91:continue
    phase=rng.random()*math.tau;local=(angle+math.pi/8)%(math.pi/4)-math.pi/8;start=2.34/math.cos(local);length=rng.uniform(.65,1.0);points=[]
    for j in range(45):
        t=j/44;a=angle+.13*math.sin(t*4+phase)*t;r=start+length*t;points.append(Vector((r*math.cos(a),r*math.sin(a),.035+.11*(1-t)**5+.015*math.sin(t*8)**2)))
    root_mesh('Ground_interwoven_root',points,rng.uniform(.024,.045))
    for j,sign in [(15,-1),(26,1)]:
        origin=points[j];direction=Vector((math.cos(angle+sign*.65),math.sin(angle+sign*.65),0));ll=rng.uniform(.25,.45);branch=[]
        for n in range(25):t=n/24;co=origin+direction*ll*t;co.z=origin.z*(1-t)+.025*t+.008*math.sin(t*math.pi);branch.append(co)
        root_mesh('Fine_root_fork',branch,.013)
scene=bpy.context.scene;scene.cycles.samples=24;camera=scene.camera
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(folder/'r16/authoring.blend'))
for name,x,y,z in [('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22),('perspective',1,-1,.7),('roof_detail',.7,-1,1.8)]:
    camera.location=(x*15,y*15,2.5+z*5);look_at(camera,(0,0,2.5));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(dest));report=json.loads((folder/'r15/inspection/inspection.json').read_text());report.update(revision='r16',source='r15 instrument, rebuilt closed mitered frieze, staggered individual stonework, independent obelisks, inset amethyst plinth and UV bark roots',sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),status='candidate_not_reviewed');(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
