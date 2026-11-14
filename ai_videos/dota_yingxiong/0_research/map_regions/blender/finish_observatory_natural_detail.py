"""Natural amethyst clusters, branching vines, fern skirt and seated cast dome."""
from pathlib import Path
import bpy,json,sys,math,random
from mathutils import Vector,Quaternion
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));SRC=WORLD/'background/map_3d/environment_sources';folder=next(WORLD.glob('background/*/bg23_*/model_3d'));out=folder/'r18';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r17/inspection/bg23_r17.blend'));coll=bpy.data.collections['ASSET_bg23'];rng=random.Random(2318)
# The bronze skirt now overlaps the stone bearing surface instead of dipping into it.
for o in coll.objects:
    if o.name.startswith(('Cast_bronze_dome','Concentric_cast_relief','Cast_spiral_relief','Fine_cast_volute')):
        o.scale.x*=1.19;o.scale.y*=1.19;o.location.z+=.06
    if o.name.startswith(('Natural_climbing_','Climbing_vine','Climbing_leaf_cluster')):o.hide_render=True
    if o.name.startswith(('Ground_interwoven_root','Fine_root_fork')):
        # Keep individual roots low and thick enough to read as living wood.
        o.data.materials[0].node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.9
        for n in o.data.materials[0].node_tree.nodes:
            if n.type=='VALTORGB':n.color_ramp.elements[0].color=(.085,.047,.020,1);n.color_ramp.elements[-1].color=(.36,.25,.13,1)
# A flattened cross-section reads as cast relief rather than gold wire.
cu=bpy.data.curves.new('Cast_relief_profile','CURVE');cu.dimensions='2D';s=cu.splines.new('POLY');s.points.add(31);s.use_cyclic_u=True
for k,p in enumerate(s.points):a=k*math.tau/32;p.co=(.014*math.cos(a),.004*math.sin(a),0,1)
profile=bpy.data.objects.new('Hidden_cast_profile',cu);coll.objects.link(profile);profile.hide_render=True
for o in coll.objects:
    if o.name.startswith(('Concentric_cast_relief','Cast_spiral_relief','Fine_cast_volute')):o.data.bevel_mode='OBJECT';o.data.bevel_object=profile;o.data.twist_mode='Z_UP'
for name in ['Cast_bronze_with_verdigris','Polished_worn_brass']:
    nt=bpy.data.materials[name].node_tree;bs=nt.nodes.get('Principled BSDF');tc=nt.nodes.new('ShaderNodeTexCoord');mp=nt.nodes.new('ShaderNodeVectorMath');mp.operation='MULTIPLY';mp.inputs[1].default_value=(35,2,5);nt.links.new(tc.outputs['Object'],mp.inputs[0]);noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=25;noise.inputs['Detail'].default_value=4;nt.links.new(mp.outputs[0],noise.inputs['Vector']);b=nt.nodes.new('ShaderNodeBump');b.inputs['Distance'].default_value=.0008;b.inputs['Strength'].default_value=.45;nt.links.new(noise.outputs[0],b.inputs['Height']);nt.links.new(b.outputs[0],bs.inputs['Normal']);rough=nt.nodes.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.24;rough.inputs['To Max'].default_value=.60;nt.links.new(noise.outputs[0],rough.inputs['Value']);nt.links.new(rough.outputs[0],bs.inputs['Roughness'])
purple=bpy.data.materials['Unlit_dark_amethyst']
for slab in list(coll.objects):
    if not slab.name.startswith('Inset_amethyst_plinth_slab'):continue
    center=sum((v.co for v in slab.data.vertices),Vector())/len(slab.data.vertices);angle=round(math.atan2(center.y,center.x)/(math.pi/4))*math.pi/4;n=Vector((math.cos(angle),math.sin(angle),0));t=Vector((-n.y,n.x,0));slab.hide_render=True
    for k in range(15):
        root=center+t*rng.uniform(-.105,.105)+Vector((0,0,rng.uniform(-.10,.10)));axis=(n+Vector((rng.uniform(-.35,.35),rng.uniform(-.35,.35),rng.uniform(-.5,.5)))).normalized();u=axis.cross(Vector((0,0,1))).normalized();v=axis.cross(u);radius=rng.uniform(.022,.055);length=rng.uniform(.045,.13);verts=[]
        for z,r in [(0,radius),(.65*length,radius*.95)]:
            for j in range(6):a=j*math.tau/6;verts.append(tuple(root+axis*z+r*(u*math.cos(a)+v*math.sin(a))))
        verts.append(tuple(root+axis*length));faces=[tuple(range(5,-1,-1))]+[(j,(j+1)%6,(j+1)%6+6,j+6) for j in range(6)]+[(6+j,6+(j+1)%6,12) for j in range(6)];me=bpy.data.meshes.new('Natural_amethyst_prism');me.from_pydata(verts,[],faces);o=bpy.data.objects.new('Raw_amethyst_cluster_crystal',me);coll.objects.link(o);me.materials.append(purple)
