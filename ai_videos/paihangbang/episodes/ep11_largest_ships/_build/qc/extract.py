import json, subprocess, sys, os, random
ep = r'C:\workspace\micro-drama-platform\ai_videos\paihangbang\episodes\ep11_largest_ships'
times = json.load(open(ep + r'\_build\qc\card_times.json', encoding='cp1252'))
which = sys.argv[1]  # master | risk
vid = ep + (r'\render\ep11_largest_ships_master.mp4' if which == 'master' else r'\render\ep11_largest_ships_master_with-risk-images.mp4')
outd = os.path.join(ep, '_build', 'qc', 'frames', which)
os.makedirs(outd, exist_ok=True)
pts = []
if which == 'master':
    pts += [('intro_1.0', 1.0), ('intro_4.9', 4.9), ('start_hold_5.5', 5.5)]
    for label, f, t in times:
        if t is None: continue
        tt = max(t, 0.0) if t > 0 else 6.0
        pts.append((label.replace('#', 'r').replace(' ', '_')[:40], tt))
    pts += [('champ_hold_321', 321.0), ('champ_end_324', 324.1), ('tally_326', 326.0), ('tally_330', 330.9),
            ('sources_333', 333.0), ('end_340', 340.0), ('end_352', 352.9), ('last_frame', 353.2)]
    random.seed(11)
    for i in range(8):
        t = round(random.uniform(5, 353), 2); pts.append((f'rand_{t}', t))
else:
    sel = ['#2 ', '#10 ', '#21 ', '#32 ', '#36 ', '#37 ', '#22 ']
    for label, f, t in times:
        if any(label.startswith(s) for s in sel):
            pts.append((label.replace('#', 'r').replace(' ', '_')[:40], t))
    pts += [('intro_4.9', 4.9), ('tally_330', 330.9), ('end_352', 352.9)]
for name, t in pts:
    safe = ''.join(c if c.isalnum() or c in '._-' else '_' for c in name)
    out = os.path.join(outd, f'{t:07.2f}_{safe}.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', vid, '-frames:v', '1', out], check=True)
print(len(pts))
