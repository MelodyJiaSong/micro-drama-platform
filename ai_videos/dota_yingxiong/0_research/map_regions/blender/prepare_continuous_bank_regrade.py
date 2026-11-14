"""Regrade bank transitions with explicit walk-edge slope constraints instead of frozen heights."""
from pathlib import Path
import numpy as np,json
from scipy.ndimage import gaussian_filter,distance_transform_edt,map_coordinates
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';data=np.load(OUT/'bank_working_arrays_v026.npz');co=data['co'];z=co[:,:,2];codes=data['codes'];walk=(codes&1)!=0;ramp=(codes&16)!=0
def smooth(a):a=np.clip(a,0,1);return a*a*(3-2*a)
distance=distance_transform_edt(z>=-6.8)*.8;weight=smooth((18-distance)/9)*smooth((z+10)/1.2)*smooth((1-z)/3)
x,y=co[:,:,0],co[:,:,1];j,i=np.indices(z.shape,dtype=np.float32);dx=2.5*np.sin(x*.12+y*.07)+1.1*np.sin(y*.24-x*.1);dy=2.7*np.sin(y*.13-x*.055)+1.1*np.sin(x*.22+y*.10)
target=map_coordinates(gaussian_filter(z,sigma=5,mode='nearest'),[j+dy/.8,i+dx/.8],order=1,mode='nearest');delta=np.clip(target-z,-3,3)*weight;delta[walk]=np.clip(delta[walk],-.8,.8);delta[ramp]=np.clip(delta[ramp],-.6,.6)
result=(z+delta).astype(np.float32)
# Keep adjacent walk vertices within the original grade, or a gentle 35-degree
# equivalent .7 rise/run. This constrains actual geometry, not just nav flags.
horizontal=walk[:,1:]&walk[:,:-1];vertical=walk[1:,:]&walk[:-1,:]
limx=np.maximum(np.abs(z[:,1:]-z[:,:-1]),.56);limy=np.maximum(np.abs(z[1:,:]-z[:-1,:]),.56)
for _ in range(120):
 diff=result[:,1:]-result[:,:-1];excess=np.maximum(np.abs(diff)-limx,0)*np.sign(diff)*horizontal;result[:,1:]-=excess*.24;result[:,:-1]+=excess*.24
 diff=result[1:,:]-result[:-1,:];excess=np.maximum(np.abs(diff)-limy,0)*np.sign(diff)*vertical;result[1:,:]-=excess*.24;result[:-1,:]+=excess*.24
excessx=float(np.max((np.abs(result[:,1:]-result[:,:-1])-limx)[horizontal]));excessy=float(np.max((np.abs(result[1:,:]-result[:-1,:])-limy)[vertical]));assert max(excessx,excessy)<.01
np.save(OUT/'bank_sculpt_v028_heights.npy',result)
report={'source':'environment_v027.blend','status':'prepared_author_trial','method':'Continuous bank regrade within original water corridor; 4m smoothing and 2–4m height-domain warp; walk elevations allowed at most 0.8m initial adjustment and ramp elevations 0.6m, followed by adjacent-walk grade constraint','navigation_flags_and_xy_unchanged':True,'walk_vertex_max_delta_m':float(np.max(np.abs(result-z)[walk])),'ramp_vertex_max_delta_m':float(np.max(np.abs(result-z)[ramp])),'adjacent_walk_max_grade_constraint_excess_m':max(excessx,excessy),'grade_constraint':'For each adjacent pair of walkable 0.8m vertices: abs(dz) <= max(original abs(dz),0.56m), tolerance 0.01m','changed_vertices':int(np.count_nonzero(np.abs(result-z)>.001)),'maximum_height_delta_m':float(np.max(np.abs(result-z))),'mean_water_level_m':-6.800000190734863,'warning':'Author trial; preserve path flags and constrain slopes, but visually inspect banks, reground all placements, and rerun map navigation sampling. This is not full collision acceptance.'}
(OUT/'bank_sculpt_v028_prepare.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
