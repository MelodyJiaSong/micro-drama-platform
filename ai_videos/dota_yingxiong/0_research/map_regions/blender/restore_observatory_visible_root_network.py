"""Restore buried root centres and close the two measured cast-hook ends."""
from pathlib import Path
import bpy,json,sys,math,random,bmesh
from mathutils import Vector,kdtree
from mathutils.geometry import closest_point_on_tri
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r34';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r33/inspection/bg23_r33.blend'));coll=bpy.data.collections['ASSET_bg23'];parent=bpy.data.objects['Asset_metre_calibration'];rng=random.Random(2334);prior=[];primary=[]
for ob in coll.objects:
 if not ob.hide_render and ob.name.startswith(('Pier_climbing_buttress_root','Connected_pier_root_branch')):ob.hide_render=True;ob.hide_viewport=True
 if ob.hide_render or not ob.name.startswith('Woven_pale_primary_root'):continue
 count=len(ob.data.vertices)//14
 for j in range(count):
  vs=[ob.data.vertices[j*14+k] for k in range(14)];centre=sum((v.co for v in vs),Vector())/14;t=j/(count-1);prior.append(centre.z);target=.18*(1-t)**3+.065*(1-t**5)+.012*math.sin(t*11)*math.sin(t*math.pi)-.08*t**8
  for v in vs:v.co.z+=target-centre.z
  centre.z=target;primary.append(centre)
 ob.data.update()
tree=kdtree.KDTree(len(primary))
for i,p in enumerate(primary):tree.insert(Vector((p.x,p.y,0)),i)
tree.balance();restored=0
for ob in coll.objects:
 if ob.hide_render or ob.type!='MESH' or not ob.name.startswith(('Connected_crossing_rootlet','Interwoven_circumferential_root')):continue
 count=len(ob.data.vertices)//14;first=sum((ob.data.vertices[k].co for k in range(14)),Vector())/14;start=primary[tree.find(Vector((first.x,first.y,0)))[1]].z
 for j in range(count):
  vs=[ob.data.vertices[j*14+k] for k in range(14)];centre=sum((v.co for v in vs),Vector())/14;t=j/(count-1)
  target=start*(1-t)+.045*math.sin(t*math.pi)-.06*t**7 if ob.name.startswith('Connected_crossing') else .055*math.sin(t*math.pi)+.015*math.sin(t*12)**2-.035*(abs(t-.5)*2)**8
  for v in vs:v.co.z+=target-centre.z
 ob.data.update();restored+=1
feeder=0
for ob in coll.objects:
 if ob.hide_render or ob.type!='CURVE' or not ob.name.startswith('Fine_feeder_root'):continue
 for sp in ob.data.splines:
  for j,p in enumerate(sp.points):t=j/max(1,len(sp.points)-1);p.co.z=.025*(1-t*t)+.012*math.sin(t*math.pi)-.035*t**6
 feeder+=1
# Place the small terminal on the measured end of the tube, rather than retaining
# the stale end position from the older flat-band hook.
hook=bpy.data.objects['Continuous_round_hook_and_cradle_return'];end=sum((v.co for v in hook.data.vertices[-20:]),Vector())/20;terminal=bpy.data.objects['Question_hook_terminal_ball'];terminal.location=end;rr=max(v.co.length for v in terminal.data.vertices);terminal.scale=(.073/rr,)*3
socket=bpy.data.objects['Cast_round_to_flat_cradle_socket'];bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();vv=[];ff=[];inv=parent.matrix_world.inverted()
for source in [hook,socket]:
 ev=source.evaluated_get(deps);mesh=ev.to_mesh();offset=len(vv);transform=inv@source.matrix_world;vv.extend(tuple(transform@v.co) for v in mesh.vertices);ff.extend(tuple(offset+i for i in p.vertices) for p in mesh.polygons);ev.to_mesh_clear();source.hide_render=True;source.hide_viewport=True
hook.name='Archive_r33_round_hook_before_socket_union';mesh=bpy.data.meshes.new('Unified_cast_hook_socket');mesh.from_pydata(vv,[],ff);cast=bpy.data.objects.new('Continuous_round_hook_and_cradle_return',mesh);coll.objects.link(cast);cast.parent=parent;mesh.materials.append(bpy.data.materials['Cast_bronze_with_verdigris']);bpy.ops.object.select_all(action='DESELECT');cast.select_set(True);bpy.context.view_layer.objects.active=cast;remesh=cast.modifiers.new('Cast_joint_surface_union','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.003;remesh.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=remesh.name);sm=cast.modifiers.new('Cast_joint_micro_fillet','SMOOTH');sm.factor=.35;sm.iterations=3;bpy.ops.object.modifier_apply(modifier=sm.name)
bpy.context.view_layer.update();ball=max((o for o in coll.objects if not o.hide_render and o.name.startswith('Reference_mirror_sphere')),key=lambda o:o.matrix_world.translation.z);center=ball.matrix_world.translation;radius=max((ball.matrix_world@v.co-center).length for v in ball.data.vertices);cast.data.calc_loop_triangles();world=[cast.matrix_world@v.co for v in cast.data.vertices];gap=min((closest_point_on_tri(center,*[world[i] for i in tri.vertices])-center).length-radius for tri in cast.data.loop_triangles);capgap=(terminal.matrix_world.translation-center).length-radius-.073*parent.scale.x;assert min(gap,capgap)>0,(gap,capgap)
scene=bpy.context.scene;scene['production_status']='AUTHOR_TRIAL_NOT_ACCEPTED';scene.cycles.samples=48;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report=json.loads((folder/'r33/authoring.json').read_text());report.update(revision='r34',source='r33 inspection',root_centre_repair={'cause':'Earlier height warp lowered primary and cross-root centres into the ground; later corner roots were visible instead of the intended circumferential network','prior_primary_centre_z_range':[min(prior),max(prior)],'new_primary_centre_z_range':[min(p.z for p in primary),max(p.z for p in primary)],'restored_cross_roots':restored,'restored_feeders':feeder,'corner_pier_claws_hidden':True,'door_corridor_xy_preserved':True},cast_repair={'terminal_parent_position':list(end),'terminal_radius_parent_m':.073,'socket_voxel_union_resolution_parent_m':.003,'casting_sphere_clearance_m':gap,'terminal_sphere_clearance_m':capgap},remaining=['Root network visibility and continuity at ground level','Terminal and joint appearance','All earlier material refinements','Independent review']);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('ROOT_NETWORK_AND_CAST_ENDS_REPAIRED',flush=True)
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('hook_side_detail',(8,1.0,4.55),(1.1,1.0,4.45),1.5),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
