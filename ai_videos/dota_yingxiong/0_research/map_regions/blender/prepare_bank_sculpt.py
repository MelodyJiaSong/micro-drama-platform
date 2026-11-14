"""Prepare a height-only erosion trial; keep walk and ramp vertices exactly fixed."""
from pathlib import Path
import numpy as np,json
from scipy.ndimage import gaussian_filter,distance_transform_edt,map_coordinates
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
data=np.load(OUT/'bank_working_arrays_v026.npz');co=data['co'];z=co[:,:,2];codes=data['codes'];protected=(codes&(1|16))!=0
water=z<-6.8;distance=distance_transform_edt(~water)*.8;clearance=distance_transform_edt(~protected)*.8
def smooth(a):
 a=np.clip(a,0,1);return a*a*(3-2*a)
weight=smooth((clearance-.8)/3.2)*smooth((16-distance)/8)*smooth((z+11)/2)*smooth((1-z)/3)
x,y=co[:,:,0],co[:,:,1];j,i=np.indices(z.shape,dtype=np.float32)
dx=1.5*np.sin(x*.17+y*.08)+.9*np.sin(y*.31-x*.09)
dy=1.5*np.sin(y*.19-x*.065)+.8*np.sin(x*.29+y*.12)
rounded=gaussian_filter(z,sigma=3,mode='nearest')
target=map_coordinates(rounded,[j+dy/.8,i+dx/.8],order=1,mode='nearest')
rough=.12*np.sin(x*.8+np.sin(y*.31))*np.cos(y*.69)+.07*np.sin(x*1.67+y*1.19)
delta=np.clip(target-z,-2.1,2.1)*weight+rough*weight
delta[protected]=0;result=(z+delta).astype(np.float32)
assert np.array_equal(z[protected],result[protected])
np.save(OUT/'bank_sculpt_v027_heights.npy',result)
report={'source':'environment_v026.blend','status':'prepared_author_trial','method':'2.4m Gaussian bank rounding and multiscale horizontal domain warp of sampled heights; 0.8m to 4m fade away from walk/ramp vertices','protected_vertex_max_delta_m':float(np.max(np.abs(result-z)[protected])),'changed_vertices':int(np.count_nonzero(np.abs(result-z)>.001)),'maximum_height_delta_m':float(np.max(np.abs(result-z))),'xy_displacement_m':0,'warning':'Navigation cells are fixed, but shoreline shape, mesh slopes and new contacts require visual inspection; no acceptance implied.'}
(OUT/'bank_sculpt_v027_prepare.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
