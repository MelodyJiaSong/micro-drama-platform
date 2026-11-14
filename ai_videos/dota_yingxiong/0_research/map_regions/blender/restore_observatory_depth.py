"""Spread the cast instrument in depth, expose roots and build stepped buttress bases."""
from pathlib import Path
import bpy,json,sys,math
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r22';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r21/inspection/bg23_r21.blend'));coll=bpy.data.collections['ASSET_bg23']
old_positions=[(0,0,4.49),(-1.17,-.24,4.03),(1.20,.30,4.90),(-.53,-.03,3.68),(1.58,-.12,3.82),(-.36,.24,4.01)];depth=[0,-.95,.95,.65,-.65,-1.0];sphere_moves=[]
for ob in coll.objects:
 if ob.hide_render:continue
 if ob.name.startswith(('Reference_mirror_sphere','Sphere_cast_cradle')):
  i=min(range(6),key=lambda i:(ob.location.x-old_positions[i][0])**2+(ob.location.y-old_positions[i][1])**2)
  sphere_moves.append({'name':ob.name,'old_y':ob.location.y,'new_y':depth[i]});ob.location.y=depth[i]
 elif ob.name.startswith('Wide_flat_cast_support'):
  verts=ob.data.vertices;count=len(verts)//4;end=sum((verts[(count-1)*4+k].co for k in range(4)),Vector())/4
  i=min(range(1,6),key=lambda i:(end.x-old_positions[i][0])**2+(end.y-old_positions[i][1])**2);delta=depth[i]-old_positions[i][1]
  for j in range(count):
   t=j/(count-1);shift=delta*t*t*(3-2*t)
   for k in range(4):verts[j*4+k].co.y+=shift
  ob.data.update()
 elif ob.name.startswith('High_open_question_mark_hook'):
  for v in ob.data.vertices:v.co.y+=.65
 elif ob.name.startswith('Question_hook_terminal_ball'):ob.location.y+=.65
 elif ob.name.startswith('Open_C_meridian'):
  rotation=Matrix.Rotation(math.radians(35),4,'Z');pivot=Vector((0,0,3.69))
  for v in ob.data.vertices:v.co=rotation@(v.co-pivot)+pivot
 elif ob.name.startswith('Dense_base_fern_skirt'):ob.scale*=.58
 elif ob.name.startswith('Grounded_branching_bark_root'):
  verts=ob.data.vertices;count=len(verts)//18
  for j in range(count):
   centre=sum((verts[j*18+k].co for k in range(18)),Vector())/18
   for k in range(18):
    v=verts[j*18+k];v.co=centre+(v.co-centre)*2.35;v.co.z=max(-.012,v.co.z)
  ob.data.update()
def block(name,centre,width,depth,height,mat,parent):
 vertices=[(x*width/2,y*depth/2,z*height/2) for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
 faces=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)];me=bpy.data.meshes.new(name);me.from_pydata(vertices,[],faces);ob=bpy.data.objects.new(name,me)
 coll.objects.link(ob);ob.parent=parent;ob.location=centre;ob.data.materials.append(mat)
 be=ob.modifiers.new('Worn_limestone_edges','BEVEL');be.width=.018;be.segments=3
 return ob
piers=[];shaft_groups={}
for shaft in list(coll.objects):
 if shaft.hide_render or not shaft.name.startswith('Unbroken_tapered_obelisk'):continue
 coords=[shaft.matrix_basis@v.co for v in shaft.data.vertices];lo=Vector(tuple(min(p[a] for p in coords) for a in range(3)));hi=Vector(tuple(max(p[a] for p in coords) for a in range(3)));cx,cy=(lo.x+hi.x)/2,(lo.y+hi.y)/2
 group=shaft_groups.setdefault((round(cx,3),round(cy,3)),{'shaft':shaft,'coords':[]});group['coords'].extend(coords)
for (cx,cy),group in shaft_groups.items():
 shaft=group['shaft'];coords=group['coords'];lo=Vector(tuple(min(p[a] for p in coords) for a in range(3)));hi=Vector(tuple(max(p[a] for p in coords) for a in range(3)));width=max(hi.x-lo.x,hi.y-lo.y);mat=shaft.data.materials[0]
 for j,(w,z,h) in enumerate([(width+.40,.095,.19),(width+.25,.25,.12),(width+.12,.39,.16)]):block('Buttress_stepped_footing_'+str(j),(cx,cy,z),w,w,h,mat,shaft.parent)
 mid=lo.z+(hi.z-lo.z)*.45
 for j,(w,z,h) in enumerate([(width+.10,mid-.045,.09),(width+.16,mid+.015,.035)]):block('Buttress_midshaft_stringcourse_'+str(j),(cx,cy,z),w,w,h,mat,shaft.parent)
 piers.append({'shaft':shaft.name,'centre':[cx,cy],'shaft_width':width,'footing_width':width+.40,'stringcourse_height':mid})
assert len(piers)==4,piers
scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=48;scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'bg23','revision':'r22','source':'r21','status':'author_preview_not_accepted','sphere_and_cradle_moves':sphere_moves,'instrument_y_span_before_scale_m':1.95,'root_radius_multiplier':2.35,'fern_scale_multiplier':.58,'buttress_piers':piers,'remaining':['Author side-view and contact checks','Independent multi-angle review','Nonblocking material refinements']},indent=2),encoding='utf-8')
for name,pos in [('perspective_preview',(9,-14,7.5)),('east_preview',(12,0,3.0))]:
 scene.camera.location=pos;scene.camera.data.ortho_scale=6.7;look_at(scene.camera,(0,0,2.4));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
