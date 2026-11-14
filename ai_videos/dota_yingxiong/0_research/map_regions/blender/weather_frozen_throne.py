"""Weathered basalt, asymmetric fractured ice and physical frost accretions."""
from pathlib import Path
import bpy,bmesh,json,sys,math,random
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import material,look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('background/*/bg3_*/model_3d'));out=folder/'r04';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r03/authoring.blend'));coll=bpy.data.collections['ASSET_bg3'];rng=random.Random(304)
stone=bpy.data.materials['Dark_hewn_frozen_basalt'];nt=stone.node_tree;bs=nt.nodes.get('Principled BSDF');tc=nt.nodes.new('ShaderNodeTexCoord');mapping=nt.nodes.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs['Scale'].default_value=.6;nt.links.new(tc.outputs['Object'],mapping.inputs[0]);im=nt.nodes.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(WORLD/'background/map_3d/textures/rocky_terrain_diff_2k.jpg'),check_existing=True);im.projection='BOX';im.projection_blend=.35;nt.links.new(mapping.outputs[0],im.inputs[0]);gray=nt.nodes.new('ShaderNodeRGBToBW');nt.links.new(im.outputs['Color'],gray.inputs[0]);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.004,.006,.008,1);ramp.color_ramp.elements[1].color=(.055,.067,.075,1);nt.links.new(gray.outputs[0],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.035;bump.inputs['Strength'].default_value=.8;nt.links.new(gray.outputs[0],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
tex=bpy.data.textures.new('Natural_stone_fractures',type='CLOUDS');tex.noise_scale=.14;tex.noise_depth=2
for o in coll.objects:
    if o.name.startswith(('Individual_coursed_basalt','Single_front_stone_step','Stair_side_parapet','Brazier_stone_pier','Brazier_pier_cap')):
        sub=o.modifiers.new('Chipped_surface_tessellation','SUBSURF');sub.subdivision_type='SIMPLE';sub.levels=3;sub.render_levels=3;dis=o.modifiers.new('Actual_eroded_stone','DISPLACE');dis.texture=tex;dis.texture_coords='GLOBAL';dis.strength=.045;dis.mid_level=.52
# Ice surface: weak broken cracks and subtle micro-roughness, blue absorption.
ice=bpy.data.materials['Clear_ancient_cyan_ice'];nt=ice.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.065
for n in nt.nodes:
    if n.type=='VOLUME_ABSORPTION':n.inputs['Color'].default_value=(.26,.66,.80,1);n.inputs['Density'].default_value=.10
    if n.type=='MATH' and n.operation=='LESS_THAN':n.inputs[1].default_value=.003
    if n.type=='MATH' and n.operation=='MULTIPLY':n.inputs[1].default_value=.30
old=bpy.data.objects['Solid_transmissive_ice_crystal'];old.hide_render=True
profile=[(2,3.45),(3.6,3.55),(5.3,3.03),(7.2,2.78),(8.8,2.40),(10.5,1.83),(11.9,1.30),(13.0,.78),(14,.015)];N=16;verts=[];faces=[]
for j,(z,r) in enumerate(profile):
    for k in range(N):
        a=-math.pi/2+math.pi/N+k*math.tau/N;rr=r*(1+.08*math.sin(k*2.23+j*1.1)+rng.uniform(-.035,.035));verts.append((rr*math.cos(a)+.10*math.sin(j),rr*.72*math.sin(a),z+(rng.uniform(-.25,.25) if 0<j<len(profile)-1 else 0)))
for j in range(len(profile)-1):
    for k in range(N):
        a=j*N+k;b=j*N+(k+1)%N;c=(j+1)*N+(k+1)%N;d=(j+1)*N+k
        if k%3:faces.extend([(a,b,c),(a,c,d)])
        else:faces.append((a,b,c,d))
faces.extend([tuple(range(N-1,-1,-1)),tuple((len(profile)-1)*N+k for k in range(N))]);me=bpy.data.meshes.new('Irregular_fractured_ice');me.from_pydata(verts,[],faces);bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new('Asymmetric_solid_ice_monolith',me);coll.objects.link(o);me.materials.append(ice)
frost=material('Accumulated_rough_white_frost',(.48,.62,.68),.87);fb=frost.node_tree.nodes.get('Principled BSDF');fb.inputs['Subsurface Weight'].default_value=.15
def attach(o,name,mat):
    for c in list(o.users_collection):c.objects.unlink(o)
    coll.objects.link(o);o.name=name;o.data.materials.append(mat);return o
# Frost follows exposed horizontal stone edges, broken into irregular deposits.
for k in range(240):
    a=rng.random()*math.tau;r=rng.uniform(6.75,7.02)
    if math.sin(a)<-.94:continue
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=(r*math.cos(a),r*math.sin(a),2.015));o=attach(bpy.context.object,'Uneven_platform_frost',frost);o.scale=(rng.uniform(.04,.18),rng.uniform(.04,.14),rng.uniform(.02,.055))
    if k%3==0:
        length=rng.uniform(.12,.60);bpy.ops.mesh.primitive_cone_add(vertices=7,radius1=.003,radius2=rng.uniform(.018,.040),depth=length,location=(7.02*math.cos(a),7.02*math.sin(a),1.98-length/2));attach(bpy.context.object,'Gravity_formed_icicle',ice)
for j in range(16):
    for k in range(12):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=(rng.uniform(-2.02,2.02),-8.95+j*.25,.125*(j+1)+.015));o=attach(bpy.context.object,'Scattered_step_hoarfrost',frost);o.scale=(rng.uniform(.025,.09),.028,.015)
# Low shards merge into the monolith footprint and create a fractured silhouette.
for k in range(24):
    a=k*math.tau/24;r=rng.uniform(2.6,3.55);height=rng.uniform(.35,2.7);bpy.ops.mesh.primitive_cone_add(vertices=rng.choice([5,6,7]),radius1=rng.uniform(.18,.55),radius2=.01,depth=height,location=(r*math.cos(a),r*.72*math.sin(a),2+height/2));o=attach(bpy.context.object,'Fractured_ice_foot',ice);o.rotation_euler=(rng.uniform(-.18,.18),rng.uniform(-.18,.18),a)
fire=bpy.data.materials['Copper_green_volumetric_flame']
for n in fire.node_tree.nodes:
    if n.type=='MATH' and n.operation=='MULTIPLY' and n.inputs[1].default_value==45:n.inputs[1].default_value=160
for o in coll.objects:
    if o.name.startswith('Real_green_fire_volume'):o.scale.x*=.65;o.scale.y*=.65;o.scale.z*=1.25
scene=bpy.context.scene;scene.cycles.samples=24;scene.camera.data.ortho_scale=17.5;scene.camera.location=(0,-45,10);look_at(scene.camera,(0,0,7));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'south_preview.png');bpy.ops.render.render(write_still=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r04','status':'author_preview_pending','source':'r03 with physically eroded dark stone, asymmetrically faceted ice, icicles and frost accretion','total_height_m':14,'platform_diameter_m':14,'platform_height_m':2,'armour_contains_person':False},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
