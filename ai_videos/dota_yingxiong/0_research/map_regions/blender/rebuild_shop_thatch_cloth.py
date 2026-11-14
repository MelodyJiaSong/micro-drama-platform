"""Construct layered thatch courses and separately draped cloth panels."""
from pathlib import Path
import bpy,bmesh,json,sys,math,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
from build_production_map import mesh_object,surface
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));a=next(a for a in json.loads((WORLD/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'))['assets'] if a['id']=='bg12');folder=ROOT/a['model_directory'];out=folder/'r09';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r08/authoring.blend'));coll=bpy.data.collections['ASSET_bg12'];ob=next(o for o in coll.objects if o.type=='MESH' and o.name.startswith('geometry'));me=ob.data
cloth_indices=[i for i,m in enumerate(me.materials) if 'woven_cloth' in m.name];roof_indices=[i for i,m in enumerate(me.materials) if 'straw_underlayer' in m.name]
bm=bmesh.new();bm.from_mesh(me);points=np.array([tuple(f.calc_center_median()) for f in bm.faces if f.material_index in cloth_indices]);remove=[f for f in bm.faces if f.material_index in cloth_indices+roof_indices];bmesh.ops.delete(bm,geom=remove,context='FACES');bm.to_mesh(me);bm.free();me.update()
for o in list(coll.objects):
 if o.name.startswith('Roof_straw_fibres'):bpy.data.objects.remove(o,do_unlink=True)
rng=np.random.default_rng(287129);mats=[]
for i,(dark,light) in enumerate([((.07,.06,.009),(.25,.19,.04)),((.09,.085,.015),(.33,.29,.07)),((.03,.055,.008),(.11,.15,.025)),((.14,.09,.025),(.38,.25,.075)),((.06,.08,.012),(.20,.23,.04))]):mats.append(surface('Layered_roof_straw_'+str(i),dark,light,32,.88,.0008))
curves=[]
for i,mat in enumerate(mats):
 cu=bpy.data.curves.new('Layered_thatch_course_'+str(i),'CURVE');cu.dimensions='3D';cu.bevel_depth=.0032;cu.bevel_resolution=0;cu.materials.append(mat);o=bpy.data.objects.new(cu.name,cu);coll.objects.link(o);curves.append(cu)
strand_count=0
for cx,cy,bottom,top,radius,courses in [(-1.05,.46,3.55,5.43,2.05,8),(1.65,.9,4.05,6.48,2.10,10)]:
 def rad(z):return .045+radius*np.clip((top-z)/(top-bottom),0,1)**.83
 # Hidden structural thatch body is a coherent roof, rather than lumpy tongues.
 vs=[];fs=[];levels=30;segments=96
 for j in range(levels+1):
  t=j/levels;z=top-(top-bottom)*t;r=rad(z)
  for k in range(segments):
   ang=k*math.tau/segments;rr=r*(1+.012*math.sin(ang*7+t*2));vs.append((cx+rr*math.cos(ang),cy+rr*math.sin(ang),z))
 for j in range(levels):
  for k in range(segments):fs.append((j*segments+k,j*segments+(k+1)%segments,(j+1)*segments+(k+1)%segments,(j+1)*segments+k))
 roof=mesh_object('Structural_thatch_underlayer',vs,fs,[mats[0]],[],coll)
 for f in roof.data.polygons:f.use_smooth=True
 for course,zroot in enumerate(np.linspace(top-.08,bottom+.20,courses)):
  rroot=rad(zroot);count=max(500,int(math.tau*rroot/.004))
  for k in range(count):
   ang=k*math.tau/count+rng.uniform(-.007,.007);drop=rng.uniform(.24,.40);zr=zroot+rng.uniform(-.025,.025);rr=rad(zr)+rng.uniform(.015,.035);length=rad(zr-drop)-rr+rng.uniform(.035,.10);bend=rng.uniform(-.035,.035);s=curves[(k+course)%5].splines.new('POLY');s.points.add(4)
   for j,p in enumerate(s.points):
    t=j/4;theta=ang+bend*t;radial=rr+length*t;zz=zr-drop*t+.035*math.sin(t*math.pi)-.06*t**3
    p.co=(cx+radial*math.cos(theta),cy+radial*math.sin(theta),zz,1);p.radius=[.6,1,.95,.7,.12][j]
   strand_count+=1
# Physical cloth with a coherent colour per panel and stitched golden edging.
cloth=[]
for name,dark,light in [('Crimson',(.055,.003,.005),(.19,.013,.02)),('Deep_purple',(.018,.003,.03),(.07,.012,.10)),('Golden_hem',(.16,.08,.012),(.42,.27,.055))]:
 mat=surface('Separate_'+name+'_woven_cloth',dark,light,16,.91,.0008);nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Sheen Weight'].default_value=.18;bs.inputs['Sheen Roughness'].default_value=.75;cloth.append(mat)
groups={}
for x,y,z in points:
 dx=(x-.3)/3.2;dy=(y-.8)/2.4
 if abs(dx)>abs(dy):side='east' if dx>0 else 'west';key=(side,int(math.floor((y+2)/.9)))
 else:side='north' if dy>0 else 'south';key=(side,int(math.floor((x+3.3)/.95)))
 groups.setdefault(key,[]).append((x,y,z))
panel_records=[]
for (side,index),pts in sorted(groups.items()):
 if len(pts)<80:continue
 pts=np.array(pts);horizontal=0 if side in ('north','south') else 1;perp=1-horizontal;low,high=np.quantile(pts[:,horizontal],[.015,.985]);width=high-low
 if width<.26:continue
 fixed=float(np.median(pts[:,perp]));outward=1 if side in ('north','east') else -1;fixed+=outward*.035
 def position(u,v):
  co=[0,0,0];co[horizontal]=low+width*u;co[perp]=fixed+outward*(.045*math.sin(math.pi*u)*math.sin(math.pi*v)+.012*math.sin(u*math.pi*8)*v);co[2]=2.64-.045*math.sin(math.pi*u)-v*(.40+.16*math.sin(math.pi*u));return co
 vs=[];fs=[];indices=[];nu,nv=24,16
 for j in range(nv+1):
  for i in range(nu+1):vs.append(position(i/nu,j/nv))
 for j in range(nv):
  for i in range(nu):
   fs.append((j*(nu+1)+i,j*(nu+1)+i+1,(j+1)*(nu+1)+i+1,(j+1)*(nu+1)+i));indices.append(2 if j>=nv-2 or i==0 or i==nu-1 else index%2)
 panel=mesh_object('Draped_'+side+'_panel_'+str(index),vs,fs,cloth,indices,coll)
 for f in panel.data.polygons:f.use_smooth=True
 solid=panel.modifiers.new('Woven_cloth_thickness','SOLIDIFY');solid.thickness=.004;sub=panel.modifiers.new('Soft_drape','SUBSURF');sub.levels=1
 panel_records.append({'side':side,'index':index,'width_m':float(width),'fixed':fixed})
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.camera.data.ortho_scale=11.8;scene.camera.location=(14,-25,11);look_at(scene.camera,(.2,0,3.5));bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'revision':'r09','status':'author_preview_pending','source':'r08','changes':['Rebuilt roofs as discrete overlapping thatch courses','Separate hanging cloth meshes with individual crimson/purple materials and woven gold hems'],'straw_strands':strand_count,'cloth_panels':panel_records,'remaining':['Bamboo, wall weave, bone charm and hanging grass bundle still need refinement','All-view inspection pending']},indent=2),encoding='utf-8');scene.render.filepath=str(out/'shop_preview.png');bpy.ops.render.render(write_still=True)
