"""Validate and rebuild this shared asset library. Local files only; never generates media."""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import html
import json
import os
import re
import struct
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
AUDIT = REPO / '.audit/adhoc_agents/2026-10-22/xianxia-assets-20261022'
PRESENTATION_AUDIT = REPO / '.audit/adhoc_agents/2026-10-22/xianxia-nav-multiview'
IMAGE_PURPOSES = {
    'concept_anchor': '单张概念锚点',
    'object_anchor': '完整物件概念锚点',
    'living_type_anchor': '生灵种型形体设定',
    'bound_spirit_anchor': '依附载体的灵体设定',
    'mechanism_sequence': '功法因果过程示意；演示形体不登记为角色',
    'organization_insignia': '组织徽记；不代表建筑或全套服制',
    'environment_anchor': '场所概念锚点',
    'structure_diagram': '结构与状态示意',
    'spatial_mechanism': '阵法空间机制示意',
    'effect_process': '传播过程与效果参考；不是实体器物',
}

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary=path.with_name('.'+path.name+'.'+uuid.uuid4().hex+'.tmp')
    try:
        temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        temporary.replace(path)
    finally:
        if temporary.exists():temporary.unlink()

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def local(relative):
    p = (ROOT / relative).resolve()
    if not p.is_relative_to(ROOT):
        raise ValueError(f'Path outside library: {relative}')
    return p

def review_notes(value):
    if isinstance(value,str):return [value] if value else []
    if isinstance(value,list):return [note for item in value for note in review_notes(item)]
    if isinstance(value,dict):return [note for item in value.values() for note in review_notes(item)]
    return []

def reviews():
    found = {}
    receipt_path=PRESENTATION_AUDIT/'frozen_reviews.json'
    frozen=read(receipt_path) if receipt_path.exists() else {}
    for p in sorted([*(AUDIT/'spawns').glob('*/images.json'), *(PRESENTATION_AUDIT/'spawns').glob('*/images.json')]):
        report=p.parent/'output.md'
        if not report.is_file():continue
        if p.is_relative_to(PRESENTATION_AUDIT):
            receipt=frozen.get(p.parent.name)
            if not receipt or receipt['images_sha256']!=sha(p) or receipt['report_sha256']!=sha(report):continue
        envelope=report.read_text(encoding='utf-8').split('---',2)
        if len(envelope)<3 or not re.search(r'^status:\s*(complete|partial)\s*$',envelope[1],re.M):continue
        data=read(p)
        rows=data if isinstance(data,list) else data.get('images',data.get('reviews',[]))
        for row in rows:
            if row.get('sha256'):
                item=dict(row)
                item['evidence']=p.relative_to(REPO).as_posix()
                item['evidence_sha256']=sha(p)
                item['report_evidence']=report.relative_to(REPO).as_posix()
                item['report_sha256']=sha(report)
                found[(row['id'],row['sha256'])]=item
    registry = ROOT / 'qc/review_runs.json'
    if registry.is_file():
        for receipt in read(registry)['reviews']:
            evidence = REPO / receipt['images']
            report = REPO / receipt['report']
            if not evidence.is_file() or not report.is_file():
                continue
            if sha(evidence) != receipt['images_sha256'] or sha(report) != receipt['report_sha256']:
                continue
            envelope = report.read_text(encoding='utf-8').split('---', 2)
            if len(envelope) < 3 or not re.search(r'^status:\s*(complete|partial)\s*$', envelope[1], re.M):
                continue
            for row in read(evidence)['images']:
                if not row.get('sha256'):
                    continue
                found[(row['id'], row['sha256'])] = dict(row, evidence=receipt['images'], evidence_sha256=receipt['images_sha256'], report_evidence=receipt['report'], report_sha256=receipt['report_sha256'])
    return found

def adopt_approved_revisions(jobs, evidence):
    path=ROOT/'revision_jobs.json'
    if not path.exists():return
    revisions=read(path);byid={j['id']:j for j in jobs['jobs']}
    for r in revisions['jobs']:
        output=local(r['output'])
        if not output.exists():
            receipt=AUDIT/'revision_runs'/f"{r['id']}_v{r['attempt']}.json"
            if receipt.exists():r['status']=read(receipt)['status']
            continue
        digest=sha(output);review=evidence.get((r['id'],digest))
        r['sha256']=digest
        r['status']='generated_unreviewed' if not review else {'pass':'reviewed','pass_with_notes':'reviewed_with_notes','revise':'revision_required'}.get(review['verdict'],'generated_unreviewed')
        if not r['status'].startswith('reviewed') and (REPO/byid[r['id']]['output']).is_file():continue
        j=byid[r['id']];relative=output.relative_to(REPO).as_posix()
        current_attempt=max([1]+[prior['attempt'] for prior in revisions['jobs'] if prior['id']==r['id'] and (ROOT/prior['output']).relative_to(REPO).as_posix()==Path(j['output']).as_posix()])
        if r['attempt']<current_attempt:continue
        if Path(j['output']).as_posix()==relative:continue
        old=REPO/j['output']
        j.setdefault('history',[]).append({'output':j['output'],'prompt':j['prompt'],'sha256':sha(old) if old.exists() else None,'reason':r['reason']})
        j['output']=relative;j['prompt']=(ROOT/r['prompt']).relative_to(REPO).as_posix()
        event={'time':datetime.now(timezone.utc).isoformat(),'id':r['id'],'new_output':relative,'sha256':digest,'review_evidence':review['evidence'] if review else None,'action':'bind independently accepted revision; previous PNG preserved' if r['status'].startswith('reviewed') else 'bind missing-image recovery candidate; not yet accepted'}
        with (AUDIT/'revision_adoptions.jsonl').open('a',encoding='utf-8') as stream:stream.write(json.dumps(event,ensure_ascii=False)+'\n')
    revisions['status']='all_reviewed' if all(r['status'].startswith('reviewed') for r in revisions['jobs']) else 'in_progress'
    save(path,revisions)