with bpy.data.libraries.load(str(next((SRC/'fern_02').glob('*.blend'))),link=False) as (s,d):d.objects=[f'fern_02_{x}' for x in 'abcd']
ferns=d.objects
for i in range(180):
    angle=rng.random()*math.tau
    if math.sin(angle)<-.91:continue
    local=(angle+math.pi/8)%(math.pi/4)-math.pi/8;r=2.44/math.cos(local)+rng.uniform(.02,.36);o=ferns[i%4].copy();o.data=ferns[i%4].data;coll.objects.link(o);o.name='Dense_base_fern_skirt';o.location=(r*math.cos(angle),r*math.sin(angle),.015);o.scale=(rng.uniform(.65,1.25),)*3;o.rotation_euler.z=rng.random()*math.tau
leaf=next(o for o in coll.objects if o.name.startswith('Climbing_leaf_cluster'));wood=bpy.data.materials['Oak_door_and_roots']
for stem in range(45):
    side=rng.randrange(8);angle=-math.pi/2+side*math.pi/4;n=Vector((math.cos(angle),math.sin(angle),0));t=Vector((-n.y,n.x,0));u=rng.uniform(-.88,.88);height=rng.uniform(.7,2.65);velocity=0;points=[]
    if side==0 and abs(u)<.78:continue
    for j in range(61):
        z=height*j/60;velocity=.8*velocity+rng.uniform(-.025,.025);u=max(-.92,min(.92,u+velocity));rad=2.39 if z<2.35 else 2.44;co=n*rad+t*u+Vector((0,0,z));points.append(co)
        if j%2==0:
            for sign in [-1,1]:
                o=leaf.copy();o.data=leaf.data;coll.objects.link(o);o.name='Wall_attached_ivy_leaf';o.hide_render=False;o.hide_viewport=False;o.location=co+t*sign*rng.uniform(.025,.13)+Vector((0,0,rng.uniform(-.04,.04)));o.scale=(rng.uniform(.45,.85),)*3;o.rotation_mode='QUATERNION';o.rotation_quaternion=n.to_track_quat('Z','Y')@Quaternion((0,0,1),rng.uniform(-1.5,1.5))
    cu=bpy.data.curves.new('Irregular_living_vine','CURVE');cu.dimensions='3D';cu.bevel_depth=.0025;cu.bevel_resolution=2;s=cu.splines.new('POLY');s.points.add(len(points)-1)
    for j,(p,co) in enumerate(zip(s.points,points)):p.co=(*co,1);p.radius=1-j/len(points)*.65
    o=bpy.data.objects.new('Branching_wall_vine',cu);coll.objects.link(o);cu.materials.append(wood)
for im in bpy.data.images:
    if im.source=='FILE' and not im.packed_file:
        paths=list(SRC.glob('*/textures/'+Path(im.filepath.replace('\\','/')).name))
        if paths:im.filepath=str(paths[0]);im.reload()
scene=bpy.context.scene;scene.cycles.samples=16;scene.render.resolution_x=900;scene.render.resolution_y=900;camera=scene.camera;camera.location=(10.5,-15,11.5);look_at(camera,(0,0,2.5));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'roof_preview.png');bpy.ops.render.render(write_still=True);(out/'authoring.json').write_text(json.dumps({'revision':'r18','status':'author_preview_pending','source':'r17; actual amethyst crystal clusters, flattened cast relief, dome bearing repaired, irregular wall-attached vines and fern skirt'},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
