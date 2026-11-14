"""Fit real rock scan relief into a local river bank; bury all patch borders."""
from pathlib import Path
import bpy,json,numpy as np,sys,argparse
from mathutils import Vector,kdtree
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
parser=argparse.ArgumentParser();parser.add_argument('--revision',choices=['v037','v038'],default='v037');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/f'environment_{args.revision}.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v036.blend'));fields=np.load(OUT/'cliff_embedding_fields.npz');z,gx,gy,clearance,water,codes=[fields[k] for k in ['z','gx','gy','clearance','water','codes']]
def sample(array,x,y):
 u,v=np.clip((x+409.6)/.8,0,1024),np.clip((y+409.6)/.8,0,1024);i,j=np.minimum(u.astype(int),1023),np.minimum(v.astype(int),1023);a,b=u-i,v-j;return (array[j,i]*(1-a)+array[j,i+1]*a)*(1-b)+(array[j+1,i]*(1-a)+array[j+1,i+1]*a)*b
source=OUT/'environment_sources/rock_face_02/rock_face_02_2k.blend'
with bpy.data.libraries.load(str(source),link=False) as (src,dst):dst.objects=['rock_face_02']
scan=dst.objects[0];mesh=scan.data
if args.revision=='v038':
 for i,mat in enumerate(list(mesh.materials)):
  mat=mat.copy();mesh.materials[i]=mat;nt=mat.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');source_colour=bs.inputs['Base Color'].links[0].from_socket;mul=nt.nodes.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=(.45,.47,.43,1);nt.links.new(source_colour,mul.inputs[1]);nt.links.new(mul.outputs[0],bs.inputs['Base Color'])
co=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('co',co);co=co.reshape(-1,3);plane=np.linalg.lstsq(np.column_stack((co[:,0],co[:,2],np.ones(len(co)))),co[:,1],rcond=None)[0];residual=co[:,1]-np.column_stack((co[:,0],co[:,2],np.ones(len(co))))@plane
edge_count={}
for p in mesh.polygons:
 ids=list(p.vertices)
 for a,b in zip(ids,ids[1:]+ids[:1]):key=tuple(sorted((a,b)));edge_count[key]=edge_count.get(key,0)+1
boundary={v for edge,count in edge_count.items() if count==1 for v in edge};tree=kdtree.KDTree(len(boundary))
for j,i in enumerate(boundary):tree.insert(Vector((float(co[i,0]),0,float(co[i,2]))),j)
tree.balance();edge_distance=np.array([tree.find(Vector((float(v[0]),0,float(v[2]))))[2] for v in co]);taper=np.clip(edge_distance/.55,0,1);taper=taper*taper*(3-2*taper);sx=(co[:,0]-(co[:,0].min()+co[:,0].max())*.5);sz=(co[:,2]-co[:,2].min())/np.ptp(co[:,2]);rng=np.random.default_rng(3701)
camera=bpy.data.objects['River_Eye_Level'];cp=np.array(camera.location[:2]);forward=camera.matrix_world.to_quaternion()@Vector((0,0,-1));direction=np.array(forward[:2]);direction/=np.linalg.norm(direction);jj,ii=np.indices(z.shape);xx=ii*.8-409.6;yy=jj*.8-409.6;dx,dy=xx-cp[0],yy-cp[1];slope=np.hypot(gx,gy);eligible=(slope>.65)&(slope<3)&(clearance>1.2)&(z>water+.7)&(z<water+9)&(np.hypot(dx,dy)<170)&((dx*direction[0]+dy*direction[1])>10);candidates=np.column_stack(np.nonzero(eligible));rng.shuffle(candidates);anchors=[]
for row,col in candidates:
 p=np.array([xx[row,col],yy[row,col]])
 if any(np.linalg.norm(p-a)<8.5 for a in anchors):continue
 anchors.append(p)
 if len(anchors)>=85:break
