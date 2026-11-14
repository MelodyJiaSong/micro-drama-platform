"""Add prepared continuous relief while retaining original terrain and nav geometry."""
from pathlib import Path
import bpy,json,numpy as np
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v034.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v033.blend'));data=np.load(OUT/'cliff_surface_relief_v034.npz');source=bpy.data.objects['Terrain_683d'].data;me=bpy.data.meshes.new('Continuous_blocked_cliff_surface_relief');me.from_pydata(data['vertices'].tolist(),[],data['faces'].tolist());coll=bpy.data.collections.new('18_Continuous_cliff_surfaces');bpy.context.scene.collection.children.link(coll);ob=bpy.data.objects.new('Continuous_blocked_cliff_surface_relief',me);coll.objects.link(ob);me.materials.append(bpy.data.materials['Continuous_ground'])
v,u=data['source_ij'].T;ix=np.minimum(u.astype(int),1023);iy=np.minimum(v.astype(int),1023);a=u-ix;b=v-iy
attributes=[]
for old in source.attributes:
 if old.domain!='POINT' or old.data_type!='FLOAT' or old.name.startswith('.'):continue
 values=np.empty(len(source.vertices),np.float32);old.data.foreach_get('value',values);values=values.reshape(1025,1025);sample=(values[iy,ix]*(1-a)+values[iy,ix+1]*a)*(1-b)+(values[iy+1,ix]*(1-a)+values[iy+1,ix+1]*a)*b
 attr=me.attributes.new(old.name,'FLOAT','POINT');attr.data.foreach_set('value',sample.astype(np.float32));attributes.append(old.name)
for p in me.polygons:p.use_smooth=True
solid=ob.modifiers.new('Embedded_rock_skin_thickness','SOLIDIFY');solid.thickness=.06;solid.offset=-1
scene=bpy.context.scene;scene['production_status']='CLIFF_RELIEF_V034_AUTHOR_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report=json.loads((OUT/'cliff_surface_relief_v034_prepare.json').read_text());report.update(file=dest.name,terrain_attributes_transferred=attributes,skin_thickness_m=.06,mean_water_level_m=-10.88);(OUT/'environment_v034_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SAVED_CONTINUOUS_CLIFF_RELIEF',flush=True)
scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.cycles.debug_use_compact_bvh=True;scene.render.use_simplify=True;scene.cycles.texture_limit_render='2048';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1200;scene.render.resolution_y=900
for name in ['River_Eye_Level','Map_Overview']:
 scene.camera=bpy.data.objects[name];scene.render.filepath=str(OUT/f'environment_v034_{name}.png');bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
