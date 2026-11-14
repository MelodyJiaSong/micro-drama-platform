"""Align vines to the octagonal shell, expose carving, and finish root profiles."""
from pathlib import Path
import bpy,json,sys,math,time,hashlib
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));source=folder/'r14/inspection/bg23_r14.blend';out=folder/'r15/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'bg23_r15.blend'
if dest.exists():raise FileExistsError(dest)
while not source.exists():time.sleep(10)
bpy.ops.wm.open_mainfile(filepath=str(source));coll=bpy.data.collections['ASSET_bg23']
def wallpoint(co):
    co=Vector(co);angle=math.atan2(co.y,co.x);local=(angle+math.pi/8)%(math.pi/4)-math.pi/8;r=2.405/math.cos(local);co.x=r*math.cos(angle);co.y=r*math.sin(angle);return co
for ob in list(coll.objects):
    if ob.name.startswith(('Four_sided_obelisk_cap','Exposed_obelisk_shaft')) and ob.location.y>0:ob.location.z-=.5
    if ob.name.startswith('Exposed_obelisk_shaft') and ob.location.y>0:ob.hide_render=True
    if ob.name.startswith('Obelisk_stone_course') and ob.location.y>0 and ob.location.z>2.8:ob.location.z-=.5
    if ob.name.startswith(('Carved_circular','Frieze_geometric')):
        for spline in ob.data.splines:
            for p in spline.points:
                co=Vector(p.co[:3]);co+=Vector((co.x,co.y,0)).normalized()*.010;p.co=(*co,1)
        ob.data.bevel_depth=.003
    if ob.name.startswith('Amethyst_raw_crystal') and ob.location.y<-2 and abs(ob.location.x)<.7:ob.hide_render=True
    if ob.name.startswith(('Natural_climbing_foliage','Climbing_leaf_cluster')):
        ob.location=wallpoint(ob.location);ob.scale*=1.2
        if ob.location.y<-2 and abs(ob.location.x)<.78:ob.hide_render=True
    if ob.name.startswith(('Natural_climbing_stem','Climbing_vine')):
        for s in ob.data.splines:
            for p in s.points:p.co=(*wallpoint(p.co[:3]),1)
    if ob.name.startswith('Natural_root_trunk'):
        s=ob.data.splines[0];a=math.atan2(s.points[0].co.y,s.points[0].co.x)
        for j,p in enumerate(s.points):
            t=j/(len(s.points)-1);angle=a+.04*math.sin(t*5);r=2.38+.62*t;p.co=(r*math.cos(angle),r*math.sin(angle),.04+.40*(1-t)**3,1)
    if ob.name.startswith('Root_fine_branch'):ob.hide_render=True
for name,c0,c1 in [('Cast_bronze_with_verdigris',(.20,.105,.035,1),(.035,.145,.11,1)),('Polished_worn_brass',(.37,.24,.075,1),(.60,.43,.16,1))]:
    nt=bpy.data.materials[name].node_tree
    for n in nt.nodes:
        if n.type=='VALTORGB':n.color_ramp.elements[0].color=c0;n.color_ramp.elements[-1].color=c1
    nt.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.34
scene=bpy.context.scene;scene.cycles.samples=32;scene.render.resolution_x=1200;scene.render.resolution_y=1200;camera=scene.camera
for name,x,y,z in [('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22),('perspective',1,-1,.7),('roof_detail',.7,-1,1.8)]:
    camera.location=(x*15,y*15,2.5+z*5);look_at(camera,(0,0,2.5));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report=json.loads((folder/'r14/inspection/inspection.json').read_text());report.update(revision='r15',source='r14 with exposed ornament, natural wall-hugging foliage and continuous roots',sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),status='candidate_not_reviewed');(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
