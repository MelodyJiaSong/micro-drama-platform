"""Replace melted skull decorations with verified CC0 scan-derived geometry."""
from pathlib import Path
import bpy,json,math,numpy as np,random,sys
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
from build_production_map import surface
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('background/*/bg26_*/model_3d'));out=folder/'r04';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
source=WORLD/'background/map_3d/environment_sources/blender_human_base_meshes/realistic_skull.blend'
bpy.ops.wm.open_mainfile(filepath=str(folder/'r03/authoring.blend'));coll=bpy.data.collections['ASSET_bg26'];body=max((o for o in coll.objects if o.type=='MESH'),key=lambda o:len(o.data.polygons));me=body.data
vs=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',vs);vs=vs.reshape(-1,3);vi=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',vi);co=vs[vi.reshape(-1,3)].mean(1)
labels=np.empty(len(me.polygons),np.int32);me.polygons.foreach_get('material_index',labels)
idx={m.name:i for i,m in enumerate(me.materials)};metal=idx['Tower_hammered_purple_grey_metal'];bone=idx['Tower_weathered_ivory_bone'];crystal=idx['Tower_internal_luminous_fluorite']
z=co[:,2];r=np.linalg.norm(co[:,:2],axis=1);labels[(z>7.5)&(z<8.5)&(labels==bone)]=metal
labels[(z>8.5)&(r>1.65)&(labels!=crystal)]=bone;me.polygons.foreach_set('material_index',labels)
# Collapse the old fused skull relief inside a new closed support band. This
# leaves a closed interior and avoids loose triangles around the new skulls.
r=np.linalg.norm(vs[:,:2],axis=1);mask=(vs[:,2]>6.8)&(vs[:,2]<7.85)&(r>3.15);vs[mask,:2]*=(3.15/r[mask])[:,None];me.vertices.foreach_set('co',vs.ravel());me.update()
if me.has_custom_normals:me.normals_split_custom_set([(0,0,0)]*len(me.loops))
for o in list(coll.objects):
 if o.name.startswith('Recessed_copper_stair_tread'):bpy.data.objects.remove(o,do_unlink=True)
def relocate(o):
 for c in list(o.users_collection):c.objects.unlink(o)
 coll.objects.link(o);return o
bandmat=surface('Skull_ring_blackened_bronze',(.022,.017,.019),(.10,.072,.06),12,.52,.006);bandmat.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=.75
bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=3.57,depth=1.05,location=(0,0,7.325));band=relocate(bpy.context.object);band.name='Closed_skull_support_band';band.data.materials.append(bandmat)
bevel=band.modifiers.new('Cast_band_edges','BEVEL');bevel.width=.04;bevel.segments=3
for zz in [6.80,7.85]:
 bpy.ops.mesh.primitive_torus_add(major_radius=3.60,minor_radius=.075,major_segments=96,minor_segments=10,location=(0,0,zz));o=relocate(bpy.context.object);o.name='Skull_ring_bronze_rim';o.data.materials.append(bandmat)
with bpy.data.libraries.load(str(source),link=False) as (src,dst):dst.objects=['Skull - Realistic']
skull=dst.objects[0];coll.objects.link(skull);skull.location=(0,0,0);skull.rotation_euler=(0,0,0)
for modifier in skull.modifiers:
 if modifier.type=='MULTIRES':modifier.levels=min(2,modifier.total_levels);modifier.render_levels=min(2,modifier.total_levels)
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();detailed=bpy.data.meshes.new_from_object(skull.evaluated_get(deps),depsgraph=deps)
bpy.data.objects.remove(skull,do_unlink=True)
v=np.empty(len(detailed.vertices)*3,np.float32);detailed.vertices.foreach_get('co',v);v=v.reshape(-1,3);lo=v.min(0);hi=v.max(0);v-=((lo+hi)/2);v*=.78/(hi[2]-lo[2]);detailed.vertices.foreach_set('co',v.ravel());detailed.materials.clear()
ivory=surface('Scanned_skull_aged_ivory',(.25,.21,.14),(.67,.60,.44),55,.78,.0007);bs=ivory.node_tree.nodes.get('Principled BSDF');bs.inputs['Subsurface Weight'].default_value=.025
nt=ivory.node_tree;bs=nt.nodes.get('Principled BSDF');src=bs.inputs['Base Color'].links[0].from_socket;ao=nt.nodes.new('ShaderNodeAmbientOcclusion');ao.inputs['Distance'].default_value=.045;mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.65;nt.links.new(src,mix.inputs[1]);nt.links.new(ao.outputs['Color'],mix.inputs[2]);nt.links.new(mix.outputs[0],bs.inputs['Base Color']);detailed.materials.append(ivory)
for p in detailed.polygons:p.use_smooth=True
rng=random.Random(2604);count=0
for bay in range(8):
 for offset in [8,18,28,38]:
  angle=math.radians(bay*45+offset);o=bpy.data.objects.new('Scanned_skull_%02d'%count,detailed);coll.objects.link(o);o.location=(3.74*math.cos(angle),3.74*math.sin(angle),7.35+rng.uniform(-.035,.035));o.rotation_euler=(rng.uniform(-.03,.03),rng.uniform(-.05,.05),angle+math.pi/2);o.scale=(rng.uniform(.94,1.02),)*3;count+=1
# Preserve dark transparent fluorite instead of a uniformly luminous mint core.
nt=me.materials[crystal].node_tree;bs=nt.nodes.get('Principled BSDF')
for link in list(bs.inputs['Base Color'].links):nt.links.remove(link)
bs.inputs['Base Color'].default_value=(.008,.065,.021,1);bs.inputs['Transmission Weight'].default_value=.8;bs.inputs['Roughness'].default_value=.14;bs.inputs['IOR'].default_value=1.434
tc=nt.nodes.new('ShaderNodeTexCoord');sep=nt.nodes.new('ShaderNodeSeparateXYZ');nt.links.new(tc.outputs['Object'],sep.inputs[0]);fade=nt.nodes.new('ShaderNodeMapRange');fade.inputs['From Min'].default_value=7;fade.inputs['From Max'].default_value=12;fade.inputs['To Min'].default_value=1.8;fade.inputs['To Max'].default_value=.03;nt.links.new(sep.outputs['Z'],fade.inputs[0]);nt.links.new(fade.outputs[0],bs.inputs['Emission Strength'])
scene=bpy.context.scene;scene.cycles.samples=32;scene.render.filepath=str(out/'tower_preview.png');bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'revision':'r04','source':'r03 plus verified official Blender CC0 Skull - Realistic','status':'author_preview_pending','changes':['32 separate scan-derived skulls with real orbital, nasal and tooth geometry','Closed metal band hides the old fused relief','Upper metal collars restored; only actual upper ribs use ivory','Misaligned replacement treads removed','Dark green fluorite with lower internal light gradient'],'skull_mesh_faces':len(detailed.polygons),'skull_instances':count,'source_sha256':'1e0bad1693cc1824be5efc2351a71105ff388af80f356e5bd48a0c9e4d83ec99','remaining':['Skull orientation, band junctions and full-view material boundaries need inspection']},indent=2),encoding='utf-8');bpy.ops.render.render(write_still=True)
