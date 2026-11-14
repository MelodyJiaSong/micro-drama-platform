"""Separate solid ice, floating empty armour, single stair and green fire bowls."""
from pathlib import Path
import bpy,bmesh,json,math,random,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import material,look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg3_*/model_3d'));out=folder/'r03';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r02/inspection/bg3_r02.blend'));coll=bpy.data.collections['ASSET_bg3']
for o in list(coll.objects):coll.objects.unlink(o)
rng=random.Random(303)
def mesh(name,verts,faces,mat,smooth=False):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new(name,me);coll.objects.link(o);me.materials.append(mat)
    for p in me.polygons:p.use_smooth=smooth
    return o
def attach(o,name,mat):
    for c in list(o.users_collection):c.objects.unlink(o)
    coll.objects.link(o);o.name=name;o.data.materials.append(mat);return o
def block(name,loc,dim,mat,bevel=.02):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=attach(bpy.context.object,name,mat);o.scale=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:m=o.modifiers.new('Worn_edges','BEVEL');m.width=bevel;m.segments=3
    return o
def curve(name,points,radius,mat):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=3;s=cu.splines.new('POLY');s.points.add(len(points)-1)
    for p,co in zip(s.points,points):p.co=(*co,1)
    ob=bpy.data.objects.new(name,cu);coll.objects.link(ob);cu.materials.append(mat);return ob
def sphere(name,loc,scale,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=24,radius=1,location=loc);o=attach(bpy.context.object,name,mat);o.scale=scale
    for p in o.data.polygons:p.use_smooth=True
    return o
def weather(name,c0,c1,rough,metal=0,scale=8):
    m=material(name,c0,rough);nt=m.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Metallic'].default_value=metal;tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=scale;noise.inputs['Detail'].default_value=5;nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);r=nt.nodes.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(*c0,1);r.color_ramp.elements[1].color=(*c1,1);nt.links.new(noise.outputs[0],r.inputs[0]);nt.links.new(r.outputs[0],bs.inputs['Base Color']);b=nt.nodes.new('ShaderNodeBump');b.inputs['Distance'].default_value=.012 if metal==0 else .002;b.inputs['Strength'].default_value=.55;nt.links.new(noise.outputs[0],b.inputs['Height']);nt.links.new(b.outputs[0],bs.inputs['Normal']);return m
stone=weather('Dark_hewn_frozen_basalt',(.025,.030,.027),(.14,.15,.13),.88);steel=weather('Floating_blackened_iron',(.018,.023,.03),(.075,.085,.10),.32,.85,26);trim=weather('Worn_armour_edge',(.08,.055,.025),(.19,.14,.075),.35,.85,35);bronze=weather('Copper_salt_braziers',(.035,.07,.05),(.18,.105,.025),.5,.8,14)
nt=stone.node_tree;bs=nt.nodes.get('Principled BSDF');old=bs.inputs['Base Color'].links[0].from_socket;geo=nt.nodes.new('ShaderNodeNewGeometry');sep=nt.nodes.new('ShaderNodeSeparateXYZ');nt.links.new(geo.outputs['Normal'],sep.inputs[0]);r=nt.nodes.new('ShaderNodeMapRange');r.inputs['From Min'].default_value=.65;r.inputs['From Max'].default_value=1;r.inputs['To Max'].default_value=.30;nt.links.new(sep.outputs['Z'],r.inputs['Value']);mix=nt.nodes.new('ShaderNodeMixRGB');mix.inputs[2].default_value=(.64,.70,.72,1);nt.links.new(r.outputs[0],mix.inputs[0]);nt.links.new(old,mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
# Solid circular platform, continuous side walls and a single south stair.
bpy.ops.mesh.primitive_cylinder_add(vertices=128,radius=6.85,depth=1.95,location=(0,0,.975));attach(bpy.context.object,'Solid_circular_platform_core',stone)
for course in range(5):
    for k in range(32):
        a=(k+course%2*.5)*math.tau/32;da=math.tau/32;lo,hi=a+.002,a+da-.002;v=[]
        for z in [course*.4+.008,(course+1)*.4-.008]:
            for radius,angle in [(6.5,lo),(7,lo),(7,hi),(6.5,hi)]:v.append((radius*math.cos(angle),radius*math.sin(angle),z))
        ob=mesh('Individual_coursed_basalt_block',v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],stone);be=ob.modifiers.new('Chipped_block_edges','BEVEL');be.width=rng.uniform(.014,.035);be.segments=2
