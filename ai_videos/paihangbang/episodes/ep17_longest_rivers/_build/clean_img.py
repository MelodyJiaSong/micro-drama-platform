import json, os, glob
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
a = {x['file'] for x in json.load(open('assets.json', encoding='utf-8'))}
for f in glob.glob('assets/img/*'):
    f = f.replace(os.sep, '/')
    if f not in a and not f.endswith('_gen.png'):
        os.replace(f, '_build/old_img/' + os.path.basename(f)); print('moved', f)
