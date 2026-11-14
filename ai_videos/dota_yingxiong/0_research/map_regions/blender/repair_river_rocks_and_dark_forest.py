"""Use verified full crowns and thick boulders; remove repetitive wave-shaped bank relief."""
from pathlib import Path
import bpy,json,math,random,numpy as np
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v019.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v018.blend'));changed=[]
for target,source,height in [(5,0,11.5),(6,1,12.8)]:
 src=next(o for o in bpy.data.collections[f'LIB_Tree_{source}'].objects if o.type=='MESH');coll=bpy.data.collections[f'LIB_Tree_{target}'];old=list(coll.objects)
 ob=src.copy();ob.data=src.data.copy();coll.objects.link(ob);ob.name=f'Full_blighted_crown_{target}';ratio=height/src.dimensions.z;ob.scale*=ratio
 for i,mat in enumerate(list(ob.data.materials)):
  mat=mat.copy();ob.data.materials[i]=mat;mat.name='Dark_forest_'+mat.name
  if not mat.use_nodes:continue
  nt=mat.node_tree;bs=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
  if not bs:continue
  mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(.20,.24,.16,1)
  if bs.inputs['Base Color'].is_linked:nt.links.new(bs.inputs['Base Color'].links[0].from_socket,mix.inputs[1])
  else:mix.inputs[1].default_value=bs.inputs['Base Color'].default_value
  nt.links.new(mix.outputs[0],bs.inputs['Base Color']);bs.inputs['Specular IOR Level'].default_value=.2
 changed.append({'target':target,'source_verified_full_crown':source,'height_m':height,'source_faces':len(src.data.polygons),'old_faces':[len(o.data.polygons) for o in old if o.type=='MESH']})
 for o in old:coll.objects.unlink(o)
nt=bpy.data.materials['Continuous_ground'].node_tree;n,l=nt.nodes,nt.links;removed=0
for wave in list(n):
 if wave.type!='TEX_WAVE':continue
 targets=[link.to_socket for link in wave.outputs['Color'].links]
 if not targets:continue
 coord=wave.inputs['Vector'].links[0].from_socket;scale=n.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs[3].default_value=.3;l.new(coord,scale.inputs[0])
 tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(OUT/'textures/mossy_rock_disp_2k.png'),check_existing=True);tex.image.colorspace_settings.name='Non-Color';tex.projection='BOX';tex.projection_blend=.25;l.new(scale.outputs[0],tex.inputs['Vector'])
 for socket in targets:l.new(tex.outputs[0],socket)
 n.remove(wave);removed+=1
terrain=bpy.data.objects['Terrain_683d'].data;co=np.empty(len(terrain.vertices)*3,np.float32);terrain.vertices.foreach_get('co',co);co=co.reshape(1025,1025,3);z=co[:,:,2]
def height(px,py):
 u,v=np.clip((px+409.6)/.8,0,1023.999),np.clip((py+409.6)/.8,0,1023.999);i,j=int(u),int(v);a,b=u-i,v-j
 return float((z[j,i]*(1-a)+z[j,i+1]*a)*(1-b)+(z[j+1,i]*(1-a)+z[j+1,i+1]*a)*b)
proto=bpy.data.collections['RIVER_SCAN_boulder_01'];rng=random.Random(29119);replaced=0
for o in bpy.data.collections['07_Cliff_Relief'].objects:
 px,py=o.location[:2];ground=height(px,py)
 if not -8<ground<-2:continue
 o.instance_collection=proto;s=rng.uniform(1,1.6);o.scale=(s*rng.uniform(.8,1.25),s*rng.uniform(.75,1.1),s*rng.uniform(.9,1.25));o.location.z=ground-rng.uniform(.25,.55);o.rotation_euler=(rng.uniform(-.5,.5),rng.uniform(-.4,.4),rng.uniform(0,math.tau));replaced+=1
for o in bpy.data.collections['17_River_bank_detail'].objects:
 if o.name.startswith('Broken_shore_outcrop'):o.instance_collection=proto
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V019 CANDIDATE; full dark crowns and river rocks require review'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(OUT/'environment_v019_report.json').write_text(json.dumps({'file':dest.name,'source':'environment_v018.blend','status':'candidate_pending_visual_review','tree_changes':changed,'replaced_large_shore_plates':replaced,'removed_wave_bank_textures':removed,'terrain_and_anchor_positions_changed':False,'remaining':['Inspect canopy footprint','Inspect shore rock placement','Independent review']},indent=2),encoding='utf-8')
print('SAVED',dest,flush=True);scene.cycles.device='CPU';scene.cycles.samples=48;scene.cycles.use_denoising=True;scene.render.resolution_x=1200;scene.render.resolution_y=900
for name in ['Mid_River','Map_Overview']:
 scene.camera=bpy.data.objects[name];scene.render.filepath=str(OUT/f'environment_v019_{name}.png');bpy.ops.render.render(write_still=True)
