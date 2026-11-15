import hashlib
import json
from pathlib import Path

SB = Path(__file__).resolve().parent
TOPIC = SB.parent
ROOT = TOPIC.parents[2]

def rel(path):
    return path.relative_to(ROOT).as_posix()

def build():
    plan_path = SB / 'shot_plan.json'
    plan = json.loads(plan_path.read_text(encoding='utf-8'))
    panels = {p['id']: p for p in json.loads((SB / 'panels.json').read_text(encoding='utf-8'))['panels']}
    source_sha = hashlib.sha256(plan_path.read_bytes()).hexdigest()
    scenes, ids = [], set()
    for scene in plan['scenes']:
        result = {k: v for k, v in scene.items() if k != 'shots'}
        result['shots'] = []
        for shot in scene['shots']:
            assert shot['id'] not in ids, f"重复镜号：{shot['id']}"
            ids.add(shot['id'])
            assert shot['duration_estimate'] > 0
            assert all(shot[f] and shot[f] != '—' for f in ('camera','blocking','action'))
            assert shot['cues'][0]['start'] == 0 and shot['cues'][-1]['end'] == shot['duration_estimate']
            assert all(a['end'] == b['start'] for a,b in zip(shot['cues'],shot['cues'][1:]))
            panel = panels[shot['panel']]
            diagram = SB / 'diagrams' / f"{shot['id']}.png"
            image = diagram if diagram.exists() else SB / panel.get('image', f"{panel['id']}.png")
            assert image.is_file(), f'缺参考图：{image}'
            kind = '本镜功能示意图' if diagram.exists() else f"{panel['id']}场景概念参考；非本镜已生成首帧"
            prompt = SB / 'shots' / f"{shot['id']}.txt"
            prompt.parent.mkdir(exist_ok=True)
            cues = '；'.join(f"{c['start']:g}–{c['end']:g}秒：{c['action']}" for c in shot['cues'])
            prompt.write_text('\n'.join([
                f"{shot['id']} {shot['title']}｜{scene['location']}",
                f"估算 {shot['duration_estimate']} 秒；须用正式音频校准。",kind,
                '摄影：'+shot['camera'],'调度：'+shot['blocking'],'分拍：'+cues,
                '转场：'+shot['transition'],'图形：'+shot['graphic'],
                '台词：'+' / '.join(f"{d['speaker']}：{d['text']}" for d in shot['dialogue']),
                '画面来源：'+panel['source'],'事实台账：'+', '.join(shot['claims']),
                '结构以研究模型重建；此为分镜设计，不是收费视频提交包。'
            ]),encoding='utf-8')
            result['shots'].append({
                'id':shot['id'],'key':shot['id'],'title':shot['title'],
                'duration':shot['duration_estimate'],'durationBasis':'estimate',
                'cast':shot['cast'],'dialogue':shot['dialogue'],
                'action':f"【{kind}】{shot['title']}：{shot['action']}",
                'blocking':shot['blocking'],'beats':'估算分拍：'+cues,
                'camera':shot['camera']+' 转场：'+shot['transition']+' 图形：'+shot['graphic']+' 画面来源：'+panel['source'],
                'image':{'path':rel(image),'mtime':image.stat().st_mtime_ns//1_000_000_000},
                'framePrompt':rel(prompt),'packPrompt':'','shotDir':rel(SB/'shots'),
                'note':'估算时长；'+kind,'sourcePanel':panel['id'],'claims':shot['claims']})
        result['total']=sum(s['duration'] for s in result['shots'])
        scenes.append(result)
    total=sum(s['total'] for s in scenes)
    board={
        'title':'探索 · 血脂 t11：血管里的小船','eyebrow':'教学视频 · 探索 · t11 分镜修订',
        'lang':'zh','version':plan['version'],'updated':plan['date'],'source_sha256':source_sha,
        'notes':[f"{plan['version']}：{len(scenes)}场、{len(ids)}镜，估算 {total//60}分{total%60:02d}秒。每张卡的秒数均为设计估算，尚未由配音实测。",
                 plan['image_policy'],'台词为分镜草稿。正式讲稿、双语台词审及整集音频听审后校准时长，再进入视频生成。',
                 '全片只有林和凯，父亲仅通过台词与单据出现。不作个人用药推荐。',
                 '比较图为假设算例：每组100人、同一5年、同一事件定义、相对风险减少20%；不是临床试验数据或个人预测。'],
        'links':[{'label':label,'path':rel(path)} for label,path in [
            ('镜头设计源',plan_path),('节拍',TOPIC/'beats.md'),('事实台账',TOPIC/'claims.json'),
            ('修订说明与复审',SB/'reviews/v3_resolution.json'),('v2审查',SB/'reviews/structure_r1.json')]],
        'scenes':scenes}
    (SB/'storyboard.json').write_text(json.dumps(board,ensure_ascii=False,indent=2),encoding='utf-8')
    voices={}
    for speaker,key in [('林','lin'),('阿凯','kai')]:
        voice=json.loads((TOPIC.parent/f'_shared/cast/{key}/voice.json').read_text(encoding='utf-8'))['voices']['zh']
        voices[speaker]={k:voice[k] for k in ('reference','reference_text')}
    manifest={'title':board['title'],'path':rel(TOPIC),'lang':'zh','voices':voices,'source_sha256':source_sha,
              'notes':[{'title':'分镜草稿','items':[plan['timing_basis']]}],
              'scenes':[{'id':s['id'],'title':s['location'],'subtitle':s['time'],
                         'shots':[{'id':x['id'],'title':x['title'],'image':x['image']['path'],
                                   'lines':[{'speaker':d['speaker'],'text':d['text']} for d in x['dialogue']]}
                                  for x in s['shots']]} for s in scenes]}
    (TOPIC/'audio/preview_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(scenes)}场，{len(ids)}镜，估算{total}秒；逐镜摄影/调度/分拍已检查。')

if __name__=='__main__':
    build()
