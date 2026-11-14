"""Combine the controlled 1024 remesh body with scanned leaves and carved eye sockets."""
from pathlib import Path
import bpy,bmesh,json,sys,math,numpy as np,argparse,random
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
p=argparse.ArgumentParser();p.add_argument('--revision',default='r19');args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m1_Treant/model_3d'));out=folder/args.revision;out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r16/inspection/m1_r16.blend'));coll=bpy.data.collections['ASSET_m1'];body=max((o for o in coll.all_objects if o.type=='MESH'),key=lambda o:len(o.data.polygons))
body.data.transform(body.matrix_world);body.parent=None;body.matrix_world.identity()
bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001)
boundary_before=sum(e.is_boundary for e in bm.edges);print('WELDED_BOUNDARY',boundary_before,flush=True)
remove=[v for v in bm.verts if v.co.z>1.60 or (v.co.z>1.37 and math.hypot(v.co.x,v.co.y)>.18) or (v.co.z>1.29 and math.hypot(v.co.x,v.co.y)>.27)]
bmesh.ops.delete(bm,geom=remove,context='VERTS')
# Remove the small low centre fragment and leave a genuine contact plane at the roots.
bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.00001,plane_co=(0,0,.022),plane_no=(0,0,1),clear_inner=True,clear_outer=False)
edges=[e for e in bm.edges if e.is_boundary];print('CROWN_ROOT_BOUNDARIES',len(edges),flush=True)
if len(edges)>40000:raise RuntimeError('Unexpected open-body mesh: do not fill an unbounded source')
filled=bmesh.ops.holes_fill(bm,edges=edges,sides=0)['faces'];bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free();body.data.update()
if body.data.has_custom_normals:body.data.normals_split_custom_set([(0,0,0)]*len(body.data.loops))
mat=body.data.materials[0];nt=mat.node_tree;bs=next(q for q in nt.nodes if q.type=='BSDF_PRINCIPLED');old=bs.inputs['Base Color'].links[0].from_socket
tint=nt.nodes.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.22,.16,.10,1);nt.links.new(old,tint.inputs[1]);nt.links.new(tint.outputs[0],bs.inputs['Base Color'])
grey=nt.nodes.new('ShaderNodeRGBToBW');nt.links.new(old,grey.inputs[0]);mask=nt.nodes.new('ShaderNodeMapRange');mask.clamp=True;mask.interpolation_type='SMOOTHSTEP';mask.inputs['From Min'].default_value=.5;mask.inputs['From Max'].default_value=.78;nt.links.new(grey.outputs[0],mask.inputs['Value'])
lichen=nt.nodes.new('ShaderNodeMixRGB');lichen.blend_type='MULTIPLY';lichen.inputs[0].default_value=1;lichen.inputs[2].default_value=(.48,.52,.38,1);nt.links.new(old,lichen.inputs[1]);mix=nt.nodes.new('ShaderNodeMixRGB');nt.links.new(mask.outputs[0],mix.inputs[0]);nt.links.new(tint.outputs[0],mix.inputs[1]);nt.links.new(lichen.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
bs.inputs['Metallic'].default_value=0;bs.inputs['Roughness'].default_value=.86;bs.inputs['Specular IOR Level'].default_value=.2
for socket in ['Metallic','Roughness']:
 for link in list(bs.inputs[socket].links):nt.links.remove(link)
# Get front-surface coordinates from this revision, not guessed screen rectangles.
bm=bmesh.new();bm.from_mesh(body.data);tree=BVHTree.FromBMesh(bm);eye_centres=[]
for px in [-.059,.059]:
 hit,normal,index,distance=tree.ray_cast(Vector((px,-2,1.312)),Vector((0,1,0)))
 if hit is None:raise RuntimeError('Eye surface ray missed')
 eye_centres.append(tuple(hit))
bm.free()
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
# A dark inner bowl is a carved concavity, not a painted circle on the bark.
eye_material=bpy.data.materials.new('Deep_dark_wood_inside_eye_socket');eye_material.use_nodes=True;eye_bs=eye_material.node_tree.nodes.get('Principled BSDF');eye_bs.inputs['Base Color'].default_value=(.0015,.001,.0006,1);eye_bs.inputs['Roughness'].default_value=.95
for i,(px,py,pz) in enumerate(eye_centres):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3,radius=1,location=(px,py-.008,pz));cutter=bpy.context.object;cutter.scale=(.024,.050,.020);rng=random.Random(29118+i)
 for v in cutter.data.vertices:v.co*=rng.uniform(.88,1.12)
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 bpy.context.view_layer.objects.active=body;mod=body.modifiers.new('Carved_eye_socket_'+str(i),'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=(px,py+.040,pz));inner=bpy.context.object;inner.name='Recessed_eye_dark_wood';inner.scale=(.019,.003,.015);inner.data.materials.append(eye_material)
 for c in list(inner.users_collection):c.objects.unlink(inner)
 coll.objects.link(inner)
# Fill the spurious centre knot behind its opening with matching wood.
front_y=sum(p[1] for p in eye_centres)/2
bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,location=(0,front_y+.012,1.278));knot=bpy.context.object;knot.name='Wood_inside_spurious_central_hole';knot.scale=(.021,.032,.031)
for c in list(knot.users_collection):c.objects.unlink(knot)
coll.objects.link(knot)
with bpy.data.libraries.load(str(folder/'r15/authoring.blend'),link=False) as (src,dst):
 dst.objects=[name for name in src.objects if name.startswith(('Scanned_maple_leaf_','Supplementary_scanned_maple_leaf','Attached_foliage_twig','Connected_supplementary_petiole','Scanned_leaf_petiole'))]
