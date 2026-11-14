from pathlib import Path
import bpy,json,numpy as np
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'))
a=next(a for a in json.loads((WORLD/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'))['assets'] if a['id']=='bg12')
bpy.ops.wm.open_mainfile(filepath=str(ROOT/a['model_directory']/'r05/inspection/bg12_r05.blend'))
ob=next(o for o in bpy.data.collections['ASSET_bg12'].objects if o.type=='MESH');v=np.empty(len(ob.data.vertices)*3,np.float32);ob.data.vertices.foreach_get('co',v);v=v.reshape(-1,3);v=v@np.array(ob.matrix_world)[:3,:3].T+np.array(ob.matrix_world)[:3,3]
print('BOUNDS',v.min(0).tolist(),v.max(0).tolist())
for side,mask in [('left',v[:,0]<0),('right',v[:,0]>0)]:
 for z in np.arange(.5,7,.5):
  pts=v[mask&(v[:,2]>=z)&(v[:,2]<z+.5)]
  if len(pts):print(side,z,len(pts),np.quantile(pts,[.05,.5,.95],axis=0).round(3).tolist())
