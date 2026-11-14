"""Visible pale root network and exposed, weathered stone construction."""
from pathlib import Path
import bpy,json,sys,math,random
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import material,look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r19';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r18/inspection/bg23_r18.blend'));coll=bpy.data.collections['ASSET_bg23'];rng=random.Random(2319)
for o in coll.objects:
    if o.name.startswith(('Ground_interwoven_root','Fine_root_fork')):o.hide_render=True
    if o.name.startswith('Dense_base_fern_skirt'):o.scale*=.7
rootmat=bpy.data.materials['Branching_root_bark'].copy();rootmat.name='Pale_weathered_aerial_root_bark'
for n in rootmat.node_tree.nodes:
    if n.type=='VALTORGB':n.color_ramp.elements[0].color=(.13,.10,.065,1);n.color_ramp.elements[-1].color=(.52,.43,.29,1)
def rootmesh(points,radius,name):
    vv=[];ff=[];lengths=[0]
    for j,p in enumerate(points):
        if j:lengths.append(lengths[-1]+(p-points[j-1]).length)
        tangent=(points[min(j+1,len(points)-1)]-points[max(j-1,0)]).normalized();u=tangent.cross(Vector((0,0,1))).normalized();v=tangent.cross(u).normalized();rad=radius*(1-j/(len(points)-1))**.8+.002
        for k in range(12):a=k*math.tau/12;vv.append(tuple(p+rad*(u*math.cos(a)+v*math.sin(a))))
    for j in range(len(points)-1):
        for k in range(12):ff.append((j*12+k,j*12+(k+1)%12,(j+1)*12+(k+1)%12,(j+1)*12+k))
    ff.extend([tuple(range(11,-1,-1)),tuple((len(points)-1)*12+k for k in range(12))]);me=bpy.data.meshes.new(name);me.from_pydata(vv,[],ff);ob=bpy.data.objects.new(name,me);coll.objects.link(ob);me.materials.append(rootmat);uv=me.uv_layers.new(name='Longitudinal_bark')
    for p in me.polygons:
        p.use_smooth=True
        for li in p.loop_indices:i=me.loops[li].vertex_index;uv.data[li].uv=(i%12/12,lengths[i//12])
for k in range(46):
    a=k*math.tau/46+rng.uniform(-.025,.025)
    if math.sin(a)<-.93:continue
    start=2.34/math.cos((a+math.pi/8)%(math.pi/4)-math.pi/8);length=rng.uniform(.85,1.45);phase=rng.random()*math.tau;pts=[]
    for j in range(55):
        t=j/54;angle=a+.07*math.sin(t*5+phase)*t;r=start+length*t;z=.028+.24*(1-t)**4+.035*math.sin(t*math.pi)**2;pts.append(Vector((r*math.cos(angle),r*math.sin(angle),z)))
    rootmesh(pts,rng.uniform(.045,.085),'Raised_pale_buttress_root')
    for idx,sign in [(20,-1),(33,1)]:
        origin=pts[idx];direction=Vector((math.cos(a+sign*.8),math.sin(a+sign*.8),0));branch=[]
        for j in range(28):t=j/27;co=origin+direction*rng.uniform(.42,.50)*t;co.z=origin.z*(1-t)+.018*t;branch.append(co)
        rootmesh(branch,.025,'Interlaced_pale_rootlet')
# The stone blocks and door planks were already separate meshes. Add visible
# edge erosion to those components, preserving their existing mortar gaps.
tex=bpy.data.textures.new('Fine_limestone_erosion',type='CLOUDS');tex.noise_scale=.07;tex.noise_depth=2
for o in coll.objects:
    if o.hide_render:continue
    if o.name.startswith(('Staggered_limestone_block','Unbroken_tapered_obelisk','Obelisk_pyramid_point','Arch_voussoir')):
        sub=o.modifiers.new('Weathering_tessellation','SUBSURF');sub.subdivision_type='SIMPLE';sub.levels=2;sub.render_levels=2;dis=o.modifiers.new('Actual_limestone_edge_erosion','DISPLACE');dis.texture=tex;dis.texture_coords='GLOBAL';dis.strength=.012;dis.mid_level=.5
    if o.name.startswith('Arched_oak_door_plank'):o.location.y+=rng.uniform(-.005,.005)
    if o.name.startswith('Obelisk_pyramid_point'):
        # Match the 0.34 m upper shaft exactly; no ledge under the point.
        center=sum((v.co for v in o.data.vertices),Vector())/len(o.data.vertices)
        for v in o.data.vertices:v.co.x=center.x+(v.co.x-center.x)*(.34/.36);v.co.y=center.y+(v.co.y-center.y)*(.34/.36)
purple=bpy.data.materials['Unlit_dark_amethyst'];purple.name='Natural_amethyst_nonemissive_PBR';bs=purple.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.17;bs.inputs['Transmission Weight'].default_value=.45;bs.inputs['Emission Strength'].default_value=0
for n in purple.node_tree.nodes:
    if n.type=='BUMP':n.inputs['Distance'].default_value=.0003;n.inputs['Strength'].default_value=.12
# Pull the question-mark arm away from the sphere so its hooked silhouette reads.
for o in coll.objects:
    if o.name.startswith(('Question_mark_crown','Question_mark_mount')):
        for s in o.data.splines:
            for p in s.points:
                p.co.x=.94+(p.co.x-.94)*1.22;p.co.z=4.13+(p.co.z-4.13)*1.13
    if o.name=='Question_mark_terminal':o.location.x=.94+(o.location.x-.94)*1.22;o.location.z=4.13+(o.location.z-4.13)*1.13
# Small socket screws on the actual flat cast orbit bands, not decorative gears.
brass=bpy.data.materials['Polished_worn_brass']
for o in list(coll.objects):
    if o.hide_render or not o.name.startswith('Connected_orbit_band_') or o.type!='MESH':continue
    for j in [15,40,65,85]:
        vs=o.data.vertices;center=sum((vs[j*4+k].co for k in range(4)),Vector())/4;center.y-=.031;bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=.009,location=center);bolt=bpy.context.object
        for c in list(bolt.users_collection):c.objects.unlink(bolt)
        coll.objects.link(bolt);bolt.name='Orbit_band_cast_rivet';bolt.scale.y=.35;bolt.data.materials.append(brass)
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=1000;scene.render.resolution_y=1000;camera=scene.camera;camera.location=(10.5,-15,9);camera.data.ortho_scale=7.5;look_at(camera,(0,0,2.35));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'perspective_preview.png');bpy.ops.render.render(write_still=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r19','status':'author_preview_pending','source':'r18 with visible pale branching roots, separate eroded masonry, shaft-matched pyramid caps, nonemissive PBR amethyst and clearer question-mark arm','construction_notes':'Each wall block and door plank is a separate closed mesh. Orbit arms are rectangular cast bands with bevel modifiers. There are exactly four pyramid caps; no duplicated caps were found.'},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
