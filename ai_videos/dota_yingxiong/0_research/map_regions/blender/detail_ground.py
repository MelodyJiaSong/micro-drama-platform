"""Small terrain relief and camera-dependent dense grass for close map shots."""
from pathlib import Path
import bpy,json,math,base64,numpy as np
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v011.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v010.blend'));terrain=bpy.data.objects['Terrain_683d'].data;co=np.empty(len(terrain.vertices)*3,np.float32);terrain.vertices.foreach_get('co',co);co=co.reshape(1025,1025,3);before=co[:,:,2].copy();x,y=co[:,:,0],co[:,:,1]
grid=json.loads((ROOT/'0_research/map_regions/navigation/grid.json').read_text());cells=np.frombuffer(base64.b64decode(grid['cells_base64']),np.uint8).reshape(512,512);ii=np.minimum(np.arange(1025)//2,511);codes=cells[::-1][ii[:,None],ii[None,:]]
noise=.045*np.sin(x*.79+y*.38)*np.cos(y*.91-x*.24)+.025*np.sin(x*1.63+y*.61)+.04*np.sin(x*.21-y*.32);noise*=np.where(codes&16,.18,1);noise*=np.clip((before+6.6)/2,0,1);co[:,:,2]+=noise;terrain.vertices.foreach_set('co',co.ravel());terrain.update();z=co[:,:,2]
def sample(x,y,arr=z):
    u,v=np.clip((x+409.6)/.8,0,1023.999),np.clip((y+409.6)/.8,0,1023.999);i,j=np.asarray(u,dtype=int),np.asarray(v,dtype=int);a,b=u-i,v-j
    return (arr[j,i]*(1-a)+arr[j,i+1]*a)*(1-b)+(arr[j+1,i]*(1-a)+arr[j+1,i+1]*a)*b
for cname in ['02_Forest','03_Asset_Placement','06_Undergrowth','07_Cliff_Relief','08_Meadow_Growth','09_Ground_Stones','13_Fallen_Timber','16_Forest_understorey']:
    for o in bpy.data.collections[cname].objects:
        px,py=o.location[:2];o.location.z+=float(sample(px,py)-sample(px,py,before))
# The early abstract ribbons were only authored scatter, not canonical map objects.
bpy.data.collections['06_Undergrowth'].hide_render=True;bpy.data.collections['06_Undergrowth'].hide_viewport=True
attrs={}
for name in ['Grass','Blight','ForestFloor','Paving']:
    a=np.empty(len(terrain.vertices),np.float32);terrain.attributes[name].data.foreach_get('value',a);attrs[name]=a.reshape(1025,1025)
rng=np.random.default_rng(11011);gy,gx=np.gradient(z,.8);points=[];scales=[];rotations=[]
for batch in range(4):
    n=2000000;px=rng.uniform(-408,408,n);py=rng.uniform(-408,408,n);i=np.clip(((px+409.6)/.8).astype(int),0,1023);j=np.clip(((py+409.6)/.8).astype(int),0,1023)
    g,b,f,p=[attrs[k][j,i] for k in ['Grass','Blight','ForestFloor','Paving']];prob=g*(.68-.28*f)*(1-b);valid=(rng.random(n)<prob)&(p<.25)&(z[j,i]>-5.7)&(np.hypot(gx[j,i],gy[j,i])<.65);px,py,i,j=px[valid],py[valid],i[valid],j[valid];zz=sample(px,py);points.append(np.column_stack((px,py,zz-.008)).astype(np.float32));s=rng.uniform(.8,1.65,len(px));scales.append(np.repeat(s,3).astype(np.float32));rot=np.zeros((len(px),3),np.float32);rot[:,2]=rng.uniform(0,math.tau,len(px));rotations.append(rot.ravel())
    print('DENSE_GRASS_BATCH',batch,len(px),flush=True)
points=np.concatenate(points);ob=bpy.data.objects['Living_ground_grass'];old=ob.data;me=bpy.data.meshes.new('Close_grass_points');me.vertices.add(len(points));me.vertices.foreach_set('co',points.ravel());me.update();ob.data=me
for name,data in [('clump_scale',np.concatenate(scales)),('clump_rotation',np.concatenate(rotations))]:
    a=me.attributes.new(name,'FLOAT_VECTOR','POINT');a.data.foreach_set('vector',data)
ng=ob.modifiers[0].node_group;n,l=ng.nodes,ng.links;inst=next(x for x in n if x.type=='INSTANCE_ON_POINTS');camera=n.new('GeometryNodeInputActiveCamera');info=n.new('GeometryNodeObjectInfo');l.new(camera.outputs[0],info.inputs['Object']);position=n.new('GeometryNodeInputPosition');distance=n.new('ShaderNodeVectorMath');distance.operation='DISTANCE';l.new(info.outputs['Location'],distance.inputs[0]);l.new(position.outputs[0],distance.inputs[1]);test=n.new('ShaderNodeMath');test.operation='LESS_THAN';test.inputs[1].default_value=110;l.new(distance.outputs['Value'],test.inputs[0]);l.new(test.outputs[0],inst.inputs['Selection'])
# Blend several metres of darker wet earth next to the river into the existing PBR.
wet=np.clip((-4.8-z)/2,0,1);a=terrain.attributes.new('RiverWetness','FLOAT','POINT');a.data.foreach_set('value',wet.astype(np.float32).ravel());mat=bpy.data.materials['Continuous_ground'];nt=mat.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');old=bs.inputs['Base Color'].links[0].from_socket;wetnode=nt.nodes.new('ShaderNodeAttribute');wetnode.attribute_name='RiverWetness';mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[2].default_value=(.28,.34,.26,1);nt.links.new(wetnode.outputs['Fac'],mix.inputs[0]);nt.links.new(old,mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V011 CANDIDATE; fine authored relief <= 0.11m, camera-dependent grass within 110m'
bpy.data.orphans_purge(do_recursive=True);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report={'file':dest.name,'status':'candidate_pending_review','ground_grass_points':len(points),'grass_camera_radius_m':110,'max_added_relief_m':float(np.abs(noise).max()),'max_ramp_added_relief_m':float(np.abs(noise)[(codes&16)!=0].max()),'canonical_xy_unchanged':True,'terrain_basis':'v009 restored original path heights; v011 adds bounded authored surface relief for realism','disabled':'06_Undergrowth early abstract scatter; canonical doodads remain'};(OUT/'environment_v011_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
