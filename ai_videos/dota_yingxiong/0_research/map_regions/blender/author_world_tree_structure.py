"""Replace the fused lower tree with six continuous roots and a hollow woven trunk."""
from pathlib import Path
import bpy,json,sys,math,random
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import material,look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));SRC=WORLD/'background/map_3d/environment_sources';folder=next(WORLD.glob('background/*/bg2_*/model_3d'));out=folder/'r06';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r05/authoring.blend'));coll=bpy.data.collections['ASSET_bg2'];rng=random.Random(206)
for o in coll.objects:
    if (o.type=='MESH' and len(o.data.polygons)>100000) or o.name.startswith('Crossed_bark_strand'):o.hide_render=True
for mat in bpy.data.materials:
    if mat.use_nodes:
        for n in mat.node_tree.nodes:
            if n.type=='HUE_SAT' and abs(n.inputs['Value'].default_value-1.35)<.001:n.inputs['Value'].default_value=.82;n.inputs['Saturation'].default_value=1.25
bark=bpy.data.materials['World_tree_fibrous_red_brown_bark']
def curve(name,points,radii,mat):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=1;cu.bevel_resolution=4;s=cu.splines.new('POLY');s.points.add(len(points)-1)
    for p,co,r in zip(s.points,points,radii):p.co=(*co,1);p.radius=r
    ob=bpy.data.objects.new(name,cu);coll.objects.link(ob);cu.materials.append(mat);return ob
for k in range(6):
    angle=k*math.tau/6+.2;points=[];radii=[];root=[]
    for j in range(81):
        t=j/80;a=angle+.16*math.sin(t*math.pi);r=1.25+6.1*t**1.3;co=Vector((r*math.cos(a),r*math.sin(a),6.3*(1-t)**1.65+.04));root.append(co)
    points=list(reversed(root));radii=[.05+.67*(1-j/80)**.65 for j in reversed(range(81))]
    for j in range(1,91):
        t=j/90;a=angle+t*math.tau*.65;r=1.25-.15*t;points.append(Vector((r*math.cos(a),r*math.sin(a),6.34+5.46*t)));radii.append(.70-.16*t)
    curve('Continuous_living_root_and_twisted_trunk',points,radii,bark)
    for startidx,sign in [(52,-1),(64,1)]:
        start=root[startidx];end=Vector((8.1*math.cos(angle+sign*.23),8.1*math.sin(angle+sign*.23),.025));branch=[start.lerp(end,j/50)+Vector((0,0,.10*math.sin(j/50*math.pi))) for j in range(51)];curve('Natural_surface_root_fork',branch,[.20*(1-j/50)+.015 for j in range(51)],bark)
# Actual aerial roots connect from the crown to soil instead of stopping in midair.
for k in range(16):
    a=k*2.399963;r=rng.uniform(3.5,5.6);top=rng.uniform(11.2,12.2);x,y=r*math.cos(a),r*math.sin(a);curve('Continuous_aerial_root',[(x+.045*math.sin(j*.22+k),y+.035*math.sin(j*.3),top*(1-j/70)) for j in range(71)],[.025*(1-j/90) for j in range(71)],bark)
iron=material('World_tree_rusted_lantern_frame',(.035,.028,.02),.62);iron.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=.75;glass=bpy.data.materials['World_tree_cyan_lantern_glass'];gb=glass.node_tree.nodes.get('Principled BSDF');gb.inputs['Emission Strength'].default_value=.25;gb.inputs['Transmission Weight'].default_value=.85
lightmat=material('World_tree_oil_lamp_light',(.1,.5,.28),.3);lb=lightmat.node_tree.nodes.get('Principled BSDF');lb.inputs['Emission Color'].default_value=(.12,1,.56,1);lb.inputs['Emission Strength'].default_value=12
def attach(o,name,mat):
    for c in list(o.users_collection):c.objects.unlink(o)
    coll.objects.link(o);o.name=name;o.data.materials.append(mat);return o
