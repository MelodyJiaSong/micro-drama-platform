"""Compare identical generated geometry under preserve and 1024 remesh processing."""
from pathlib import Path
import trimesh,numpy as np,json,hashlib,gc
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m1_Treant/model_3d'));result={'asset':'m1','scope':'topology_measurement_not_visual_acceptance','weld_precision_decimals':5,'revisions':{}}
for rev in ['r11','r16']:
 path=next((folder/rev).glob('*_processed_*.glb'));scene=trimesh.load(str(path),force='scene',process=False);meshes=[]
 for mesh in scene.geometry.values():
  _,inverse=np.unique(np.round(mesh.vertices,5),axis=0,return_inverse=True);faces=inverse[mesh.faces]
  degenerate=(faces[:,0]==faces[:,1])|(faces[:,0]==faces[:,2])|(faces[:,1]==faces[:,2]);faces=faces[~degenerate]
  edges=np.concatenate([faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]]]);edges.sort(axis=1)
  codes=edges[:,0].astype(np.uint64)*np.uint64(inverse.max()+1)+edges[:,1].astype(np.uint64);_,counts=np.unique(codes,return_counts=True)
  meshes.append({'source_vertices':len(mesh.vertices),'welded_vertices':int(inverse.max()+1),'faces':len(mesh.faces),'degenerate_faces_after_weld':int(degenerate.sum()),'boundary_edges':int((counts==1).sum()),'nonmanifold_edges':int((counts>2).sum())})
  del faces,edges,codes,counts,inverse;gc.collect()
 raw=next((folder/rev).glob('*_raw_*.glb'));result['revisions'][rev]={'processed_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'meshes':meshes}
 print(rev,json.dumps(meshes),flush=True);del scene;gc.collect()
result['identical_raw_geometry']=result['revisions']['r11']['raw_sha256']==result['revisions']['r16']['raw_sha256']
assert result['identical_raw_geometry']
(folder/'remesh_topology_comparison.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
