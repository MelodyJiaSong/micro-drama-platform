"""Record an actual author image comparison; this is never independent asset QC."""
from pathlib import Path
import argparse,json,hashlib,datetime
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d/lod_libraries'
p=argparse.ArgumentParser();p.add_argument('assets',nargs='+');p.add_argument('--version',default='overview_v004');p.add_argument('--status',choices=['usable_for_map_preview','rejected_visual_regression'],required=True);p.add_argument('--notes',required=True);args=p.parse_args()
for aid in args.assets:
 folder=OUT/args.version/aid;row={'at':datetime.datetime.now().astimezone().isoformat(),'status':args.status,'scope':'Author source/LOD comparison for map overview only. Not independent acceptance, not a close-shot quality claim.','coincident_weld':True,'boundary_protection':True,'notes':args.notes,'images':[{'file':n,'sha256':hashlib.sha256((folder/n).read_bytes()).hexdigest()} for n in ['source_comparison.png','lod_comparison.png']]};(folder/'comparison_author_check.json').write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf-8');print('AUTHOR_LOD_CHECK',aid,args.status)