def validate(lib, systems, jobs):
    errors=[]
    ids=[a['id'] for a in lib['assets']]
    if len(ids)!=len(set(ids)):errors.append('Duplicate asset IDs')
    known=set(ids)|{e['id'] for e in systems['events']}
    sources={r['id'] for r in read(ROOT/'research/sources.json')['sources']}
    roles=set(lib['relation_schema']['roles'])
    for a in lib['assets']:
        for key in ('version','name','category','function','cost_limit','counter_failure','visual_signature','activation','relations','relation_coverage','source_refs'):
            if key not in a:errors.append(f"{a['id']} missing {key}")
        prefix=a['id'].rstrip('0123456789')
        if prefix in systems['grade_semantics']['does_not_apply_to'] and a['grade'] is not None:errors.append(f"{a['id']} inappropriate grade")
        for rel in a['relations']:
            if rel['target'] not in known:errors.append(f"{a['id']} broken relation {rel['target']}")
            if rel['role'] not in roles:errors.append(f"{a['id']} unknown role {rel['role']}")
        if a['relation_coverage']=='partial' and not a['relations']:errors.append(f"{a['id']} empty partial coverage")
        for ref in a['source_refs']:
            if ref['id'] not in sources:errors.append(f"{a['id']} broken source {ref['id']}")
        image=a.get('image')
        if image and image['status'].startswith('reviewed'):
            path=local(image['anchor'])
            if not path.is_file() or sha(path)!=image['sha256']:errors.append(f"{a['id']} stale image review")
    template=read(ROOT/'adoption_template.json')
    for key in systems['adoption_contract']['required']:
        if key not in template:errors.append(f'Template missing {key}')
    for chain in systems['production_chains']:
        for target in chain['materials']+chain['tools']+[chain['site'],chain['output']]:
            if target not in known:errors.append(f"{chain['id']} unknown {target}")
    jobids=[j['id'] for j in jobs['jobs']]
    if set(jobids)!=set(ids) or len(jobids)!=len(ids):errors.append('Jobs and assets are not 1:1')
    for j in jobs['jobs']:
        p=REPO/j['prompt']
        if not p.is_file():errors.append(f"{j['id']} missing prompt")
    navigation=lib.get('navigation',[])
    if navigation:
        assigned=[key for g in navigation for s in g['children'] for key in s['asset_ids']]
        if len(assigned)!=len(set(assigned)) or set(assigned)!=set(ids):errors.append('Navigation must assign each asset exactly once')
        for g in navigation:
            if not g['children'] or not re.search(r'[\u4e00-\u9fff]',g['name']):errors.append(f"Invalid navigation group {g['id']}")
            for s in g['children']:
                if not s['asset_ids'] or not re.search(r'[\u4e00-\u9fff]',s['name']):errors.append(f"Invalid navigation subgroup {s['id']}")
    for a in lib['assets']:
        v=a.get('views')
        if v and v.get('sha256') and (not local(v['sheet']).is_file() or sha(local(v['sheet']))!=v['sha256']):errors.append(f"{a['id']} stale three-view sheet")
    errors.extend(validate_foundation(lib, systems))
    return errors


def validate_foundation(lib: dict, systems: dict) -> list[str]:
    foundation = systems.get('foundation')
    if not foundation:
        return []
    errors: list[str] = []
    assets = {a['id']: a for a in lib['assets']}
    profiles = {p['id'] for p in foundation['profiles']}
    dimensions = {d['id'] for d in foundation['dimensions']}
    template = read(ROOT / 'adoption_template.json')
    selection = template.get('foundation_selection', {})
    contracts = {c['id']: c for c in foundation.get('operational_contracts', [])}
    configuration = template.get('operational_contracts', {}).get('configuration', {})
    for cid, contract in contracts.items():
        if not contract.get('rules') or not contract.get('cases'):
            errors.append(f'{cid} missing operational rules or pressure cases')
        for field in contract['required_fields']:
            if field not in configuration.get(cid, {}):
                errors.append(f'{cid} missing adoption field {field}')
        for aid in contract['asset_ids']:
            if aid not in assets:
                errors.append(f'{cid} unknown operational asset {aid}')
            elif cid not in assets[aid].get('operational_contracts', []):
                errors.append(f'{aid} missing reverse contract link {cid}')
    for aid, asset in assets.items():
        for cid in asset.get('operational_contracts', []):
            if cid not in contracts or aid not in contracts[cid]['asset_ids']:
                errors.append(f'{aid} invalid operational contract {cid}')
    for key in foundation['adoption_fields']:
        if key not in selection:
            errors.append(f'Adoption template missing foundation field {key}')
    for dimension in foundation['dimensions']:
        if set(dimension['systems']) != profiles:
            errors.append(f"{dimension['id']} incomplete system coverage")
        for profile, cell in dimension['systems'].items():
            if not cell['branches']:
                errors.append(f"{profile}/{dimension['id']} missing branches")
            for aid in cell['asset_ids']:
                if aid not in assets:
                    errors.append(f"{profile}/{dimension['id']} unknown asset {aid}")
    navigation = {key for group in lib['navigation'] for child in group['children'] for key in child['asset_ids']}
    for asset in lib['assets']:
        meta = asset.get('foundation')
        if not meta:
            continue
        aid = asset['id']
        if meta['profile'] not in profiles or meta['dimension'] not in dimensions:
            errors.append(f'{aid} unknown foundation classification')
        cells = [d['systems'].get(meta['profile'], {}) for d in foundation['dimensions'] if d['id'] == meta['dimension']]
        if not cells or aid not in cells[0].get('asset_ids', []) or aid not in navigation:
            errors.append(f'{aid} absent from foundation matrix or navigation')
        for axis, values in meta.get('technique', {}).items():
            allowed = foundation['technique_axes'].get(axis, [])
            values = [values] if isinstance(values, str) else values
            if not values or any(value not in allowed for value in values):
                errors.append(f'{aid} invalid technique axis {axis}')
        organization = meta.get('organization')
        if organization:
            for key in foundation['organization_contract']['required']:
                if not organization.get(key):
                    errors.append(f'{aid} missing organization field {key}')
            if organization['kind'] == 'faction':
                hosts = organization.get('host_ids', [])
                if not hosts or any(assets.get(host, {}).get('foundation', {}).get('organization', {}).get('kind') not in ('sect', 'lineage', 'institution') for host in hosts):
                    errors.append(f'{aid} faction requires a real host organization')
    return errors

