"""Measure healthy rear scalp samples before reconstructing removed scan debris."""
from pathlib import Path
import bpy,json,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m309_*/model_3d'))
bpy.ops.wm.open_mainfile(filepath=str(folder/'r03/authoring.blend'))
body=bpy.data.objects['Goblin_merchant_body'];mesh=body.data
xs=np.linspace(-.10,.10,201);zs=np.linspace(.76,.95,191);rows=[]
for z in zs:
 for x in xs:
  hit,p,n,index=body.ray_cast(Vector((float(x),1,float(z))),Vector((0,-1,0)))
  if not hit:rows.append([x,z,np.nan,0,1,0]);continue
  face=mesh.polygons[index];hair=np.mean([mesh.attributes['Goblin_hair'].data[l].value for l in face.loop_indices]);skin=np.mean([mesh.attributes['Goblin_skin'].data[l].value for l in face.loop_indices])
  rows.append([x,z,p.y,n.y,hair,skin])
data=np.array(rows,np.float32);np.save(folder/'r03/rear_skull_ray_samples.npy',data)
summary={'columns':['x','z','rear_hit_y','normal_y','hair_mask','skin_mask'],'matrix_world':[list(r) for r in body.matrix_world],'samples':len(data),'z_bands':[]}
for z in np.arange(.77,.95,.02):
 selected=data[(abs(data[:,0])<.075)&(abs(data[:,1]-z)<.01)&(data[:,3]>.3)&(data[:,4]<.15)&(data[:,5]>.5)&np.isfinite(data[:,2])]
 summary['z_bands'].append({'center_z':float(z),'healthy_points':len(selected),'y_quantiles':np.quantile(selected[:,2],[.05,.5,.95]).tolist() if len(selected) else []})
(folder/'r03/rear_skull_probe.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary),flush=True)
