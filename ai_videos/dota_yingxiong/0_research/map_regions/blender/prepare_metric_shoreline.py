"""Round metric shoreline contours while constraining walk grades and wet samples."""
from pathlib import Path
import json,struct,numpy as np
from scipy.ndimage import gaussian_filter,map_coordinates,distance_transform_edt,zoom,binary_dilation,binary_propagation
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
data=np.load(OUT/'metric_terrain_v032.npz');before=data['heights'].astype(float);water=data['water_mean_heights'];codes=np.load(OUT/'bank_working_arrays_v026.npz')['codes'];walk=(codes&1)!=0;ramp=(codes&16)!=0
j,i=np.indices(before.shape,dtype=float);x=i*.8-409.6;y=j*.8-409.6
distance=distance_transform_edt(before>=water)*.8
weight=np.clip((18-distance)/12,0,1);weight=weight*weight*(3-2*weight)
dx=1.7*np.sin(x*.085+y*.063)+.7*np.sin(y*.29-x*.16);dy=1.6*np.sin(y*.09-x*.06)+.6*np.sin(x*.25+y*.13)
target=map_coordinates(gaussian_filter(before,3),[j+dy/.8,i+dx/.8],order=1,mode='nearest')
delta=np.clip(target-before,-2.4,2.4)*weight;delta[walk]=np.clip(delta[walk],-.6,.6);delta[ramp]=np.clip(delta[ramp],-.4,.4);z=before+delta
raw=(ROOT/'0_research/base_layout_refs/war3map.w3e').read_bytes();off=13;n,=struct.unpack_from('<i',raw,off);off+=4+4*n;n,=struct.unpack_from('<i',raw,off);off+=4+4*n;w,h,ox,oy=struct.unpack_from('<iiff',raw,off);off+=16;wet=np.zeros((129,129),bool);sourcewater=np.empty((129,129))
for row in range(h):
 for col in range(w):
  ground,wa,flags,variation,cliff=struct.unpack_from('<HHBBB',raw,off+7*(row*w+col));gz=((ground-8192)/4+(cliff%16-10)*128)/20;wz=((wa%16384-8192)/4-89.6-1024)/20;wet[row,col]=bool(flags&64) and gz<wz;sourcewater[row,col]=wz
hx=walk[:,1:]&walk[:,:-1];hy=walk[1:]&walk[:-1];limx=np.maximum(np.abs(before[:,1:]-before[:,:-1]),.56);limy=np.maximum(np.abs(before[1:]-before[:-1]),.56)
for _ in range(24):
 correction=np.zeros((129,129));correction[wet]=np.minimum(sourcewater[wet]-.20-z[::8,::8][wet],0);z+=gaussian_filter(zoom(correction,1025/129,order=1),.65)
 for k in range(12):
  diff=z[:,1:]-z[:,:-1];ex=np.maximum(np.abs(diff)-limx,0)*np.sign(diff)*hx;z[:,1:]-=ex*.24;z[:,:-1]+=ex*.24
  diff=z[1:]-z[:-1];ex=np.maximum(np.abs(diff)-limy,0)*np.sign(diff)*hy;z[1:]-=ex*.24;z[:-1]+=ex*.24
missing=int(np.count_nonzero(z[::8,::8][wet]>=sourcewater[wet]));assert missing==0,missing
mask=data['water_cells'];low=z<water+.05;cells=low[:-1,:-1]|low[1:,:-1]|low[:-1,1:]|low[1:,1:];connected=binary_propagation(mask&cells,mask=cells&binary_dilation(mask,iterations=8));finalmask=mask|connected
excess=max(float(np.max((np.abs(z[:,1:]-z[:,:-1])-limx)[hx])),float(np.max((np.abs(z[1:]-z[:-1])-limy)[hy])));assert excess<.01,excess
np.savez_compressed(OUT/'metric_terrain_v033.npz',heights=z.astype(np.float32),water_cells=finalmask,water_mean_heights=water)
report=json.loads((OUT/'metric_terrain_v032_prepare.json').read_text());report.update(source='environment_v032.blend',status='prepared_author_trial_not_accepted',shoreline_method='2.4m low-pass relief with 0.6–2.4m contour warp within 18m of shore; source wet points and adjacent walk grades constrained',source_wet_missing_after_correction=missing,adjacent_walk_grade_excess_m=excess,maximum_height_change_m=float(np.abs(z-before).max()),walk_height_delta_m=float(np.abs(z-before)[walk].max()),added_connected_water_cells=int((finalmask&~mask).sum()),remaining=['Apply local water-relative shader','Reground scenery','Visual shoreline inspection','Independent QC'])
(OUT/'metric_terrain_v033_prepare.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
