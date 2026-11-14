"""Apply scanned surface wear and natural climbing leaves to the authored parts."""
from pathlib import Path
import bpy,json,random,math,sys,hashlib
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));OUT=WORLD/'background/map_3d';SRC=OUT/'environment_sources';TEX=OUT/'textures'
a=next(a for a in json.loads((OUT/'asset_manifest.json').read_text(encoding='utf-8'))['assets'] if a['id']=='bg23');out=ROOT/a['model_directory']/'r13/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'bg23_r13.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/a['model_directory']/'r12/inspection/bg23_r12.blend'));coll=bpy.data.collections['ASSET_bg23'];rng=random.Random(2313)
def scanned_material(mat_name,asset,scale,tint=None):
    nt=bpy.data.materials[mat_name].node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');geo=nt.nodes.new('ShaderNodeNewGeometry');mapping=nt.nodes.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=scale;nt.links.new(geo.outputs['Position'],mapping.inputs[0])
    slots={}
    for kind in ['diff','rough']:
        path=next(TEX.glob(asset+'_'+kind+'_2k.*'));tex=nt.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(path),check_existing=True);tex.projection='BOX';tex.projection_blend=.18;nt.links.new(mapping.outputs[0],tex.inputs['Vector'])
        if kind=='rough':tex.image.colorspace_settings.name='Non-Color'
        slots[kind]=tex.outputs[0]
    color=slots['diff']
    if tint:
        mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);nt.links.new(color,mix.inputs[1]);color=mix.outputs[0]
    nt.links.new(color,bs.inputs['Base Color']);nt.links.new(slots['rough'],bs.inputs['Roughness']);bum=nt.nodes.new('ShaderNodeBump');bum.inputs['Distance'].default_value=.005;bum.inputs['Strength'].default_value=.5;nt.links.new(slots['rough'],bum.inputs['Height']);nt.links.new(bum.outputs[0],bs.inputs['Normal'])
scanned_material('Weathered_white_limestone','worn_mossy_plasterwall',.55,(1.15,1.10,.98));scanned_material('Limestone_capstones','worn_mossy_plasterwall',.75,(1.2,1.16,1.06));scanned_material('Oak_door_and_roots','wood_planks',.45,(.65,.43,.22))
# Add small irregular edge wear without changing the authored door dimensions.
for o in coll.objects:
    if o.name.startswith(('Limestone_course','Obelisk_stone_course')):
        o.location.z+=rng.uniform(-.003,.003);o.rotation_euler.z+=rng.uniform(-.002,.002)
    if o.name.startswith(('Carved_circular','Frieze_geometric')):
        for spline in o.data.splines:
            for p in spline.points:
                v=Vector(p.co[:3]);n=Vector((v.x,v.y,0)).normalized();v-=n*.01;p.co=(*v,1)
        o.data.bevel_depth=.0035
dark=bpy.data.materials['Recessed_oxidation'];nt=dark.node_tree;bs=nt.nodes.get('Principled BSDF')
for link in list(bs.inputs['Base Color'].links):nt.links.remove(link)
bs.inputs['Base Color'].default_value=(.07,.095,.07,1)
leaf=next(o for o in coll.objects if o.name.startswith('Climbing_leaf_cluster'));wood=bpy.data.materials['Oak_door_and_roots']
for trail in range(22):
    angle=rng.random()*math.tau
    if math.sin(angle)<-.88:angle+=.55
    n=Vector((math.cos(angle),math.sin(angle),0));t=Vector((-n.y,n.x,0));top=rng.uniform(.8,2.6);points=[]
    for j in range(45):
        f=j/44;z=top*f;rad=2.36+.03*math.sin(f*7);co=n*rad+t*(.22*math.sin(f*9+trail))+Vector((0,0,z));points.append(co)
        if rng.random()<.85:
            o=leaf.copy();o.data=leaf.data;coll.objects.link(o);o.name='Natural_climbing_foliage';o.location=co+t*rng.uniform(-.14,.14);o.scale=(rng.uniform(.55,.90),)*3;o.rotation_euler=(rng.uniform(-.8,.8),rng.uniform(-.5,.5),angle+rng.uniform(-1.5,1.5))
    cu=bpy.data.curves.new('Climbing_stem','CURVE');cu.dimensions='3D';cu.bevel_depth=.006;cu.bevel_resolution=2;s=cu.splines.new('POLY');s.points.add(len(points)-1)
    for p,co in zip(s.points,points):p.co=(*co,1)
    ob=bpy.data.objects.new('Natural_climbing_stem',cu);coll.objects.link(ob);cu.materials.append(wood)
scene=bpy.context.scene;scene.cycles.samples=48;camera=scene.camera
for name,x,y,z in [('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22),('perspective',1,-1,.7)]:
    camera.location=(x*15,y*15,2.5+z*5);look_at(camera,(0,0,2.5));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report=json.loads((ROOT/a['model_directory']/'r12/inspection/inspection.json').read_text());report.update(revision='r13',source='bg23_r12 component model + CC0 worn surfaces and climbing foliage',sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),status='candidate_not_reviewed',objects=len(coll.objects));(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
