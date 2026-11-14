"""Scanned uneven entry stones and timber lantern architecture."""
from pathlib import Path
import bpy,json,sys,math,random
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import material,look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg15_*/model_3d'));out=folder/'r07';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r06/authoring.blend'));coll=bpy.data.collections['ASSET_bg15'];rng=random.Random(1507)
nt=bpy.data.materials['Clear_cyan_spring_water'].node_tree;vol=next(n for n in nt.nodes if n.type=='VOLUME_ABSORPTION');vol.inputs['Color'].default_value=(.015,.18,.95,1);vol.inputs['Density'].default_value=3.0
source=next(o for o in coll.objects if o.name.startswith('Rear_spire'))
for old in list(coll.objects):
    if old.name.startswith('Weathered_entry_stair'):
        old.hide_render=True
        for k in range(3):
            o=source.copy();o.data=source.data;coll.objects.link(o);o.name='Individual_worn_entry_stone';o.location=(old.location.x+(k-1)*.57,old.location.y,old.location.z-.09);o.scale=(rng.uniform(.56,.66),rng.uniform(.39,.48),rng.uniform(.17,.21));o.rotation_euler.z=rng.uniform(-.06,.06)
    if old.name.startswith(('Lantern_','Four_sided_oak_lantern_roof')):old.hide_render=True
wood=bpy.data.materials['Dark_oak_lantern'];metal=bpy.data.materials.get('Lantern_aged_metal') or material('Lantern_aged_metal',(.035,.025,.012),.45);flame=bpy.data.materials['Candle_flame'];glass=material('Fountain_lantern_clear_glass',(.94,.98,1),.08);gb=glass.node_tree.nodes.get('Principled BSDF');gb.inputs['Transmission Weight'].default_value=1;gb.inputs['IOR'].default_value=1.45
def attach(o,name,mat):
    for c in list(o.users_collection):c.objects.unlink(o)
    coll.objects.link(o);o.name=name;o.data.materials.append(mat);return o
def block(name,loc,dim,mat):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=attach(bpy.context.object,name,mat);o.scale=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);m=o.modifiers.new('Hand_worn_edges','BEVEL');m.width=.003;m.segments=2;return o
def curve(name,points,radius,mat):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=2;s=cu.splines.new('POLY');s.points.add(len(points)-1)
    for p,co in zip(s.points,points):p.co=(*co,1)
    o=bpy.data.objects.new(name,cu);coll.objects.link(o);cu.materials.append(mat)
for x in [-1.35,1.35]:
    y=-4.15;base=.62
    for j in range(2):
        o=source.copy();o.data=source.data;coll.objects.link(o);o.name='Lantern_mossy_stone_support';o.location=(x,y,base+j*.24);o.scale=(.48-j*.055,.46-j*.045,.27)
    z=base+.52;block('Timber_lantern_base',(x,y,z),(.43,.43,.055),wood)
    for dx in [-.18,.18]:
        for dy in [-.18,.18]:block('Carved_timber_lantern_post',(x+dx,y+dy,z+.19),(.032,.032,.36),wood)
    for axis in [0,1]:
        for side in [-1,1]:
            pos=[x,y,z+.19];pos[axis]+=.18;dims=[.33,.33,.31];dims[axis]=.003;block('Thin_clear_lantern_window',pos,dims,glass)
            for dd in [-.055,.055]:
                pp=pos.copy();pp[1-axis]+=dd;pp[axis]+=.004*side;dim=[.012,.012,.32];block('Vertical_window_lattice',pp,dim,wood)
            for zz in [.10,.27]:
                pp=pos.copy();pp[2]=z+zz;pp[axis]+=.006*side;dim=[.35,.35,.012];dim[axis]=.012;block('Horizontal_window_lattice',pp,dim,wood)
    profile=[(.025,z+.57),(.10,z+.52),(.25,z+.40),(.36,z+.415)];vv=[];ff=[];N=32
    for rad,zz in profile:
        for k in range(N):
            a=k*math.tau/N;octagon=1/math.cos((a+math.pi/8)%(math.pi/4)-math.pi/8);vv.append((x+rad*octagon*math.cos(a),y+rad*octagon*math.sin(a),zz))
    for j in range(3):
        for k in range(N):a=j*N+k;b=j*N+(k+1)%N;ff.append((a,b,b+N,a+N))
    me=bpy.data.meshes.new('Curved_octagonal_timber_roof');me.from_pydata(vv,[],ff);o=bpy.data.objects.new('Curved_octagonal_timber_roof',me);coll.objects.link(o);me.materials.append(wood);solid=o.modifiers.new('Thick_roof_boards','SOLIDIFY');solid.thickness=.012
    for k in range(16):a=k*math.tau/16;curve('Individual_roof_board_joint',[(x+rad*math.cos(a),y+rad*math.sin(a),zz+.008) for rad,zz in profile],.005,metal)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=12,radius=.035,location=(x,y,z+.60));attach(bpy.context.object,'Roof_finial',metal)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=12,radius=.023,location=(x,y,z+.15));o=attach(bpy.context.object,'Visible_lantern_oil_flame',flame);o.scale.z=2.1
    data=bpy.data.lights.new('Warm_lantern_oil_light','POINT');data.energy=9;data.color=(1,.43,.12);data.shadow_soft_size=.025;o=bpy.data.objects.new('Warm_lantern_oil_light',data);coll.objects.link(o);o.location=(x,y,z+.17)
scene=bpy.context.scene;scene.cycles.samples=32;scene.camera.location=(0,-25,10.5);scene.camera.data.ortho_scale=12.2;look_at(scene.camera,(0,0,2.3));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'south_preview.png');bpy.ops.render.render(write_still=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r07','status':'author_preview_pending','source':'r06 with closed scanned entry stones, octagonal curved timber lantern roofs, lattice and clear panes, mineral water absorption','water_surface_height_m':1.04,'waterfall_impact_y':2.9},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
