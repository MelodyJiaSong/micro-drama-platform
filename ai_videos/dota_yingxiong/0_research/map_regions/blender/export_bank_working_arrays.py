"""Read-only source arrays for a constrained bank sculpt trial."""
from pathlib import Path
import bpy,numpy as np,json,base64
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v026.blend'));me=bpy.data.objects['Terrain_683d'].data;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(1025,1025,3)
grid=json.loads((ROOT/'0_research/map_regions/navigation/grid.json').read_text());cells=np.frombuffer(base64.b64decode(grid['cells_base64']),np.uint8).reshape(512,512);ix=np.minimum(np.arange(1025)//2,511);codes=cells[::-1][ix[:,None],ix[None,:]]
z=co[:,:,2];gy,gx=np.gradient(z,.8);bank=(z>-9)&(z<-2)&(np.hypot(gx,gy)>.1);protected=(codes&(1|16))!=0
np.savez_compressed(OUT/'bank_working_arrays_v026.npz',co=co,codes=codes)
values,counts=np.unique(codes[bank],return_counts=True);print(json.dumps({'bank_vertices':int(bank.sum()),'protected_bank_vertices':int((bank&protected).sum()),'codes':dict(zip(map(str,values),map(int,counts)))}),flush=True)
