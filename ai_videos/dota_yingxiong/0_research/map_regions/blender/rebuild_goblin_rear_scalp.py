"""Reconstruct a measured rear scalp patch; retain the rest of the goblin mesh."""
from pathlib import Path
import bpy,bmesh,json,numpy as np,sys,argparse
from mathutils import Vector,kdtree
from mathutils.geometry import barycentric_transform
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
parser=argparse.ArgumentParser();parser.add_argument('--revision',choices=['r04','r05'],default='r04');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m309_*/model_3d'));out=folder/args.revision;out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r03/authoring.blend'));body=bpy.data.objects['Goblin_merchant_body'];source=body.data;coll=bpy.data.collections['ASSET_m309']
d=np.load(folder/'r03/rear_skull_ray_samples.npy');x,z,y,n,h,s=d.T
ok=(abs(x)<.075)&(z>.805)&(z<.944)&(y>.035)&(n>.3)&(h<.15)&(s>.5)
def basis(x,z):
 u=x/.08;v=(z-.87)/.08
 return np.column_stack([np.ones_like(u),u,v,u*u,u*v,v*v])
a=basis(x,z);mask=ok.copy()
for _ in range(5):
 coef=np.linalg.lstsq(a[mask],y[mask],rcond=None)[0];error=y-a@coef;mask=ok&(abs(error)<.006)
assert mask.sum()>2000 and np.sqrt(np.mean(error[mask]**2))<.003
healthy=d[mask];tree=kdtree.KDTree(len(healthy))
for j,row in enumerate(healthy):tree.insert(Vector((float(row[0]),0,float(row[1]))),j)
tree.balance()
cx,cz,rx,rz=(-.003,.875,.085,.065) if args.revision=='r05' else (-.003,.884,.08,.045)
gx,gz=np.meshgrid(np.linspace(cx-rx,cx+rx,int(rx*2000)+1),np.linspace(cz-rz,cz+rz,int(rz*2000)+1));xz=np.column_stack((gx.ravel(),gz.ravel()));ell=((xz[:,0]-cx)/rx)**2+((xz[:,1]-cz)/rz)**2
depth=basis(xz[:,0],xz[:,1])@coef;uv=np.zeros((len(xz),2));valid=np.flatnonzero(ell<=1)
for j in valid:
 xx,zz=map(float,xz[j]);hit,p,normal,index=body.ray_cast(Vector((xx,1,zz)),Vector((0,-1,0)))
 edge=max(0,min(1,(ell[j]-.55)/.45))
 if hit and p.y>.025 and abs(p.y-depth[j])<.008:depth[j]=depth[j]*(1-edge)+p.y*edge
 depth[j]-=.0005+.001*edge
 near=healthy[tree.find(Vector((xx,0,zz)))[1]]
 hit,p,normal,index=body.ray_cast(Vector((float(near[0]),1,float(near[1]))),Vector((0,-1,0)))
 if hit:
  face=source.polygons[index];loops=list(face.loop_indices)[:3];coords=[source.vertices[source.loops[l].vertex_index].co for l in loops];chart=[Vector((*source.uv_layers.active.data[l].uv,0)) for l in loops];value=barycentric_transform(p,*coords,*chart);uv[j]=value.x,value.y
faces=[];width=gx.shape[1]
for row in range(gx.shape[0]-1):
 for col in range(width-1):
  k=row*width+col
  for tri in [(k,k+width+1,k+1),(k,k+width,k+width+1)]:
   if np.max(ell[list(tri)])<=1:faces.append(tri)
used=np.unique(faces);remap={int(old):new for new,old in enumerate(used)}
mesh=bpy.data.meshes.new('Measured_reconstructed_rear_scalp');mesh.from_pydata([(float(xz[i,0]),float(depth[i]),float(xz[i,1])) for i in used],[],[[remap[i] for i in tri] for tri in faces]);mesh.update();ob=bpy.data.objects.new(mesh.name,mesh);coll.objects.link(ob)
for mat in source.materials:mesh.materials.append(mat)
chart=mesh.uv_layers.new(name=source.uv_layers.active.name)
for poly,tri in zip(mesh.polygons,faces):
 poly.use_smooth=True
 for loop,old in zip(poly.loop_indices,tri):chart.data[loop].uv=uv[old]
for name in ['Goblin_skin','Goblin_coat','Goblin_trim','Goblin_hair','Goblin_eye_region']:
 attr=mesh.attributes.new(name,'FLOAT','CORNER');attr.data.foreach_set('value',np.full(len(mesh.loops),1.0 if name=='Goblin_skin' else 0.0,np.float32))
if args.revision=='r05':
 mat=bpy.data.materials.new('Goblin_reconstructed_scalp_skin');mat.use_nodes=True;nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=n.get('Principled BSDF');geo=n.new('ShaderNodeNewGeometry');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=180;noise.inputs['Detail'].default_value=3;l.new(geo.outputs['Position'],noise.inputs[0]);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.11,.13,.038,1);ramp.color_ramp.elements[1].color=(.19,.21,.075,1);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.61;bs.inputs['Subsurface Weight'].default_value=.025
 pore=n.new('ShaderNodeTexNoise');pore.inputs['Scale'].default_value=1800;pore.inputs['Detail'].default_value=2;l.new(geo.outputs['Position'],pore.inputs[0]);bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.00012;bump.inputs['Strength'].default_value=.25;l.new(pore.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],bs.inputs['Normal']);mesh.materials.clear();mesh.materials.append(mat)
# Remove only rear, attached scanned hair fragments inside the repair region.
bm=bmesh.new();bm.from_mesh(source);hair=bm.loops.layers.float.get('Goblin_hair');remove=[]
for face in bm.faces:
 p=face.calc_center_median()
 inside=((p.x-cx)/rx)**2+((p.z-cz)/rz)**2
 if args.revision=='r05' and p.y>.025 and inside<.90:remove.append(face)
 elif .02<p.y and .80<p.z<.935 and abs(p.x)<.09 and np.mean([loop[hair] for loop in face.loops])>.20:remove.append(face)
removed=len(remove)
if remove:bmesh.ops.delete(bm,geom=remove,context='FACES')
bm.normal_update();bm.to_mesh(source);bm.free();source.update()
scene=bpy.context.scene;scene['production_status']='REAR_SKULL_RECONSTRUCTION_AUTHOR_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
report=json.loads((folder/'r03/authoring.json').read_text());report.update(revision=args.revision,source='r03',status='author_trial_pending_view',rear_scalp={'healthy_samples':int(mask.sum()),'fit_rmse_m':float(np.sqrt(np.mean(error[mask]**2))),'fit_coefficients':coef.tolist(),'patch_vertices':len(used),'patch_triangles':len(faces),'removed_rear_fragment_faces':removed,'procedural_skin_instead_of_nearest_uv':args.revision=='r05','limitation':'Separate fitted surface patch, not a welded topology reconstruction; inspect seams and side silhouette.'})
(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('REAR_SCALP_SAVED',json.dumps(report['rear_scalp']),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('back_detail',(0,2,.85),(0,0,.85),.36),('back_side',(1.4,2,.86),(0,0,.85),.40),('face_detail',(0,-2,.82),(0,0,.82),.42)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
