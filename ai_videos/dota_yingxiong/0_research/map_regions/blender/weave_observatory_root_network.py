"""Replace pointed radial roots with continuous pale, branching ground-hugging roots."""
from pathlib import Path
import bpy,json,sys,math,random
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r24';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r23/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];parent=bpy.data.objects['Asset_metre_calibration'];rng=random.Random(2324)
for ob in coll.objects:
 if ob.name.startswith('Grounded_branching_bark_root'):ob.hide_render=True;ob.hide_viewport=True
 elif ob.name.startswith('Dense_base_fern_skirt'):ob.scale*=1.25
mat=bpy.data.materials['Scanned_weathered_root_bark'].copy();mat.name='Pale_living_aerial_root_bark';nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED');color=bs.inputs['Base Color'].links[0].from_socket
gray=n.new('ShaderNodeRGBToBW');l.new(color,gray.inputs[0]);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.035;ramp.color_ramp.elements[0].color=(.065,.044,.025,1);ramp.color_ramp.elements[1].position=.65;ramp.color_ramp.elements[1].color=(.44,.33,.21,1);l.new(gray.outputs[0],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color']);bs.inputs['Specular IOR Level'].default_value=.15
root_count=0;root_endpoints=[]
def tube(points,radius,name):
 global root_count
 verts=[];faces=[];rings=14;distance=[0.0]
 for j,p in enumerate(points):
  if j:distance.append(distance[-1]+(p-points[j-1]).length)
  tangent=(points[min(j+1,len(points)-1)]-points[max(0,j-1)]).normalized();u=tangent.cross(Vector((0,0,1))).normalized();v=tangent.cross(u).normalized();t=j/(len(points)-1)
  r=radius*(.94-.52*t)*(1+.09*math.sin(t*18))
  for k in range(rings):
   a=k*math.tau/rings;rr=r*(1+.10*math.sin(a*5+j*.19));verts.append(tuple(p+rr*(math.cos(a)*u+math.sin(a)*v)))
 for j in range(len(points)-1):
  for k in range(rings):faces.append((j*rings+k,j*rings+(k+1)%rings,(j+1)*rings+(k+1)%rings,(j+1)*rings+k))
 faces.extend([tuple(range(rings-1,-1,-1)),tuple((len(points)-1)*rings+k for k in range(rings))]);me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);ob=bpy.data.objects.new(name,me);coll.objects.link(ob);ob.parent=parent;me.materials.append(mat);uv=me.uv_layers.new(name='Root_longitudinal_scan')
 for face in me.polygons:
  face.use_smooth=True
  for li in face.loop_indices:
   i=me.loops[li].vertex_index;uv.data[li].uv=(i%rings/rings,distance[i//rings]*.8)
 root_count+=1;root_endpoints.append(list(points[-1]));return ob
def wall_radius(a):return 2.39/math.cos((a+math.pi/8)%(math.pi/4)-math.pi/8)
for i in range(58):
 a=i*math.tau/58+rng.uniform(-.035,.035)
 if math.sin(a)<-.94:continue
 start=wall_radius(a)-.07;length=rng.uniform(.65,1.05);bend=rng.uniform(-.31,.31);radius=rng.uniform(.040,.073);phase=rng.random()*math.tau;points=[]
 for j in range(81):
  t=j/80;angle=a+bend*(t+.15*math.sin(t*6));r=start+length*t+.025*math.sin(t*9+phase)*math.sin(t*math.pi)
  z=.29*(1-t)**3+.045+.018*math.sin(t*8+phase)*math.sin(t*math.pi)-.115*t**7
  points.append(Vector((r*math.cos(angle),r*math.sin(angle),z)))
 tube(points,radius,'Woven_pale_primary_root')
 for idx,sign in [(25,-1),(48,1)]:
  origin=points[idx];oa=math.atan2(origin.y,origin.x);orad=math.hypot(origin.x,origin.y);turn=sign*rng.uniform(.20,.43);extension=rng.uniform(.25,.55);branch=[]
  for j in range(49):
   t=j/48;angle=oa+turn*t;r=orad+extension*t+.025*math.sin(t*8);z=origin.z*(1-t)+.045*math.sin(t*math.pi)+.012*math.sin(t*10)*math.sin(t*math.pi)-.065*t**6;branch.append(Vector((r*math.cos(angle),r*math.sin(angle),z)))
  if any(p.y<-2.25 and abs(p.x)<.76 for p in branch):continue
  tube(branch,radius*.48,'Connected_crossing_rootlet')
# Coarse circumferential roots intertwine with radial branches near the foot of each wall.
for i in range(8):
 a=i*math.pi/4;points=[]
 for j in range(101):
  t=j/100;angle=a+(t-.5)*.72;r=wall_radius(angle)+.14+.06*math.sin(t*11+i);z=.025+.065*math.sin(t*math.pi)+.022*math.sin(t*15)**2-.04*(abs(t-.5)*2)**8;points.append(Vector((r*math.cos(angle),r*math.sin(angle),z)))
 if any(p.y<-2.25 and abs(p.x)<.76 for p in points):continue
 tube(points,.045,'Interwoven_circumferential_root')
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';scene.camera.location=(9,-14,7.5);scene.camera.data.ortho_scale=6.7;look_at(scene.camera,(0,0,2.4))
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'bg23','revision':'r24','source':'r23','status':'author_preview_not_accepted','changes':['Curved pale scanned-bark roots with actual branching','Circumferential interweaving around plinth','Thick ends buried below ground instead of pointed surface spikes','Slightly increased fern skirt with door corridor excluded'],'root_objects':root_count,'terminal_z_range':[min(p[2] for p in root_endpoints),max(p[2] for p in root_endpoints)],'remaining':['Author visual inspection','Root/fern balance and ground contact','Independent review']},indent=2),encoding='utf-8');print('ROOT_NETWORK_SAVED',root_count,flush=True)
scene.render.filepath=str(out/'perspective_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.location=(6,-7,3);scene.camera.data.ortho_scale=3.8;look_at(scene.camera,(1.25,-.9,.35));scene.render.filepath=str(out/'root_detail.png');bpy.ops.render.render(write_still=True)
