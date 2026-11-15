"""Adopt only independently passed current PNGs with immutable audit copies."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
SB=Path(__file__).resolve().parent
TOPIC=SB.parent
REV=TOPIC/'reviews/codex_takeover_r1'
AUD=ROOT/'.audit/adhoc_agents/2026-11-15/chip-takeover-057/spawns/text_review'
LEGACY=dict(zip(['P01','P02','P03','P04','P05','P06','P07','P08','P09','P10','P12','P13','P14','V18C'],
               ['chip_close','shrink_travel','solder_hall','package_exploded','die_city','wiring_city','signal_electrons','phone_blur','gate_array','transistor_wide','scale_guess','return','desk_recap','array_signal']))

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    approvals={}
    order=['frames_batch1.json','frames_batch2.json','frames_batch3.json','frames_legacy.json','frames_mechanism.json','frames_batch4.json','frames_batch5.json','frames_repairs.json','frames_final.json']
    for name in order:
        report=REV/name
        if not report.exists(): continue
        audit=AUD/name
        assert audit.exists() and sha(report)==sha(audit), f'Review audit differs: {name}'
        data=json.loads(report.read_text(encoding='utf-8'))
        for row in data['results']:
            if row['verdict']!='pass': continue
            raw=row['file'].replace('\\','/')
            path=ROOT/raw if raw.startswith('edu_videos/') else TOPIC/raw
            assert path.is_file() and sha(path)==row['sha256'],f'PNG differs: {path}'
            key=LEGACY.get(path.stem) or re.sub(r'_(?:math_)?r\d+$','',path.stem)
            approvals[key]={'path':path.relative_to(ROOT).as_posix(),'sha256':row['sha256'],'status':'pass',
                            'review':report.relative_to(ROOT).as_posix(),'review_sha256':sha(report),
                            'kind':'code-scientific-figure' if '_math_' in path.stem else 'concept-keyframe'}
    (SB/'frame_approvals.json').write_text(json.dumps(approvals,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(approvals)} independent current-PNG approvals adopted')

if __name__=='__main__': main()
