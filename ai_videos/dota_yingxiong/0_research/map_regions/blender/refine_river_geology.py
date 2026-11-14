"""River optics and eroded bank detail; keep traversable terrain unchanged."""
from pathlib import Path
import bpy,json,base64,math,random,numpy as np
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';SRC=OUT/'environment_sources'
dest=OUT/'environment_v017.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v016.blend'))
terrain=bpy.data.objects['Terrain_683d'].data
co=np.empty(len(terrain.vertices)*3,np.float32);terrain.vertices.foreach_get('co',co);co=co.reshape(1025,1025,3)
z=co[:,:,2];before=z.copy();x,y=co[:,:,0],co[:,:,1]
water=bpy.data.objects['River_surface'];water_z=float(water.data.vertices[0].co.z)
grid=json.loads((ROOT/'0_research/map_regions/navigation/grid.json').read_text());cells=np.frombuffer(base64.b64decode(grid['cells_base64']),np.uint8).reshape(512,512)
ix=np.minimum(np.arange(1025)//2,511);codes=cells[::-1][ix[:,None],ix[None,:]];protected=(codes&(1|16))!=0
margin=protected.copy()
for _ in range(2):
 p=np.pad(margin,1,mode='edge');margin=p[1:-1,1:-1]|p[:-2,1:-1]|p[2:,1:-1]|p[1:-1,:-2]|p[1:-1,2:]
gy,gx=np.gradient(z,.8);slope=np.hypot(gx,gy)
bank=np.clip(1-np.abs(z-(water_z+1.5))/4.5,0,1)*np.clip((slope-.12)*2,0,1)*(~margin)
# Aperiodic cross-frequency relief is limited to blocked banks, below foot routes.
relief=(np.sin(x*1.71+np.sin(y*.79)*2.4)*np.cos(y*1.29+x*.23)*.18+
        np.sin(x*.53-y*.77+np.sin(x*.15)*3)*.25+np.sin(y*2.81+x*.97)*.07)
z[:]+=bank*relief
terrain.vertices.foreach_set('co',co.ravel());terrain.update()
assert float(np.max(np.abs(z-before)[protected]))==0
def height(px,py,arr=z):
 u,v=np.clip((px+409.6)/.8,0,1023.999),np.clip((py+409.6)/.8,0,1023.999);i,j=int(u),int(v);a,b=u-i,v-j
 return float((arr[j,i]*(1-a)+arr[j,i+1]*a)*(1-b)+(arr[j+1,i]*(1-a)+arr[j+1,i+1]*a)*b)
def nav(px,py):return int(cells[int(np.clip((409.6-py)/1.6,0,511)),int(np.clip((px+409.6)/1.6,0,511))])
for cname in ['02_Forest','03_Asset_Placement','06_Undergrowth','07_Cliff_Relief','08_Meadow_Growth','09_Ground_Stones','13_Fallen_Timber','17_River_bank_detail']:
 for o in bpy.data.collections[cname].objects:
  px,py=o.location[:2];o.location.z+=height(px,py)-height(px,py,before)
# Replace the upright repeated thin rock plates with varied scanned boulders.
protos=[]
for asset in ['boulder_01','coast_rocks_02']:
 with bpy.data.libraries.load(str(next((SRC/asset).glob('*.blend'))),link=False) as (src,dst):
  names=[n for n in src.objects if asset in n and ('LOD1' in n or 'LOD2' in n)]
  dst.objects=names[:1] or [n for n in src.objects if asset in n][:1]
 ob=dst.objects[0];ob.location=(0,0,0);ob.hide_render=False;ob.hide_viewport=False
 collection=bpy.data.collections.new('RIVER_SCAN_'+asset);collection.objects.link(ob)
 # Normalize the source to a 2 m maximum dimension; later instance scales are metres.
 extent=max(max(v.co[a] for v in ob.data.vertices)-min(v.co[a] for v in ob.data.vertices) for a in range(3))
 ob.scale=(2/extent,)*3;protos.append(collection)
rng=random.Random(29117);replaced=0
for ob in bpy.data.collections['17_River_bank_detail'].objects:
 if not ob.name.startswith('Broken_shore_outcrop'):continue
 px,py=ob.location[:2];radius=1.1
 if any(nav(px+dx,py+dy)&(1|16) for dx,dy in [(0,0),(radius,0),(-radius,0),(0,radius),(0,-radius)]):continue
 ob.instance_collection=protos[replaced%2];ob.location.z=height(px,py)-rng.uniform(.25,.65)
 s=rng.uniform(.45,1.1);ob.scale=(s*rng.uniform(.75,1.3),s*rng.uniform(.65,1.2),s*rng.uniform(.65,1.0));ob.rotation_euler=(rng.uniform(-.6,.6),rng.uniform(-.5,.5),rng.uniform(0,math.tau));replaced+=1
# Bank shader: scanned sediment/rock, damp water line, fine stratification.
nt=bpy.data.materials['Continuous_ground'].node_tree;n,l=nt.nodes,nt.links
bs=next(q for q in n if q.type=='BSDF_PRINCIPLED');geo=n.new('ShaderNodeNewGeometry');pos=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Position'],pos.inputs[0])
def mathnode(op,a,b):
 q=n.new('ShaderNodeMath');q.operation=op
 for inp,val in zip(q.inputs,[a,b]):
  if isinstance(val,(float,int)):inp.default_value=val
  else:l.new(val,inp)
 return q.outputs[0]
def ramp(value,lo,hi):
 q=n.new('ShaderNodeMapRange');q.clamp=True;q.interpolation_type='SMOOTHSTEP';q.inputs['From Min'].default_value=lo;q.inputs['From Max'].default_value=hi;l.new(value,q.inputs['Value']);return q.outputs[0]
def blend(a,b,f):
 q=n.new('ShaderNodeMixRGB');l.new(f,q.inputs[0]);l.new(a,q.inputs[1]);l.new(b,q.inputs[2]);return q.outputs[0]
def scan(pattern,scale):
 tc=n.new('ShaderNodeVectorMath');tc.operation='SCALE';tc.inputs[3].default_value=scale;l.new(geo.outputs['Position'],tc.inputs[0]);tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(next((OUT/'textures').glob(pattern))),check_existing=True);tex.projection='BOX';tex.projection_blend=.3;l.new(tc.outputs[0],tex.inputs[0]);return tex.outputs[0]
