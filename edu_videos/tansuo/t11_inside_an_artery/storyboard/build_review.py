import json
from pathlib import Path

SB=Path(__file__).resolve().parent
board=json.loads((SB/'storyboard.json').read_text(encoding='utf-8'))
review={
    'title':board['title']+' · '+board['version'],'character':'edu_videos/tansuo t11_inside_an_artery',
    'updated':board['updated'],'notes':board['notes'],
    'sections':[{'id':scene['id'],'title':scene['location'],'layout':'wide',
                 'hint':f"{len(scene['shots'])}镜；估算{scene['total']}秒",
                 'items':[{'id':s['id'],'label':s['title'],'path':s['image']['path'],'kind':'image',
                           'desc':s['action']+'\n摄影：'+s['camera']+'\n分拍：'+s['beats']+'\n'+
                                  '\n'.join(f"{d['speaker']}：{d['text']}" for d in s['dialogue'])}
                          for s in scene['shots']]} for scene in board['scenes']]}
(SB/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf-8')
print('review.json已从现行分镜派生。')
