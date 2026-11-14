import json,hashlib,os
from PIL import Image
a=json.load(open('assets.json',encoding='utf-8'))
for e in a:
    f=e['file']
    try:
        im=Image.open(f); sz=im.size
        h=hashlib.sha256(open(f,'rb').read()).hexdigest()==e.get('sha256')
    except Exception as ex:
        sz=str(ex); h=None
    print(os.path.basename(f), sz, 'sha_ok' if h else 'SHA_MISMATCH', '|', e.get('licence'), '|', e.get('author'), '|', e.get('source_page') or e.get('commons_page'), '|', e.get('fop_note','')[:60])
