"""Restore eight empty Boolean results with closed directly engraved stone bands."""
from pathlib import Path
import bpy,json,math,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r28';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r27/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];parent=bpy.data.objects['Asset_metre_calibration'];mat=bpy.data.materials['Grey_cyan_carved_stone']
for ob in list(coll.objects):
 if ob.name.startswith('Mitered_continuous_frieze'):ob.hide_render=True;ob.hide_viewport=True
def segment(x,z,a,b):
 dx,dz=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz)))
 return math.hypot(x-a[0]-t*dx,z-a[1]-t*dz)
def engraving(x,z):
 d=min(abs(z-2.378),abs(z-2.574))
 for center in [-.63,0,.63]:
  d=min(d,abs(math.hypot(x-center,z-2.476)-.067))
 for center in [-.315,.315]:
  p=[(center-.104,2.476),(center,2.536),(center+.104,2.476),(center,2.416),(center-.104,2.476)]
  d=min(d,*(segment(x,z,a,b) for a,b in zip(p,p[1:])))
 return .006*max(0,1-d/.0045)
reports=[]
for side in range(8):
 phi=-math.pi/2+side*math.pi/4;n=Vector((math.cos(phi),math.sin(phi),0));t=Vector((-n.y,n.x,0));nu,nv=420,64;verts=[];faces=[]
 for layer in range(2):
  for j in range(nv+1):
   z=2.35+.262*j/nv
   for i in range(nu+1):
    q=-1+2*i/nu;r=2.42 if layer==0 else 2.10;x=q*r*math.tan(math.pi/8)
    depth=engraving(x,z) if layer==0 else 0
    verts.append(tuple(n*(r-depth)+t*x+Vector((0,0,z))))
 count=(nu+1)*(nv+1)
 for j in range(nv):
  for i in range(nu):
   k=j*(nu+1)+i;f=(k,k+1,k+nu+2,k+nu+1);faces.extend([f,tuple(v+count for v in reversed(f))])
 boundary=list(range(nu+1))+[j*(nu+1)+nu for j in range(1,nv+1)]+[nv*(nu+1)+i for i in range(nu-1,-1,-1)]+[j*(nu+1) for j in range(nv-1,0,-1)]
 for a,b in zip(boundary,boundary[1:]+boundary[:1]):faces.append((b,a,a+count,b+count))
 me=bpy.data.meshes.new('Closed_engraved_frieze');me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new('Restored_closed_engraved_frieze',me);coll.objects.link(ob);ob.parent=parent;me.materials.append(mat)
 uv=me.uv_layers.new(name='Stone_metres')
 for face in me.polygons:
  for li in face.loop_indices:
   co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co.dot(t)+side*3,co.z)
 edge_counts={}
 for face in faces:
  for a,b in zip(face,face[1:]+face[:1]):key=tuple(sorted((a,b)));edge_counts[key]=edge_counts.get(key,0)+1
 assert all(v==2 for v in edge_counts.values()),'Frieze must be closed'
 assert len(me.polygons)>10000
 reports.append({'side':side,'vertices':len(verts),'faces':len(faces),'nonmanifold_edges':sum(v!=2 for v in edge_counts.values()),'z_span':[2.35,2.612]})
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.camera.location=(9,-14,7.5);scene.camera.data.ortho_scale=6.9;look_at(scene.camera,(0,0,2.5));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'bg23','revision':'r28','source':'r27','status':'author_preview_not_accepted','diagnosis':'All eight evaluated frieze meshes in r27 had zero vertices after Boolean carving','change':'Closed stone bands with directly modelled recessed circles, diamonds and borders; no Boolean cutters','geometry_checks':reports,'remaining':['Visual roof contact and carving inspection','Independent review']},indent=2),encoding='utf-8')
for name,loc,target,scale in [('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9),('frieze_detail',(0,-8,3.4),(0,-2,2.2),2.8)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
