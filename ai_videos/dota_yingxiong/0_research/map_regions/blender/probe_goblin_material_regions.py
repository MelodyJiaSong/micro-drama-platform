"""Sample actual UV albedo at measured body regions before semantic colour correction."""
from pathlib import Path
import bpy,json,numpy as np,colorsys
from mathutils import Vector
from mathutils.geometry import barycentric_transform
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m309_*/model_3d'))
bpy.ops.wm.open_mainfile(filepath=str(folder/'r01/inspection/m309_r01.blend'));body=max((o for o in bpy.data.collections['ASSET_m309'].all_objects if o.type=='MESH' and not o.hide_render),key=lambda o:len(o.data.polygons));mesh=body.data;image=next(n.image for m in mesh.materials for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and n.image.colorspace_settings.name=='sRGB');pixels=np.empty(len(image.pixels),np.float32);image.pixels.foreach_get(pixels);width,height=image.size;pixels=pixels.reshape(height,width,4);inv=body.matrix_world.inverted();direction=inv.to_3x3()@Vector((0,1,0));rows=[]
for name,x,z in [('scalp',0,.92),('cheek',-.035,.80),('nose',0,.82),('torso',0,.46),('left_sleeve',-.13,.59),('left_jacket',-.075,.64),('right_jacket',.075,.64),('trim',-.055,.58),('pants',-.055,.29),('leg',-.065,.15),('hand',0,.60),('eye_left',-.035,.84)]:
 samples=[]
 for dx,dz in [(0,0),(-.005,0),(.005,0),(0,-.005),(0,.005)]:
  hit,p,n,index=body.ray_cast(inv@Vector((x+dx,-2,z+dz)),direction)
  if not hit:continue
  f=mesh.polygons[index];loops=list(f.loop_indices)[:3];co=[mesh.vertices[mesh.loops[l].vertex_index].co for l in loops];uv=[Vector((*mesh.uv_layers.active.data[l].uv,0)) for l in loops];sample=barycentric_transform(p,*co,*uv);ix=min(width-1,max(0,int(sample.x*width)));iy=min(height-1,max(0,int(sample.y*height)));rgb=pixels[iy,ix,:3].tolist();samples.append({'world':list(body.matrix_world@p),'rgb':rgb,'hsv':colorsys.rgb_to_hsv(*rgb)})
 rows.append({'region':name,'samples':samples})
(folder/'material_region_probe.json').write_text(json.dumps({'body':body.name,'matrix':list(map(list,body.matrix_world)),'probes':rows},indent=2),encoding='utf-8');print(json.dumps(rows),flush=True)