for j in range(16):
    y=-8.8+j*.25;z=.125*(j+1);block('Single_front_stone_step',(0,y,z/2),(4.2,.33,z),stone,.025)
    for side in [-1,1]:block('Stair_side_parapet',(side*2.28,y,z+.21),(.36,.34,.42),stone,.025)
# Separate, closed, faceted ice monolith.
ice=material('Clear_ancient_cyan_ice',(.94,.99,1),.045);nt=ice.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Transmission Weight'].default_value=1;bs.inputs['IOR'].default_value=1.31;absorb=nt.nodes.new('ShaderNodeVolumeAbsorption');absorb.inputs['Color'].default_value=(.43,.80,.95,1);absorb.inputs['Density'].default_value=.035;nt.links.new(absorb.outputs[0],nt.nodes.get('Material Output').inputs['Volume']);tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1.7;noise.inputs['Detail'].default_value=3;nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);warp=nt.nodes.new('ShaderNodeVectorMath');warp.operation='ADD';nt.links.new(tc.outputs['Object'],warp.inputs[0]);nt.links.new(noise.outputs['Color'],warp.inputs[1]);vor=nt.nodes.new('ShaderNodeTexVoronoi');vor.feature='DISTANCE_TO_EDGE';vor.inputs['Scale'].default_value=2.0;nt.links.new(warp.outputs[0],vor.inputs['Vector']);crack=nt.nodes.new('ShaderNodeMath');crack.operation='LESS_THAN';crack.inputs[1].default_value=.008;nt.links.new(vor.outputs['Distance'],crack.inputs[0]);weight=nt.nodes.new('ShaderNodeMath');weight.operation='MULTIPLY';weight.inputs[1].default_value=.55;nt.links.new(crack.outputs[0],weight.inputs[0]);white=nt.nodes.new('ShaderNodeBsdfPrincipled');white.inputs['Base Color'].default_value=(.73,.85,.89,1);white.inputs['Roughness'].default_value=.45;mix=nt.nodes.new('ShaderNodeMixShader');nt.links.new(weight.outputs[0],mix.inputs[0]);nt.links.new(bs.outputs[0],mix.inputs[1]);nt.links.new(white.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],nt.nodes.get('Material Output').inputs['Surface'])
profile=[(2,3.45),(4.3,3.30),(7.4,2.65),(10.2,1.95),(12.2,1.20),(14,.015)];verts=[];faces=[];N=12
for j,(z,radius) in enumerate(profile):
    for k in range(N):a=-math.pi/2+math.pi/12+k*math.tau/N;rr=radius*(1+.04*math.sin(k*3+j));verts.append((rr*math.cos(a),rr*.72*math.sin(a),z))
for j in range(len(profile)-1):
    for k in range(N):faces.append((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k))
