"""Repair masonry projection and complete the observatory's physical details."""
from pathlib import Path
import bpy,json,math,random,sys,hashlib
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inspect_model import look_at,material
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));OUT=WORLD/'background/map_3d'
a=next(a for a in json.loads((OUT/'asset_manifest.json').read_text(encoding='utf-8'))['assets'] if a['id']=='bg23');folder=ROOT/a['model_directory'];out=folder/'r14/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'bg23_r14.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r13/inspection/bg23_r13.blend'));coll=bpy.data.collections['ASSET_bg23'];rng=random.Random(2314)
surface_names={'Weathered_white_limestone','Limestone_capstones','Oak_door_and_roots'}
# Face-projected UVs use one consistent world basis; BOX projection previously mixed
# world positions with rotated local face normals and stretched east/west walls.
for ob in coll.objects:
    if ob.type!='MESH' or not any(m and m.name in surface_names for m in ob.data.materials):continue
    me=ob.data;uv=me.uv_layers.active or me.uv_layers.new(name='Physical_surface_metres')
    for poly in me.polygons:
        normal=ob.matrix_world.to_3x3()@poly.normal;axis=max(range(3),key=lambda i:abs(normal[i]))
        axes=[(1,2),(0,2),(0,1)][axis]
        for li in poly.loop_indices:
            co=ob.matrix_world@me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]],co[axes[1]])
for name in surface_names:
    nt=bpy.data.materials[name].node_tree;tc=nt.nodes.new('ShaderNodeTexCoord')
    for tex in [n for n in nt.nodes if n.type=='TEX_IMAGE']:
        tex.projection='FLAT'
        if tex.inputs['Vector'].links:
            mapping=tex.inputs['Vector'].links[0].from_node;nt.links.new(tc.outputs['UV'],mapping.inputs[0])
    if name=='Oak_door_and_roots':
        for n in nt.nodes:
            if n.type=='MIX_RGB' and n.blend_type=='MULTIPLY':n.inputs[2].default_value=(.20,.14,.075,1)
# Exposed obelisk shafts now rise above the cornice; masonry body is unchanged.
for ob in coll.objects:
    if ob.name.startswith(('Obelisk_stone_course','Four_sided_obelisk_cap')):
        if ob.location.z>2.45:ob.location.z+=.50
    if ob.name.startswith('Four_sided_obelisk_cap'):
        x,y=ob.location[:2]
        for j in range(2):
            source=next(o for o in coll.objects if o.name.startswith('Obelisk_stone_course') and abs(o.location.x-x)<.01 and abs(o.location.y-y)<.01)
            new=source.copy();new.data=source.data.copy();coll.objects.link(new);new.name='Exposed_obelisk_shaft';new.location=(x,y,2.81+j*.25);new.scale=(.68,.68,.96)
    if ob.name.startswith('Carved_stone_frieze'):ob.scale.x*=1.05
    if ob.name.startswith('Amethyst_raw_crystal'):
        ob.scale=(1.6,.6,1.0);ob.location.z=.24
        normal=Vector((ob.location.x,ob.location.y,0)).normalized();ob.location-=normal*.065
    if ob.name.startswith('Base_fern'):ob.scale*=1.55
    if ob.name.startswith(('Natural_climbing_foliage','Climbing_leaf_cluster')) and ob.location.y<-2 and abs(ob.location.x)<.7:ob.hide_render=True
    if ob.name.startswith('Natural_climbing_stem'):
        if any(p.co.y<-2 and abs(p.co.x)<.7 for s in ob.data.splines for p in s.points):ob.hide_render=True
    if ob.name.startswith('Connected_orbit_band') and ob.type=='MESH':
        # Widen the flat casting without changing its contact endpoints.
        for i in range(0,len(ob.data.vertices),4):
            group=list(ob.data.vertices)[i:i+4];center=sum((v.co for v in group),Vector())/4
            for v in group:v.co=center+(v.co-center)*1.55
