"""Restore scanned leafless branch silhouettes for the blighted forest biome."""
from pathlib import Path
import bpy,bmesh,json,math
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v025.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v024.blend'))
anchors={o.name:tuple(o.location) for o in bpy.data.collections['02_Forest'].objects};changes=[]
for variant in [5,6]:
 for ob in bpy.data.collections[f'LIB_Tree_{variant}'].objects:
  if ob.type!='MESH':continue
  ob.data=ob.data.copy();me=ob.data;leaf_indices=[i for i,m in enumerate(me.materials) if m and any(t in m.name.lower() for t in ['leaf','leaves','foliage'])]
  assert leaf_indices,ob.name
  bm=bmesh.new();bm.from_mesh(me);before=len(bm.faces);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.material_index in leaf_indices],context='FACES');bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.to_mesh(me);bm.free();me.update()
  assert len(me.polygons)>10000
  changes.append({'variant':variant,'object':ob.name,'removed_leaf_faces':before-len(me.polygons),'retained_bark_and_branch_faces':len(me.polygons)})
# Existing blight flags choose most dead trees; the north-east bank also contains
# ordinary green ground tiles. Apply the same diagonal biome inference already
# used by the outer landscape, preserving the exact canonical tree anchors.
reassigned=[]
for cname in ['02_Forest','14_Distant_Landscape']:
 for i,ob in enumerate(bpy.data.collections[cname].objects):
  if ob.instance_type!='COLLECTION' or not ob.instance_collection or not ob.instance_collection.name.startswith('LIB_Tree_'):continue
  x,y=ob.location[:2];old=ob.instance_collection.name
  if x+y>40 and old in [f'LIB_Tree_{j}' for j in range(5)]:
   ob.instance_collection=bpy.data.collections[f'LIB_Tree_{5+i%3}'];reassigned.append({'name':ob.name,'from':old,'to':ob.instance_collection.name})
assert all(tuple(bpy.data.objects[name].location)==pos for name,pos in anchors.items())
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V025 CANDIDATE; leafless Dire canopy pending inspection';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(OUT/'environment_v025_report.json').write_text(json.dumps({'file':dest.name,'source':'environment_v024.blend','status':'candidate_pending_author_review','changes':changes,'biome_reassignments':reassigned,'biome_rule':'Retain original blight-selected types; also use leafless variants when x+y>40m, consistent with existing outer landscape biome. Artistic inference, not a claim of original species identity.','canonical_anchor_count':len(anchors),'canonical_anchor_positions_unchanged':True,'terrain_and_navigation_unchanged':True,'remaining':['Branch silhouette and canopy coverage','River and overview author inspection','Independent environment review']},indent=2),encoding='utf-8');print('LEAFLESS_CANOPY_SAVED',flush=True)
scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.cycles.debug_use_compact_bvh=True;scene.render.use_simplify=True;scene.cycles.texture_limit_render='2048';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1200;scene.render.resolution_y=900
for name in ['Mid_River','Map_Overview']:
 scene.camera=bpy.data.objects[name];scene.render.filepath=str(OUT/f'environment_v025_{name}.png');bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
