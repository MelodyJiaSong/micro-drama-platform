"""Lower the rear feet without changing the crouched silhouette or claw contact."""
from pathlib import Path
import bpy,json,numpy as np,sys,hashlib
from mathutils import Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'))
a=next(a for a in json.loads((WORLD/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'))['assets'] if a['id']=='m4')
out=ROOT/a['model_directory']/'r03/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'m4_r03.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/a['model_directory']/'r02/inspection/m4_r02.blend'))
obj=next(o for o in bpy.data.collections['ASSET_m4'].objects if o.type=='MESH');mesh=obj.data;mesh.transform(obj.matrix_world);obj.matrix_world=Matrix.Identity(4)
v=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('co',v);v=v.reshape(-1,3);deltas=[]
for sign in [-1,1]:
    feet=(v[:,1]>.08)&(v[:,2]<.2)&(v[:,0]*sign>0)
    if not np.any(feet):raise RuntimeError('No rear foot found')
    delta=float(v[feet,2].min());deltas.append(delta)
    zweight=np.clip((.55-v[:,2])/.30,0,1);zweight=zweight*zweight*(3-2*zweight)
    yweight=np.clip((v[:,1]-.02)/.10,0,1);side=(v[:,0]*sign>0)
    v[:,2]-=delta*zweight*yweight*side
mesh.vertices.foreach_set('co',v.ravel());mesh.update()
scene=bpy.context.scene;scene.cycles.samples=24;camera=scene.camera
for name,x,y,z in [('perspective',1,-1,.7),('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22)]:
    camera.location=(x*3.9,y*3.9,.65+z*1.3);look_at(camera,(0,0,.65));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(out/'inspection.json').write_text(json.dumps({'asset_id':'m4','revision':'r03','status':'refined_candidate_not_reviewed','source':'m4_r02.blend','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'target_height_m':1.3,'foot_displacements_m':deltas,'views':['south.png','east.png','north.png','west.png','perspective.png']},indent=2))
