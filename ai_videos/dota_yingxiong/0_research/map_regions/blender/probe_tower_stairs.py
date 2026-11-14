from pathlib import Path
import bpy,math,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg26_*/model_3d'))
bpy.ops.wm.open_mainfile(filepath=str(folder/'r02/authoring.blend'))
ob=max((o for o in bpy.data.collections['ASSET_bg26'].objects if o.type=='MESH'),key=lambda o:len(o.data.polygons))
rows=[]
for deg in range(360):
 d=Vector((math.cos(math.radians(deg)),math.sin(math.radians(deg)),0));rr=[]
 for z in [2,3,4]:
  hit,loc,normal,idx=ob.ray_cast(d*15+Vector((0,0,z)),-d)
  if hit:rr.append(math.hypot(loc.x,loc.y))
 if len(rr)==3:rows.append((deg,sum(rr)/3))
mins=[row for i,row in enumerate(rows) if row[1]<rows[(i-1)%360][1] and row[1]<rows[(i+1)%360][1]]
print('LOCAL_MINIMA',json.dumps(sorted(mins,key=lambda x:x[1])[:24]),flush=True)
