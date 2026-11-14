"""Restore warm, volumetric rootwork and a continuously rounded spatial hook."""
from pathlib import Path
import bpy,json,sys,math,random
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r31';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r30/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];parent=bpy.data.objects['Asset_metre_calibration'];bronze=bpy.data.materials['Cast_bronze_with_verdigris'];bark=bpy.data.materials['Tileable_root_bark_actual_scale'];rng=random.Random(2331)
def tube(name,points,radii,mat,sides=16):
 verts=[];faces=[];length=[0]
 for j,p in enumerate(points):
  if j:length.append(length[-1]+(p-points[j-1]).length)
  tangent=(points[min(j+1,len(points)-1)]-points[max(j-1,0)]).normalized();u=tangent.cross(Vector((0,0,1)))
  if u.length<.01:u=tangent.cross(Vector((0,1,0)))
  u.normalize();v=tangent.cross(u).normalized()
  for k in range(sides):a=k*math.tau/sides;verts.append(tuple(p+radii[j]*(u*math.cos(a)+v*math.sin(a))))
 for j in range(len(points)-1):
  for k in range(sides):faces.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
 faces.extend([tuple(range(sides-1,-1,-1)),tuple((len(points)-1)*sides+k for k in range(sides))]);me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);ob=bpy.data.objects.new(name,me);coll.objects.link(ob);ob.parent=parent;me.materials.append(mat);uv=me.uv_layers.new(name='Longitudinal_surface')
 for face in me.polygons:
  face.use_smooth=True
  for li in face.loop_indices:i=me.loops[li].vertex_index;uv.data[li].uv=(i%sides/sides,length[i//sides]*.8)
 return ob
for node in bark.node_tree.nodes:
 if node.type=='VALTORGB' and abs(node.color_ramp.elements[1].position-.45)<.001:
  node.color_ramp.elements[0].color=(.038,.027,.016,1);node.color_ramp.elements[1].color=(.24,.17,.105,1)
for ob in coll.objects:
 if not ob.hide_render and ob.name.startswith('Woven_pale_primary_root'):
  for j in range(len(ob.data.vertices)//14):
   vs=[ob.data.vertices[j*14+k] for k in range(14)];c=sum((v.co for v in vs),Vector())/14
   for v in vs:v.co=c+(v.co-c)*1.32
  ob.data.update()
# Larger roots originate against stone corner piers, then branch into the
# existing ground web. They avoid the door axis and the crystal alcove centres.
newroots=0
for i in range(4):
 a=math.pi/4+i*math.pi/2
 for side in [-1,1]:
  phase=rng.random()*math.tau;points=[];radii=[]
  for j in range(81):
   t=j/80;angle=a+side*(.055+.13*t)+.035*math.sin(t*7+phase)*math.sin(t*math.pi);r=2.55+.95*t;zz=.55*(1-t)**3+.035+.025*math.sin(t*8)*math.sin(t*math.pi)-.105*t**6;points.append(Vector((r*math.cos(angle),r*math.sin(angle),zz)));radii.append(.092*(1-t)**.70+.008)
  tube('Pier_climbing_buttress_root',points,radii,bark);newroots+=1
  origin=points[34]
  for branch in [-1,1]:
   branchpoints=[];rr=[]
   for j in range(41):
    t=j/40;p=origin+Vector((math.cos(a+branch*.65),math.sin(a+branch*.65),0))*.65*t;p.z=origin.z*(1-t)+.025*math.sin(t*math.pi)-.075*t**5;branchpoints.append(p);rr.append(.039*(1-t)**.75+.003)
   tube('Connected_pier_root_branch',branchpoints,rr,bark);newroots+=1
ferns=[o for o in coll.objects if not o.hide_render and o.name.startswith('Dense_base_fern_skirt')]
for ob in ferns:ob.scale*=1.25
added=0
for i in range(104):
 a=rng.random()*math.tau;r=2.42/math.cos((a+math.pi/8)%(math.pi/4)-math.pi/8)+rng.uniform(.13,.53);x,y=r*math.cos(a),r*math.sin(a)
 if y<-2 and abs(x)<.95:continue
 src=ferns[i%len(ferns)];ob=src.copy();ob.data=src.data;coll.objects.link(ob);ob.name='Irregular_fern_root_margin';ob.location=(x,y,-.015);ob.scale*=rng.uniform(.68,1.05);ob.rotation_euler.z=rng.uniform(0,math.tau);added+=1
# Widen a subset of ivy patches using real existing leaves, without covering
# every wall or obscuring the door. Parent-space tangent offsets follow walls.
leaves=[o for o in coll.objects if not o.hide_render and o.name.startswith('Wall_attached_ivy_leaf')]
ivyadded=0
for i,src in enumerate(leaves):
 if i%3:continue
 p=src.location;a=round(math.atan2(p.y,p.x)/(math.pi/4))*math.pi/4;tangent=Vector((-math.sin(a),math.cos(a),0));delta=rng.uniform(-.10,.10);loc=p+tangent*delta
 if loc.y<-2 and abs(loc.x)<.82:continue
 ob=src.copy();ob.data=src.data;coll.objects.link(ob);ob.name='Ivy_patch_secondary_leaf';ob.location=loc;ob.scale*=rng.uniform(.8,1.20);ivyadded+=1
hook=bpy.data.objects['High_open_question_mark_hook'];points=[sum((hook.data.vertices[j*4+k].co for k in range(4)),Vector())/4 for j in range(len(hook.data.vertices)//4)];pivot=points[0].copy();rotation=Matrix.Rotation(math.radians(35),3,'Z');points=[pivot+rotation@(p-pivot) for p in points];hook.hide_render=True;hook.hide_viewport=True;tube('Rounded_spatial_question_mark_hook',points,[.052]*len(points),bronze)
terminal=bpy.data.objects.get('Question_hook_terminal_ball')
if terminal:terminal.location=pivot+rotation@(terminal.location-pivot)
for ob in coll.objects:
 if ob.name.startswith(('Hook_to_globe_cradle_structural_bracket','Bracket_cast_attachment_lug','Bracket_visible_rivet')):ob.hide_render=True;ob.hide_viewport=True
start=Vector((1.20,.95,4.685));end=pivot;control1=start+Vector((0,0,-.20));control2=end+Vector((0,0,-.18));points=[]
for j in range(65):
 t=j/64;points.append((1-t)**3*start+3*(1-t)**2*t*control1+3*(1-t)*t*t*control2+t**3*end)
tube('Continuous_cast_hook_cradle_return',points,[.055]*len(points),bronze)
scene=bpy.context.scene;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'bg23','revision':'r31','source':'r30','status':'author_preview_not_accepted','changes':['Warmer grey-brown scanned root bark and restored primary girth','Eight corner-pier roots with joined branches and buried ends','Larger existing fern skirt plus irregular margin patches and wider ivy','Replace flat hook with round cast section rotated 35 degrees; continuously curved connection replaces rectangular bracket'],'new_root_segments':newroots,'added_ferns':added,'added_ivy_leaves':ivyadded,'hook_stem_parent':list(pivot),'remaining':['Root contact and crystal clearance','Hook silhouette and sphere clearance','Full independent review']},indent=2),encoding='utf-8');print('OBSERVATORY_R31_SAVED',flush=True)
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9),('hook_side_detail',(8,1.0,4.55),(1.1,1.0,4.45),1.5)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
