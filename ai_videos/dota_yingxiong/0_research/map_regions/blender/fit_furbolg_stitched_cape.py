"""Fit the continuous sewn cape to the actual old shell, interpolating its holes."""
from pathlib import Path
import bpy,bmesh,json,sys,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m21_Polar_Furbolg/model_3d'));out=folder/'r08';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r07/authoring.blend'));coll=bpy.data.collections['ASSET_m21'];old=bpy.data.objects['Reconstructed_leather_cape_shell'];cloth=bpy.data.objects['Continuous_stitched_hide'];bm=bmesh.new();bm.from_mesh(old.data);tree=BVHTree.FromBMesh(bm);bm.free();nu,nv=160,180
co=np.empty(len(cloth.data.vertices)*3,np.float32);cloth.data.vertices.foreach_get('co',co);co=co.reshape(nv+1,nu+1,3);before=co.copy();z=np.full((nv+1,nu+1),np.nan,np.float32)
for j in range(nv+1):
 for i in range(nu+1):
  hit,normal,face,d=tree.ray_cast(Vector((float(co[j,i,0]),float(co[j,i,1]),3)),Vector((0,0,-1)))
  if hit is not None:z[j,i]=hit.z+.008
known=np.isfinite(z);hit_count=int(known.sum());assert hit_count>z.size*.45,hit_count
# Only holes and off-edge cells are interpolated; smooth the captured coarse reconstruction.
for _ in range(400):
 if np.isfinite(z).all():break
 p=np.pad(z,1,mode='edge');neighbors=np.stack((p[:-2,1:-1],p[2:,1:-1],p[1:-1,:-2],p[1:-1,2:]));counts=np.isfinite(neighbors).sum(axis=0);fill=np.isnan(z)&(counts>0);z[fill]=np.nansum(neighbors,axis=0)[fill]/counts[fill]
assert np.isfinite(z).all()
for _ in range(36):
 p=np.pad(z,1,mode='edge');z=(p[1:-1,1:-1]*4+p[:-2,1:-1]+p[2:,1:-1]+p[1:-1,:-2]+p[1:-1,2:])/8
co[:,:,2]=z;delta=z-before[:,:,2];cloth.data.vertices.foreach_set('co',co.ravel());cloth.data.update()
def offset(x,y):
 v=np.clip((y+.51)/1.18,0,1);width=.55+.035*np.sin(v*np.pi);u=np.clip((x/width+1)/2,0,1);a,b=u*nu,v*nv;i,j=min(int(a),nu-1),min(int(b),nv-1);a-=i;b-=j
 return float((delta[j,i]*(1-a)+delta[j,i+1]*a)*(1-b)+(delta[j+1,i]*(1-a)+delta[j+1,i+1]*a)*b)
for ob in coll.objects:
 if ob.name.startswith(('Raised_hide_panel_seam','Cross_laced_hide_stitch','Cross_hide_panel_seam')):
  for sp in ob.data.splines:
   for p in sp.points:p.co.z+=offset(p.co.x,p.co.y)
fringe=bpy.data.objects['Hide_front_fur_fringe'].data;positions=np.empty(len(fringe.attributes['position'].data)*3,np.float32);fringe.attributes['position'].data.foreach_get('vector',positions);positions=positions.reshape(-1,5,3)
for strand in positions:strand[:,2]+=offset(*strand[0,:2])
fringe.attributes['position'].data.foreach_set('vector',positions.ravel())
# Remove only small detached remnants behind the torso; preserve face and claw components.
body=bpy.data.objects['geometry_0'];bm=bmesh.new();bm.from_mesh(body.data);unseen=set(bm.verts);removed=0
while unseen:
 first=unseen.pop();pending=[first];group=[first]
 while pending:
  v=pending.pop()
  for edge in v.link_edges:
   q=edge.other_vert(v)
   if q in unseen:unseen.remove(q);pending.append(q);group.append(q)
 if len(group)<1200:
  center=sum((v.co for v in group),Vector())/len(group)
  if center.y>.12 and center.z>.6:bmesh.ops.delete(bm,geom=group,context='VERTS');removed+=len(group)
bm.to_mesh(body.data);bm.free()
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.camera.location=(6,-7,3);scene.camera.data.ortho_scale=2.9;look_at(scene.camera,(0,0,1.15));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m21','revision':'r08','source':'r07','status':'author_preview_not_accepted','changes':['Fit continuous hide to actual prior garment surface','Interpolate ray-missed holes instead of retaining generated pits','Fit seams and fringe to same surface','Remove small disconnected rear cloth fragments'],'surface_ray_hits':hit_count,'surface_vertices':int(z.size),'removed_fragment_vertices':removed,'remaining':['Garment silhouette, folds and contact','Author and independent inspection']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.location=(3,4,3.2);scene.camera.data.ortho_scale=1.5;look_at(scene.camera,(0,.1,1.8));scene.render.filepath=str(out/'roof_poles_preview.png');bpy.ops.render.render(write_still=True)
