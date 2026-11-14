import re, sys, glob
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
for f in sorted(glob.glob('raw/articles/*.wikitext')):
    w = Path(f).read_text(encoding='utf-8')
    m = re.search(r'\|\s*max[-_]depth\s*=\s*(.*)', w)
    if not m: print('==', Path(f).stem, 'NO max_depth'); continue
    line = m.group(1)[:600]
    names = re.findall(r'<ref name\s*=\s*"?([^"/>]+?)"?\s*/?>', line) + re.findall(r'\{\{sfn\|([^}]+)\}\}', line)
    print('==', Path(f).stem, '::', re.sub(r'<ref[^>]*>.*?</ref>', '[ref]', line)[:200])
    for inline in re.findall(r'<ref[^>/]*>(.*?)</ref>', line):
        print('   inline:', inline[:400])
    for n in names:
        n = n.strip()
        d = re.search(r'<ref name\s*=\s*"?' + re.escape(n) + r'"?\s*>(.*?)</ref>', w, re.S)
        if d: print('   ', n, '=>', re.sub(r'\s+', ' ', d.group(1))[:400])
        else: print('   ', n, '=> (sfn/undefined)')
    # also sentences mentioning deepest / maximum depth in body
    body = re.sub(r'<ref[^>]*>.*?</ref>|<ref[^>]*/>', '', w, flags=re.S)
    for s in re.findall(r'[^.\n]{0,200}(?:maximum depth|deepest point|max(?:imum)? depth of|deepest part)[^.\n]{0,200}', body, re.I)[:4]:
        print('    body:', s.strip()[:350])
