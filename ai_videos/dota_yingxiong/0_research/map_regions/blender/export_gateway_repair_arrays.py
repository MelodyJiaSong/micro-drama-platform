"""Export the unchanged r07 body for an isolated connectivity repair trial."""
from pathlib import Path
import bpy, numpy as np
ROOT=Path(__file__).resolve().parents[3]
folder=next(next(ROOT.glob('2_*')).glob('characters/*/m303_*/model_3d'))
out=folder/'r08';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r07/authoring.blend'))
me=bpy.data.objects['Gateway_merchant_body'].data;me.calc_loop_triangles()
vertices=np.empty(len(me.vertices)*3,np.float64);me.vertices.foreach_get('co',vertices)
faces=np.empty(len(me.loop_triangles)*3,np.int32);me.loop_triangles.foreach_get('vertices',faces)
np.savez_compressed(out/'source_geometry.npz',vertices=vertices.reshape(-1,3),faces=faces.reshape(-1,3))
print('EXPORTED',len(me.vertices),len(me.loop_triangles),flush=True)
