"""Reference-based cast instrument, recessed frieze and grounded root network."""
from pathlib import Path
import bpy,bmesh,math,random,json,sys
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at,material
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('background/*/bg23_*/model_3d'));out=folder/'r21';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r20/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];rng=random.Random(2321)
bronze=bpy.data.materials['Cast_bronze_with_verdigris'];brass=bpy.data.materials['Polished_worn_brass'];silver=bpy.data.materials['Mirror_silver']
for ob in coll.objects:
    if ob.name.startswith(('New_orrery_','Spatial_','Continuous_question','Raised_pale_','Twisting_connected_','Interlaced_pale_','Carved_circular','Frieze_geometric')):ob.hide_render=True
    if ob.name.startswith('Dense_base_fern_skirt'):ob.scale*=1.65
    if ob.name.startswith(('Cast_bronze_dome','Concentric_cast_relief','Cast_spiral_relief','Fine_cast_volute')):
        if ob.type=='MESH':
            for v in ob.data.vertices:v.co.z=2.55+(v.co.z-2.55)*.57
        elif ob.type=='CURVE':
            for s in ob.data.splines:
                for p in s.points:p.co.z=2.55+(p.co.z-2.55)*.57-.008
        if ob.location.z>1:ob.location.z=2.55+(ob.location.z-2.55)*.57

def mesh(name,v,f,mat):
    me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);o=bpy.data.objects.new(name,me);coll.objects.link(o)
    if mat:me.materials.append(mat)
    return o
def attach(o,name,mat):
    for c in list(o.users_collection):c.objects.unlink(o)
    coll.objects.link(o);o.name=name;o.data.materials.append(mat);return o
def cyl(name,pos,r,h,mat):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=h,location=pos);o=attach(bpy.context.object,name,mat);b=o.modifiers.new('Rounded_cast_edges','BEVEL');b.width=.005;b.segments=3;return o
def sphere(name,pos,r,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=r,location=pos);o=attach(bpy.context.object,name,mat)
    for p in o.data.polygons:p.use_smooth=True
    return o
def beam(name,points,width=.14,thickness=.045):
    vv=[];ff=[]
    for i,p in enumerate(points):
        d=(points[min(i+1,len(points)-1)]-points[max(i-1,0)]).normalized();u=Vector((0,1,0));u=(u-d*u.dot(d)).normalized();v=d.cross(u).normalized()
        for a,b in [(-1,-1),(1,-1),(1,1),(-1,1)]:vv.append(tuple(p+u*a*thickness/2+v*b*width/2))
    for j in range(len(points)-1):
        for k in range(4):ff.append((j*4+k,j*4+(k+1)%4,(j+1)*4+(k+1)%4,(j+1)*4+k))
    ff.extend([(3,2,1,0),tuple((len(points)-1)*4+k for k in range(4))]);o=mesh(name,vv,ff,bronze);be=o.modifiers.new('Worn_cast_edge','BEVEL');be.width=.004;be.segments=3;return o
def bezier(a,b,c,d,count=100):return [(1-t)**3*a+3*(1-t)**2*t*b+3*(1-t)*t*t*c+t**3*d for t in [j/count for j in range(count+1)]]
cyl('Cast_instrument_foot',(0,0,3.06),.24,.15,bronze)
cyl('Substantial_segmented_axis',(0,0,3.70),.105,1.25,bronze)
for z in [3.15,3.45,3.51,3.93,4.16,4.30]:cyl('Cast_axis_brass_collar',(0,0,z),.145,.035,brass)
cyl('Companion_instrument_column',(-.25,.11,3.32),.055,.52,bronze)
for z in [3.10,3.53]:cyl('Companion_column_collar',(-.25,.11,z),.085,.025,brass)
balls=[((0,0,4.49),.17),((-1.17,-.24,4.03),.38),((1.20,.30,4.90),.37),((-.53,-.03,3.68),.19),((1.58,-.12,3.82),.23),((-.36,.24,4.01),.12)]
for i,(pos,r) in enumerate(balls):
    p=Vector(pos);sphere('Reference_mirror_sphere',p,r,silver);cyl('Sphere_cast_cradle',(p.x,p.y,p.z-r-.015),r*.38,.055,brass)
    if i:
        a=Vector((0,0,3.10));b=Vector((p.x*.52,p.y*.35,2.98));c=Vector((p.x,p.y,3.24));d=Vector((p.x,p.y,p.z-r-.035));beam('Wide_flat_cast_support',bezier(a,b,c,d),.15 if i in [1,2] else .10)
