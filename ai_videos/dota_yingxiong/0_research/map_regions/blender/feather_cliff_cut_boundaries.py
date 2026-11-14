"""Blend the navigation-clipped rock boundaries into terrain over a metre-wide collar."""
from pathlib import Path
import bpy,json,numpy as np,sys
from mathutils import Vector,kdtree
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v041.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v040.blend'));z=np.load(OUT/'cliff_embedding_fields.npz')['z']
def sample(xy):
 u,v=np.clip(((xy+409.6)/.8).T,0,1024);i,j=np.minimum(u.astype(int),1023),np.minimum(v.astype(int),1023);a,b=u-i,v-j
 return z[j,i]*(1-a)*(1-b)+z[j,i+1]*a*(1-b)+z[j+1,i]*(1-a)*b+z[j+1,i+1]*a*b
rows=[]
for ob in bpy.data.collections['19_Embedded_scan_cliff_trial'].objects:
 if ob.hide_render:continue
 me=ob.data;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3);ids=np.empty(len(me.polygons)*3,np.int32);me.polygons.foreach_get('vertices',ids);faces=ids.reshape(-1,3);edges=np.concatenate([faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]]]);edges.sort(1);unique,count=np.unique(edges,axis=0,return_counts=True);boundary=np.unique(unique[count==1]);tree=kdtree.KDTree(len(boundary))
 for j,index in enumerate(boundary):tree.insert(Vector((float(co[index,0]),float(co[index,1]),0)),j)
 tree.balance();distance=np.array([tree.find(Vector((float(p[0]),float(p[1]),0)))[2] for p in co]);t=np.clip(distance/1.20,0,1);weight=t*t*(3-2*t);ground=sample(co[:,:2]);before=co[:,2].copy();co[:,2]=ground+(co[:,2]-ground)*weight-.04*(1-weight);me.vertices.foreach_set('co',co.ravel());me.update();rows.append({'object':ob.name,'blended_vertices':int((weight<1).sum()),'max_lowering_m':float(np.max(before-co[:,2]))})
scene=bpy.context.scene;scene['production_status']='LOCAL_CLIFF_EDGE_BLEND_AUTHOR_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));(OUT/'environment_v041_report.json').write_text(json.dumps({'file':dest.name,'source':'environment_v040.blend','status':'local_author_trial_pending_view','method':'1.2m smoothstep distance from all cut boundaries; bring raised scan down to terrain, with outermost 4cm burial. XY and triangle topology unchanged, preserving v040 conservative path exclusion.','patches':rows,'remaining':['Stretched edge texture','Cut profile appearance','Still only local coverage']},indent=2),encoding='utf-8')
scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.render.threads_mode='FIXED';scene.render.threads=6;scene.render.resolution_x=1200;scene.render.resolution_y=900;scene.render.use_simplify=True;scene.cycles.texture_limit_render='2048';scene.render.use_border=False
close=json.loads((OUT/'environment_v038_close_cameras.json').read_text())[0];camera=bpy.data.objects['River_Eye_Level'];scene.camera=camera;camera.location=close['camera'];look_at(camera,Vector(close['target']));camera.data.type='PERSP';camera.data.lens=42;scene.render.filepath=str(OUT/'environment_v041_Rock_River_Close.png');bpy.ops.render.render(write_still=True)
