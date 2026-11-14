"""Replace the visible central knot with a shallow bark fill and close the head cavity."""
from pathlib import Path
import bpy,json,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m1_Treant/model_3d'));out=folder/'r21';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r20/authoring.blend'));coll=bpy.data.collections['ASSET_m1'];body=max((o for o in coll.objects if o.type=='MESH'),key=lambda o:len(o.data.polygons));knot=next(o for o in coll.objects if o.name.startswith('Wood_inside_spurious'));eyes=[o for o in coll.objects if o.name.startswith('Recessed_eye_dark_wood')]
knot.location.y=sum(o.location.y for o in eyes)/len(eyes)-.037*body.scale.y;knot.scale.y=.003
# Recessed core is behind the front bark and below the leaf canopy, not a visible cap.
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4,radius=1,location=(0,.012,1.36));core=bpy.context.object;core.name='Recessed_bark_core_inside_head';core.scale=(.084,.075,.17)
for c in list(core.users_collection):c.objects.unlink(core)
coll.objects.link(core);core.data.materials.append(body.data.materials[0])
for p in core.data.polygons:p.use_smooth=True
scene=bpy.context.scene;scene.cycles.samples=64;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.camera.location=(0,-6,1.25);scene.camera.data.ortho_scale=2.25;look_at(scene.camera,(0,0,.95));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m1','revision':'r21','source':'r20','status':'author_preview_not_accepted','changes':['Shallow flush bark patch at false centre hole','Recessed textured core within open head fork'],'remaining':['Head patch visibility','Branch transitions','Independent review']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.data.ortho_scale=.9;scene.camera.location=(.4,-3,1.9);look_at(scene.camera,(0,0,1.55));scene.render.filepath=str(out/'crown_detail.png');bpy.ops.render.render(write_still=True)
