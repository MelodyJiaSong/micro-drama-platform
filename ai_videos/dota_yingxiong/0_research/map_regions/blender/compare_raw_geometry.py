"""Render raw and processed source geometry under identical clay and lighting."""
from pathlib import Path
import bpy,json,sys,numpy as np
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at,material
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m1_Treant/model_3d/r01'));out=folder/'diagnostics';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'inspection/m1_r01.blend'));processed=list(bpy.data.collections['ASSET_m1'].all_objects);scene=bpy.context.scene;clay=material('Raw_processed_geometry_control',(.18,.18,.18),.82)
def clay_meshes(objects):
 for ob in objects:
  if ob.type!='MESH':continue
  ob.data.materials.clear();ob.data.materials.append(clay);ob.data.polygons.foreach_set('material_index',np.zeros(len(ob.data.polygons),np.int32))
  if ob.data.has_custom_normals:ob.data.normals_split_custom_set([(0,0,0)]*len(ob.data.loops))
clay_meshes(processed);scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.resolution_x=900;scene.render.resolution_y=900;scene.camera.data.ortho_scale=.95;scene.camera.location=(.8,-3,1.9);look_at(scene.camera,(0,0,1.5));scene.render.filepath=str(out/'processed_crown_clay.png');bpy.ops.render.render(write_still=True)
for ob in processed:ob.hide_render=True
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(next(folder.glob('*_raw_*.glb'))));raw=list(set(bpy.data.objects)-before);bpy.context.view_layer.update();points=[o.matrix_world@Vector(p) for o in raw if o.type=='MESH' for p in o.bound_box];lo=Vector([min(p[i] for p in points) for i in range(3)]);hi=Vector([max(p[i] for p in points) for i in range(3)]);scale=1.9/(hi.z-lo.z);transform=Matrix.Scale(scale,4)@Matrix.Translation(-Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z)))
for ob in raw:
 if ob.parent is None:ob.matrix_world=transform@ob.matrix_world
bpy.context.view_layer.update();clay_meshes(raw);scene.render.filepath=str(out/'raw_crown_clay.png');bpy.ops.render.render(write_still=True)
(out/'raw_geometry_comparison.json').write_text(json.dumps({'status':'diagnostic_not_asset_acceptance','processed_faces':sum(len(o.data.polygons) for o in processed if o.type=='MESH'),'raw_faces':sum(len(o.data.polygons) for o in raw if o.type=='MESH'),'material':'same neutral clay','camera_and_lights':'same scene; no exposure adjustment','source':'r01 generator output; source artifacts unchanged'},indent=2),encoding='utf-8')
