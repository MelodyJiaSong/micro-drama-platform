"""Replace prototype moss with shared CC0 plant geometry and correct quartz optics."""
from pathlib import Path
import bpy,json,sys,random
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));SRC=WORLD/'background/map_3d/environment_sources/moss_01';folder=next(WORLD.glob('background/*/bg23_*/model_3d'));out=folder/'r44';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r43/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];rng=random.Random(2344)
with bpy.data.libraries.load(str(next(SRC.glob('*.blend'))),link=False) as (src,dst):dst.objects=[f'moss_01_{letter}_LOD1' for letter in 'abcdefghij']
prototypes=dst.objects;metrics=[]
for ob in prototypes:
 ob.data=ob.data.copy();coords=[v.co.copy() for v in ob.data.vertices];lo=Vector(tuple(min(v[i] for v in coords) for i in range(3)));hi=Vector(tuple(max(v[i] for v in coords) for i in range(3)));center=Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z));scale=.11/max(hi.x-lo.x,hi.y-lo.y)
 for v in ob.data.vertices:v.co=(v.co-center)*scale
 ob.data.update();metrics.append({'source':ob.name,'faces':len(ob.data.polygons),'source_dimensions':list(hi-lo),'scale_to_11cm':scale})
tufts=[o for o in coll.objects if o.name.startswith('Cornice_moss_tuft')]
for i,ob in enumerate(tufts):ob.data=prototypes[i%len(prototypes)].data;ob.rotation_euler.z=rng.uniform(0,6.283);ob.scale*=rng.uniform(.75,1.25)
for image in bpy.data.images:
 if 'moss_01' not in image.name or image.packed_file:continue
 name=Path(image.filepath.replace('\\','/')).name;matches=list(SRC.rglob(name))
 if not matches:raise FileNotFoundError(name)
 image.filepath=str(matches[0]);image.reload()
for mat in bpy.data.materials:
 if not mat.name.startswith('Inset_quartz_amethyst_'):continue
 nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.72,.62,.85,1);bs.inputs['Transmission Weight'].default_value=1;bs.inputs['Roughness'].default_value=.13;bs.inputs['IOR'].default_value=1.54;bs.inputs['Coat Weight'].default_value=0
 volume=nt.nodes.new('ShaderNodeVolumeAbsorption');volume.inputs['Color'].default_value=(.32,.065,.55,1);volume.inputs['Density'].default_value=9;nt.links.new(volume.outputs[0],next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL').inputs['Volume'])
scene=bpy.context.scene;scene.cycles.transmission_bounces=max(scene.cycles.transmission_bounces,8);scene.cycles.transparent_max_bounces=max(scene.cycles.transparent_max_bounces,16);scene['production_status']='SCANNED_MOSS_QUARTZ_AUTHOR_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report=json.loads((folder/'r43/authoring.json').read_text());report.update(revision='r44',source='r43',status='author_trial_pending_view',moss_source={'asset':'moss_01','url':'https://polyhaven.com/a/moss_01','license':'CC0','provenance':str((SRC/'provenance.json').relative_to(ROOT)),'shared_LOD1_prototypes':metrics,'instances':len(tufts)},quartz='Dielectric transmission with volume absorption, IOR 1.54, no emission',remaining=['Actual moss scale and material loading','Quartz depth and edge highlights','Root and soil appearance','Independent review']);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SCANNED_MOSS_SAVED',len(tufts),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=48;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