nt=bpy.data.materials['Grey_cyan_carved_stone'].node_tree;bs=nt.nodes.get('Principled BSDF')
tex=nt.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(next((OUT/'textures').glob('worn_mossy_plasterwall_diff_2k.*'))),check_existing=True);tex.projection='BOX';tex.projection_blend=.25
tc=nt.nodes.new('ShaderNodeTexCoord');nt.links.new(tc.outputs['Object'],tex.inputs['Vector']);mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(.38,.47,.40,1);nt.links.new(tex.outputs['Color'],mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
bum=nt.nodes.new('ShaderNodeBump');bum.inputs['Distance'].default_value=.008;bum.inputs['Strength'].default_value=.6;nt.links.new(tex.outputs['Color'],bum.inputs['Height']);nt.links.new(bum.outputs[0],bs.inputs['Normal'])
silver=bpy.data.materials['Mirror_silver'].node_tree.nodes.get('Principled BSDF');silver.inputs['Roughness'].default_value=.13;silver.inputs['Base Color'].default_value=(.64,.66,.69,1)
floor=bpy.data.objects['Studio_floor'];floor.location.z=0;floor.visible_glossy=False
# Roots are a visible branching network, with pale weathered bark.
rootmat=material('Pale_root_bark',(.17,.115,.065),.83);nt=rootmat.node_tree;bs=nt.nodes.get('Principled BSDF');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=55;noise.inputs['Detail'].default_value=5;bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.007;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
def curve(name,pts,r,mat):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=3;s=cu.splines.new('POLY');s.points.add(len(pts)-1)
    for i,(p,co) in enumerate(zip(s.points,pts)):p.co=(*co,1);p.radius=max(.08,1-i/len(pts))
    ob=bpy.data.objects.new(name,cu);coll.objects.link(ob);cu.materials.append(mat);return ob
for old in [o for o in coll.objects if o.name.startswith('Surface_root')]:old.hide_render=True
for k in range(55):
    angle=rng.uniform(0,math.tau)
    if math.sin(angle)<-.92:continue
    pts=[]
    for j in range(45):
        f=j/44;r=2.13+f*rng.uniform(.65,.8);theta=angle+.07*math.sin(f*5+k);pts.append((r*math.cos(theta),r*math.sin(theta),.045+.52*(1-f)**3+.03*math.sin(f*7)**2))
    curve('Natural_root_trunk',pts,rng.uniform(.035,.07),rootmat)
    for side in [-1,1]:
        start=Vector(pts[22]);end=Vector(pts[-1])+Vector((side*.18,side*.18,0));branch=[start.lerp(end,j/20)+Vector((0,0,.03*math.sin(j/20*math.pi))) for j in range(21)];curve('Root_fine_branch',branch,.018,rootmat)
# Slightly denser engraved dome relief follows the existing surface profile.
brass=bpy.data.materials['Polished_worn_brass']
for k in range(24):
    a0=k*math.tau/24;pts=[]
    for j in range(101):
        t=j/100*math.tau*1.3;rr=.09*(1-j/125);u=1.77+rr*math.cos(t);v=rr*math.sin(t);r=math.hypot(u,v);z=2.64+(1.86-r)*(.08/.21)+.012;pts.append((u*math.cos(a0)-v*math.sin(a0),u*math.sin(a0)+v*math.cos(a0),z))
    curve('Fine_cast_volute',pts,.005,brass)
scene=bpy.context.scene;scene.cycles.samples=40;camera=scene.camera
views=[('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22),('perspective',1,-1,.7),('roof_detail',.7,-1,1.8)]
for name,x,y,z in views:
    camera.location=(x*15,y*15,2.5+z*5);look_at(camera,(0,0,2.5));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report=json.loads((folder/'r13/inspection/inspection.json').read_text());report.update(revision='r14',sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),source='bg23_r13; repaired physical UVs, exposed obelisk shafts, textured frieze, branch roots, metallic environment reflections',status='candidate_not_reviewed',objects=len(coll.objects),supplemental_views=['roof_detail.png']);(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
