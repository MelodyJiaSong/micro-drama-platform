"""Union crown roots with the trunk and use one scanned bark surface across joints."""
from pathlib import Path
import bpy,bmesh,json,sys,random,math,argparse
from mathutils import Vector,Matrix,Quaternion
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
p=argparse.ArgumentParser();p.add_argument('--revision',default='r15');args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('characters/*/m1_Treant/model_3d'));out=folder/args.revision;out.mkdir(exist_ok=True);scan=WORLD/'background/map_3d/environment_sources/bark_brown_02'
if (out/'authoring.blend').exists():raise FileExistsError(out)
assert json.loads((scan/'provenance.json').read_text())['license']=='CC0'
bpy.ops.wm.open_mainfile(filepath=str(folder/'r13/authoring.blend'));coll=bpy.data.collections['ASSET_m1'];body=max((o for o in coll.all_objects if o.type=='MESH'),key=lambda o:len(o.data.polygons));branches=[o for o in coll.objects if o.type=='CURVE' and o.name.startswith('Native_crown_branch')]
bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,location=(0,.03,1.47));core=bpy.context.object;core.name='Interior_wood_at_crown_cut';core.scale=(.14,.10,.16)
for c in list(core.users_collection):c.objects.unlink(core)
coll.objects.link(core)
bpy.ops.object.select_all(action='DESELECT')
for ob in [body,core]+branches:ob.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.convert(target='MESH');bpy.ops.object.join();body=bpy.context.object;body.name='Continuous_treant_trunk_roots_and_crown_branches'
bm=bmesh.new();bm.from_mesh(body.data);before_verts=len(bm.verts);print('WELD_START',before_verts,flush=True);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0001);merged=before_verts-len(bm.verts);boundary=[e for e in bm.edges if e.is_boundary];print('WELD_DONE',merged,'BOUNDARY',len(boundary),flush=True)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));prep={'vertices_merged':merged,'boundary_edges_before_fill':len(boundary),'filled_faces':0,'boundary_edges_after_fill':len(boundary),'closure_method':'solidify open shell before voxel union; interior crown core'};bm.to_mesh(body.data);bm.free();body.data.update();print('PREPARED_INPUT',json.dumps(prep),flush=True)
if prep['boundary_edges_after_fill']:
 solid=body.modifiers.new('Close_remaining_open_surface_shell','SOLIDIFY');solid.thickness=.0045;solid.offset=-.5;solid.use_quality_normals=True;bpy.ops.object.modifier_apply(modifier=solid.name)
remesh=body.modifiers.new('Close_head_cut_and_merge_branch_roots','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.0028;remesh.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=remesh.name)
smooth=body.modifiers.new('Remove_small_reconstruction_fragments','SMOOTH');smooth.factor=.22;smooth.iterations=3;bpy.ops.object.modifier_apply(modifier=smooth.name)
mat=bpy.data.materials.new('Continuous_scanned_furrowed_bark_lichen_and_moss');mat.use_nodes=True;nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=n.get('Principled BSDF');bs.inputs['Metallic'].default_value=0;bs.inputs['Roughness'].default_value=.82;bs.inputs['Specular IOR Level'].default_value=.20
tc=n.new('ShaderNodeTexCoord');scale=n.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(2,2,1);l.new(tc.outputs['Object'],scale.inputs[0])
def texture(suffix,noncolor=False):
 node=n.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(next(scan.glob('*_'+suffix+'_4k.*'))),check_existing=True);node.projection='BOX';node.projection_blend=.22
 if noncolor:node.image.colorspace_settings.name='Non-Color'
 l.new(scale.outputs[0],node.inputs['Vector']);return node
color=texture('diff');height=texture('disp',True);rough=texture('rough',True)
tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.62,.48,.36,1);l.new(color.outputs['Color'],tint.inputs[1]);surface=tint.outputs[0]
def noise(scaleval):
 node=n.new('ShaderNodeTexNoise');node.inputs['Scale'].default_value=scaleval;node.inputs['Detail'].default_value=4;l.new(tc.outputs['Object'],node.inputs['Vector']);return node