leaves=dst.objects
for ob in leaves:coll.objects.link(ob)
with bpy.data.libraries.load(str(folder/'r13/authoring.blend'),link=False) as (src,dst):dst.objects=[name for name in src.objects if name.startswith('Native_crown_branch')]
branches=dst.objects
branch_material=next(m for m in bpy.data.materials if m.name.startswith('Continuous_scanned_furrowed_bark'))
for ob in branches:
 coll.objects.link(ob);ob.data.materials.clear();ob.data.materials.append(branch_material)
knot.data.materials.append(branch_material)
# Expand the crown about its branch attachment, then normalize the overall stature.
from mathutils import Matrix
bpy.context.view_layer.update()
pivot=Vector((0,0,1.43));transform=Matrix.Translation(pivot)@Matrix.Diagonal((1.18,1.18,1.36,1))@Matrix.Translation(-pivot)
for ob in leaves+branches:ob.matrix_world=transform@ob.matrix_world
for v in body.data.vertices:
 arm=max(0,min(1,(abs(v.co.x)-.15)/.09))*max(0,min(1,(1.12-v.co.z)/.25))
 v.co.y-=.045*arm
body.data.update()
# Bring all roots to the same ground datum after the small underside trim.
for ob in coll.objects:ob.location.z-=.022
bpy.context.view_layer.update();top=max((ob.matrix_world@Vector(corner)).z for ob in coll.objects if ob.type in ['MESH','CURVE'] for corner in ob.bound_box);height_scale=1.9/top
for ob in coll.objects:ob.location*=height_scale;ob.scale*=height_scale
bpy.context.view_layer.update()
lowest=min((ob.matrix_world@Vector(corner)).z for ob in coll.objects if ob.type in ['MESH','CURVE'] and not ob.hide_render for corner in ob.bound_box)
assert lowest>-.015,('Unexpected below-ground asset geometry',lowest)
for m in bpy.data.materials:
 if not m.name.startswith('Scanned_maple'):continue
 for n in m.node_tree.nodes:
  if n.type=='BSDF_PRINCIPLED':n.inputs['Specular IOR Level'].default_value=.18
scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=64;scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1000;scene.render.resolution_y=1000
for ob in scene.objects:
 if ob.type=='LIGHT':ob.data.energy*=.55
scene.camera.location=(0,-6,1.25);scene.camera.data.ortho_scale=2.25;look_at(scene.camera,(0,0,.95));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m1','revision':args.revision,'source':['r16 remesh1024 body','r15 scanned leaves','r13 main crown branches'],'status':'author_preview_not_accepted','source_boundary_edges_after_weld':boundary_before,'crown_and_root_boundary_edges':len(edges),'filled_faces':len(filled),'eye_ray_hits':eye_centres,'root_trim_m':.022,'final_height_m':1.9,'height_scale':height_scale,'changes':['Preserve 1024 remesh bark geometry','Larger scanned leaf crown with original branch roots','Smaller irregular carved eye sockets with recessed dark interiors','Darken bark and preserve pale green lichen','Advance forearms slightly for side-view separation','Trim underside fragment and re-ground roots'],'remaining':['Author visual inspection','Seams at crown branch connections','Exact face landmark appearance','Full independent review']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.data.ortho_scale=.9;scene.camera.location=(.4,-3,1.9);look_at(scene.camera,(0,0,1.55));scene.render.filepath=str(out/'crown_detail.png');bpy.ops.render.render(write_still=True)
