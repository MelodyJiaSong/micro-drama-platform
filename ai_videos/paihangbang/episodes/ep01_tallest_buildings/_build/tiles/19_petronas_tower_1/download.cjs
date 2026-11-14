const fs = require('fs');
const ids = [31643157,26725611,8175726,34389898,39971101,3758432,433942];
(async()=>{for(let i=0;i<ids.length;i++){const id=ids[i];const url=`https://images.pexels.com/photos/${id}/pexels-photo-${id}.jpeg`;const r=await fetch(url,{headers:{'User-Agent':'Mozilla/5.0'}});if(!r.ok){console.log(id,r.status);continue;}fs.writeFileSync(`19_petronas_tower_1/cand/c${i+2}.jpg`,Buffer.from(await r.arrayBuffer()));console.log(`c${i+2}`,id,r.headers.get('content-type'));}})().catch(console.error);
