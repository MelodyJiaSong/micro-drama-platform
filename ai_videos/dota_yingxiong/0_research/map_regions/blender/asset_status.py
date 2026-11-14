"""Read actual artifacts and hash-bound QC, publish a local inspection index."""
from pathlib import Path
import json,hashlib,datetime,html,os,urllib.parse,subprocess,re
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest()
def link(p):return urllib.parse.quote(os.path.relpath(p,OUT).replace('\\','/'),safe='/')
def main():
    manifest=json.loads((OUT/'asset_manifest.json').read_text(encoding='utf-8'));rows=[];cards=[]
    draftpath=OUT/'draft_refresh_state.json';draftdata=json.loads(draftpath.read_text(encoding='utf-8')) if draftpath.exists() else {};pins_path=OUT/'draft_asset_selection.json';pins=json.loads(pins_path.read_text(encoding='utf-8')).get('assets',{}) if pins_path.exists() else {}
    for a in manifest['assets']:
        folder=ROOT/a['model_directory'];options=sorted(folder.glob('r*/inspection/'+a['id']+'_*.blend'));accepted=[];latest_review=None
        for blend in options:
            review=blend.parent/'independent_review.json'
            if not review.exists():continue
            r=json.loads(review.read_text(encoding='utf-8'))
            if blend==options[-1]:latest_review=r
            if r.get('verdict')=='pass' and r.get('blend_sha256')==sha(blend):
                evidence=r.get('evidence_files',[])
                if evidence and all((ROOT/e['path']).exists() and sha(ROOT/e['path'])==e['sha256'] for e in evidence):accepted.append(blend)
        latest=options[-1] if options else None
        status='已通过独立检查' if accepted else '待修正' if latest_review and latest_review.get('verdict')=='fail' else '候选待检查' if latest else '尚未生成可检查模型'
        row={'id':a['id'],'name':a['name'],'kind':a['kind'],'status':status,'accepted':str(accepted[-1].relative_to(ROOT)) if accepted else None,'latest_candidate':str(latest.relative_to(ROOT)) if latest else None,'latest_review':latest_review.get('verdict') if latest_review else None,'blockers':latest_review.get('blockers',[]) if latest_review else []};rows.append(row)
        title=html.escape(a['name']);ref=ROOT/(a['views'].get('front') or a['anchor'])['path'];img=f'<img loading="lazy" src="{link(ref)}" alt="参考设计">';candidate=f'<img loading="lazy" src="{link(latest.parent/"perspective.png")}" alt="候选模型">' if latest else '<div class="empty">等待本地生成</div>'
        details=''.join('<li>'+html.escape(str(b))+'</li>' for b in row['blockers'])
        files=f'<a href="{link(latest)}">Blender 候选文件</a>' if latest else ''
        if latest_review:files+=f' · <a href="{link(latest.parent/"independent_review.json")}">独立检查记录</a>'
        if a['id'] in pins and not accepted:
            row['pinned_draft_revision']=pins[a['id']]['revision'];files+=f'<br>地图草稿固定使用 {html.escape(pins[a["id"]]["revision"])}；这不代表验收通过。'
        cards.append(f'<article data-kind="{a["kind"]}"><h2>{title}</h2><p class="state">{status}'+(f' · {latest.parent.parent.name}' if latest else '')+f'</p><div class="pair"><figure>{img}<figcaption>参考设计</figcaption></figure><figure>{candidate}<figcaption>当前候选，未通过时不作成品</figcaption></figure></div><p>{files}</p>'+('<details><summary>检查问题</summary><ul>'+details+'</ul></details>' if details else '')+'</article>')
    batch=json.loads((OUT/'batch_full_models_v1.json').read_text(encoding='utf-8'));env=sorted(OUT.glob('environment_v*.blend'));assembly=sorted(OUT.glob('assembly_working_v*.blend'));accepted_count=sum(bool(r['accepted']) for r in rows);candidate_count=sum(bool(r['latest_candidate']) for r in rows);now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    active_asset=None if batch['status']=='candidates_generated_pending_review' else batch.get('active_asset')
    report={'at':now,'status':'in_progress','total_asset_families':len(rows),'families_with_candidates':candidate_count,'accepted_families':accepted_count,'active_batch_asset':active_asset,'batch_status':batch['status'],'latest_environment':env[-1].name if env else None,'latest_assembly':assembly[-1].name if assembly else None,'assets':rows}
    matching=next((d for d in reversed(draftdata.get('drafts',[])) if d.get('file')==report['latest_assembly']),None);report['latest_assembly_environment']=matching.get('environment') if matching else None;report['active_map_environment']=draftdata.get('active_environment');report['latest_environment_acceptance']='candidate_only'
    (OUT/'current_status.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    batch_label=active_asset or '首轮候选生成完成'
    header=f'<h1>DotA 6.83d · 本地三维制作检查</h1><p>范围：地图、建筑、常驻 NPC；英雄、绑定与动画另做。未使用 Hyper3D。</p><p class="summary">{candidate_count}/{len(rows)} 类有候选 · {accepted_count}/{len(rows)} 类通过独立检查 · 当前批次 {html.escape(str(batch_label))}</p><p>文件存在不代表交付完成。以下逐项展示参考与当前候选。</p>'
    if assembly:header+=f'<p><a href="{link(assembly[-1])}">最新整图工作文件（未验收）</a></p>'
    if report['latest_assembly_environment']:header+=f'<p>该整图实际使用：{html.escape(report["latest_assembly_environment"])}。最新环境试验：{html.escape(report["latest_environment"] or "无")}，需另行检查后才合入。</p>'
    page='<!doctype html><html lang="zh"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DotA 三维制作检查</title><style>body{margin:0;background:#131817;color:#e4e9e6;font:16px/1.6 system-ui}main{max-width:1400px;margin:auto;padding:32px}h1{font-size:30px}h2{font-size:20px}.summary,.state{color:#d9c891}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:20px}article{background:#202724;border:1px solid #3b4540;border-radius:12px;padding:20px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:10px}figure{margin:0}img,.empty{width:100%;height:300px;object-fit:contain;background:#151a18}figcaption{font-size:13px;color:#aab8af}a{color:#9bd2bd}details{font-size:14px}.empty{display:grid;place-items:center;color:#85948b}li{margin-bottom:8px}@media(max-width:500px){main{padding:16px}section{grid-template-columns:1fr}img,.empty{height:240px}}</style><main>'+header+'<section>'+''.join(cards)+'</section><p>更新时间 '+html.escape(now)+'</p></main></html>'
    (OUT/'inspection_index.html').write_text(page,encoding='utf-8')
    statepath=OUT/'production_state.json';state=json.loads(statepath.read_text(encoding='utf-8'));state.update(at=now,status='in_progress',accepted_detailed_assets=accepted_count,candidate_asset_families=candidate_count,current_environment=report['latest_assembly_environment'] or report['active_map_environment'],latest_environment=report['latest_environment'],latest_assembly=report['latest_assembly'],active_stage=('All 59 candidates generated; individual repairs and map inspection continue' if batch['status']=='candidates_generated_pending_review' else 'Local batch generation and individual repair; detailed final map not accepted'),current_status='current_status.json',inspection_index='inspection_index.html')
    for key in ['attempted_asset','active_prompt_id','active_job_completed','generation_seconds','candidate_blend','candidate_quality','quality_report','independent_review']:state.pop(key,None)
    running=[]
    query="[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; @(Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(python|blender)\\.exe$' -and $_.CommandLine -match 'map_regions|dota-local-3d-287' } | Select-Object ProcessId,Name,CommandLine) | ConvertTo-Json -Compress"
    snapshot=subprocess.run(['powershell','-NoProfile','-Command',query],capture_output=True,text=True,encoding='utf-8',check=True,creationflags=subprocess.CREATE_NO_WINDOW)
    processes=json.loads(snapshot.stdout or '[]');processes=processes if isinstance(processes,list) else [processes]
    for proc in processes:
        scripts=re.findall(r'[^\\/\s\"]+\.py',proc['CommandLine'] or '')
        if scripts and proc['ProcessId']!=os.getpid():running.append({'pid':proc['ProcessId'],'script':scripts[0],'program':proc['Name']})
    scheduler=next((p['pid'] for p in running if p['script']=='batch_model_assets.py'),None)
    state['scheduler']={'status':batch['status'],'name':'full_models_v1','pid':scheduler};state['batch']={'pid':scheduler,'state':'batch_full_models_v1.json'};state['active_processes']=running;state['active_jobs']={role:next((p['pid'] for p in running if p['script']==script),None) for role,script in [('scheduler','batch_model_assets.py'),('review_watcher','review_batch_candidates.py'),('comfy_launcher','start_comfy.py')]};statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
    checkpoint=OUT/'authoring_checkpoint.json'
    if checkpoint.exists():state['followup']=json.loads(checkpoint.read_text(encoding='utf-8')).get('followup',state.get('followup'))
    launcher=state['active_jobs'].get('comfy_launcher')
    if launcher and state.get('server',{}).get('pid')!=launcher:
        state.setdefault('server',{})['previous_pid']=state['server'].get('pid');state['server']['pid']=launcher
    elif not launcher and batch['status']=='candidates_generated_pending_review':
        server=state.setdefault('server',{})
        if server.get('pid'):server['previous_pid']=server['pid']
        server.update(pid=None,status='task_server_stopped_after_completed_batch')
    draft_state=OUT/'draft_refresh_state.json'
    if draft_state.exists():state['active_map_environment']=json.loads(draft_state.read_text(encoding='utf-8')).get('active_environment','environment_v013.blend')
    state['latest_environment_acceptance']='candidate_only; existence does not imply visual or independent acceptance'
    state['current_environment']=report['latest_assembly_environment'] or report['active_map_environment'];state['latest_assembly_environment']=report['latest_assembly_environment']
    statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='assets'},ensure_ascii=False))
if __name__=='__main__':main()
