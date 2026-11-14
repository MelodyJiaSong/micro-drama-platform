"""Build 11cm moss cushions from 1-3cm source sprigs, preserving source UVs."""
from pathlib import Path
import bpy,json,sys,random,math
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r45';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r44/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];tufts=[ob for ob in coll.objects if ob.name.startswith('Cornice_moss_tuft')];report=json.loads((folder/'r44/authoring.json').read_text());metrics=report['moss_source']['shared_LOD1_prototypes'];sources=[(tufts[i].data,metrics[i]['scale_to_11cm']) for i in range(10)];rng=random.Random(2345);clusters=[]
for variant in range(5):
 verts=[];faces=[];uvs=[];material_indices=[];materials=[]
 for sprig in range(80):
  source,undo=rng.choice(sources);angle=rng.random()*math.tau;r=.05*math.sqrt(rng.random());px,py=r*math.cos(angle),r*math.sin(angle);rotation=rng.random()*math.tau;c,s=math.cos(rotation),math.sin(rotation);scale=rng.uniform(.45,1.0);offset=len(verts)
  for v in source.vertices:
   p=v.co/undo*scale;verts.append((p.x*c-p.y*s+px,p.x*s+p.y*c+py,p.z+.001))
  for poly in source.polygons:
   faces.append(tuple(offset+i for i in poly.vertices));uvs.extend(tuple(source.uv_layers.active.data[loop].uv) for loop in poly.loop_indices);mat=source.materials[poly.material_index]
   if mat not in materials:materials.append(mat)
   material_indices.append(materials.index(mat))
 mesh=bpy.data.meshes.new(f'Physical_moss_cushion_{variant}');mesh.from_pydata(verts,[],faces);mesh.update();uv=mesh.uv_layers.new(name='UVMap')
 for i,value in enumerate(uvs):uv.data[i].uv=value
 for mat in materials:mesh.materials.append(mat)
 for poly,index in zip(mesh.polygons,material_indices):poly.material_index=index;poly.use_smooth=True
 clusters.append(mesh)
for i,ob in enumerate(tufts):ob.data=clusters[i%5]
scene=bpy.context.scene;scene['production_status']='PHYSICAL_SCALE_MOSS_AUTHOR_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report.update(revision='r45',source='r44',status='author_trial_pending_view',moss_physical_scale={'source_sprigs_m':'0.009-0.030 before 0.45-1.0 random scale','sprigs_per_shared_cushion':80,'shared_cushions':5,'instances':len(tufts),'texture_UV_preserved':True},remaining=['Moss carpet scale and alpha shadows','Multi-angle geometry and materials','Independent review']);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('PHYSICAL_MOSS_SAVED',len(tufts),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=40;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
