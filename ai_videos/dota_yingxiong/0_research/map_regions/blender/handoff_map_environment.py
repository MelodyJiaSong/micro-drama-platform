"""Hand off an idle draft refresher without interrupting its active Blender render."""
from pathlib import Path
import argparse,json,subprocess,sys,time,datetime
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=next(ROOT.glob('2_*'))/'background/map_3d';AUDIT=ROOT.parents[1]/'.audit/adhoc_agents/2026-10-27/dota-local-3d-287'
p=argparse.ArgumentParser();p.add_argument('--old-pid',type=int,required=True);p.add_argument('--environment',required=True);p.add_argument('--revision',required=True);args=p.parse_args()
assert Path(args.environment).name==args.environment
assert (OUT/args.environment).exists() and (OUT/(Path(args.environment).stem+'_Map_Overview.png')).exists()
record={'at':datetime.datetime.now().astimezone().isoformat(),'old_pid':args.old_pid,'environment':args.environment,'status':'waiting_for_previous_render','selection_basis':'Author viewed environment overview and local previews; visual candidate only, independent acceptance pending'}
dest=AUDIT/('map_refresh_handoff_'+args.revision+'.json')
def save():dest.write_text(json.dumps(record,indent=2),encoding='utf-8')
save();deadline=time.monotonic()+3*3600
while time.monotonic()<deadline:
 state=json.loads((OUT/'draft_refresh_state.json').read_text(encoding='utf-8'))
 if state['status'] in ['assembling_draft','rendering_draft']:time.sleep(5);continue
 # Validate the exact process before stopping it. No unrelated Python session is touched.
 query=f"$p=Get-CimInstance Win32_Process -Filter 'ProcessId={args.old_pid}'; if ($p -and $p.CommandLine -match 'refresh_map_drafts.py') {{ Stop-Process -Id {args.old_pid}; Write-Output 'stopped_verified_refresher' }} elseif ($p) {{ throw 'PID belongs to another process' }} else {{ Write-Output 'already_exited' }}"
 result=subprocess.run(['powershell','-NoProfile','-Command',query],capture_output=True,text=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 with (AUDIT/('map_draft_refresh.'+args.revision+'.log')).open('w',encoding='utf-8') as out,(AUDIT/('map_draft_refresh.'+args.revision+'.err.log')).open('w',encoding='utf-8') as err:
  proc=subprocess.Popen([sys.executable,'-X','utf8',str(HERE/'refresh_map_drafts.py'),'--environment',args.environment],stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
 record.update(status='started_new_refresher',new_pid=proc.pid,previous_state=state['status'],previous_active_file=state.get('active_file'),stop_result=result.stdout.strip(),completed_at=datetime.datetime.now().astimezone().isoformat());save();print(json.dumps(record),flush=True);break
else:record['status']='handoff_timeout_previous_render_not_interrupted';save();raise TimeoutError(record['status'])