faces.extend([tuple(range(N-1,-1,-1)),tuple((len(profile)-1)*N+k for k in range(N))]);mesh('Solid_transmissive_ice_crystal',verts,faces,ice)
# Hollow helmet with real visor apertures; no head or body inside the armour.
helmet=sphere('Floating_empty_closed_helmet',(0,0,10.4),(.52,.42,.68),steel);bpy.context.view_layer.objects.active=helmet;helmet.select_set(True);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
cutters=[sphere('Helmet_inner_cavity',(0,0,10.39),(.47,.37,.63),steel),block('Eye_visor_cut',(0,-.42,10.49),(.90,.60,.10),steel,0),block('Nasal_visor_cut',(0,-.44,10.15),(.075,.60,.55),steel,0)]
for cutter in cutters:
    mod=helmet.modifiers.new('True_open_armour','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter;bpy.context.view_layer.objects.active=helmet;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
curve('Helmet_central_ridge',[(0,-.24,11.00),(0,-.41,10.8),(0,-.44,10.58)],.018,trim)
# Open upper shoulder shells, with three visibly separate overlapping plates.
for side in [-1,1]:
    for layer in range(3):
        cx=side*(1.13+layer*.055);cz=8.8-layer*.16;verts=[];faces=[]
        for j in range(9):
            th=.06+j/8*math.pi*.57
            for k in range(32):a=k*math.tau/32;verts.append((cx+(.66-layer*.04)*math.sin(th)*math.cos(a),.43*math.sin(th)*math.sin(a),cz+.40*math.cos(th)))
        for j in range(8):
            for k in range(32):faces.append((j*32+k,j*32+(k+1)%32,(j+1)*32+(k+1)%32,(j+1)*32+k))
        ob=mesh('Separate_layered_pauldron',verts,faces,steel,True);mod=ob.modifiers.new('Real_plate_thickness','SOLIDIFY');mod.thickness=.025;curve('Pauldron_worn_lower_lip',[verts[8*32+k] for k in range(32)]+[verts[8*32]],.015,trim)
# Cuirass is a hollow shell, with a raised central keel and separate trim.
verts=[];faces=[];rings=[(6.25,.35,.29),(6.55,.53,.36),(7.0,.68,.40),(7.5,.83,.43),(7.9,.66,.34)]
for z,rx,ry in rings:
    for k in range(32):a=k*math.tau/32;yy=ry*math.sin(a)-.10*max(0,-math.sin(a))**10;verts.append((rx*math.cos(a),yy,z))
for j in range(4):
    for k in range(32):faces.append((j*32+k,j*32+(k+1)%32,(j+1)*32+(k+1)%32,(j+1)*32+k))
chest=mesh('Floating_hollow_breastplate',verts,faces,steel,True);mod=chest.modifiers.new('Forged_cuirass_thickness','SOLIDIFY');mod.thickness=.035
for z,rx,ry in [rings[0],rings[-1]]:curve('Breastplate_edge_trim',[(rx*math.cos(k*math.tau/64),ry*math.sin(k*math.tau/64)-.10*max(0,-math.sin(k*math.tau/64))**10,z) for k in range(65)],.018,trim)
curve('Cuirass_central_keel',[(0,-.39,6.25),(0,-.50,7),(0,-.44,7.9)],.022,trim)
for side in [-1,1]:
    for z in [6.6,7.0,7.4]:curve('Embossed_chest_chevron',[(0,-.51,z-.15),(side*.35,-.47,z+.03),(side*.61,-.28,z+.25)],.014,trim)
    # Open flared vambrace and an articulated empty gauntlet.
    cx=side*1.05;verts=[];faces=[]
    for z,r in [(4.65,.17),(5.1,.20),(5.65,.31)]:
        for k in range(24):a=k*math.tau/24;verts.append((cx+r*math.cos(a),r*.72*math.sin(a),z))
    for j in range(2):
        for k in range(24):faces.append((j*24+k,j*24+(k+1)%24,(j+1)*24+(k+1)%24,(j+1)*24+k))
    ob=mesh('Floating_hollow_vambrace',verts,faces,steel,True);mod=ob.modifiers.new('Vambrace_thickness','SOLIDIFY');mod.thickness=.025
    for zz,rr in [(4.66,.18),(5.64,.32)]:curve('Vambrace_rolled_lip',[(cx+rr*math.cos(k*math.tau/64),rr*.72*math.sin(k*math.tau/64),zz) for k in range(65)],.018,trim)
    sphere('Empty_gauntlet_palm',(cx,0,4.49),(.19,.13,.22),steel)
    for finger in range(4):
        x=cx+(finger-1.5)*.085
        for joint in range(3):sphere('Articulated_gauntlet_finger',(x,-.015-joint*.035,4.29-joint*.105),(.048,.055,.075),steel)
    sphere('Gauntlet_thumb',(cx+side*.20,-.04,4.44),(.07,.075,.13),steel)
# Small real air bubbles are enclosed in the ice, not painted on its front face.
air=material('Ice_air_inclusion',(.9,.97,1),.08);ab=air.node_tree.nodes.get('Principled BSDF');ab.inputs['Transmission Weight'].default_value=1;ab.inputs['IOR'].default_value=1.0
for i in range(180):
    z=rng.uniform(3.0,11.7);r=max(.35,3.3-(z-3)*.25);x=rng.uniform(-r*.7,r*.7);y=rng.choice([-1,1])*rng.uniform(.5,r*.65);size=rng.uniform(.015,.055);sphere('Internal_trapped_air_bubble',(x,y,z),(size,size*.8,size*rng.uniform(1,2)),air)
# Copper bowls and volume flames replace the opaque blue flame lumps.
fire=bpy.data.materials.new('Copper_green_volumetric_flame');fire.use_nodes=True;nt=fire.node_tree;n,l=nt.nodes,nt.links;n.clear();output=n.new('ShaderNodeOutputMaterial');vol=n.new('ShaderNodeVolumePrincipled');vol.inputs['Density'].default_value=0;vol.inputs['Emission Color'].default_value=(.08,1,.24,1);l.new(vol.outputs[0],output.inputs['Volume']);tc=n.new('ShaderNodeTexCoord');sub=n.new('ShaderNodeVectorMath');sub.operation='SUBTRACT';sub.inputs[1].default_value=(.5,.5,.5);l.new(tc.outputs['Generated'],sub.inputs[0]);dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';l.new(sub.outputs[0],dot.inputs[0]);l.new(sub.outputs[0],dot.inputs[1]);mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=-22;l.new(dot.outputs['Value'],mul.inputs[0]);exp=n.new('ShaderNodeMath');exp.operation='EXPONENT';l.new(mul.outputs[0],exp.inputs[0]);noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=5;noise.inputs['Detail'].default_value=3;l.new(tc.outputs['Generated'],noise.inputs['Vector']);m=n.new('ShaderNodeMath');m.operation='MULTIPLY';l.new(exp.outputs[0],m.inputs[0]);l.new(noise.outputs[0],m.inputs[1]);gain=n.new('ShaderNodeMath');gain.operation='MULTIPLY';gain.inputs[1].default_value=45;l.new(m.outputs[0],gain.inputs[0]);l.new(gain.outputs[0],vol.inputs['Emission Strength'])
for side in [-1,1]:
    x,y=side*3.0,-7.1;block('Brazier_stone_pier',(x,y,.85),(.9,.9,1.7),stone);block('Brazier_pier_cap',(x,y,1.74),(1.12,1.12,.16),stone);verts=[];faces=[];profile=[(0,1.82),(.24,1.82),(.26,1.98),(.48,2.07),(.61,2.32),(.60,2.38),(.54,2.36),(.43,2.10),(.22,2.03),(0,2.03)]
    for rr,z in profile:
        for k in range(64):a=k*math.tau/64;verts.append((x+rr*math.cos(a),y+rr*math.sin(a),z))
    for j in range(len(profile)-1):
        for k in range(64):faces.append((j*64+k,j*64+(k+1)%64,(j+1)*64+(k+1)%64,(j+1)*64+k))
    mesh('Fluted_copper_fire_bowl',verts,faces,bronze,True)
    for j in range(5):sphere('Real_green_fire_volume',(x+rng.uniform(-.22,.22),y+rng.uniform(-.18,.18),2.53+rng.uniform(0,.3)),(.18,.16,rng.uniform(.35,.62)),fire)
    data=bpy.data.lights.new('Copper_salt_firelight','POINT');data.energy=80;data.color=(.15,1,.32);data.shadow_soft_size=.45;ob=bpy.data.objects.new('Copper_salt_firelight',data);coll.objects.link(ob);ob.location=(x,y,2.6)
scene=bpy.context.scene;scene.cycles.samples=24;scene.cycles.transmission_bounces=18;scene.cycles.max_bounces=24;scene.render.resolution_x=1000;scene.render.resolution_y=1000;camera=scene.camera;camera.data.ortho_scale=17.5;camera.location=(0,-45,10);look_at(camera,(0,0,7));bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'south_preview.png');bpy.ops.render.render(write_still=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r03','status':'author_preview_pending','source':'Component-authored ice, hollow armour, true single-entry circular basalt platform and volume fire','total_height_m':14,'platform_diameter_m':14,'platform_height_m':2,'armour_contains_person':False,'armour_parts':['helmet','left and right layered pauldrons','hollow cuirass','left and right vambraces and articulated gauntlets'],'air_bubbles':180},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
