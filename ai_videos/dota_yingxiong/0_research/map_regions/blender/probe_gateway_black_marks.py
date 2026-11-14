"""Distinguish black albedo marks from rays passing through actual face holes."""
from pathlib import Path
import bpy,json
from mathutils import Vector
from mathutils.geometry import barycentric_transform
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m303_*/model_3d/r07'));bpy.ops.wm.open_mainfile(filepath=str(folder/'authoring.blend'));body=bpy.data.objects['Gateway_merchant_body'];mesh=body.data;image=next(n.image for m in mesh.materials for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and n.image.colorspace_settings.name=='sRGB');pixels=list(image.pixels);width,height=image.size;rows=[]
for name,cx,cy in [('forehead',510,350),('chin',490,660),('nose_cheek',395,525),('left_collar',240,910),('right_collar',720,930)]:
 samples=[]
 for dx,dy in [(0,0),(-4,0),(4,0),(0,-4),(0,4),(-12,0),(12,0),(0,-12),(0,12)]:
  x=((cx+dx)/1000-.5)*.38;z=1.7+(.5-(cy+dy)/1000)*.38;hit,p,n,index=body.ray_cast(Vector((x,-2,z)),Vector((0,1,0)))
  if not hit:samples.append({'offset':[dx,dy],'hit':False});continue
  face=mesh.polygons[index];loops=list(face.loop_indices)[:3];coords=[mesh.vertices[mesh.loops[l].vertex_index].co for l in loops];uv=[Vector((*mesh.uv_layers.active.data[l].uv,0)) for l in loops];sample=barycentric_transform(p,*coords,*uv);ix=min(width-1,max(0,int(sample.x*width)));iy=min(height-1,max(0,int(sample.y*height)));rgb=pixels[(iy*width+ix)*4:(iy*width+ix)*4+3];samples.append({'offset':[dx,dy],'hit':True,'position':list(p),'normal':list(n),'image_rgb':rgb,'face':index})
 rows.append({'name':name,'pixel':[cx,cy],'samples':samples})
(folder/'black_mark_ray_diagnosis.json').write_text(json.dumps({'image':image.name,'camera':'face_detail orthographic .38m, horizontal -Y, target z1.70','probes':rows},indent=2),encoding='utf-8');print(json.dumps(rows),flush=True)