coll=bpy.data.collections.new('19_Embedded_scan_cliff_trial');bpy.context.scene.collection.children.link(coll);reports=[]
for number,p in enumerate(anchors):
 normal=np.array([float(sample(gx,*p)),float(sample(gy,*p))]);normal/=np.linalg.norm(normal);tangent=np.array([normal[1],-normal[0]]);low=max(float(sample(z,*(p-normal*12))),float(sample(water,*p))-.05);high=float(sample(z,*(p+normal*12)))
 if high-low<2.8:continue
 width=float(rng.uniform(1.5,2.1));base=p[None,:]+sx[:,None]*width*tangent;target=low+.05+sz*(high-low-.10);left=np.full(len(co),-16.);right=np.full(len(co),16.);hlo=sample(z,*(base+left[:,None]*normal).T);hhi=sample(z,*(base+right[:,None]*normal).T);valid=(target>=hlo)&(target<=hhi)
 for _ in range(18):
  mid=(left+right)*.5;h=sample(z,*(base+mid[:,None]*normal).T);left=np.where(h<target,mid,left);right=np.where(h>=target,mid,right)
 support=base+((left+right)*.5)[:,None]*normal;support_z=sample(z,*support.T);margin=sample(clearance,*support.T);depth=np.clip(.45-residual*1.2,0,1.3)*taper*valid*np.clip((margin-.6)/1.4,0,1)-.06;depth=np.minimum(depth,np.maximum(margin-.4,0));xy=support-depth[:,None]*normal;worldz=support_z.copy();u,v=np.clip(((xy+409.6)/.8).astype(int),0,1024).T;protected=(codes[v,u]&17)!=0;ground=sample(z,*xy.T);worldz[protected]=np.minimum(worldz[protected],ground[protected]-.04);boundary_ids=list(boundary);worldz[boundary_ids]=np.minimum(worldz[boundary_ids],ground[boundary_ids]-.03);exposed=(worldz-ground)>.01
 if args.revision=='v038':
  worldz-=.04;worldz[~valid]=np.minimum(worldz[~valid],ground[~valid]-.04);exposed=(worldz-ground)>.01
 if exposed.sum()<len(co)*.15:continue
 new=mesh.copy();new.name=f'Embedded_scan_cliff_{number:03d}';new.vertices.foreach_set('co',np.column_stack((xy,worldz)).astype(np.float32).ravel())
 if new.has_custom_normals:new.normals_split_custom_set([(0,0,0)]*len(new.loops))
 new.update();ob=bpy.data.objects.new(new.name,new);coll.objects.link(ob)
 for poly in new.polygons:poly.use_smooth=True
 reports.append({'object':ob.name,'anchor':p.tolist(),'z_range':[low,high],'horizontal_scale':width,'exposed_vertices':int(exposed.sum()),'exposed_protected_vertices':int((exposed&protected).sum()),'boundary_max_height_above_terrain_m':float(np.max((worldz-ground)[list(boundary)]))})
assert reports,'No valid embedded patches';assert all(r['exposed_protected_vertices']==0 for r in reports)
# The source is a scanned open surface; all open borders must be embedded.
report={'file':dest.name,'source':'environment_v036.blend','status':'local_author_trial_not_full_map_coverage','scan':'rock_face_02','patch_count':len(reports),'scope':'River_Eye_Level forward 170m neighbourhood only','source_mesh_faces':len(mesh.polygons),'placement_method':'Fit scan X/Z to actual bank isolines; retain scanned residual relief and UVs; fade all source mesh boundary edges below original terrain; protected path vertices forced underground','patches':reports,'terrain_navigation_geometry_unchanged':True,'remaining':['No exposed scan cut edges','Rock layer scale and repetition','Ground/water contact','Expand only after author inspection']};report['flat_surface_offset_m']=.04 if args.revision=='v038' else 0;scene=bpy.context.scene;scene['production_status']='EMBEDDED_SCANNED_CLIFF_LOCAL_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));(OUT/f'environment_{args.revision}_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('EMBEDDED_PATCHES_SAVED',len(reports),flush=True)
scene.camera=camera;scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1200;scene.render.resolution_y=900;scene.render.use_border=False;scene.render.use_crop_to_border=False;scene.render.use_simplify=True;scene.cycles.texture_limit_render='2048';scene.render.filepath=str(OUT/f'environment_{args.revision}_River_Eye_Level.png');bpy.ops.render.render(write_still=True);print('SCANNED_CLIFF_TRIAL_RENDERED',flush=True)
if args.revision=='v038':
 row=max(reports,key=lambda r:r['exposed_vertices']);p=np.array(row['anchor']);normal=np.array([float(sample(gx,*p)),float(sample(gy,*p))]);normal/=np.linalg.norm(normal);target=Vector((float(p[0]),float(p[1]),sum(row['z_range'])/2));camera.location=target+Vector((float(-normal[0]*18),float(-normal[1]*18),4));look_at(camera,target);camera.data.type='PERSP';camera.data.lens=48;scene.render.filepath=str(OUT/'environment_v038_Rock_Embedding_Close.png');bpy.ops.render.render(write_still=True);print('SCANNED_CLIFF_CLOSE_RENDERED',flush=True)
