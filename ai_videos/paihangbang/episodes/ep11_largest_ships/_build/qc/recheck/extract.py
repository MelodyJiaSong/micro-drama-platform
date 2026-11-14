import json, subprocess, sys, os, random
EP = r'C:\workspace\micro-drama-platform\ai_videos\paihangbang\episodes\ep11_largest_ships'
times = json.load(open(EP + r'\_build\qc\recheck\card_times.json', encoding='utf-8'))
which = sys.argv[1]
vid = EP + (r'\render\ep11_largest_ships_master.mp4' if which == 'master' else r'\render\ep11_largest_ships_master_with-risk-images.mp4')
outd = os.path.join(EP, '_build', 'qc', 'recheck', which); os.makedirs(outd, exist_ok=True)
pts = [('intro', 1.0), ('intro_end', 4.9)]
fixed = [('champ_a', 328.5), ('champ_b', 331.0), ('champ_c', 333.5), ('tally_a', 334.5), ('tally_b', 337.0),
         ('tally_c', 340.5), ('sources', 342.5), ('end_a', 345.0), ('end_last', 362.6)]
if which == 'master':
    pts += [('hold_5.5', 5.5), ('hold_7.0', 7.0), ('hold_7.4', 7.4), ('hold_8.0', 8.0), ('hold_8.5', 8.5)]
    for label, f, t in times:
        pts.append((label.replace('#', 'r'), t if t and t > 0 else 6.0))
    pts += fixed
    random.seed(20261104)
    for i in range(5):
        t = round(random.uniform(5, 362), 2); pts.append((f'rand_{t}', t))
else:
    sel = ['#1 ', '#2 ', '#10 ', '#13 ', '#21 ', '#30 ', '#31 ', '#33 ', '#37 ', '#38 ', '#22 ']
    for label, f, t in times:
        if any(label.startswith(s) for s in sel):
            pts.append((label.replace('#', 'r'), t))
    pts += fixed
    random.seed(4)
    for i in range(2):
        t = round(random.uniform(5, 362), 2); pts.append((f'rand_{t}', t))
for name, t in pts:
    safe = ''.join(c if c.isalnum() or c in '._-' else '_' for c in name)[:44]
    out = os.path.join(outd, f'{t:07.2f}_{safe}.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', vid, '-frames:v', '1', out], check=True)
print(which, len(pts))
