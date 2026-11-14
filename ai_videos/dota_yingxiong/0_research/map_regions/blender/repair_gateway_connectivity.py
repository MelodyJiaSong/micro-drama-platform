"""Isolated MeshFix connectivity trial, preserving disconnected accessories."""
from pathlib import Path
import sys, json, time, numpy as np, argparse
ROOT=Path(__file__).resolve().parents[3]
AUDIT=ROOT.parents[1]/'.audit/adhoc_agents/2026-10-27/dota-local-3d-287'
sys.path.insert(0,str(AUDIT/'python_deps'))
import pymeshfix
parser=argparse.ArgumentParser();parser.add_argument('--revision',default='r08',choices=['r08','r09']);args=parser.parse_args()
base=next(next(ROOT.glob('2_*')).glob('characters/*/m303_*/model_3d'));folder=base/args.revision;folder.mkdir(exist_ok=True)
if (folder/'repaired_geometry.npz').exists():raise FileExistsError(folder)
data=np.load(base/'r08/source_geometry.npz');start=time.monotonic()
repair=pymeshfix.PyTMesh();repair.load_array(data['vertices'],data['faces'])
before={'points':repair.n_points,'faces':repair.n_faces,'boundaries':repair.n_boundaries}
print('LOADED',before,flush=True)
repair.fix_connectivity()
connectivity={'points':repair.n_points,'faces':repair.n_faces,'boundaries':repair.n_boundaries}
print('CONNECTED',connectivity,flush=True)
component_removal=None
if args.revision=='r09':
    repair.remove_smallest_components();component_removal={'points':repair.n_points,'faces':repair.n_faces,'boundaries':repair.n_boundaries};print('LARGEST_BODY_COMPONENT',component_removal,flush=True)
filled=repair.fill_small_boundaries(nbe=128 if args.revision=='r08' else 0,refine=True)
if args.revision=='r09':
    print('CLEANING_INTERSECTIONS',flush=True);repair.clean(max_iters=3,inner_loops=3)
vertices,faces=repair.return_arrays()
np.savez_compressed(folder/'repaired_geometry.npz',vertices=vertices,faces=faces)
report={'status':'geometry_trial_not_visual_acceptance','source_revision':'r07',
        'tool':'pymeshfix '+pymeshfix.__version__,'reference':'https://pymeshfix.pyvista.org/_autosummary/pymeshfix.PyTMesh.html',
        'before':before,'after_connectivity':connectivity,'filled_boundary_loops':filled,
        'after':{'points':repair.n_points,'faces':repair.n_faces,'boundaries':repair.n_boundaries},
        'remove_smallest_components':args.revision=='r09','largest_component':component_removal,'global_voxel_remesh':False,'max_boundary_edges_filled':128 if args.revision=='r08' else 0,'intersection_cleaning_iterations':3 if args.revision=='r09' else 0,
        'elapsed_seconds':time.monotonic()-start,'remaining':['Transfer UV and hair masks','Ray-check measured holes','Visual comparison and independent QC']}
(folder/'connectivity_repair.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)
