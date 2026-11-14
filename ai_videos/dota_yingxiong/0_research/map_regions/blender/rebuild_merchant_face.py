"""Replace fused facial anatomy with MPFB topology and volumetric curly hair."""
from pathlib import Path
import bpy,bmesh,json,sys,random,math,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import material,look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('characters/*/m300_*/model_3d'));out=folder/'r09';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r08/inspection/m300_r08.blend'));coll=bpy.data.collections['ASSET_m300'];body=next(o for o in coll.objects if o.type=='MESH' and len(o.data.polygons)>100000);me=body.data;rng=random.Random(3009)
# Correct material segmentation on the cape using its actual surface depth.
verts=np.asarray([v.co[:] for v in me.vertices]);loops=np.asarray([i.vertex_index for i in me.loops]);fc=verts[loops].reshape(-1,3,3).mean(1);x,y,z=fc.T;labels=np.asarray([p.material_index for p in me.polygons],np.int32)
cape=((abs(x)>.25)&(y>-.06)&(z>.20)&(z<1.1))|((abs(x)>.25)&(y>-.15)&(z>.86)&(z<1.10));labels[cape]=1
earsteel=(abs(x)>.105)&(abs(x)<.175)&(z>1.075)&(z<1.169)&(y<.035);labels[earsteel]=3
me.polygons.foreach_set('material_index',labels)
cutface=(abs(x)<.123)&(z>1.035)&(z<1.168)&(y<.015)
cutbeard=(abs(x)<np.clip((z-.68)*.65+.04,.04,.18))&(y<-.13)&(z>.70)&(z<1.08)
bm=bmesh.new();bm.from_mesh(me);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in np.flatnonzero(cutface|cutbeard)],context='FACES');bm.to_mesh(me);bm.free()
for ob in coll.objects:
    if ob.name.startswith('Beard_individual_fibres'):ob.hide_render=True
# Append the real anatomy source and evaluate its stored shape keys.
with bpy.data.libraries.load(str(WORLD/'background/map_3d/anatomy_sources/mpfb_merchant_source.blend'),link=False) as (s,d):d.objects=[s.objects[0]]
human=d.objects[0];coll.objects.link(human)
for mod in human.modifiers:mod.show_viewport=False;mod.show_render=False
bpy.context.view_layer.update();ev=human.evaluated_get(bpy.context.evaluated_depsgraph_get());em=ev.to_mesh();co=[v.co.copy() for v in em.vertices];gi=human.vertex_groups['body'].index;bodyids={v.index for v in human.data.vertices if any(g.group==gi and g.weight>.1 for g in v.groups)}
polys=[list(p.vertices) for p in em.polygons if all(i in bodyids and co[i].z>1.48 for i in p.vertices)];used=sorted({i for p in polys for i in p});remap={v:i for i,v in enumerate(used)}
def transform(v):return Vector((v.x*1.5,(v.y+.12483)*1.05-.145,(v.z-1.61686)*.85+1.125))
hm=bpy.data.meshes.new('MPFB_clean_facial_loops');hm.from_pydata([transform(co[i]) for i in used],[],[[remap[i] for i in p] for p in polys]);head=bpy.data.objects.new('Anatomical_merchant_head',hm);coll.objects.link(head);ev.to_mesh_clear();bpy.data.objects.remove(human,do_unlink=True)
skin=material('Merchant_warm_weathered_skin',(.32,.12,.065),.54);nt=skin.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Subsurface Weight'].default_value=.10;bs.inputs['Subsurface Radius'].default_value=(.012,.005,.0025);bs.inputs['Specular IOR Level'].default_value=.28;tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=530;noise.inputs['Detail'].default_value=3;nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.00015;bump.inputs['Strength'].default_value=.32;nt.links.new(noise.outputs[0],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal']);hm.materials.append(skin)
for p in hm.polygons:p.use_smooth=True
sub=head.modifiers.new('Anatomical_surface_subdivision','SUBSURF');sub.levels=2;sub.render_levels=2
white=material('Merchant_eye_sclera',(.48,.42,.33),.28);iris=material('Merchant_pale_blue_iris',(.035,.11,.16),.26);pupil=material('Merchant_dark_pupil',(.002,.003,.004),.17)
def sphere(name,pos,scale,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,radius=1,location=pos);o=bpy.context.object
    for c in list(o.users_collection):c.objects.unlink(o)
    coll.objects.link(o);o.name=name;o.scale=scale;o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    return o
for side in [-1,1]:
    c=transform(Vector((side*.03194,-.12483,1.61686)));sphere('Inset_anatomical_eye',c,(.0238,.0175,.0131),white);sphere('Blue_iris',c+Vector((0,-.0171,0)),(.0072,.0018,.0072),iris);sphere('Natural_eye_pupil',c+Vector((0,-.0186,0)),(.0030,.0008,.0030),pupil)
# Individual fibres travel from jaw roots through a full beard volume, curl,
# and converge to an irregular point. Colour varies per group, not paint patches.
hairmats=[]
for k in range(8):
    t=k/7;m=material('Merchant_hair_gold_'+str(k),(.095+.14*t,.036+.065*t,.008+.020*t),.83);m.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.20;hairmats.append(m)
for kind,count in [('beard',16000),('moustache',2800),('brows',1400)]:
    cu=bpy.data.curves.new('Natural_curly_'+kind,'CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=.00013 if kind=='beard' else .00011;cu.bevel_resolution=1
    for m in hairmats:cu.materials.append(m)
    for i in range(count):
        side=rng.choice([-1,1]);u=rng.uniform(-1,1);phase=rng.random()*math.tau;length=rng.uniform(.20,.38);rootx=.115*u;rootz=1.060+rng.uniform(-.015,.025);rooty=-.167-.018*(1-u*u);depth=rng.random();s=cu.splines.new('POLY');s.points.add(22);s.material_index=rng.randrange(8)
        for j,p in enumerate(s.points):
            t=j/22
            if kind=='beard':
                zz=rootz-length*t;xx=rootx*(1-.82*t**2)+.014*math.sin(phase+t*5)*(math.sin(math.pi*t));yy=rooty-.060*math.sin(math.pi*t*.85)-depth*.032*math.sin(math.pi*t);amp=.0015+.003*math.sin(math.pi*t);xx+=amp*math.sin(phase+t*24);yy+=amp*math.cos(phase+t*24)
            elif kind=='moustache':
                xx=side*(.006+.115*t);yy=-.191-.012*math.sin(t*math.pi)+rng.uniform(-.002,.002);zz=1.077+.012*math.sin(t*math.pi)-.029*t+rng.uniform(-.006,.006);xx+=.0015*math.sin(phase+t*15)
            else:
                xx=side*(.020+.067*t);yy=-.153-.007*math.sin(t*math.pi)+rng.uniform(-.003,.003);zz=1.145+.008*math.sin(t*math.pi)+rng.uniform(-.004,.004)
            p.co=(xx,yy,zz,1);p.radius=max(.01,(1-t)**.65)
    o=bpy.data.objects.new('Volumetric_curly_'+kind,cu);coll.objects.link(o)
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=900;scene.render.resolution_y=900;camera=scene.camera;camera.data.ortho_scale=.62;camera.location=(.4,-1.8,1.18);look_at(camera,(0,-.10,1.04));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'face_preview.png');bpy.ops.render.render(write_still=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r09','status':'author_preview_pending','source':'r08 body with local MPFB facial anatomy, separate eyes and 20200 curly beard/moustache/brow fibres','face_source':'map_3d/anatomy_sources/mpfb_merchant_source.blend','base_anatomy_faces':len(hm.polygons)},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
