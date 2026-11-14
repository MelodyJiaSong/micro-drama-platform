from pathlib import Path
import bpy,json,numpy as np
root=Path(__file__).resolve().parents[3]
w=next(root.glob('2_*'))
m=json.loads((w/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'))
a=next(a for a in m['assets'] if a['id']=='m300')
p=root/a['model_directory']/'r01/inspection/m300_r01.blend'
bpy.ops.wm.open_mainfile(filepath=str(p))
o=next(o for o in bpy.data.collections['ASSET_m300'].objects if o.type=='MESH')
v=np.empty(len(o.data.vertices)*3,np.float32);o.data.vertices.foreach_get('co',v);v=v.reshape(-1,3);mat=np.array(o.matrix_world);v=v@mat[:3,:3].T+mat[:3,3]
print('BOUNDS',v.min(0),v.max(0))
for lo,hi in [(1.05,1.15),(.95,1.05),(.85,.95),(.65,.85),(.2,.45),(.0,.2)]:
 q=v[(v[:,2]>lo)&(v[:,2]<hi)];print('Z',lo,hi,'xyz percentiles',np.percentile(q,[2,25,50,75,98],axis=0).tolist())
for mat in o.data.materials:
 print('MATERIAL',mat.name)
 for n in mat.node_tree.nodes:
  if n.type=='BSDF_PRINCIPLED':
   for inp in n.inputs:
    if inp.is_linked or inp.name in ['Metallic','Roughness','Emission Strength','Base Color','Alpha']:print('INPUT',inp.name,[(l.from_node.name,l.from_socket.name) for l in inp.links],str(inp.default_value))
 for n in mat.node_tree.nodes:
  if n.type=='TEX_IMAGE':print('IMAGE',n.name,n.image.name,list(n.image.size),[(l.to_node.name,l.to_socket.name) for l in n.outputs['Color'].links])
uv=np.empty(len(o.data.loops)*2,np.float32);o.data.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2)
vi=np.empty(len(o.data.loops),np.int32);o.data.loops.foreach_get('vertex_index',vi)
image=next(n.image for n in o.data.materials[0].node_tree.nodes if n.type=='TEX_IMAGE' and any(l.to_socket.name=='Base Color' for l in n.outputs['Color'].links))
pixels=np.empty(image.size[0]*image.size[1]*4,np.float32);image.pixels.foreach_get(pixels);pixels=pixels.reshape(image.size[1],image.size[0],4)
c=pixels[(uv[:,1]*image.size[1]).astype(int).clip(0,image.size[1]-1),(uv[:,0]*image.size[0]).astype(int).clip(0,image.size[0]-1),:3]
vc=np.zeros((len(v),3),np.float32);vc[vi]=c
for name,mask in [('cloak_back',(v[:,1]>.18)&(v[:,2]>.4)&(v[:,2]<.8)),('cloak_side',(abs(v[:,0])>.28)&(v[:,2]>.7)&(v[:,2]<.9)),('beard',(abs(v[:,0])<.1)&(v[:,1]<-.20)&(v[:,2]>.8)&(v[:,2]<.95))]:
 print('REGION',name,'n',sum(mask),'RGB',np.percentile(vc[mask],[5,50,95],axis=0).tolist())
