"""Prepare current terrain and protected-path distances for scan placement."""
from pathlib import Path
import numpy as np
from scipy.ndimage import distance_transform_edt
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';data=np.load(OUT/'metric_terrain_v033.npz');z=data['heights'];codes=np.load(OUT/'bank_working_arrays_v026.npz')['codes'];gy,gx=np.gradient(z,.8);clearance=distance_transform_edt((codes&17)==0)*.8
np.savez_compressed(OUT/'cliff_embedding_fields.npz',z=z,gx=gx,gy=gy,clearance=clearance.astype(np.float32),water=data['water_mean_heights'],codes=codes);print('CLIFF_EMBEDDING_FIELDS_PREPARED')