# Large C meridian remains open on the left and joins the segmented shaft.
points=[Vector((.09+.81*math.cos(a),.18,3.69+.59*math.sin(a))) for a in [math.radians(-102+j/120*205) for j in range(121)]]
beam('Open_C_meridian',points,.105)
# Hook is behind and above the highest globe, with a visibly open lower gap.
center=Vector((1.20,.62,5.15));arc=[center+Vector((.43*math.cos(a),0,.43*math.sin(a))) for a in [math.radians(j/100*158) for j in range(101)]]
stem=bezier(Vector((1.20,.62,4.51)),Vector((1.57,.62,4.66)),Vector((1.63,.62,5.00)),arc[0],45)
beam('High_open_question_mark_hook',stem+arc[1:],.105);sphere('Question_hook_terminal_ball',arc[-1],.052,brass)
# Weathering variation follows the metal surface; fine scratches remain subtle.
for mat in [bronze,brass,silver]:
    nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=95;noise.inputs['Detail'].default_value=3
    ramp=nt.nodes.new('ShaderNodeMapRange');ramp.inputs['To Min'].default_value=.10 if mat==silver else .24;ramp.inputs['To Max'].default_value=.19 if mat==silver else .55;nt.links.new(noise.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Roughness'])

# Scanned bark mapped along each root, rather than smooth generic noise.
bark=material('Scanned_weathered_root_bark',(.17,.12,.07),.9);nt=bark.node_tree;bs=nt.nodes.get('Principled BSDF');source=WORLD/'background/map_3d/environment_sources/dead_tree_trunk_02/textures'
for suffix,socket in [('diff_2k.jpg','Base Color'),('rough_2k.exr','Roughness')]:
    node=nt.nodes.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(source/('dead_tree_trunk_02_'+suffix)),check_existing=True)
    if socket=='Roughness':node.image.colorspace_settings.name='Non-Color'
    nt.links.new(node.outputs['Color'],bs.inputs[socket])
