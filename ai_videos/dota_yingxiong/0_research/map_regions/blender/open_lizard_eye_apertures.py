"""Correct the independently reported unreadable eyes, preserving the body detail."""
from pathlib import Path
import bpy,json,sys,math,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
from transfer_uv_in_chunks import transfer_uv
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m26_*/model_3d'));out=folder/'r14';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r13/authoring.blend'));body=bpy.data.objects['Closed_lizard_surface_3mm'];source=bpy.data.objects['Archive_r07_lizard_before_closed_surface'];report=json.loads((folder/'r13/authoring.json').read_text());co=np.empty(len(body.data.vertices)*3,np.float32);body.data.vertices.foreach_get('co',co);co=co.reshape(-1,3);changes=[]
for row in report['eyes']:
 side=row['side'];p=Vector(row['surface']);oldcenter=Vector(row['centre']);normal=Vector(row['normal']);u=(Vector((1,0,0))-normal*normal.x).normalized();v=normal.cross(u)
 if v.z<0:v=-v
 radius=.038;center=oldcenter+normal*.006;factor=radius/row['radius_m'];eye=bpy.data.objects[f'Reptile_eye_{side}'];eye.location=center;eye.scale*=factor
 for name in ['Iris','Pupil']:
  ob=bpy.data.objects[f'Reptile_{name}_{side}']
  for vertex in ob.data.vertices:vertex.co=center+(vertex.co-oldcenter)*factor
  ob.data.update()
 delta=co-np.array(p);du=delta@np.array(u);dv=delta@np.array(v);depth=delta@np.array(normal);d=np.sqrt((du/.036)**2+(dv/.024)**2);t=np.clip((1.12-d)/.30,0,1);weight=t*t*(3-2*t)*(np.abs(depth)<.08);shift=np.maximum(0,depth+.047)*weight;co-=np.array(normal)[None,:]*shift[:,None]
 lid=bpy.data.objects[f'Reptile_lid_rim_{side}']
 for ring in range(5):
  t=ring/4
  for k in range(96):
   a=math.tau*k/96;dx=.030*math.cos(a);dz=.018*math.sin(a);inner=center+u*dx+v*dz+normal*(math.sqrt(max(0,radius*radius-dx*dx-dz*dz))+.0005);edge=p+u*(.048*math.cos(a))+v*(.034*math.sin(a));hit,q,nn,face=body.ray_cast(edge+normal*.12,-normal)
   if hit:edge=q-normal*.0004
   lid.data.vertices[ring*96+k].co=inner.lerp(edge,t)
 lid.data.update();uvout=out/f'lid_uv_{side}';uvout.mkdir(exist_ok=True);transfer_uv(source,lid,uvout);lid.data.materials.clear();lid.data.materials.append(body.data.materials[0]);changes.append({'side':side,'old_radius_m':row['radius_m'],'new_radius_m':radius,'centre':list(center),'iris_diameter_m':.038*factor,'lid_aperture_width_m':.060,'lid_aperture_height_m':.036,'outward_shift_m':.006})
body.data.vertices.foreach_set('co',co.ravel());body.data.update();scene=bpy.context.scene;scene['production_status']='EYE_APERTURE_AUTHOR_TRIAL_OTHER_BLOCKERS_REMAIN';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report.update(revision='r14',source='r13',status='author_trial_pending_view',eye_aperture_repair=changes,remaining=['Eye integration and readable vertical pupil','Pitted back and keratin silhouettes','Small wires/fragments','Texture clarity and repaired cavity seams','Independent review']);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('EYE_APERTURES_SAVED',json.dumps(changes),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('head_detail',(5,-3,2.4),(1.65,0,1.05),1.9),('head_side',(1.85,-5,1.1),(1.85,0,1.1),1.5),('author_preview',(6,-8,4.3),(0,0,1.2),5.8)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
