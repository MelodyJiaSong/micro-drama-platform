"""Unify the remaining yellow tooth surfaces without painting the jaw skin."""
from pathlib import Path
import bpy,json,numpy as np,sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m4_Ghoul/model_3d'));out=folder/'r14';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r13/authoring.blend'));coll=bpy.data.collections['ASSET_m4'];body=next(o for o in coll.objects if o.type=='MESH' and len(o.data.polygons)>100000);me=body.data;probe=np.load(folder/'r04/material_probe.npz');co=probe['co'];rgb=probe['colors'];x,y,z=co.T;yellow=(rgb[:,2]<rgb[:,0]*.47)&(rgb[:,0]>.25)
tooth=(((abs(x)<.09)&(y<-.40)&(z>.67)&(z<.80))|((abs(x)>.07)&(abs(x)<.115)&(y<-.36)&(z>.70)&(z<.805)))&yellow;labels=np.empty(len(me.polygons),np.int32);me.polygons.foreach_get('material_index',labels);labels[tooth.reshape(-1,3).sum(1)>=2]=2;me.polygons.foreach_set('material_index',labels)
for o in coll.objects:
    if o.name.startswith('Amber_iris'):
        mat=o.data.materials[0];bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.28,.34,.035,1)
scene=bpy.context.scene;scene.cycles.samples=16;scene.render.resolution_x=720;scene.render.resolution_y=720;bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'face_preview.png');bpy.ops.render.render(write_still=True);(out/'authoring.json').write_text(json.dumps({'revision':'r14','status':'author_preview_pending','tooth_faces':int((labels==2).sum()),'source':'r13 with calibrated yellow-green eyes and uniform aged dentition'},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
