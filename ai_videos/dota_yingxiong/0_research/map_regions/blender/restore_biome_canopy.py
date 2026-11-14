"""Restore blighted canopy coverage and remove camera-dependent grass colour bands."""
from pathlib import Path
import bpy,bmesh,json,numpy as np,random,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';SRC=OUT/'environment_sources'
dest=OUT/'environment_v018.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v017.blend'))
anchors={o.name:tuple(o.location) for o in bpy.data.collections['02_Forest'].objects}
with bpy.data.libraries.load(str(next((SRC/'tree_small_02').glob('*.blend'))),link=False) as (src,dst):dst.objects=['tree_small_02_LOD1']
source=dst.objects[0];source.location=(0,0,0);source.hide_render=False;source.hide_viewport=False;source.data=source.data.copy()
materials=[]
for index,original in enumerate(list(source.data.materials)):
 mat=original.copy();mat.name='Blighted_canopy_'+original.name;source.data.materials[index]=mat
 if not mat.use_nodes:continue
 nt=mat.node_tree;bs=next((q for q in nt.nodes if q.type=='BSDF_PRINCIPLED'),None)
 if bs is None:continue
 tint=(.17,.12,.18,1) if 'leav' in original.name.lower() else (.38,.32,.29,1)
 old=bs.inputs['Base Color'].links[0].from_socket if bs.inputs['Base Color'].is_linked else None
 mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=tint
 if old:nt.links.new(old,mix.inputs[1])
 else:mix.inputs[1].default_value=bs.inputs['Base Color'].default_value
 nt.links.new(mix.outputs[0],bs.inputs['Base Color']);bs.inputs['Specular IOR Level'].default_value=.22
 materials.append(mat.name)
source_height=max(v.co.z for v in source.data.vertices)-min(v.co.z for v in source.data.vertices)
for variant in [5,6]:
 c=bpy.data.collections[f'LIB_Tree_{variant}'];old=list(c.objects);o=source.copy();c.objects.link(o);scale=(11.5+(variant-5)*1.2)/source_height;o.scale=(scale*(.8 if variant==6 else 1),scale,scale)
 for ob in old:c.objects.unlink(ob)
nt=bpy.data.materials['Continuous_ground'].node_tree
for node in nt.nodes:
 if node.type!='MIX_RGB' or node.blend_type!='MULTIPLY' or not node.inputs[1].is_linked:continue
 tex=node.inputs[1].links[0].from_node
 if tex.type=='TEX_IMAGE' and tex.image and tex.image.name=='grass_ground_diff_2k.jpg':
  for link in list(node.inputs[2].links):nt.links.remove(link)
  node.inputs[2].default_value=(.14,.32,.055,1)
# Ground coverage is a spatial property, never a function of camera distance.
outer=bpy.data.objects['Continuous_outer_land'].data
coords=np.empty(len(outer.vertices)*3,np.float32);outer.vertices.foreach_get('co',coords);coords=coords.reshape(-1,3)
blight=np.clip((coords[:,0]+coords[:,1]+80)/160,0,1).astype(np.float32)
for name,value in [('Grass',np.ones(len(coords),np.float32)),('ForestFloor',np.full(len(coords),.08,np.float32)),('Blight',blight)]:outer.attributes[name].data.foreach_set('value',value)
bm=bmesh.new();bm.from_mesh(outer)
normal_flip=float(np.median([f.normal.z for f in bm.faces]))<0
if normal_flip:bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(outer)
outer_tree=BVHTree.FromBMesh(bm);bm.free();outer.update()
# Outside-map trees inherit their biome and grow in patches rather than even spacing.
rng=random.Random(29118);outside=bpy.data.collections['14_Distant_Landscape'];existing=[o for o in outside.objects if o.instance_type=='COLLECTION'];added=0
for ob in existing:
 px,py=ob.location[:2]
 if px+py>40:ob.instance_collection=bpy.data.collections[f'LIB_Tree_{5+added%2}']
 patch=.5+.3*math.sin(px*.031+py*.012)*math.cos(py*.027)+.2*math.sin(px*.077-py*.041)
 if patch<.32:ob.hide_render=True;continue
 for _ in range(2 if patch>.60 else 1):
  new=ob.copy();outside.objects.link(new);new.name='Distant_forest_cluster';dx,dy=rng.uniform(-8,8),rng.uniform(-8,8);px2,py2=px+dx,py+dy
  if max(abs(px2),abs(py2))<420:outside.objects.unlink(new);continue
  new.location.x=px2;new.location.y=py2
  # Raycast the actual outer mesh instead of guessing a height from the old analytic surface.
  loc,normal,face,distance=outer_tree.ray_cast(Vector((px2,py2,100)),Vector((0,0,-1)))
  if loc is not None:new.location.z=loc.z
  new.rotation_euler.z=rng.uniform(0,math.tau);new.scale*=rng.uniform(.75,1.15);added+=1
assert all(tuple(bpy.data.objects[name].location)==pos for name,pos in anchors.items())
for image in bpy.data.images:
 if image.source!='FILE' or image.packed_file:continue
 matches=list(SRC.glob('*/textures/'+Path(image.filepath.replace('\\','/')).name))
 if matches:image.filepath=str(matches[0]);image.reload()
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V018 CANDIDATE; biome canopy and ground coverage pending review'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
report={'file':dest.name,'source':'environment_v017.blend','status':'candidate_pending_visual_review','canonical_tree_anchors_unchanged':len(anchors),'terrain_geometry_changed':False,'outer_normals_flipped':normal_flip,'outside_cluster_trees_added':added,'blighted_tree_variants':[5,6],'new_materials':materials,'grass_colour_camera_dependent':False,'remaining':['independent environment review','protected tree footprint review with new canopies']}
(OUT/'environment_v018_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=48;scene.cycles.use_denoising=True;scene.render.resolution_x=1200;scene.render.resolution_y=900
for name in ['Map_Overview','Scourge_Base','Sentinel_Merchant_Ground_Eye']:
 scene.camera=bpy.data.objects[name];scene.render.filepath=str(OUT/f'environment_v018_{name}.png');bpy.ops.render.render(write_still=True)
