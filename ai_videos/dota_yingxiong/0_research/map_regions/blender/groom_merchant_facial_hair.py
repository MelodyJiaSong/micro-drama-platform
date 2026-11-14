"""Grow a full curly beard and moustache from the actual facial surface."""
from pathlib import Path
import bpy,json,sys,math,random
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m300_*/model_3d'));out=folder/'r13';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r12/authoring.blend'));coll=bpy.data.collections['ASSET_m300'];rng=random.Random(30013)
for ob in coll.objects:
    if ob.name.startswith('Volumetric_curly_'):ob.hide_render=True
head=bpy.data.objects['Anatomical_merchant_head'];deps=bpy.context.evaluated_depsgraph_get();ev=head.evaluated_get(deps);em=ev.to_mesh();bvh=BVHTree.FromPolygons([v.co.copy() for v in em.vertices],[list(p.vertices) for p in em.polygons]);ev.to_mesh_clear()
materials=[bpy.data.materials['Merchant_hair_gold_'+str(k)] for k in range(8)]
for m in materials:
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.52;bs.inputs['Specular IOR Level'].default_value=.30
roots=[]
for _ in range(45000):
    x=rng.uniform(-.102,.102);z=rng.uniform(1.005,1.111)
    if abs(x)<.042 and z>1.063:continue
    p,n,idx,d=bvh.ray_cast(Vector((x,-1,z)),Vector((0,1,0)))
    if p is not None and p.y<-.075 and n.y<-.12:roots.append((p+n*.00035,n))
if len(roots)<500:raise RuntimeError('Not enough real facial hair roots')
for kind,count in [('beard',18000),('moustache',6000)]:
    cu=bpy.data.curves.new('Surface_rooted_curly_'+kind,'CURVE');cu.dimensions='3D';cu.bevel_depth=.00011;cu.bevel_resolution=1
    for m in materials:cu.materials.append(m)
    for i in range(count):
        if kind=='beard':root,n=rng.choice(roots);length=rng.uniform(.17,.36)*(1-.25*abs(root.x)/.1)
        else:
            x=rng.uniform(-.070,.070);z=rng.uniform(1.081,1.100);root,n,idx,d=bvh.ray_cast(Vector((x,-1,z)),Vector((0,1,0)))
            if root is None or root.y>-.075:continue
            root+=n*.0003;length=rng.uniform(.022,.055)
        phase=rng.random()*math.tau;freq=rng.uniform(20,38);amp=rng.uniform(.003,.011);s=cu.splines.new('POLY');s.points.add(32);s.material_index=rng.randrange(8);side=1 if root.x>=0 else -1
        for j,p in enumerate(s.points):
            t=j/32
            if kind=='beard':
                xx=root.x*(1-.72*t*t)+amp*math.sin(phase+t*freq)*math.sin(math.pi*t);yy=root.y-.025*t-.045*math.sin(math.pi*t)+amp*math.cos(phase+t*freq)*math.sin(math.pi*t);zz=root.z-length*t
            else:
                xx=root.x+side*length*t*.8;yy=root.y-.009*math.sin(t*math.pi)+.0015*math.cos(phase+t*18)*t;zz=root.z-length*t*.50+.0018*math.sin(phase+t*17)*t
            p.co=(xx,yy,zz,1);p.radius=max(.003,(1-t)**.8)
    ob=bpy.data.objects.new('Actual_surface_grown_'+kind,cu);coll.objects.link(ob)
body=next(o for o in coll.objects if o.type=='MESH' and len(o.data.polygons)>100000)
for p in body.data.polygons:
    p.use_smooth=True;x,y,z=p.center
    if .91<z<1.13 and (abs(x)>.12 or y>-.10):p.material_index=1
scene=bpy.context.scene;scene.cycles.samples=32;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.camera.data.ortho_scale=.62;scene.camera.location=(.4,-1.8,1.18);look_at(scene.camera,(0,-.1,1.04));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'face_preview.png');bpy.ops.render.render(write_still=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r13','status':'author_preview_pending','source':'r12 with facial-surface-raycast hair roots, 18000 curly beard fibres and up to 6000 short moustache fibres, smooth body surface normals and corrected upper cape material','valid_facial_root_samples':len(roots)},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