def block(name,loc,dims,mat):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=attach(bpy.context.object,name,mat);o.scale=dims;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);be=o.modifiers.new('Aged_metal_edges','BEVEL');be.width=.015;be.segments=2;return o
for k,(x,y,z) in enumerate([(-2.8,-1.5,5.4),(2.65,-1.6,6.1),(-2.2,2,6.5),(2.2,2,5.7)]):
    top=9.8;curve('Lantern_bearing_branch',[(0,0,10),(x*.45,y*.45,10.1),(x,y,top)],[.40,.22,.07],bark)
    for j in range(int((top-z-.6)/.15)):
        zz=z+.63+j*.15;bpy.ops.mesh.primitive_torus_add(major_radius=.055,minor_radius=.009,major_segments=16,minor_segments=6,location=(x,y,zz),rotation=(math.pi/2,0,j%2*math.pi/2));o=attach(bpy.context.object,'Lantern_iron_chain_link',iron);o.scale.y=1.4
    block('Lantern_bottom_plate',(x,y,z-.45),(.66,.66,.10),iron);block('Lantern_top_plate',(x,y,z+.45),(.72,.72,.10),iron)
    for dx in [-.28,.28]:
        for dy in [-.28,.28]:block('Lantern_corner_frame',(x+dx,y+dy,z),(.045,.045,.9),iron)
    for axis in [0,1]:
        for side in [-1,1]:
            loc=[x,y,z];loc[axis]+=.285;loc[axis]-=.57 if side<0 else 0;dims=[.55,.55,.80];dims[axis]=.008;block('Cyan_glass_lantern_panel',loc,dims,glass)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=.10,location=(x,y,z-.1));o=attach(bpy.context.object,'Small_oil_light',lightmat);o.scale=(.65,.65,1.8)
    data=bpy.data.lights.new('Physical_cyan_lamp','POINT');data.energy=18;data.color=(.25,1,.66);data.shadow_soft_size=.09;o=bpy.data.objects.new('Physical_cyan_lamp',data);coll.objects.link(o);o.location=(x,y,z-.05)
# Stems and foliage give every glowing fungus a physical attachment.
for o in list(coll.objects):
    if o.name.startswith('Living_luminous_fungus'):
        r=math.hypot(o.location.x,o.location.y);base=.29 if r<4.5 else 0;curve('Luminous_fungus_stalk',[(o.location.x,o.location.y,base),(o.location.x,o.location.y,o.location.z)],[.03,.025],bark)
with bpy.data.libraries.load(str(next((SRC/'fern_02').glob('*.blend'))),link=False) as (s,d):d.objects=[f'fern_02_{v}' for v in 'abcd']
for i in range(170):
    a=rng.random()*math.tau;r=rng.uniform(4.6,7.9)
    if math.sin(a)<-.90:continue
    src=d.objects[i%4];o=src.copy();o.data=src.data;coll.objects.link(o);o.name='Root_base_living_fern';o.location=(r*math.cos(a),r*math.sin(a),0);o.scale=(rng.uniform(1.0,2),)*3;o.rotation_euler.z=rng.random()*math.tau
for im in bpy.data.images:
    if im.source=='FILE' and not im.packed_file:
        paths=list(SRC.glob('*/textures/'+Path(im.filepath.replace('\\','/')).name))
        if paths:im.filepath=str(paths[0]);im.reload()
scene=bpy.context.scene;scene.cycles.samples=16;scene.render.resolution_x=900;scene.render.resolution_y=900;camera=scene.camera;camera.data.ortho_scale=27;camera.location=(0,-70,19);look_at(camera,(0,0,10));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'south_preview.png');bpy.ops.render.render(write_still=True);(out/'authoring.json').write_text(json.dumps({'revision':'r06','status':'author_preview_pending','source':'r05 independent leaves with fully separate six-root woven structure, visible engraved platform and four suspended physical lanterns','platform_diameter_m':9,'structural_roots':6,'lanterns':4},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