mask=mathnode('SUBTRACT',1,ramp(pos.outputs['Z'],water_z+1.1,water_z+4.2))
rock=scan('rocky_terrain_diff_2k.*',.23);mud=scan('brown_mud_02_diff_2k.*',.35)
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=.7;noise.inputs['Detail'].default_value=5;l.new(geo.outputs['Position'],noise.inputs[0])
colour=blend(mud,rock,ramp(noise.outputs['Fac'],.35,.7))
tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.32,.29,.24,1);l.new(colour,tint.inputs[1])
old=bs.inputs['Base Color'].links[0].from_socket;l.new(blend(old,tint.outputs[0],mask),bs.inputs['Base Color'])
wet=mathnode('SUBTRACT',1,ramp(pos.outputs['Z'],water_z-.12,water_z+.55))
rough=n.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.82;rough.inputs['To Max'].default_value=.28;l.new(wet,rough.inputs['Value']);l.new(rough.outputs[0],bs.inputs['Roughness'])
layers=n.new('ShaderNodeTexWave');layers.bands_direction='Z';layers.inputs['Scale'].default_value=3.2;layers.inputs['Distortion'].default_value=7;layers.inputs['Detail Scale'].default_value=.65;l.new(geo.outputs['Position'],layers.inputs['Vector'])
bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.09;l.new(mask,bump.inputs['Strength']);l.new(layers.outputs['Color'],bump.inputs['Height']);l.new(bs.inputs['Normal'].links[0].from_socket,bump.inputs['Normal']);l.new(bump.outputs[0],bs.inputs['Normal'])
# White transmissive surface plus a real absorbing volume provides depth colour.
mat=bpy.data.materials['River_water'];nt=mat.node_tree;n,l=nt.nodes,nt.links;n.clear()
out=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled');bs.inputs['Base Color'].default_value=(.96,.985,.98,1);bs.inputs['Roughness'].default_value=.055;bs.inputs['IOR'].default_value=1.333;bs.inputs['Transmission Weight'].default_value=1;l.new(bs.outputs[0],out.inputs['Surface'])
absorb=n.new('ShaderNodeVolumeAbsorption');absorb.inputs['Color'].default_value=(.28,.62,.49,1);absorb.inputs['Density'].default_value=.14;l.new(absorb.outputs[0],out.inputs['Volume'])
tc=n.new('ShaderNodeTexCoord');stretch=n.new('ShaderNodeVectorMath');stretch.operation='MULTIPLY';stretch.inputs[1].default_value=(.6,2.2,1);l.new(tc.outputs['Object'],stretch.inputs[0])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=2.3;noise.inputs['Detail'].default_value=3;noise.inputs['Roughness'].default_value=.65;l.new(stretch.outputs[0],noise.inputs['Vector'])
bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.028;bump.inputs['Strength'].default_value=.4;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],bs.inputs['Normal'])
solid=water.modifiers.new('Closed_water_volume','SOLIDIFY');solid.thickness=12;solid.offset=-1
for image in bpy.data.images:
 if image.source!='FILE' or image.packed_file:continue
 matches=list(SRC.glob('*/textures/'+Path(image.filepath.replace('\\','/')).name))
 if matches:image.filepath=str(matches[0]);image.reload()
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V017 CANDIDATE; river optics and banks require visual and independent review'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
report={'file':dest.name,'source':'environment_v016.blend','status':'candidate_pending_visual_review','protected_walk_ramp_height_change_m':float(np.max(np.abs(z-before)[protected])),'blocked_bank_max_relief_m':float(np.max(np.abs(z-before))),'bank_boulders_replaced':replaced,'water_level_unchanged_m':water_z,'water_volume_depth_m':12,'canonical_xy_unchanged':True,'remaining':['river macro outline','routes','forest density','outer landscape','base scale','independent review']}
(OUT/'environment_v017_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=64;scene.cycles.use_denoising=True;scene.cycles.max_bounces=10;scene.cycles.transmission_bounces=8;scene.render.resolution_x=1200;scene.render.resolution_y=900
for name in ['Mid_River','River_Eye_Level']:
 scene.camera=bpy.data.objects[name];scene.render.filepath=str(OUT/f'environment_v017_{name}.png');bpy.ops.render.render(write_still=True)
