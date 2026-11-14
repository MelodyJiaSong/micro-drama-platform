import json, subprocess, os, random
vid = r'C:/workspace/micro-drama-platform/ai_videos/paihangbang/episodes/ep17_longest_rivers/render/ep17_longest_rivers_master.mp4'
c = json.load(open('centers.json', encoding='utf-8'))
pts = [('intro', t) for t in (0.5, 2.0, 3.5, 4.6)] + [('hold', t) for t in (6.0, 7.4, 7.8, 8.0)]
for kind, rank, name, t in c:
    if t <= 5.0: continue
    lab = (f'r{rank:02d}_' + name.split('–')[0].replace(' ', '')) if kind == 'card' else f'ins_after{rank}'
    pts.append((lab, t))
pts += [('champ', 349.0), ('champ', 353.4), ('tally', 355.0), ('tally', 360.3), ('sources', 362.6), ('end', 366.0), ('end', 382.5)]
random.seed(20261104)
rs = sorted(round(random.uniform(5, 382), 2) for _ in range(5))
pts += [('rand', x) for x in rs]
os.makedirs('frames', exist_ok=True)
for lab, t in pts:
    out = f'frames/{t:07.2f}_{lab}.png'
    if not os.path.exists(out):
        subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', vid, '-frames:v', '1', out], check=True)
print(len(pts), 'random', rs)
