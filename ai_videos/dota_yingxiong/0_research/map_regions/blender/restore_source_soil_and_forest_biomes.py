"""Use source tile categories to distinguish soil and avoid dead trees on green southeast tiles."""
from pathlib import Path
import bpy,numpy as np,json,math
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v030.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v029.blend'));data=json.loads((ROOT/'0_research/base_layout_refs/terrain_samples.json').read_text());flags=np.array(data['flags']);tile=flags&15
def softened(a):
 p=np.pad(a.astype(np.float32),1,mode='edge');return (p[1:-1,1:-1]*4+p[:-2,1:-1]+p[2:,1:-1]+p[1:-1,:-2]+p[1:-1,2:])/8
grass=softened(np.isin(tile,[2,3,4,5]));blight=softened((flags&32)!=0);soil=softened(tile==1)
def sample(a,x,y):
 u,v=np.clip((x+409.6)/6.4,0,127.9999),np.clip((y+409.6)/6.4,0,127.9999);i,j=np.asarray(u,dtype=int),np.asarray(v,dtype=int);u,v=u-i,v-j;return (a[j,i]*(1-u)+a[j,i+1]*u)*(1-v)+(a[j+1,i]*(1-u)+a[j+1,i+1]*u)*v
terrain=bpy.data.objects['Terrain_683d'].data;co=np.empty(len(terrain.vertices)*3,np.float32);terrain.vertices.foreach_get('co',co);co=co.reshape(-1,3);attr=terrain.attributes.new('Source_soil_tile_Cdrd','FLOAT','POINT');attr.data.foreach_set('value',sample(soil,co[:,0],co[:,1]).astype(np.float32))
anchors={o.name:tuple(o.location) for o in bpy.data.collections['02_Forest'].objects};changes=[]
for cname in ['02_Forest','14_Distant_Landscape']:
 for i,ob in enumerate(bpy.data.collections[cname].objects):
  if ob.instance_type!='COLLECTION' or not ob.instance_collection or not ob.instance_collection.name.startswith('LIB_Tree_'):continue
  x,y=ob.location[:2];g,b=float(sample(grass,x,y)),float(sample(blight,x,y));dead=b>.2 or (x+y>40 and g<.4)
  old=ob.instance_collection.name;olddead=int(old.rsplit('_',1)[1])>=5
  if dead==olddead:continue
  ob.instance_collection=bpy.data.collections[f'LIB_Tree_{5+i%3 if dead else i%5}'];changes.append({'object':ob.name,'source':old,'selected':ob.instance_collection.name,'source_grass_mask':g,'source_blight_mask':b})
assert all(tuple(bpy.data.objects[name].location)==p for name,p in anchors.items())
nt=bpy.data.materials['Continuous_ground'].node_tree;n,l=nt.nodes,nt.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED');colour=bs.inputs['Base Color'].links[0].from_socket
soilattr=n.new('ShaderNodeAttribute');soilattr.attribute_name='Source_soil_tile_Cdrd';blightattr=n.new('ShaderNodeAttribute');blightattr.attribute_name='Blight';paving=n.new('ShaderNodeAttribute');paving.attribute_name='Paving'
def mathnode(op,a,b):
 q=n.new('ShaderNodeMath');q.operation=op
 for socket,value in zip(q.inputs,[a,b]):
  if isinstance(value,(float,int)):socket.default_value=value
  else:l.new(value,socket)
 return q.outputs[0]
weight=mathnode('MULTIPLY',soilattr.outputs['Fac'],mathnode('SUBTRACT',1,blightattr.outputs['Fac']));weight=mathnode('MULTIPLY',weight,mathnode('SUBTRACT',1,paving.outputs['Fac']));geo=n.new('ShaderNodeNewGeometry');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=.09;noise.inputs['Detail'].default_value=3;l.new(geo.outputs['Position'],noise.inputs['Vector']);variation=n.new('ShaderNodeMapRange');variation.inputs['To Min'].default_value=.60;variation.inputs['To Max'].default_value=.88;l.new(noise.outputs['Fac'],variation.inputs['Value']);weight=mathnode('MULTIPLY',weight,variation.outputs[0]);tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[2].default_value=(.20,.26,.36,1);l.new(weight,tint.inputs[0]);l.new(colour,tint.inputs[1]);l.new(tint.outputs[0],bs.inputs['Base Color'])
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V030 AUTHOR TRIAL; source-aware soil and tree biome selection';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report={'file':dest.name,'source':'environment_v029.blend','status':'candidate_pending_author_view','source_sha256':data['source_sha256'],'ground_change':'Separate source tile index 1 (Cdrd) from the previous shared soil treatment; desaturated darker scanned earth outside already-blighted/paved regions, with broad variation','tree_selection':'Original grass/blight masks override the prior blanket x+y>40 dead-tree inference; northeast non-grass remains leafless, source grass patches are restored to live variants','tree_changes':changes,'canonical_xyz_unchanged':True,'terrain_navigation_and_water_unchanged':True,'mean_water_level_m':-6.800000190734863,'remaining':['Original minimap biome comparison','Ground closeup','Full independent environment review']};(OUT/'environment_v030_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SOURCE_BIOMES_SAVED',len(changes),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.cycles.use_denoising=True;scene.cycles.debug_use_compact_bvh=True;scene.render.use_simplify=True;scene.cycles.texture_limit_render='2048';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1200;scene.render.resolution_y=900
for name in ['River_Eye_Level','Map_Overview','Scourge_Base']:
 scene.camera=bpy.data.objects[name];scene.render.filepath=str(OUT/f'environment_v030_{name}.png');bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