node=nt.nodes.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(source/'dead_tree_trunk_02_nor_gl_2k.exr'),check_existing=True);node.image.colorspace_settings.name='Non-Color';nm=nt.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.8;nt.links.new(node.outputs['Color'],nm.inputs['Color']);nt.links.new(nm.outputs[0],bs.inputs['Normal'])
def root(points,radius):
    vv=[];ff=[];distance=[0];rings=18
    for j,p in enumerate(points):
        if j:distance.append(distance[-1]+(p-points[j-1]).length)
        d=(points[min(j+1,len(points)-1)]-points[max(j-1,0)]).normalized();u=d.cross(Vector((0,0,1))).normalized();w=d.cross(u);t=j/(len(points)-1);r=radius*(1-t)**.7+.002
        for k in range(rings):
            a=k*math.tau/rings;rr=r*(1+.11*math.sin(a*5+j*.17)+.06*math.sin(j*1.3+k));vv.append(tuple(p+rr*(u*math.cos(a)+w*math.sin(a))))
    for j in range(len(points)-1):
        for k in range(rings):ff.append((j*rings+k,j*rings+(k+1)%rings,(j+1)*rings+(k+1)%rings,(j+1)*rings+k))
    ff.extend([tuple(range(rings-1,-1,-1)),tuple((len(points)-1)*rings+k for k in range(rings))]);o=mesh('Grounded_branching_bark_root',vv,ff,bark);uv=o.data.uv_layers.new(name='Longitudinal_bark')
    for p in o.data.polygons:
        p.use_smooth=True
        for li in p.loop_indices:i=o.data.loops[li].vertex_index;uv.data[li].uv=(i%rings/rings,distance[i//rings]*.65)
for i in range(28):
    a=i*math.tau/28+rng.uniform(-.09,.09)
    if math.sin(a)<-.94:continue
    start=2.39/math.cos((a+math.pi/8)%(math.pi/4)-math.pi/8);length=rng.uniform(.55,1.05);bend=rng.uniform(-.28,.28);pts=[]
    for j in range(65):
        t=j/64;aa=a+bend*math.sin(t*2.8);r=start+length*t;z=.018+.09*(1-t)**2+.018*math.sin(t*math.pi*2)**2-.035*t**6;pts.append(Vector((r*math.cos(aa),r*math.sin(aa),z)))
    radius=rng.uniform(.025,.055);root(pts,radius)
    for idx,sign in [(24,-1),(38,1)]:
        origin=pts[idx];d=Vector((math.cos(a+sign*.9),math.sin(a+sign*.9),0));length2=rng.uniform(.35,.62);branch=[]
        for j in range(42):
            t=j/41;p=origin+d*length2*t;p.z=origin.z*(1-t)+.012*math.sin(t*math.pi)-.018*t;branch.append(p)
        root(branch,radius*.5)

# Replace painted-looking knots with real shallow circular and star incisions.
for side,band in enumerate(sorted([o for o in coll.objects if o.name.startswith('Mitered_continuous_frieze')],key=lambda o:o.name)):
    phi=-math.pi/2+side*math.pi/4;normal=Vector((math.cos(phi),math.sin(phi),0));tangent=Vector((-normal.y,normal.x,0));cut_vertices=[];cut_faces=[]
    def path(points):
        if (points[-1]-points[0]).length<.0001:points=points[:-1]
        start=len(cut_vertices);count=len(points);rings=12
        for i,p in enumerate(points):
            direction=(points[(i+1)%count]-points[(i-1)%count]).normalized();across=direction.cross(normal).normalized()
            for k in range(rings):
                a=k*math.tau/rings;cut_vertices.append(tuple(p+.008*(normal*math.cos(a)+across*math.sin(a))))
        for i in range(count):
            for k in range(rings):cut_faces.append((start+i*rings+k,start+i*rings+(k+1)%rings,start+((i+1)%count)*rings+(k+1)%rings,start+((i+1)%count)*rings+k))
    for j in range(4):
        c=normal*2.418+tangent*((j-1.5)*.45)+Vector((0,0,2.47))
        if j%2==0:
            path([c+tangent*.080*math.cos(k*math.tau/64)+Vector((0,0,.080*math.sin(k*math.tau/64))) for k in range(65)])
        else:
            path([c+tangent*((.084 if k%2==0 else .032)*math.cos(k*math.pi/4))+Vector((0,0,(.084 if k%2==0 else .032)*math.sin(k*math.pi/4))) for k in range(9)])
    cutter=mesh('Temporary_closed_carving_tubes',cut_vertices,cut_faces,None);tool_mesh=cutter.data
    for data in [tool_mesh,band.data]:
        bm=bmesh.new();bm.from_mesh(data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(data);bm.free()
    bpy.context.view_layer.objects.active=band
    for previous in list(band.modifiers):bpy.ops.object.modifier_apply(modifier=previous.name)
    mod=band.modifiers.new('Actual_recessed_carving','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
# Model calibration is retained: one parent scales all authored components uniformly.
parent=bpy.data.objects.new('Asset_metre_calibration',None);coll.objects.link(parent)
for ob in list(coll.objects):
    if ob!=parent and ob.parent is None:ob.parent=parent
parent.scale=(5/5.63,)*3
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.camera.location=(9,-14,7.5);scene.camera.data.ortho_scale=6.6;look_at(scene.camera,(0,0,2.45));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'revision':'r21','status':'author_preview_pending','source':'r20','repairs':['Reference-height instrument with broad cast bands, collars and open C meridian','Question hook separated behind globe and terminal ball restored','Scanned-bark grounded branching roots','Boolean recessed circle and star frieze','Lower dome with flatter inlay'],'uniform_scale':5/5.63,'sphere_positions_before_scale':[p for p,r in balls]},indent=2))
scene.render.filepath=str(out/'perspective_preview.png');bpy.ops.render.render(write_still=True);print('PREVIEW',scene.render.filepath,flush=True)
