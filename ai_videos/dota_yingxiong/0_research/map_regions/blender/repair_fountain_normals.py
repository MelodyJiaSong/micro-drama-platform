"""Repair inverted closed water/ground normals and detail the fountain banks."""
from pathlib import Path
import bpy,bmesh,json,math,random,sys,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import material,look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));OUT=WORLD/'background/map_3d';SRC=OUT/'environment_sources';folder=next(WORLD.glob('background/*/bg15_*/model_3d'));out=folder/'r04';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r03/authoring.blend'));coll=bpy.data.collections['ASSET_bg15'];rng=random.Random(1504);normal_report={}
for name in ['Solid_grounded_hillside_and_basin','Refractive_reservoir_water']:
    ob=bpy.data.objects[name];bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update();normal_report[name]={'faces':len(ob.data.polygons),'upward_faces':sum(p.normal.z>.5 for p in ob.data.polygons),'downward_faces':sum(p.normal.z<-.5 for p in ob.data.polygons)}
water=bpy.data.materials['Clear_cyan_spring_water'];nt=water.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.97,.995,1,1);bs.inputs['Roughness'].default_value=.045;absorb=next(n for n in nt.nodes if n.type=='VOLUME_ABSORPTION');absorb.inputs['Color'].default_value=(.03,.50,.78,1);absorb.inputs['Density'].default_value=.8
calcite=bpy.data.materials['Pale_calcite_basin'];nt=calcite.node_tree;bs=nt.nodes.get('Principled BSDF');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=5;noise.inputs['Detail'].default_value=6;tc=nt.nodes.new('ShaderNodeTexCoord');nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.29,.34,.30,1);ramp.color_ramp.elements[1].color=(.70,.73,.66,1);nt.links.new(noise.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.007;bump.inputs['Strength'].default_value=.4;nt.links.new(noise.outputs[0],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
rocks=[o for o in coll.objects if o.name.startswith(('Natural_limestone_pinnacle','Rear_spire','Ground_embedded_rock'))]
# Desaturate the warm source rock, retaining its scan and adding moss in crevices.
mats={}
for ob in rocks:
    for slot in ob.material_slots:
        original=slot.material
        if not original:continue
        if original.name not in mats:
            m=original.copy();m.name='Cool_mossy_'+original.name;nt=m.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');source=bs.inputs['Base Color'].links[0].from_socket;hue=nt.nodes.new('ShaderNodeHueSaturation');hue.inputs['Saturation'].default_value=.15;hue.inputs['Value'].default_value=.74;nt.links.new(source,hue.inputs['Color']);tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=4;noise.inputs['Detail'].default_value=5;nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);r=nt.nodes.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.45;r.color_ramp.elements[1].position=.68;r.color_ramp.elements[1].color=(.8,.8,.8,1);nt.links.new(noise.outputs[0],r.inputs[0]);mix=nt.nodes.new('ShaderNodeMixRGB');mix.inputs[2].default_value=(.065,.11,.018,1);nt.links.new(hue.outputs[0],mix.inputs[1]);nt.links.new(r.outputs[0],mix.inputs[0]);nt.links.new(mix.outputs[0],bs.inputs['Base Color']);mats[original.name]=m
        slot.link='OBJECT';slot.material=mats[original.name]
# Scale the lantern assemblies about their supports rather than about world origin.
for o in coll.objects:
    if o.name.startswith(('Lantern_','Four_sided_oak_lantern_roof')):
        if o.type=='MESH' and o.name.startswith('Four_sided_oak_lantern_roof'):
            for v in o.data.vertices:v.co.z=.76+(v.co.z-.76)*.62
        else:o.location.z=.76+(o.location.z-.76)*.62;o.scale*=.75
hill=bpy.data.objects['Solid_grounded_hillside_and_basin']
hill_bvh=BVHTree.FromPolygons([v.co.copy() for v in hill.data.vertices],[list(p.vertices) for p in hill.data.polygons])
rock_bvhs={}
rock_transforms={o.name:(o.matrix_world.copy(),o.matrix_world.inverted(),o.location.copy()) for o in rocks}
for rock in rocks:
    key=rock.data.name
    if key not in rock_bvhs:rock_bvhs[key]=BVHTree.FromPolygons([v.co.copy() for v in rock.data.vertices],[list(p.vertices) for p in rock.data.polygons])
with bpy.data.libraries.load(str(next((SRC/'grass_medium_01').glob('*.blend'))),link=False) as (s,d):d.objects=[n for n in s.objects if n.startswith('grass_medium_01') and n.endswith('LOD2')]
grass=d.objects
if not grass:raise RuntimeError('Grass source unavailable')
placed=0;grass_points=[];grass_scales=[];grass_angles=[]
for i in range(6500):
    a=rng.random()*math.tau;r=math.sqrt(rng.uniform(3.42**2,5.05**2));x,y=r*math.cos(a),r*math.sin(a)
    if y<-3.2 and abs(x)<1.0:continue
    p,n,index,distance=hill_bvh.ray_cast(Vector((x,y,5)),Vector((0,0,-1)))
    if p is None:continue
    grass_points.append(tuple(p+Vector((0,0,-.01))));grass_angles.append((0,0,rng.random()*math.tau));grass_scales.append((rng.uniform(.8,1.6),)*3);placed+=1
lib=bpy.data.collections.new('Fountain_grass_prototypes')
for o in grass:o.location=(0,0,0);lib.objects.link(o)
me=bpy.data.meshes.new('Fountain_bank_grass_points');me.from_pydata(grass_points,[],[])
for name,data in [('scale',grass_scales),('rotation',grass_angles)]:a=me.attributes.new(name,'FLOAT_VECTOR','POINT');a.data.foreach_set('vector',np.asarray(data,dtype=np.float32).ravel())
o=bpy.data.objects.new('Living_bank_grass',me);coll.objects.link(o);ng=bpy.data.node_groups.new('Fountain_grass_instances','GeometryNodeTree');ng.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');ng.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');nodes,links=ng.nodes,ng.links;inp=nodes.new('NodeGroupInput');output=nodes.new('NodeGroupOutput');info=nodes.new('GeometryNodeCollectionInfo');info.inputs['Collection'].default_value=lib;info.inputs['Separate Children'].default_value=True;info.inputs['Reset Children'].default_value=True;inst=nodes.new('GeometryNodeInstanceOnPoints');inst.inputs['Pick Instance'].default_value=True;links.new(inp.outputs['Geometry'],inst.inputs['Points']);links.new(info.outputs['Instances'],inst.inputs['Instance']);links.new(inst.outputs['Instances'],output.inputs['Geometry'])
for name,socket in [('scale','Scale'),('rotation','Rotation')]:a=nodes.new('GeometryNodeInputNamedAttribute');a.data_type='FLOAT_VECTOR';a.inputs['Name'].default_value=name;links.new(a.outputs['Attribute'],inst.inputs[socket])
mod=o.modifiers.new('Instanced_bank_grass','NODES');mod.node_group=ng
print('BANK_GRASS',placed,flush=True)
# Small ferns occupy actual upper rock surfaces, keeping each root in contact.
ferns=[o for o in coll.objects if o.name.startswith('Living_fern_and_bank_foliage')];added=0
for i in range(550):
    rock=rocks[i%len(rocks)]
    if rock.name.startswith('Ground_'):continue
    worldmat,inv,loc=rock_transforms[rock.name];xx=rng.uniform(-.5,.5);yy=rng.uniform(-.5,.5);origin=Vector((loc.x+xx,loc.y+yy,6));p,n,index,distance=rock_bvhs[rock.data.name].ray_cast(inv@origin,(inv.to_3x3()@Vector((0,0,-1))).normalized())
    if p is None:continue
    world=worldmat@p;normal=worldmat.to_3x3().inverted().transposed()@n
    if world.z<1.0 or normal.normalized().z<.15:continue
    src=ferns[i%len(ferns)];o=src.copy();o.data=src.data;coll.objects.link(o);o.name='Rock_crevice_fern';o.location=world-Vector((0,0,.025));o.rotation_euler.z=rng.random()*math.tau;o.scale=(rng.uniform(.25,.75),)*3;added+=1
for im in bpy.data.images:
    if im.source=='FILE' and not im.packed_file:
        found=list(SRC.glob('*/textures/'+Path(im.filepath.replace('\\','/')).name))
        if found:im.filepath=str(found[0]);im.reload()
scene=bpy.context.scene;scene.cycles.samples=16;scene.render.resolution_x=900;scene.render.resolution_y=900;camera=scene.camera;camera.location=(0,-25,11.25);look_at(camera,(0,0,2.3));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'south_preview.png');bpy.ops.render.render(write_still=True)
report={'revision':'r04','status':'author_preview_pending','normal_repair':normal_report,'bank_grass_clumps':placed,'rock_crevice_ferns':added};(out/'authoring.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
