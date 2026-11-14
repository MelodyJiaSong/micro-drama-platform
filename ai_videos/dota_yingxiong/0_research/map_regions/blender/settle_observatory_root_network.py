"""Replace upright root collars with low bark-covered growth and visible soil contact."""
from pathlib import Path
import bpy,json,sys,math,numpy as np
from mathutils import Vector,kdtree
from mathutils.geometry import closest_point_on_tri
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r37';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r36/inspection/bg23_r36.blend'));coll=bpy.data.collections['ASSET_bg23'];primary=[];paths=[]
for ob in coll.objects:
 if ob.hide_render or not ob.name.startswith('Woven_pale_primary_root'):continue
 count=len(ob.data.vertices)//14;path=[]
 for j in range(count):
  vs=[ob.data.vertices[j*14+k] for k in range(14)];centre=sum((v.co for v in vs),Vector())/14;t=j/(count-1);new=centre.copy();new.z=.105*(1-t)**2+.060*math.sin(t*math.pi)-.075*t**6;factor=.64+.16*t
  for v in vs:v.co=new+(v.co-centre)*factor
  primary.append(new);path.append(new)
 ob.data.update();paths.append(path)
tree=kdtree.KDTree(len(primary))
for i,p in enumerate(primary):tree.insert((p.x,p.y,0),i)
tree.balance();branches=0
for ob in coll.objects:
 if ob.hide_render or ob.type!='MESH' or not ob.name.startswith(('Connected_crossing_rootlet','Interwoven_circumferential_root')):continue
 count=len(ob.data.vertices)//14;origin=sum((ob.data.vertices[k].co for k in range(14)),Vector())/14;start=primary[tree.find((origin.x,origin.y,0))[1]]
 for j in range(count):
  vs=[ob.data.vertices[j*14+k] for k in range(14)];centre=sum((v.co for v in vs),Vector())/14;t=j/(count-1);new=centre.copy()
  if ob.name.startswith('Connected'):
   new.x+=(start.x-origin.x)*(1-t)**2;new.y+=(start.y-origin.y)*(1-t)**2;new.z=start.z*(1-t)+.035*math.sin(t*math.pi)-.065*t**6
  else:new.z=.045*math.sin(t*math.pi)+.012*math.sin(t*12)**2-.04*(abs(t-.5)*2)**8
  for v in vs:v.co=new+(v.co-centre)*.78
 ob.data.update();branches+=1
# Hummocks were inside the plinth after the root paths changed. Put them below
# the visible outer third, with an irregular edge that sinks below ground.
mounds=sorted((o for o in coll.objects if o.name.startswith('Small_irregular_root_soil_hummock') and not o.hide_render),key=lambda o:o.name)
for i,ob in enumerate(mounds):
 centre=sum((v.co for v in ob.data.vertices),Vector())/len(ob.data.vertices);path=paths[(i*2)%len(paths)];target=path[int(len(path)*.63)]
 for v in ob.data.vertices:
  v.co.x+=(target.x-centre.x);v.co.y+=(target.y-centre.y)
 ob.data.update()
bark=bpy.data.materials['Tileable_root_bark_actual_scale'];nt=bark.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');texture=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and n.image and '_diff_' in n.image.name)
hsv=nt.nodes.new('ShaderNodeHueSaturation');hsv.inputs['Saturation'].default_value=.28;hsv.inputs['Value'].default_value=.78;nt.links.new(texture.outputs['Color'],hsv.inputs['Color']);nt.links.new(hsv.outputs[0],bs.inputs['Base Color']);bs.inputs['Specular IOR Level'].default_value=.12
for n in nt.nodes:
 if n.type=='BUMP':n.inputs['Distance'].default_value=.007;n.inputs['Strength'].default_value=.85
hook=bpy.data.objects['Continuous_round_hook_and_cradle_return'];terminal=bpy.data.objects['Question_hook_terminal_ball'];tip=terminal.location.copy();delta=Vector((0,0,.19))
for v in hook.data.vertices:
 d=(v.co-tip).length;t=max(0,1-d/.42);v.co+=delta*t*t*(3-2*t)
hook.data.update();terminal.location+=delta
bpy.context.view_layer.update();ball=max((o for o in coll.objects if not o.hide_render and o.name.startswith('Reference_mirror_sphere')),key=lambda o:o.matrix_world.translation.z);center=ball.matrix_world.translation;radius=max((ball.matrix_world@v.co-center).length for v in ball.data.vertices)
hook.data.calc_loop_triangles();world=[hook.matrix_world@v.co for v in hook.data.vertices];gap=min((closest_point_on_tri(center,*[world[i] for i in tri.vertices])-center).length-radius for tri in hook.data.loop_triangles);capradius=max((terminal.matrix_world@v.co-terminal.matrix_world.translation).length for v in terminal.data.vertices);capgap=(terminal.matrix_world.translation-center).length-radius-capradius
assert min(gap,capgap)>0,(gap,capgap)
report={'asset_id':'bg23','revision':'r37','source':'r36 inspection','status':'author_trial_pending_view','root_primary_count':len(paths),'root_branches':branches,'root_start_height_parent_m':.105,'root_section_scale':[.64,.8],'soil_hummocks_relocated':len(mounds),'bark':'Direct scanned diffuse with saturation .28 and value .78; discarded compounded ramp remaps; 7mm normal bump','hook_clearance_m':{'entire_casting_to_sphere':gap,'terminal_to_sphere':capgap},'measurement_method':'Minimum closest point over all actual hook triangles to analytic uniform sphere, minus radius; terminal measured as sphere. Positive gap does not establish good projected silhouette.','remaining':['Natural root contact and texture','Socket-to-cradle joint appearance','Full independent review']}
scene=bpy.context.scene;scene['production_status']='ROOT_GROUND_CONTACT_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SAVED',json.dumps(report),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9),('hook_side_detail',(8,1.0,4.55),(1.1,1.0,4.45),1.5)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
