"""Prepare sub-metre continuous rock relief outside protected walk/ramp margins."""
from pathlib import Path
import numpy as np,json
from scipy.ndimage import distance_transform_edt
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';data=np.load(OUT/'metric_terrain_v033.npz');z=data['heights'];codes=np.load(OUT/'bank_working_arrays_v026.npz')['codes'];gy,gx=np.gradient(z,.8);slope=np.hypot(gx,gy);clearance=distance_transform_edt((codes&17)==0)*.8
weight=np.clip((slope-.55)/.65,0,1)*np.clip((clearance-1.6)/1.2,0,1)*np.clip((z-data['water_mean_heights']+.35)/.5,0,1)
eligible=np.maximum.reduce([weight[:-1,:-1],weight[1:,:-1],weight[:-1,1:],weight[1:,1:]])>.015
j,i=np.nonzero(eligible);subj,subi=np.indices((4,4));fj=(j[:,None]*4+subj.ravel()).ravel();fi=(i[:,None]*4+subi.ravel()).ravel();a=fj*4097+fi;faces=np.column_stack((a,a+1,a+4098,a+4097));unique,inverse=np.unique(faces,return_inverse=True);jj,ii=np.divmod(unique,4097);u=ii/4;v=jj/4;ix=np.minimum(u.astype(int),1023);iy=np.minimum(v.astype(int),1023);du=u-ix;dv=v-iy
def sample(array):return (array[iy,ix]*(1-du)+array[iy,ix+1]*du)*(1-dv)+(array[iy+1,ix]*(1-du)+array[iy+1,ix+1]*du)*dv
x=ii*.2-409.6;y=jj*.2-409.6;height=sample(z);normal=np.column_stack((-sample(gx),-sample(gy),np.ones(len(x))));normal/=np.linalg.norm(normal,axis=1)[:,None];mask=sample(weight);mask=mask*mask*(3-2*mask)
detail=.13*np.sin(x*2.1+np.sin(y*1.3))*np.cos(height*3.6)+.08*np.cos(y*4.3-x*2.6+height*1.9)+.035*np.sin(x*9.1+y*7.7+height*8.3)+.07*np.sin(height*6.2+.8*np.sin(x*.7+y*.4))
offset=(.23+detail)*mask+.0015
vertices=np.column_stack((x,y,height))+normal*offset[:,None]
np.savez_compressed(OUT/'cliff_surface_relief_v034.npz',vertices=vertices.astype(np.float32),faces=inverse.reshape(-1,4).astype(np.int32),source_ij=np.column_stack((v,u)).astype(np.float32),relief_weight=mask.astype(np.float32))
report={'status':'prepared_author_trial_not_accepted','source':'environment_v033.blend','fine_surface_step_m':.2,'vertices':len(vertices),'quads':len(faces),'maximum_normal_offset_m':float(offset.max()),'minimum_protected_margin_m':1.6,'navigation_geometry_unchanged':True,'method':'Continuous sub-metre skin over steep blocked terrain, stratified and irregular normal relief; embedded edges and 1.6m protected walk/ramp margin','remaining':['Apply terrain materials and corner attributes','Check cliff-to-ground transitions','Render river eye and overview','Independent review']}
(OUT/'cliff_surface_relief_v034_prepare.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
