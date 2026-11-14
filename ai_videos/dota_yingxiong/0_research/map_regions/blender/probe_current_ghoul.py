from pathlib import Path
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m4_Ghoul/model_3d'));bpy.ops.wm.open_mainfile(filepath=str(folder/'r15/inspection/m4_r15.blend'));ob=next(o for o in bpy.data.collections['ASSET_m4'].objects if o.type=='MESH' and len(o.data.polygons)>100000);me=ob.data
print('MATRIX',list(map(list,ob.matrix_world)));print('MATERIALS',[(i,m.name) for i,m in enumerate(me.materials)])
v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);v=v@np.array(ob.matrix_world)[:3,:3].T+np.array(ob.matrix_world)[:3,3];idx=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',idx);co=v[idx].reshape(-1,3,3).mean(1)
uv=np.empty(len(me.loops)*2,np.float32);me.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,3,2).mean(1);im=next(n.image for n in me.materials[0].node_tree.nodes if n.type=='TEX_IMAGE' and n.image.colorspace_settings.name=='sRGB');pix=np.empty(len(im.pixels),np.float32);im.pixels.foreach_get(pix);pix=pix.reshape(im.size[1],im.size[0],4);rgb=pix[(uv[:,1]*im.size[1]).astype(int).clip(0,im.size[1]-1),(uv[:,0]*im.size[0]).astype(int).clip(0,im.size[0]-1),:3]
mask=(abs(co[:,0])<.16)&(co[:,1]<-.30)&(co[:,2]>.6)&(co[:,2]<1.1)&(rgb[:,2]<rgb[:,0]*.47)&(rgb[:,0]>.25)
print('YELLOW_FACE',len(co[mask]),np.quantile(co[mask],[.05,.5,.95],axis=0).tolist())
for zz in np.arange(.65,1.05,.05):
 p=co[mask&(co[:,2]>=zz)&(co[:,2]<zz+.05)]
 if len(p):print('BAND',zz,len(p),np.quantile(p,[.05,.5,.95],axis=0).tolist())
