"""Repair only five measured pinhole regions; preserve the original body mesh."""
from pathlib import Path
import bpy,json,sys,numpy as np
from mathutils import Vector,kdtree
from mathutils.geometry import barycentric_transform
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m303_*/model_3d'));out=folder/'r10';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r07/authoring.blend'));body=bpy.data.objects['Gateway_merchant_body'];source=body.data;coll=bpy.data.collections['ASSET_m303'];rows=[]
for name,cx,cz,radius in [('forehead',.0038,1.757,.006),('chin',-.00228,1.6392,.006),('nose_cheek',-.0399,1.6905,.008),('left_collar',-.0988,1.5442,.010),('right_collar',.0836,1.5366,.010)]:
 step=.0005;n=int(round(radius*2/step))+1;gx,gz=np.meshgrid(np.linspace(cx-radius,cx+radius,n),np.linspace(cz-radius,cz+radius,n));xz=np.column_stack((gx.ravel(),gz.ravel()));depth=np.full(len(xz),np.nan);uv=np.zeros((len(xz),2));normal_y=np.ones(len(xz))
 for j,(x,z) in enumerate(xz):
  hit,p,normal,index=body.ray_cast(Vector((float(x),-2,float(z))),Vector((0,1,0)))
  if not hit:continue
  depth[j]=p.y;normal_y[j]=normal.y;face=source.polygons[index];loops=list(face.loop_indices)[:3];coords=[source.vertices[source.loops[l].vertex_index].co for l in loops];chart=[Vector((*source.uv_layers.active.data[l].uv,0)) for l in loops];sample=barycentric_transform(p,*coords,*chart);uv[j]=sample.x,sample.y
 median=float(np.nanmedian(depth));good=np.isfinite(depth)&(np.abs(depth-median)<.018)&(normal_y<-.05);bad=~good;tree=kdtree.KDTree(int(good.sum()))
 for j in np.flatnonzero(good):tree.insert(Vector((float(xz[j,0]),0,float(xz[j,1]))),int(j))
 tree.balance();fitted=depth.copy();nearest=np.arange(len(xz));distance=np.zeros(len(xz));repaired=np.zeros(len(xz),bool)
 for j in np.flatnonzero(bad):
  found=tree.find_n(Vector((float(xz[j,0]),0,float(xz[j,1]))),24)
  if len(found)<6 or found[0][2]>.0045:continue
  ids=np.array([f[1] for f in found]);d=np.array([f[2] for f in found]);a=np.column_stack((xz[ids]-xz[j],np.ones(len(ids))));w=1/np.maximum(d,.00025);coef=np.linalg.lstsq(a*w[:,None],depth[ids]*w,rcond=None)[0];fitted[j]=coef[2]-.00008;nearest[j]=ids[0];distance[j]=d[0];repaired[j]=True
 faces=[]
 for y in range(n-1):
  for x in range(n-1):
   a=y*n+x
   for tri in [(a,a+1,a+n+1),(a,a+n+1,a+n)]:
    ids=np.array(tri)
    if repaired[ids].any() and np.all(good[ids]|repaired[ids]) and np.max(np.linalg.norm(xz[ids]-[cx,cz],axis=1))<radius:faces.append(tri)
 if not faces:rows.append({'name':name,'status':'no_patch'});continue
 used=np.unique(faces);indexmap={int(old):new for new,old in enumerate(used)};vertices=[(float(xz[i,0]),float(fitted[i]-.00003),float(xz[i,1])) for i in used];mesh=bpy.data.meshes.new('Measured_pinhole_'+name);mesh.from_pydata(vertices,[],[[indexmap[i] for i in tri] for tri in faces]);mesh.update();ob=bpy.data.objects.new(mesh.name,mesh);coll.objects.link(ob)
 for mat in source.materials:mesh.materials.append(mat)
 chart=mesh.uv_layers.new(name=source.uv_layers.active.name)
 for poly,tri in zip(mesh.polygons,faces):
  poly.use_smooth=True
  # A single neighbouring front-facing UV chart avoids pulling colour from
  # the back surface or interpolating across unrelated UV islands.
  anchor=next((i for i in tri if good[i]),int(nearest[tri[0]]))
  for loop in poly.loop_indices:chart.data[loop].uv=uv[anchor]
 rows.append({'name':name,'radius_m':radius,'sample_step_m':step,'valid_front_samples':int(good.sum()),'repaired_samples':int(repaired.sum()),'patch_vertices':len(vertices),'patch_triangles':len(faces),'max_interpolation_distance_m':float(distance.max()),'source_body_unchanged':True})
 print('LOCAL_PATCH',json.dumps(rows[-1]),flush=True)
scene=bpy.context.scene;scene['production_status']='MEASURED_LOCAL_HOLE_PATCH_AUTHOR_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'asset_id':'m303','revision':'r10','source':'r07','status':'author_trial_pending_view','patches':rows,'limitations':['Local surface patches are separate meshes, not topology welds','UV colours are sampled from nearby valid front triangles','Other face, hair and clothing defects remain']},indent=2),encoding='utf-8')
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('face_detail',(0,-2,1.7),(0,0,1.7),.38),('face_side',(1.3,-2,1.7),(0,0,1.7),.38),('author_preview',(4,-6,2),(0,0,.925),2.37)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
