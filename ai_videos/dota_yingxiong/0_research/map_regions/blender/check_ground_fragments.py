"""Identify tiny disconnected debris below the principal connected body."""
import bpy,bmesh,numpy as np

def inspect_and_remove(obj,remove=False):
 bm=bmesh.new();bm.from_mesh(obj.data);original_vertex_count=len(bm.verts)
 # glTF UV seams duplicate positions. They are not disconnected physical debris.
 # Weld a copy at one micrometre before analysing connected components.
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001)
 welded_vertex_count=len(bm.verts);bm.verts.ensure_lookup_table();bm.verts.index_update()
 labels=np.full(len(bm.verts),-1,np.int32);components=[]
 for v in bm.verts:
  if labels[v.index]>=0:continue
  idx=len(components);stack=[v];labels[v.index]=idx;members=[]
  while stack:
   current=stack.pop();members.append(current.index)
   for edge in current.link_edges:
    other=edge.other_vert(current)
    if labels[other.index]<0:labels[other.index]=idx;stack.append(other)
  components.append(members)
 areas=np.zeros(len(components));counts=np.zeros(len(components),np.int32)
 for f in bm.faces:
  idx=labels[f.verts[0].index];areas[idx]+=f.calc_area();counts[idx]+=1
 principal=int(areas.argmax());total=float(areas.sum());world=obj.matrix_world
 body_bottom=min((world@bm.verts[i].co).z for i in components[principal]);all_bottom=min((world@v.co).z for v in bm.verts);candidates=[];deleted=[]
 for idx,verts in enumerate(components):
  if idx==principal or areas[idx]>=total*.005:continue
  zs=[(world@bm.verts[i].co).z for i in verts]
  if max(zs)<body_bottom-1e-6:
   candidates.append({'component':idx,'faces':int(counts[idx]),'area_fraction':float(areas[idx]/total),'min_z':min(zs),'max_z':max(zs)});deleted.extend(bm.verts[i] for i in verts)
 result={'object':obj.name,'component_count':len(components),'principal_area_fraction':float(areas[principal]/total),'original_min_z':all_bottom,'principal_min_z':body_bottom,'below_body_fragments':candidates,'removed':False,'geometry_weld_applied':False,'coincident_vertices_merged_in_analysis':original_vertex_count-welded_vertex_count,'analysis_weld_distance_local':.000001}
 if remove and deleted and areas[principal]/total>.95:
  bmesh.ops.delete(bm,geom=deleted,context='VERTS');bm.to_mesh(obj.data);obj.data.update();result['removed']=True;result['geometry_weld_applied']=True
  if obj.data.has_custom_normals:obj.data.normals_split_custom_set([(0,0,0)]*len(obj.data.loops))
 bm.free();return result

if __name__=='__main__':
 from pathlib import Path
 import json,sys,argparse
 parser=argparse.ArgumentParser();parser.add_argument('--asset',default='m5');parser.add_argument('--revision',required=True);args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
 ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));manifest=json.loads((WORLD/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'));asset=next(a for a in manifest['assets'] if a['id']==args.asset);folder=ROOT/asset['model_directory'];out=folder/args.revision;out.mkdir(exist_ok=True)
 if (out/'authoring.blend').exists():raise FileExistsError(out)
 bpy.ops.wm.open_mainfile(filepath=str(folder/'r01/inspection'/f'{args.asset}_r01.blend'));coll=bpy.data.collections['ASSET_'+args.asset];reports=[inspect_and_remove(o,True) for o in coll.objects if o.type=='MESH']
 low=min((o.matrix_world@v.co).z for o in coll.objects if o.type=='MESH' for v in o.data.vertices)
 for ob in coll.objects:
  if ob.parent is None:ob.location.z-=low
 scene=bpy.context.scene;scene.cycles.samples=32;scene.render.resolution_x=900;scene.render.resolution_y=900;scene['production_status']='GROUNDING_REPAIR_AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
 (out/'authoring.json').write_text(json.dumps({'asset_id':args.asset,'revision':args.revision,'source':'r01','status':'author_preview_not_accepted','component_audit':reports,'vertical_shift_m':-low,'remaining':['Feet vs staff contact needs visual review','Original geometry and material QC failures remain']},indent=2),encoding='utf-8')
 scene.render.filepath=str(out/'grounding_preview.png');bpy.ops.render.render(write_still=True)
