"""Place the preserved frieze relief on the rebuilt mitered shell."""
from pathlib import Path
import bpy,math,json,sys,hashlib
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r17/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'bg23_r17.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r16/authoring.blend'));coll=bpy.data.collections['ASSET_bg23']
for ob in coll.objects:
    if ob.name.startswith(('Carved_circular','Frieze_geometric')):
        for s in ob.data.splines:
            for p in s.points:
                co=Vector(p.co[:3]);angle=round(math.atan2(co.y,co.x)/(math.pi/4))*math.pi/4;n=Vector((math.cos(angle),math.sin(angle),0));co+=n*(2.426-co.dot(n));p.co=(*co,1)
        ob.data.bevel_depth=.004
scene=bpy.context.scene;scene.cycles.samples=32;scene.render.resolution_x=1200;scene.render.resolution_y=1200;camera=scene.camera
bpy.ops.wm.save_as_mainfile(filepath=str(folder/'r17/authoring.blend'))
for name,x,y,z in [('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22),('perspective',1,-1,.7),('roof_detail',.7,-1,1.8)]:
    camera.location=(x*15,y*15,2.5+z*5);look_at(camera,(0,0,2.5));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(dest));report=json.loads((folder/'r15/inspection/inspection.json').read_text());report.update(revision='r17',source='r16 rebuilt masonry with frieze carving aligned to its new outer shell',sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),status='candidate_not_reviewed',repairs=['closed mitered cap','staggered individually textured limestone blocks','continuous freestanding tapered obelisks','inset amethyst plinth','low branching textured roots','restored continuous frieze relief']);(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