def refresh(lib,jobs):
    evidence=reviews();byid={a['id']:a for a in lib['assets']};accepted=[]
    adopt_approved_revisions(jobs,evidence)
    for j in jobs['jobs']:
        a=byid[j['id']];p=REPO/j['output'];receipt=REPO/j['receipt'] if j.get('receipt') else AUDIT/'image_runs'/f"{j['id']}.json"
        state='planned';digest=None;review=None
        if p.is_file():
            digest=sha(p);state='generated_unreviewed'
            review=evidence.get((j['id'],digest))
            if review:
                state={'pass':'reviewed','pass_with_notes':'reviewed_with_notes','revise':'revision_required'}.get(review['verdict'],'generated_unreviewed')
                accepted.append(review)
        elif receipt.is_file():
            state={'started':'in_progress','failed_or_unknown':'failed_or_unknown'}.get(read(receipt).get('status'),'planned')
        a['image']={'anchor':p.relative_to(ROOT).as_posix(),'prompt':(REPO/j['prompt']).relative_to(ROOT).as_posix(),'status':state,'purpose':a.get('foundation',{}).get('image_role','concept_anchor'),'sha256':digest}
        if j.get('pending_replacement'):
            a['image']['pending_replacement'] = j['pending_replacement']
        if review:
            a['image']['review_notes']=review_notes(review.get('issues',review.get('notes',[])))
            a['image']['review_evidence']=review['evidence']
        if p.is_file():
            with p.open('rb') as stream:header=stream.read(24)
            if header[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError(f'Not a PNG: {p}')
            a['image']['actual_dimensions']=list(struct.unpack('>II',header[16:24]))
        if j.get('history'):a['image']['history']=j['history']
        j['status']=state
    presentation=ROOT/'presentation_jobs.json'
    view_reviews=[];view_candidates={}
    if presentation.exists():
        for task in read(presentation)['jobs']:
            if task['kind']!='three_view_sheet':continue
            output=local(task['output']); digest=sha(output) if output.is_file() else None
            row=evidence.get((task['id'],digest)); receipt=REPO/task['receipt'] if task.get('receipt') else PRESENTATION_AUDIT/'receipts'/(task['key']+'.json')
            state='generated_unreviewed' if digest else {'started':'in_progress','failed_or_unknown':'failed_or_unknown'}.get(read(receipt)['status'],'planned') if receipt.exists() else 'planned'
            if row:
                state={'pass':'reviewed','pass_with_notes':'reviewed_with_notes','revise':'revision_required'}[row['verdict']]
            view={'sheet':task['output'],'prompt':task['prompt'],'sha256':digest,'status':state,'panels':task['panels'],'orientation':task['orientation'],'review_notes':review_notes(row.get('issues',row.get('notes',[]))) if row else []}
            if row:view['review_evidence']=row['evidence']
            if digest:
                with output.open('rb') as stream:header=stream.read(24)
                if header[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError(f'Not a PNG: {output}')
                view['actual_dimensions']=list(struct.unpack('>II',header[16:24]))
            view_candidates.setdefault(task['id'],[]).append(view)
        for aid,candidates in view_candidates.items():
            approved=[v for v in candidates if v['status'].startswith('reviewed')]
            generated=[v for v in candidates if v['sha256']]
            chosen=(approved or generated or candidates)[-1]
            byid[aid]['views']=chosen
            if evidence.get((aid,chosen['sha256'])):view_reviews.append(evidence[(aid,chosen['sha256'])])
    save(ROOT/'qc/images.json',{'scope':'Matching current PNG hashes only; unreviewed images never count as accepted.','images':accepted,'three_view_sheets':view_reviews})
    save(ROOT/'library.json',lib);save(ROOT/'image_jobs.json',jobs)

def systems_md(s):
    lines=['# 公共世界规则 · '+s['version'],'','由 `systems.json` 生成。名称可选，能力与边界均为本库设计。','','## 修炼进阶','','| ID | 境界 | 新增能力 | 限制 | 突破门槛 |','|---|---|---|---|---|']
    for r in s['realms']:lines.append(f"| {r['id']} | {r['name']} | {r['new_capability']} | {r['limit']} | {r['promotion_gate']} |")
    lines+=['','凡人是基线，基础修仙八阶；真仙至大罗为默认关闭的仙域扩展。渡劫为考验事件，飞升为跨界事件。炼体、熟练度另计，不折算成境界。','','## 品阶与相性','',s['grade_semantics']['meaning'],'',s['grade_semantics']['operator_rule'],'','| ID | 品阶 | 作用/承载层级 |','|---|---|---|']
    for g in s['item_grades']:lines.append(f"| {g['id']} | {g['name']} | {g['scope']} |")
    lines+=['','品质：'+ ' / '.join(s['quality'])+'。稀有度：'+' / '.join(s['rarity'])+'。完整度：'+' / '.join(s['condition'])+'。这些轴互不替代。','',s['elements']['note'],'','相生：木→火→土→金→水→木。相克：木→土→水→火→金→木。属性色只帮助识别属性，不表示品质。','','## 能源、储物与经济','']
    lines+=['- '+r for r in s['energy']['rules']+s['economy']['rules']]
    lines+=['','## 六条示范生产链','','每条都是部分设计；数量、损耗、工具负载和产量仍要由采用剧配置。','','| 链 | 输入 | 工具/场所 | 产物 | 副产物与检验 |','|---|---|---|---|---|']
    for c in s['production_chains']:lines.append(f"| {c['id']} {c['name']} | {', '.join(c['materials'])} | {', '.join(c['tools'])} / {c['site']} | {c['output']} | {c['byproducts']}；{c['checks']} |")
    lines+=['','## 跨剧采用契约','',s['adoption_contract']['null_rules'],'',s['adoption_contract']['quantities'],'','采用字段：'+', '.join(s['adoption_contract']['required'])+'。','',s['adoption_contract']['promotion_to_shot'],'','## 基础原则','']
    lines+=['- '+r for r in s['principles']]
    lines.extend(foundation_md(s.get('foundation')))
    (ROOT/'systems.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


def foundation_md(foundation: dict | None) -> list[str]:
    if foundation is None:
        return []
    lines = ['', '## 三体系 Foundation', '', foundation['provenance'], '', '### 身份与边界', '']
    lines.extend('- ' + rule for rule in foundation['identity_rules'])
    for profile in foundation['profiles']:
        lines += ['', '### ' + profile['name'], '', '| 维度 | 定义 |', '|---|---|']
        for key, label in [('basis', '族源/传承基础'), ('energy', '能源'), ('talent', '资质'), ('progression', '进阶'), ('society', '社会'), ('visual', '视觉'), ('failure', '代价与失效')]:
            lines.append(f"| {label} | {profile[key]} |")
    lines += ['', '### 大类与子类矩阵', '', '每格先列子类，括号内为已有代表资产ID。子类定义完整不等于每个子类已有条目或图片；已有仙家资产复用原ID。', '', '| 维度 | 仙家 | 妖族 | 魔族 |', '|---|---|---|---|']
    for dimension in foundation['dimensions']:
        cells = []
        for profile in foundation['profiles']:
            cell = dimension['systems'][profile['id']]
            cells.append('、'.join(cell['branches']) + '（' + '、'.join(cell['asset_ids']) + '）')
        lines.append('| ' + dimension['name'] + ' | ' + ' | '.join(cells) + ' |')
    lines += ['', '### 功法的正交分类', '', foundation['technique_axes']['rule'], '', '| 分类轴 | 可选值 |', '|---|---|']
    for key, values in foundation['technique_axes'].items():
        if isinstance(values, list):
            lines.append(f"| {key} | {'、'.join(values)} |")
    lines += ['', foundation['technique_axes']['mastery_rule']]
    for profile in foundation['profiles']:
        track = foundation['progression_tracks'][profile['id']]
        lines += ['', '### ' + profile['name'] + '进阶口径', '', track['rule']]
        if track.get('steps'):
            lines += ['', '| 里程碑 | 获得能力 | 验证条件 | 持续限制 |', '|---|---|---|---|']
            lines.extend('| ' + ' | '.join(step) + ' |' for step in track['steps'])
    lines += ['', '### 组织契约', '', foundation['organization_contract']['rule'], '']
    lines.extend('- ' + value for value in foundation['organization_contract']['kinds'].values())
    lines += ['', '每个组织填写：' + '、'.join(foundation['organization_contract']['required']) + '。', '', '### 跨体系兼容', '', '| 接口 | 规则 |', '|---|---|']
    lines.extend(f"| {row['topic']} | {row['rule']} |" for row in foundation['cross_system_rules'])
    if foundation.get('operational_contracts'):
        lines += ['', '### 组合操作与制度契约', '', foundation['operational_contract_rule']]
        for contract in foundation['operational_contracts']:
            lines += ['', '#### ' + contract['id'] + ' · ' + contract['name'], '', '适用资产：' + '、'.join(contract['asset_ids']), '', '采用前填写：' + '、'.join(contract['required_fields'])]
            lines += ['', *['- ' + rule for rule in contract['rules']], '', '压力测试：', *['- ' + case for case in contract['cases']]]
    lines += ['', '### 采用与完成边界', '', foundation['adoption_rule'], '', '补充采用字段：' + '、'.join(foundation['adoption_fields']) + '。', '', '图片、动作视频和具体剧采用各自验收。当前独立深审见 qc/deep_review.json；历史审查仅对应各自记录的指纹。']
    return lines

def cards(lib):
    names={a['id']:a['name'] for a in lib['assets']}
    sources={r['id']:r for r in read(ROOT/'research/sources.json')['sources']}
    for a in lib['assets']:
        i=a['image'];folder=local(i['anchor']).parent
        text=[f"# {a['id']} · {a['name']}",'','由 library.json 生成；修改主数据后运行 maintenance.py --refresh。','',f"版本：{a['version']}｜类别：{a['category']}｜品阶：{a['grade'] or '不适用'}",'',f"功能：{a['function']}",'',f"触发：{a['activation']['trigger']}",'',f"使用条件：{a['activation']['requirement']}",'',f"代价 / 边界：{a['cost_limit']}",'',f"失效 / 克制：{a['counter_failure']}",'',f"外观识别：{a['visual_signature']}",'',a['parameters'],'','## 图像','',f"状态：{i['status']}；用途：{IMAGE_PURPOSES.get(i.get('purpose'), i.get('purpose', '单张概念锚点'))}。",'',f"[Prompt]({Path(i['prompt']).name})"]
        if i['sha256']:text += ['',f"![概念锚点]({Path(i['anchor']).name})",'',f"SHA256：`{i['sha256']}`"]
        if i.get('review_notes'):text+=['','### 概念验收备注','']+['- '+note for note in i['review_notes']]
        if i.get('pending_replacement'):text+=['','### 待完成修订','',i['pending_replacement']['reason']]
        if a.get('operational_contracts'):
            system_path=Path(os.path.relpath(ROOT/'systems.md',folder)).as_posix()
            text+=['','### 操作契约','','采用本项前核对 [组合操作与制度契约]('+system_path+')：'+ '、'.join(a['operational_contracts'])+'。空值不视为可用。']
        if a.get('production_notes'):text+=['','### 制作与操作说明','']+['- '+note for note in a['production_notes']]
        if a.get('views'):
            v=a['views'];text+=['','## 正面、侧面、背面三视图','',f"状态：{v['status']}。左起依次为{'、'.join(v['panels'])}。",'',f"[三视图描述]({Path(v['prompt']).name})"]
            if v['sha256']:text+=['',f"![正面、侧面、背面]({Path(v['sheet']).name})",'',f"SHA256：`{v['sha256']}`"]
            text += ['',v['orientation']]+['- '+n for n in v['review_notes']]
        text+=['','## 状态设计','']+['- '+k+'：'+v for k,v in a['state_design'].items()]
        if a.get('material_handling'):text+=['','## 材料保管','']+['- '+k+'：'+v for k,v in a['material_handling'].items()]
        text+=['','## 关联','',f"覆盖：{a['relation_coverage']}；不构成完整制造清单。"]
        for r in a['relations']:text+=['',f"- {r['role']}：{r['target']} {names.get(r['target'],'系统事件')}；{'必需' if r['required'] else '可选实例'}；{r['note']}"]
        text+=['','## 出处范围','',a['origin']]
        for r in a['source_refs']:
            src=sources[r['id']]
            text+=['',f"- [{r['id']}]({src['url']})：{r['supports']}"]
        if not a['source_refs']:text+=['','本项没有单独的文献归属；类别文化背景见研究报告，不为具体能力背书。']
        meta = a.get('foundation')
        if meta:
            text += ['', '## Foundation 分类', '', f"体系：{meta['profile']}；维度：{meta['dimension']}；实体：{meta['entity_kind']}。", '', meta['media_policy']]
            if meta.get('identity_note'):
                text += ['', meta['identity_note']]
            for section in ('technique', 'organization'):
                if meta.get(section):
                    text += ['', '### ' + ('功法分类' if section == 'technique' else '组织制度'), '', '| 字段 | 定义 |', '|---|---|']
                    for key, value in meta[section].items():
                        text.append(f"| {key} | {('、'.join(value) if isinstance(value, list) else value)} |")
        (folder/'card.md').write_text('\n'.join(text)+'\n',encoding='utf-8')

HTML=r'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>仙侠公共资产库</title>
<style>:root{color-scheme:dark;--bg:#101816;--panel:#1b2722;--text:#ece7d8;--muted:#a5b3a7;--gold:#d4b97b}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.65 system-ui,"Microsoft YaHei",sans-serif}header,main,footer{max-width:1480px;margin:auto;padding:30px 4vw}header{padding-top:48px}small,.muted{color:var(--muted)}h1{font-size:clamp(30px,4vw,52px);font-weight:500;letter-spacing:.08em;margin:8px 0}h2{font-weight:500}a{color:var(--gold)}.bar{display:flex;gap:12px;flex-wrap:wrap;align-items:center}input,select,button{font:inherit;border:1px solid #405447;border-radius:8px;padding:10px 14px;background:#14221c;color:var(--text)}input{flex:1;min-width:250px}button{cursor:pointer}button:hover{border-color:var(--gold)}.stats{display:flex;gap:30px;flex-wrap:wrap;margin:24px 0}.stat b{display:block;font-size:28px;font-weight:500;color:var(--gold)}nav{display:flex;gap:22px;flex-wrap:wrap}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(245px,1fr));gap:20px;margin-top:24px}.card{background:var(--panel);border:1px solid #304036;border-radius:12px;overflow:hidden;cursor:pointer}.card:hover{border-color:var(--gold)}.card img,.empty{width:100%;height:210px;object-fit:contain;background:#d6d7ce}.empty{display:flex;align-items:center;justify-content:center;color:#435248}.card .body{padding:16px}.card h3{font-size:19px;margin:0 0 6px;font-weight:500}.tag{display:inline-block;font-size:12px;border:1px solid #526653;border-radius:5px;padding:1px 6px;margin-top:8px;color:#b6c8b3}.warn{color:#e6be74;border-color:#98743b}dialog{width:min(1100px,94vw);max-height:92vh;background:var(--panel);color:var(--text);border:1px solid #576652;border-radius:14px;padding:24px}dialog::backdrop{background:#000b}.detail{display:grid;grid-template-columns:1fr 1fr;gap:24px}.detail img{width:100%;max-height:70vh;object-fit:contain;background:#c9cdc4}.detail dt{color:var(--gold);margin-top:14px}.detail dd{margin:0}pre{white-space:pre-wrap;word-break:break-all;font:12px/1.5 monospace}.close{float:right}.pages{display:flex;justify-content:center;gap:20px;margin:30px}.note{border-left:3px solid var(--gold);padding-left:15px;color:var(--muted)}@media(max-width:720px){.detail{grid-template-columns:1fr}.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.card img,.empty{height:160px}.card .body{padding:10px}.card h3{font-size:16px}header,main,footer{padding-left:18px;padding-right:18px}}</style>
<header><small>世界规则 / 物件 / 空间 / 视觉参考 · v1.0.0</small><h1>仙侠公共资产库</h1><p>为多部剧复用而建。按 ID 固定外形和机制，再为每部剧配置边界与数值。</p><div id="stats" class="stats"></div><nav><a href="systems.md">世界规则</a><a href="research/report.md">研究报告</a><a href="appendix.md">术语与采用手册</a><a href="visual_guide.md">视觉规范</a><a href="library.json">主数据 JSON</a><a href="qc/deep_review.md">\u6df1\u5ea6\u5ba1\u67e5\u4e0e\u6574\u6539</a><a href="qc/images.json">逐图验收</a></nav><p class="note">基础图是概念锚点，建筑与场景另附正面、侧面、背面三面板设定图。未审图不计验收通过；不是三维模型或已完成的镜头资料包。来源支持背景，具体能力是本库设计。</p></header>
<main><div class="bar"><input id="q" aria-label="搜索资产" placeholder="搜索名称、ID、能力或别名，例如：重瞳、筑基、藏经阁"><select id="cat" aria-label="资产类别"><option value="">全部类别</option></select><select id="state" aria-label="验收状态"><option value="">全部图像状态</option><option value="reviewed">已验收</option><option value="generated_unreviewed">已出图待审</option><option value="revision_required">需修订</option><option value="planned">尚未出图</option></select></div><p id="count" class="muted" aria-live="polite"></p><div id="grid" class="grid"></div><div class="pages"><button id="prev">上一页</button><span id="page"></span><button id="next">下一页</button></div></main><footer><small id="stamp"></small></footer><dialog id="modal"><button class="close" id="close">关闭</button><div id="detail"></div></dialog>
<script id="data" type="application/json">__DATA__</script><script>
const data=JSON.parse(document.getElementById('data').textContent),assets=data.assets;let page=0;const size=24,$=id=>document.getElementById(id),esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const labels={reviewed:'已验收',reviewed_with_notes:'已验收 · 有备注',generated_unreviewed:'已出图 · 待审',revision_required:'需修订',planned:'待生成',in_progress:'生成中',failed_or_unknown:'失败或结果未知'};
for(const c of data.categories){const o=document.createElement('option');o.value=c.name;o.textContent=c.name;$('cat').append(o)}
const generated=assets.filter(a=>a.image.sha256).length,accepted=assets.filter(a=>a.image.status.startsWith('reviewed')).length;
$('stats').innerHTML=[['资产定义',assets.length],['已生成图片',generated],['已验收图片',accepted],['研究来源',data.source_count]].map(([t,n])=>`<div class="stat"><b>${n}</b>${t}</div>`).join('');$('stamp').textContent='本地资料快照：'+data.generated_at+'。仅修改JSON主数据，再运行维护工具更新本页。';
function filtered(){const q=$('q').value.trim().toLowerCase(),c=$('cat').value,s=$('state').value;return assets.filter(a=>(!c||a.category===c)&&(!q||JSON.stringify([a.id,a.name,a.function,a.aliases,a.visual_signature,a.foundation]).toLowerCase().includes(q))&&(!s||(s==='reviewed'?a.image.status.startsWith(s):s==='planned'?['planned','in_progress','failed_or_unknown'].includes(a.image.status):a.image.status===s)))}
function render(){const list=filtered();page=Math.min(page,Math.max(0,Math.ceil(list.length/size)-1));$('count').textContent=`找到 ${list.length} 项；关系链中的“可选实例”不代表必须同时使用。`;$('grid').innerHTML=list.slice(page*size,(page+1)*size).map(a=>`<article class="card" tabindex="0" role="button" data-id="${a.id}" aria-label="查看 ${esc(a.name)}">${a.image.sha256?`<img loading="lazy" src="${esc(a.image.anchor)}" alt="${esc(a.name)} 概念锚点">`:'<div class="empty">概念已定义 · 图像待完成</div>'}<div class="body"><small>${a.id} · ${esc(a.category)}</small><h3>${esc(a.name)}</h3><div>${esc(a.function)}</div><span class="tag ${a.image.status.startsWith('reviewed')?'':'warn'}">${labels[a.image.status]||a.image.status}</span></div></article>`).join('');$('page').textContent=`${list.length?page+1:0} / ${Math.ceil(list.length/size)}`;$('prev').disabled=page===0;$('next').disabled=(page+1)*size>=list.length}
function detail(id){const a=assets.find(a=>a.id===id);if(!a)return;const pairs=[['\u5f85\u5b8c\u6210\u4fee\u8ba2',a.image.pending_replacement?.reason||'\u65e0'],['\u5236\u4f5c\u4e0e\u64cd\u4f5c\u8bf4\u660e',(a.production_notes||[]).join('\uff1b')||'\u65e0'],['\u64cd\u4f5c\u5951\u7ea6',(a.operational_contracts||[]).join(' / ')||'\u65e0'],['能力',a.function],['触发',a.activation.trigger],['使用条件',a.activation.requirement],['代价与限制',a.cost_limit],['克制与失效',a.counter_failure],['外观识别',a.visual_signature],['品阶',a.grade||'不适用'],['版本',a.version],['数值配置',a.parameters],['体系与维度',a.foundation?[a.foundation.profile,a.foundation.dimension].join(' / '):'既有公共资产'],['功法分类',a.foundation?.technique?Object.entries(a.foundation.technique).map(([k,v])=>k+'：'+(Array.isArray(v)?v.join('、'):v)).join('；'):'不适用'],['组织制度',a.foundation?.organization?Object.entries(a.foundation.organization).map(([k,v])=>k+'：'+(Array.isArray(v)?v.join('、'):v)).join('；'):'不适用'],['概念验收备注',(a.image.review_notes||[]).join('；')||'暂无']];$('detail').innerHTML=`<h2>${a.id} · ${esc(a.name)}</h2><p>${labels[a.image.status]}</p><div class="detail"><div>${a.image.sha256?`<a href="${esc(a.image.anchor)}" target="_blank"><img src="${esc(a.image.anchor)}" alt="${esc(a.name)}"></a>`:'<div class="empty">尚无图片</div>'}<p><a href="${esc(a.image.prompt)}">原始 Prompt</a> · <a href="${esc(a.image.anchor.replace(/[^/]+$/,'card.md'))}">资产卡</a></p><pre>SHA256: ${esc(a.image.sha256||'未生成')}</pre></div><div><dl>${pairs.map(([k,v])=>`<dt>${k}</dt><dd>${esc(v)}</dd>`).join('')}</dl><h3>关联 · ${esc(a.relation_coverage)}</h3>${a.relations.map(r=>`<p><a href="#" data-related="${r.target}">${esc(r.target)}</a> ${esc(r.role)} · ${r.required?'必需':'可选实例'}<br><small>${esc(r.note)}</small></p>`).join('')||(a.relation_coverage==='not_required'?'<p>无需人工组成关系。</p>':'<p>关联尚未建模；采用前需补所需生产或运行机制。</p>')}${a.material_handling?'<h3>材料保管</h3>'+Object.entries(a.material_handling).map(([k,v])=>`<p>${esc(k)}：${esc(v)}</p>`).join(''):''}<h3>出处范围</h3><p>${esc(a.origin)}</p>${a.source_refs.map(r=>`<p>${esc(r.id)}：${esc(r.supports)}</p>`).join('')}</div></div>`;if(a.views){const v=a.views;$('detail').innerHTML+=`<section><h3>正面 · 侧面 · 背面</h3><p>${labels[v.status]||v.status} · 左起依次${esc(v.panels.join('、'))}</p>${v.sha256?`<a href="${esc(v.sheet)}" target="_blank"><img style="width:100%;height:auto" src="${esc(v.sheet)}" alt="${esc(a.name)} 三视图"></a>`:'<p>三视图正在制作</p>'}<p>${esc((v.review_notes||[]).join('；'))}</p></section>`}if(!$('modal').open)$('modal').showModal()}
for(const id of ['q','cat','state'])$(id).addEventListener('input',()=>{page=0;render()});$('prev').onclick=()=>{page--;render()};$('next').onclick=()=>{page++;render()};$('grid').onclick=e=>{const c=e.target.closest('[data-id]');if(c)detail(c.dataset.id)};$('grid').onkeydown=e=>{if(e.key==='Enter'){const c=e.target.closest('[data-id]');if(c)detail(c.dataset.id)}};$('detail').onclick=e=>{const link=e.target.closest('[data-related]');if(link){e.preventDefault();detail(link.dataset.related)}};$('close').onclick=()=>$('modal').close();render();
</script></html>'''

def build(lib,systems,jobs):
    stamp=datetime.now(timezone.utc).isoformat()
    counts=Counter(a['image']['status'] for a in lib['assets'])
    manifest={'version':lib['version'],'generated_at':stamp,'assets':len(lib['assets']),'categories':dict(Counter(a['category'] for a in lib['assets'])),'image_status':dict(counts),'images_generated':sum(bool(a['image']['sha256']) for a in lib['assets']),'images_accepted':sum(v for k,v in counts.items() if k.startswith('reviewed')),'relations':sum(len(a['relations']) for a in lib['assets']),'research_sources':len(read(ROOT/'research/sources.json')['sources']),'source_of_truth':['library.json','systems.json','research/sources.json','image_jobs.json'],'audit_root':AUDIT.relative_to(REPO).as_posix(),'limits':['单图概念锚点，不是多角度或三维模型','相机空间与规模需具体剧补','无剧情、人物、声音或视频','未审图不计验收通过']}
    manifest['png_files']=len(list(ROOT.rglob('*.png')))
    if (ROOT/'presentation_jobs.json').exists():manifest['source_of_truth'].append('presentation_jobs.json')
    manifest['audit_roots']=[AUDIT.relative_to(REPO).as_posix(),PRESENTATION_AUDIT.relative_to(REPO).as_posix()]
    deep_review=ROOT/'qc/deep_review.json'
    if deep_review.exists():
        audit=read(deep_review).get('audit')
        if audit:manifest['audit_roots'].append(audit)
    manifest['navigation_groups']=len(lib.get('navigation',[]))
    manifest['navigation_subgroups']=sum(len(g['children']) for g in lib.get('navigation',[]))
    views=[a['views'] for a in lib['assets'] if a.get('views')]
    manifest['three_view_sheets']={'required':len(views),'generated':sum(bool(v['sha256']) for v in views),'accepted':sum(v['status'].startswith('reviewed') for v in views),'status':dict(Counter(v['status'] for v in views))}
    manifest['limits'][0]='概念锚点与建筑场景三面设定图；不是三维模型或已完成镜头素材包'
    manifest['anchor_dimensions']=dict(Counter('x'.join(map(str,a['image']['actual_dimensions'])) for a in lib['assets'] if a['image'].get('actual_dimensions')))
    manifest['category_progress']={}
    for category in manifest['categories']:
        group=[a for a in lib['assets'] if a['category']==category]
        manifest['category_progress'][category]={'defined':len(group),'generated':sum(bool(a['image']['sha256']) for a in group),'accepted':sum(a['image']['status'].startswith('reviewed') for a in group),'statuses':dict(Counter(a['image']['status'] for a in group))}
    save(ROOT/'manifest.json',manifest)
    systems_md(systems);cards(lib)
    category_order={c['prefix']:i for i,c in enumerate(lib['categories'])}
    gallery_order=sorted(lib['assets'],key=lambda a:(int(''.join(c for c in a['id'] if c.isdigit())),category_order[a['id'].rstrip('0123456789')]))
    payload=dict(lib,assets=gallery_order,generated_at=stamp,source_count=manifest['research_sources'])
    packed=json.dumps(payload,ensure_ascii=False).replace('<','\\u003c')
    (ROOT/'index.html').write_text(HTML.replace('__DATA__',packed).replace('· v1.0.0', '· v' + lib['version']),encoding='utf-8')
    lines=['# 当前完成与验收状态','',f"更新时间：{stamp}",'',f"资产定义 {manifest['assets']}；基础图已生成 {manifest['images_generated']}；基础图已验收 {manifest['images_accepted']}。",'','状态按当前 PNG SHA 计算。历史失败和旧版图片保留；概念审图通过不等于镜头资料包已就绪。','','| 基础图状态 | 数量 |','|---|---:|']
    lines += [f'| {k} | {v} |' for k,v in counts.items()]
    lines += ['',f"中文导航：{manifest['navigation_groups']} 大类 / {manifest['navigation_subgroups']} 小类。",'',f"建筑与场景三视图：应有 {len(views)}；已生成 {manifest['three_view_sheets']['generated']}；已验收 {manifest['three_view_sheets']['accepted']}。"]
    lines += ['','## 按类别覆盖','', '| 类别 | 定义 | 有图 | 已验收 |','|---|---:|---:|---:|']
    lines += [f"| {name} | {c['defined']} | {c['generated']} | {c['accepted']} |" for name,c in manifest['category_progress'].items()]
    lines += ['','## 需要继续处理的图片','']
    for a in lib['assets']:
        if a['image']['status'] in ('revision_required','failed_or_unknown'):
            lines.append(f"- {a['id']} {a['name']}：{a['image']['status']}。")
    lines+=['','## 三视图待处理项目','']
    for a in lib['assets']:
        v=a.get('views')
        if v and not v['status'].startswith('reviewed'):
            lines.append(f"- {a['id']} {a['name']}：{v['status']}。"+'；'.join(v.get('review_notes',[])))
    lines += ['','逐图意见见 `qc/images.json`；本轮独立深审与整改见 [深度审查](qc/deep_review.md)，历史文字审查见 `qc/semantic.json`。基础任务见 `image_jobs.json`，修订记录见 `revision_jobs.json`，补图与三视图任务见 `presentation_jobs.json`。','']
    (ROOT/'STATUS.md').write_text('\n'.join(lines),encoding='utf-8')
    return manifest

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--refresh',action='store_true')
    parser.add_argument('--require-images',action='store_true');parser.add_argument('--require-views',action='store_true');args=parser.parse_args()
    lib=read(ROOT/'library.json');systems=read(ROOT/'systems.json');jobs=read(ROOT/'image_jobs.json')
    if args.refresh:refresh(lib,jobs)
    errors=validate(lib,systems,jobs)
    if args.require_images:
        errors += [f"{a['id']} missing required image" for a in lib['assets'] if not a['image'].get('sha256') or not local(a['image']['anchor']).is_file()]
    if args.require_views:
        errors += [f"{a['id']} missing required front/side/back sheet" for a in lib['assets'] if (a['id'].startswith(('BG','LAND')) or a.get('foundation', {}).get('dimension') == 'places') and (not a.get('views',{}).get('sha256') or not local(a['views']['sheet']).is_file())]
    if errors:
        print('\n'.join(errors));raise SystemExit(1)
    if args.refresh:print(json.dumps(build(lib,systems,jobs),ensure_ascii=False,indent=2))
    else:print(f"OK: {len(lib['assets'])} IDs, typed references, grade applicability, adoption fields, prompts, current reviewed hashes")

if __name__=='__main__':main()
