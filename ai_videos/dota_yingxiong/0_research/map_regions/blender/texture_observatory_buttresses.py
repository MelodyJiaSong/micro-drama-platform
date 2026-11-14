"""Apply metre-scale stone UVs to the new buttress bases and stringcourses."""
from pathlib import Path
import bpy,json,sys,random
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r23';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r22/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];rng=random.Random(2323);changed=[]
for ob in coll.objects:
 if not ob.name.startswith(('Buttress_stepped_footing','Buttress_midshaft_stringcourse')):continue
 me=ob.data;me.update();uv=me.uv_layers.new(name='Stone_individual_metres');offset=(rng.uniform(-20,20),rng.uniform(-20,20))
 for p in me.polygons:
  axis=max(range(3),key=lambda i:abs(p.normal[i]));axes=[(1,2),(0,2),(0,1)][axis]
  for li in p.loop_indices:
   v=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]]+offset[0],v[axes[1]]+offset[1])
 me.materials.clear();me.materials.append(bpy.data.materials['Weathered_white_limestone'])
 sub=ob.modifiers.new('Fine_edge_weathering','SUBSURF');sub.subdivision_type='SIMPLE';sub.levels=2;sub.render_levels=2
 dis=ob.modifiers.new('Limestone_surface_erosion','DISPLACE');dis.texture=bpy.data.textures['Fine_limestone_erosion'];dis.texture_coords='GLOBAL';dis.strength=.008;changed.append(ob.name)
assert len(changed)==20,len(changed)
scene=bpy.context.scene;scene.cycles.samples=48;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
report=json.loads((folder/'r22/authoring.json').read_text());report.update(revision='r23',source='r22',status='author_preview_not_accepted',stone_uvs_and_weathering_added=changed);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
for name,pos in [('perspective_preview',(9,-14,7.5)),('east_preview',(12,0,3.0))]:
 scene.camera.location=pos;scene.camera.data.ortho_scale=6.7;look_at(scene.camera,(0,0,2.4));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
