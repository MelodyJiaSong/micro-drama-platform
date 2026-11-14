import fs from 'node:fs';
const items=[
['c1','https://images.unsplash.com/photo-1696758525283-0396e523f542?fm=jpg&q=100'],
['c2','https://images.pexels.com/photos/5992305/pexels-photo-5992305.jpeg'],
['c3','https://images.pexels.com/photos/35422113/pexels-photo-35422113.jpeg'],
...Array.from({length:6},(_,i)=>['w'+(i+1),'https://www.wongtung.com/wp-content/uploads/2019/01/030970_190123-WT-web-project-page'+(i?i+1:'')+'.jpg'])
];
await Promise.all(items.map(async([id,url])=>{try{const r=await fetch(url,{headers:{'User-Agent':'Mozilla/5.0'},signal:AbortSignal.timeout(90000)});if(!r.ok)throw Error(r.status);const b=Buffer.from(await r.arrayBuffer());if(b[0]!==255||b[1]!==216)throw Error('not JPEG');fs.writeFileSync(new URL('./'+(id.startsWith('c')?'cand/':'')+id+'.jpg',import.meta.url),b);console.log(id,b.length);}catch(e){console.log(id,e.message)}}));
