"""Use the original W3E water-enabled cells instead of an unbounded map-wide slab."""
from pathlib import Path
import bpy,json,struct,hashlib,numpy as np
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v026.blend'
if dest.exists():raise FileExistsError(dest)
src=ROOT/'0_research/base_layout_refs/war3map.w3e';raw=src.read_bytes();off=13;n,=struct.unpack_from('<i',raw,off);off+=4+4*n;n,=struct.unpack_from('<i',raw,off);off+=4+4*n;w,h,ox,oy=struct.unpack_from('<iiff',raw,off);off+=16;assert (w,h)==(129,129)
flags=np.frombuffer(raw,offset=off,count=w*h*7,dtype=np.uint8).reshape(h,w,7)[:,:,4];enabled=(flags&64)!=0;cells=enabled[:-1,:-1]|enabled[1:,:-1]|enabled[:-1,1:]|enabled[1:,1:]
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v025.blend'));water=bpy.data.objects['River_surface'];old=water.data;level=float((water.matrix_world@old.vertices[0].co).z)
# 0.8m geometric surface samples inside the source's water-enabled cells.
mask=np.repeat(np.repeat(cells,8,axis=0),8,axis=1);j,i=np.nonzero(mask);a=j*1025+i;faces=np.column_stack((a,a+1,a+1026,a+1025));unique,inverse=np.unique(faces,return_inverse=True);jj,ii=np.divmod(unique,1025);x=(ox+ii*16)/20;y=(oy+jj*16)/20
waves=.018*np.sin((x*.62+y*.78)*2.5)+.009*np.sin((x*.85-y*.53)*5.1)+.004*np.sin(x*9.2+y*7.1);verts=np.column_stack((x,y,level+waves));me=bpy.data.meshes.new('W3E_bounded_rippled_water');me.from_pydata(verts.tolist(),[],inverse.reshape(-1,4).tolist());me.materials.append(bpy.data.materials['River_water']);me.update();water.data=me;water.matrix_world.identity()
for p in me.polygons:p.use_smooth=True
nt=me.materials[0].node_tree;bs=next(q for q in nt.nodes if q.type=='BSDF_PRINCIPLED');bs.inputs['Roughness'].default_value=.07
for q in nt.nodes:
 if q.type=='BUMP':q.inputs['Distance'].default_value=.012;q.inputs['Strength'].default_value=.35
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V026 CANDIDATE; original water cell bounds and physical ripples';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(OUT/'environment_v026_report.json').write_text(json.dumps({'file':dest.name,'source':'environment_v025.blend','status':'candidate_pending_author_review','water_source':str(src.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'cell_inclusion':'Any of four original W3E corner water-enable flags; land occludes the overlapping cell edges','enabled_source_cells':int(cells.sum()),'surface_vertices':len(verts),'surface_faces':len(faces),'mean_water_level_m':level,'ripple_height_range_m':[float(waves.min()),float(waves.max())],'terrain_navigation_and_anchors_unchanged':True,'remaining':['No claim of fixing 37 source wet vertices raised above water in terrain','Inspect original pool limits and shoreline contacts','Independent environment review']},indent=2),encoding='utf-8');print('BOUNDED_WATER_SAVED',flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.cycles.use_denoising=True;scene.cycles.debug_use_compact_bvh=True;scene.render.use_simplify=True;scene.cycles.texture_limit_render='2048';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1200;scene.render.resolution_y=900
for name in ['River_Eye_Level','Map_Overview']:
 scene.camera=bpy.data.objects[name];scene.render.filepath=str(OUT/f'environment_v026_{name}.png');bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
