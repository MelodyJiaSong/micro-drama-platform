"""Keep the source's submerged vertices while retaining the continuous bank sculpt."""
from pathlib import Path
import struct,json,numpy as np
from scipy.ndimage import zoom,gaussian_filter
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';raw=(ROOT/'0_research/base_layout_refs/war3map.w3e').read_bytes();off=13
n,=struct.unpack_from('<i',raw,off);off+=4+4*n;n,=struct.unpack_from('<i',raw,off);off+=4+4*n;w,h,ox,oy=struct.unpack_from('<iiff',raw,off);off+=16;expected=np.zeros((h,w),bool)
for j in range(h):
 for i in range(w):
  ground,water,flags,variation,cliff=struct.unpack_from('<HHBBB',raw,off+7*(j*w+i));waterz=(((water&0x3fff)-8192)/4-89.6-1024)/32;groundz=((cliff&15)-10)*4+(ground-8192)/128;expected[j,i]=bool(flags&64) and groundz<waterz
data=np.load(OUT/'bank_working_arrays_v026.npz');original=data['co'][:,:,2];codes=data['codes'];walk=(codes&1)!=0;z=np.load(OUT/'bank_sculpt_v028_heights.npy');start=z.copy()
horizontal=walk[:,1:]&walk[:,:-1];vertical=walk[1:,:]&walk[:-1,:];limx=np.maximum(np.abs(original[:,1:]-original[:,:-1]),.56);limy=np.maximum(np.abs(original[1:,:]-original[:-1,:]),.56)
for iteration in range(20):
 coarse=np.zeros((129,129),np.float32);coarse[expected]=np.minimum(-7.04-z[::8,::8][expected],0)
 if np.min(coarse)<-.001:z+=gaussian_filter(zoom(coarse,1025/129,order=1,grid_mode=False),sigma=.65,mode='nearest')
 for _ in range(12):
  diff=z[:,1:]-z[:,:-1];e=np.maximum(np.abs(diff)-limx,0)*np.sign(diff)*horizontal;z[:,1:]-=e*.24;z[:,:-1]+=e*.24
  diff=z[1:,:]-z[:-1,:];e=np.maximum(np.abs(diff)-limy,0)*np.sign(diff)*vertical;z[1:,:]-=e*.24;z[:-1,:]+=e*.24
miss=int(np.count_nonzero(z[::8,::8][expected]>=-6.8));assert miss==0,miss
excess=max(float(np.max((np.abs(z[:,1:]-z[:,:-1])-limx)[horizontal])),float(np.max((np.abs(z[1:,:]-z[:-1,:])-limy)[vertical])));assert excess<.01,excess
np.save(OUT/'bank_sculpt_v029_heights.npy',z.astype(np.float32));report={'source':'environment_v028.blend','status':'prepared_author_trial','method':'Restore all 885 submerged original W3E vertices with smoothly interpolated local bed lowering, retaining v028 curves and explicit adjacent-walk slope constraint','source_submerged_vertices':int(expected.sum()),'source_submerged_vertices_missing_after_regrade':miss,'adjacent_walk_max_grade_constraint_excess_m':excess,'grade_constraint':'abs(dz) <= max(original abs(dz),0.56m) per adjacent walkable 0.8m vertices; tolerance 0.01m','mean_water_level_m':-6.800000190734863,'maximum_local_lowering_from_v028_m':float(np.max(start-z)),'maximum_total_change_from_v026_m':float(np.max(np.abs(z-original))),'walk_vertex_max_total_change_m':float(np.max(np.abs(z-original)[walk])),'navigation_flags_and_xy_unchanged':True,'remaining':['Original dry vertices and continuous shoreline shape','Whole-map sampling after regrounding','Author image inspection and independent environment review']};(OUT/'bank_sculpt_v029_prepare.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
