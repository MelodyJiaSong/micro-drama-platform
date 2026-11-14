import re,subprocess,sys,random
tag,video,extra=sys.argv[1],sys.argv[2],sys.argv[3:]
times=[]
for line in open('_build/qc/recheck/card_times.txt',encoding='utf-8'):
    m=re.search(r't=\s*([\d.]+)s',line)
    if m and line.startswith(('card','insight')): times.append(float(m.group(1)))
times=[float(x) for x in extra] if extra else times
for t in times:
    out=f'_build/qc/recheck/{tag}/{tag}_{t:07.2f}.jpg'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t}','-i',video,'-frames:v','1','-q:v','3',out],check=True)
print(len(times))
