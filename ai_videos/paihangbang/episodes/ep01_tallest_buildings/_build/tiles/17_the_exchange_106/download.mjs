import fs from 'node:fs';
const items = [
['c2','https://images.unsplash.com/photo-1712913172668-208ce27ff0b2?fm=jpg&q=100'],
['c3','https://images.unsplash.com/photo-1764866558095-3be59831f45f?fm=jpg&q=100'],
['c4','https://images.unsplash.com/photo-1709433895293-b36e78cf96f1?fm=jpg&q=100'],
['c5','https://images.unsplash.com/photo-1582041674426-39a8454c995b?fm=jpg&q=100'],
['c6','https://images.pexels.com/photos/34168183/pexels-photo-34168183.jpeg'],
['c7','https://images.pexels.com/photos/13457656/pexels-photo-13457656.jpeg']
];
await Promise.all(items.map(async ([id,url])=>{try{const r=await fetch(url,{headers:{'User-Agent':'Mozilla/5.0'},signal:AbortSignal.timeout(120000)});if(!r.ok)throw Error(r.status);const b=Buffer.from(await r.arrayBuffer()); if(b[0]!==255||b[1]!==216)throw Error('not JPEG');fs.writeFileSync(new URL('./cand/'+id+'.jpg',import.meta.url),b);console.log(id,b.length);}catch(e){console.log(id,e.message)}}));