macro=noise(8);fine=noise(95);moss=noise(35)
def threshold(value,lo,hi):
 node=n.new('ShaderNodeMapRange');node.interpolation_type='SMOOTHSTEP';node.clamp=True;node.inputs['From Min'].default_value=lo;node.inputs['From Max'].default_value=hi;l.new(value,node.inputs['Value']);return node.outputs[0]
def multiply(a,b):
 node=n.new('ShaderNodeMath');node.operation='MULTIPLY';l.new(a,node.inputs[0]);l.new(b,node.inputs[1]);return node.outputs[0]
lichen=multiply(threshold(macro.outputs['Fac'],.48,.67),threshold(fine.outputs['Fac'],.56,.69));mix=n.new('ShaderNodeMixRGB');l.new(lichen,mix.inputs[0]);l.new(surface,mix.inputs[1]);mix.inputs[2].default_value=(.18,.20,.16,1);surface=mix.outputs[0]
mossmask=multiply(threshold(macro.outputs['Fac'],.50,.65),threshold(moss.outputs['Fac'],.43,.65));mix=n.new('ShaderNodeMixRGB');l.new(mossmask,mix.inputs[0]);l.new(surface,mix.inputs[1]);mix.inputs[2].default_value=(.016,.031,.004,1);l.new(mix.outputs[0],bs.inputs['Base Color'])
bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.009;bump.inputs['Strength'].default_value=.72;l.new(height.outputs['Color'],bump.inputs['Height']);l.new(bump.outputs[0],bs.inputs['Normal']);remap=n.new('ShaderNodeMapRange');remap.inputs['To Min'].default_value=.65;remap.inputs['To Max'].default_value=.93;l.new(rough.outputs['Color'],remap.inputs['Value']);l.new(remap.outputs['Result'],bs.inputs['Roughness']);body.data.materials.clear();body.data.materials.append(mat)
for ob in coll.objects:
 if ob.type=='CURVE' and ob.name.startswith('Attached_foliage_twig'):ob.data.materials.clear();ob.data.materials.append(mat)
rng=random.Random(1414);leaves=[o for o in coll.objects if o.name.startswith('Scanned_maple_leaf_')];extra=0
for leaf in leaves[::2]:
 ob=leaf.copy();ob.data=leaf.data;coll.objects.link(ob);ob.name='Supplementary_scanned_maple_leaf';offset=Vector((rng.uniform(-.035,.035),rng.uniform(-.04,.04),rng.uniform(-.02,.055)));ob.location+=offset;ob.rotation_quaternion=ob.rotation_quaternion@Quaternion((0,1,0),rng.uniform(-.9,.9));ob.scale*=rng.uniform(.8,1.15)
 cu=bpy.data.curves.new('Connected_supplementary_petiole','CURVE');cu.dimensions='3D';cu.bevel_depth=.0008;cu.bevel_resolution=1;sp=cu.splines.new('POLY');sp.points.add(1);sp.points[0].co=(*leaf.location,1);sp.points[1].co=(*ob.location,1);stem=bpy.data.objects.new(cu.name,cu);coll.objects.link(stem);cu.materials.append(mat);extra+=1
scene=bpy.context.scene;scene.cycles.samples=64;scene.cycles.device='CPU';scene.camera.location=(0,-6,1.25);scene.camera.data.ortho_scale=2.25;look_at(scene.camera,(0,0,.95));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m1','revision':args.revision,'source':'r13','status':'author_preview_not_accepted','changes':['Weld UV-split source vertices and solidify remaining open surfaces before volumetric union','Voxel union of main crown branches with trunk and an interior crown core','Unified scanned brown furrowed bark on body and main branches','Small lichen patches and green moss in shader','Denser connected scanned leaf clusters'],'mesh_preparation':prep,'voxel_size_m':.0028,'body_faces':len(body.data.polygons),'leaf_count':len(leaves)+extra,'source_provenance':str((scan/'provenance.json').relative_to(ROOT)),'remaining':['Author visual check','Geometry and bark orientation','Eyes, fingers and root debris','Full multi-angle independent review']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.data.ortho_scale=.9;scene.camera.location=(.4,-3,1.9);look_at(scene.camera,(0,0,1.57));scene.render.filepath=str(out/'crown_detail.png');bpy.ops.render.render(write_still=True)
