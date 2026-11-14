"""Compare source W3E water components to the current terrain, without modifying it."""
from pathlib import Path
import bpy,json,struct,hashlib,numpy as np,argparse,sys
parser=argparse.ArgumentParser();parser.add_argument('--environment',default='environment_v025.blend');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
assert Path(args.environment).name==args.environment
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';src=ROOT/'0_research/base_layout_refs/war3map.w3e';raw=src.read_bytes();off=13
n,=struct.unpack_from('<i',raw,off);off+=4+4*n;n,=struct.unpack_from('<i',raw,off);off+=4+4*n
w,h,ox,oy=struct.unpack_from('<iiff',raw,off);off+=16;assert (w,h)==(129,129)
expected=np.zeros((h,w),bool);flagged=expected.copy();water_z=np.zeros((h,w),float)
for j in range(h):
 for i in range(w):
  ground,water,flags,variation,cliff=struct.unpack_from('<HHBBB',raw,off+7*(j*w+i));layer=cliff&15;flagged[j,i]=bool(flags&64)
  # Compare the source in game units, independently of the Blender scale.
  water_z[j,i]=((water&0x3fff)-8192)/4-89.6-1024
  ground_z=(layer-10)*128+(ground-8192)/4
  expected[j,i]=bool(flags&64) and ground_z<water_z[j,i]
def components(mask):
 points={(int(j),int(i)) for j,i in zip(*np.nonzero(mask))};rows=[]
 while points:
  stack=[points.pop()];part=[]
  while stack:
   j,i=stack.pop();part.append((j,i))
   for p in [(j+1,i),(j-1,i),(j,i+1),(j,i-1)]:
    if p in points:points.remove(p);stack.append(p)
  if len(part)<4:continue
  xs=[p[1] for p in part];ys=[p[0] for p in part];rows.append({'vertices':len(part),'grid_bounds_xy':[min(xs),min(ys),max(xs),max(ys)],'metre_bounds_xy':[(ox+min(xs)*128)/20,(oy+min(ys)*128)/20,(ox+max(xs)*128)/20,(oy+max(ys)*128)/20]})
 return sorted(rows,key=lambda r:-r['vertices'])
bpy.ops.wm.open_mainfile(filepath=str(OUT/args.environment));me=bpy.data.objects['Terrain_683d'].data;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(1025,1025,3);surface=bpy.data.objects['River_surface'];level=float((surface.matrix_world@surface.data.vertices[0].co).z)
coverage=np.ones((129,129),bool);local_levels=np.full((129,129),level);metric=bool(bpy.context.scene.get('vertical_game_units_per_m')==20.)
if surface.data.name.startswith('W3E_bounded'):
 reportpath=OUT/(Path(args.environment).stem+'_report.json');level=json.loads(reportpath.read_text(encoding='utf-8'))['mean_water_level_m']
 points=np.empty(len(surface.data.vertices)*3,np.float32);surface.data.vertices.foreach_get('co',points);points=points.reshape(-1,3);indices=np.rint((points[:,:2]+409.6)/.8).astype(int);exact=np.all(indices%8==0,axis=1);coarse=indices[exact]//8;coverage[:]=False;coverage[coarse[:,1],coarse[:,0]]=True;local_levels[:]=level
 if metric:
  from mathutils import kdtree
  xy=points[exact,:2].astype(float);waves=.018*np.sin((xy[:,0]*.62+xy[:,1]*.78)*2.5)+.009*np.sin((xy[:,0]*.85-xy[:,1]*.53)*5.1)+.004*np.sin(xy[:,0]*9.2+xy[:,1]*7.1);means=points[exact,2]-waves;local_levels[coarse[:,1],coarse[:,0]]=means;tree=kdtree.KDTree(len(coarse))
  for index,(i,j) in enumerate(coarse):tree.insert((float(i),float(j),0),index)
  tree.balance()
  for j,i in zip(*np.nonzero(~coverage)):local_levels[j,i]=means[tree.find((float(i),float(j),0))[1]]
observed=(co[::8,::8,2]<local_levels)&coverage
report={'status':'read_only_diagnostic_not_visual_acceptance','source':str(src.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'format_reference':'https://github.com/stijnherfst/HiveWE/wiki/war3map.w3e-Terrain','source_flagged_water_vertices':int(flagged.sum()),'source_submerged_water_vertices':int(expected.sum()),'source_components':components(expected),'current_environment':'environment_v025.blend','current_water_level_m':level,'current_submerged_129_grid_vertices':int(observed.sum()),'current_components':components(observed),'source_wet_vertices_missing_in_current':int((expected&~observed).sum()),'current_wet_vertices_outside_source_mask':int((observed&~expected).sum()),'interpretation':'Source main river is an interior connected component with separate edge pools. Do not infer it must connect to map boundaries from the minimap alone. Counts are coarse vertex checks, not full shoreline shape, navigation or visual approval.','height_scale_note':'Current residual height was scaled by horizontal units_per_m=20 while cliff layers use 32 game units per vertical metre. This does not remove source wet vertices in the source-coordinate calculation, but should remain documented for future terrain refinement.'}
report['current_environment']=args.environment;report['coverage_method']='Original map-wide surface' if coverage.all() else 'Coarse terrain vertices covered by the actual bounded water mesh';report['underwater_terrain_without_water_surface']=int(((co[::8,::8,2]<local_levels)&~coverage).sum())
if metric:report['height_scale_note']='Horizontal, cliff layers, residual heights and source water now use 20 game units/metre; source wet mask is compared in original game units.';report['local_water_mean_range_m']=[float(local_levels[coverage].min()),float(local_levels[coverage].max())];report['water_height_sampling']='Actual bounded mesh samples minus known geometric ripples; uncovered coarse points use the nearest covered mean only to flag missing coverage.'
dest=OUT/('original_water_footprint_audit.json' if args.environment=='environment_v025.blend' else Path(args.environment).stem+'_water_footprint_audit.json')
if dest.exists():raise FileExistsError(dest)
dest.write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
