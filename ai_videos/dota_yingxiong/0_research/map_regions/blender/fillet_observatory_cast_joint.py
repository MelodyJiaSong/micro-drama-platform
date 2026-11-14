"""Restore a smooth hook arc, locally fillet its socket, and warm limestone reflectance."""
from pathlib import Path
import bpy,json,sys
from mathutils import Vector
from mathutils.geometry import closest_point_on_tri
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r38';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r37/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];hook=bpy.data.objects['Continuous_round_hook_and_cradle_return'];mesh_name=hook.data.name
with bpy.data.libraries.load(str(folder/'r36/authoring.blend'),link=False) as (src,dst):
 assert mesh_name in src.meshes,mesh_name
 dst.meshes=[mesh_name]
hook.data=dst.meshes[0]
for v in hook.data.vertices:
 t=max(0,min(1,(v.co.z-4.75)/.40));v.co.z+=.19*t*t*(3-2*t)
hook.data.update();vg=hook.vertex_groups.new(name='Local_cast_socket_fillet');centre=Vector((1.20,1.02,4.61))
for v in hook.data.vertices:
 t=max(0,min(1,(.25-(v.co-centre).length)/.10))
 if t:vg.add([v.index],t*t*(3-2*t),'REPLACE')
bpy.ops.object.select_all(action='DESELECT');hook.select_set(True);bpy.context.view_layer.objects.active=hook;mod=hook.modifiers.new('Local_two_centimetre_cast_fillet','SMOOTH');mod.vertex_group=vg.name;mod.factor=.65;mod.iterations=60;bpy.ops.object.modifier_apply(modifier=mod.name)
for name in ['Weathered_white_limestone','Limestone_capstones']:
 mat=bpy.data.materials.get(name)
 if not mat:continue
 nt=mat.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');source=bs.inputs['Base Color'].links[0].from_socket;mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(1.20,1.08,.82,1);nt.links.new(source,mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
bpy.context.view_layer.update();ball=max((o for o in coll.objects if not o.hide_render and o.name.startswith('Reference_mirror_sphere')),key=lambda o:o.matrix_world.translation.z);center=ball.matrix_world.translation;radius=max((ball.matrix_world@v.co-center).length for v in ball.data.vertices);hook.data.calc_loop_triangles();points=[hook.matrix_world@v.co for v in hook.data.vertices];gap=min((closest_point_on_tri(center,*[points[i] for i in tri.vertices])-center).length-radius for tri in hook.data.loop_triangles);terminal=bpy.data.objects['Question_hook_terminal_ball'];capradius=max((terminal.matrix_world@v.co-terminal.matrix_world.translation).length for v in terminal.data.vertices);capgap=(terminal.matrix_world.translation-center).length-radius-capradius;assert min(gap,capgap)>0,(gap,capgap)
report=json.loads((folder/'r37/authoring.json').read_text());report.update(revision='r38',source='r37 with r36 undeformed hook mesh',hook_refinement='Uniform upper arc elevation with broad transition; source cap and terminal stay aligned; localized socket relaxation',hook_clearance_m={'entire_casting_to_sphere':gap,'terminal_to_sphere':capgap},limestone_reflectance_multiplier=[1.20,1.08,.82],remaining=['Joint appearance under close-up light','Root-soil naturalness','Independent review'])
scene=bpy.context.scene;scene['production_status']='CAST_JOINT_AND_STONE_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SAVED',json.dumps(report),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('hook_side_detail',(8,1.0,4.55),(1.1,1.0,4.45),1.5),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
