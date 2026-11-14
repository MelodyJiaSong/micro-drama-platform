"""Join the sampled remaining leather collar to the reconstructed cape shell."""
from pathlib import Path
import bpy,bmesh,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m21_Polar_Furbolg/model_3d'));out=folder/'r06';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r05/authoring.blend'));coll=bpy.data.collections['ASSET_m21'];cloth=bpy.data.objects['Reconstructed_leather_cape_shell'];body=bpy.data.objects['geometry_0'];me=body.data
bm=bmesh.new();bm.from_mesh(me);layer=bm.verts.layers.float.get('LeatherCoverage');assert layer is not None
selected=set()
for face in bm.faces:
 p=face.calc_center_median();coverage=sum(v[layer] for v in face.verts)/len(face.verts)
 if p.z>1.45 and coverage>.66 and not(abs(p.x)<.19 and p.y<-.36 and p.z<1.60):selected.add(face.index)
copy=me.copy();cb=bmesh.new();cb.from_mesh(copy);bmesh.ops.delete(cb,geom=[f for f in cb.faces if f.index not in selected],context='FACES');bmesh.ops.recalc_face_normals(cb,faces=list(cb.faces));cb.to_mesh(copy);cb.free();bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.index in selected],context='FACES');bm.to_mesh(me);bm.free()
strip=bpy.data.objects.new('Retained_lower_leather_collar',copy);coll.objects.link(strip);copy.materials.clear();copy.materials.append(cloth.data.materials[0]);bpy.ops.object.select_all(action='DESELECT');strip.select_set(True);bpy.context.view_layer.objects.active=strip
solid=strip.modifiers.new('Collar_thickness','SOLIDIFY');solid.thickness=.022;solid.offset=0;bpy.ops.object.modifier_apply(modifier=solid.name)
cloth.select_set(True);bpy.context.view_layer.objects.active=cloth;bpy.ops.object.join()
# Volumetric union closes the old horizontal seam and joins intersecting cloth sections.
mod=cloth.modifiers.new('Union_collar_and_cape','REMESH');mod.mode='VOXEL';mod.voxel_size=.008;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
bm=bmesh.new();bm.from_mesh(cloth.data);edges=[e for e in bm.edges if e.is_boundary];filled=bmesh.ops.holes_fill(bm,edges=edges,sides=40).get('faces',[]);filled_count=len(filled);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(cloth.data);bm.free()
mod=cloth.modifiers.new('Smooth_join_and_small_pits','SMOOTH');mod.factor=.65;mod.iterations=24;bpy.ops.object.modifier_apply(modifier=mod.name)
for face in cloth.data.polygons:face.use_smooth=True;face.material_index=0
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.camera.location=(6,-7,3);scene.camera.data.ortho_scale=2.9;look_at(scene.camera,(0,0,1.15));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m21','revision':'r06','source':'r05','status':'author_preview_not_accepted','evidence':'r05/cape_boundary_probe.json identifies gray strip on geometry_0 with LeatherCoverage 0.885-1.0','changes':['Extract retained collar by sampled leather coverage','Join thickened collar and upper cape with volumetric union','Close small boundary holes and soften seam'],'extracted_faces':len(selected),'filled_boundary_faces':filled_count,'remaining':['Author check of collar and fur boundary','Cape fold realism','Independent inspection']},indent=2),encoding='utf-8');print('CAPE_UNION_SAVED',flush=True)
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.location=(3,4,3.2);scene.camera.data.ortho_scale=1.5;look_at(scene.camera,(0,.1,1.8));scene.render.filepath=str(out/'roof_poles_preview.png');bpy.ops.render.render(write_still=True)
