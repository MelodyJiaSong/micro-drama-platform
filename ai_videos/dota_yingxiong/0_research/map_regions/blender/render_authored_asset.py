"""Render reviewed authoring checkpoints into hash-bound inspection candidates."""
from pathlib import Path
import bpy,bmesh,json,hashlib,sys,argparse
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
p=argparse.ArgumentParser();p.add_argument('asset');p.add_argument('--revision',required=True);p.add_argument('--base-revision',required=True);args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));manifest=json.loads((WORLD/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'));a=next(a for a in manifest['assets'] if a['id']==args.asset);folder=ROOT/a['model_directory'];out=folder/args.revision/'inspection';out.mkdir(exist_ok=True);dest=out/f'{args.asset}_{args.revision}.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(folder/args.revision/'authoring.blend'));scene=bpy.context.scene;scene.cycles.samples=max(96,scene.cycles.samples) if args.asset=='m306' and not scene.cycles.use_denoising else 24;scene.render.resolution_x=1000;scene.render.resolution_y=1000;camera=scene.camera
# The radial soil hummocks have coincident centre-ring vertices. Weld only those
# authored meshes in this inspection copy; retain the source checkpoint intact.
inspection_cleanup=[]
if args.asset=='bg23':
    for ob in bpy.data.collections['ASSET_bg23'].all_objects:
        if ob.hide_render or ob.type!='MESH' or not ob.name.startswith('Small_irregular_root_soil_hummock'):continue
        bm=bmesh.new();bm.from_mesh(ob.data);before=len(bm.verts)
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update()
        degenerate=sum(p.area<1e-12 for p in ob.data.polygons)
        if degenerate:raise ValueError((ob.name,'degenerate soil faces',degenerate))
        inspection_cleanup.append({'object':ob.name,'vertices_welded':before-len(ob.data.vertices),'degenerate_faces_after':degenerate})
empty_meshes=[o.name for o in bpy.data.collections['ASSET_'+args.asset].all_objects if not o.hide_render and o.type=='MESH' and not len(o.data.polygons)]
if empty_meshes:raise ValueError({'visible_empty_meshes':empty_meshes,'reason':'Check failed Boolean results before rendering a candidate'})
if args.asset in ['bg26','bg23','m1']:scene.cycles.samples=48
if args.asset=='m21':scene.cycles.samples=64
if args.asset=='bg23' and bpy.data.objects.get('Studio_floor'):bpy.data.objects['Studio_floor'].scale*=4
size,center,distance,ortho={'m21':(2.3,1.15,6.9,2.95),'m26':(5,1.24,15,6.4),'m303':(1.85,.925,5.55,2.37),'m16':(2.9,1.45,8.7,3.71),'m1':(1.9,.95,5.7,2.5),'m5':(2,1,6,2.56),'m4':(1.5,.75,4.5,1.9),'m300':(1.35,.675,4.05,1.73),'bg2':(20,10,70,27),'bg12':(7,3.5,25,12),'bg15':(5,2.3,25,12.5),'bg23':(5,2.5,18,7),'bg26':(13,6.5,35,18),'bg3':(14,7,45,20),'m306':(.4,.65,4,1.65)}[args.asset];camera.data.ortho_scale=ortho
for name,x,y,z in [('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22),('perspective',1,-1,.7)]:
    camera.location=(x*distance,y*distance,(2.5 if name=='perspective' else 1.65) if args.asset=='m306' else center+z*size);look_at(camera,(0,0,center));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
supplement=[]
if args.asset=='m1':camera.data.ortho_scale=.95;camera.location=(.4,-3,1.9);look_at(camera,(0,0,1.57));supplement=['crown_detail.png']
elif args.asset=='m21':camera.data.ortho_scale=.9;camera.location=(.65,-3,1.6);look_at(camera,(.15,-.15,1.28));supplement=['fur_detail.png']
elif args.asset=='m16':camera.data.ortho_scale=1.3;camera.location=(0,-4,2.5);look_at(camera,(0,0,2.5));supplement=['face_detail.png']
elif args.asset=='m4':camera.data.ortho_scale=.57;camera.location=(0,-2,1.2);look_at(camera,(0,-.38,1.04));supplement=['face_detail.png']
elif args.asset=='m300':camera.data.ortho_scale=.65;camera.location=(.7,-1.6,1.2);look_at(camera,(0,-.1,1.02));supplement=['face_detail.png']
elif args.asset=='bg2':camera.data.ortho_scale=12;camera.location=(0,-30,9);look_at(camera,(0,0,3));supplement=['base_detail.png']
elif args.asset=='bg23':camera.data.ortho_scale=6.8;camera.location=(10.5,-15,11.5);look_at(camera,(0,0,2.5));supplement=['roof_detail.png']
elif args.asset=='bg12':camera.data.ortho_scale=5;camera.location=(7,-15,8);look_at(camera,(1,.3,4.7));supplement=['roof_detail.png']
elif args.asset=='bg26':camera.data.ortho_scale=9;camera.location=(9,-20,11);look_at(camera,(0,0,9));supplement=['crystal_and_bone_detail.png']
elif args.asset=='bg3':camera.data.ortho_scale=10;camera.location=(0,-25,9);look_at(camera,(0,0,8));supplement=['ice_detail.png']
elif args.asset=='m306':camera.data.ortho_scale=.72;camera.location=(1.1,-1.6,1.25);look_at(camera,(0,.05,1));supplement=['close.png']
for name in supplement:scene.render.filepath=str(out/name);bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
if args.asset=='m26':
    scene.cycles.samples=48
    for name,loc,target,scale in [('head_detail',(5,-3,2.4),(1.65,0,1.05),1.9),('back_detail',(1,-4,4),(.1,0,1.8),2.3),('far_back_detail',(-1,4,4),(.1,0,1.8),2.3)]:
        camera.location=loc;look_at(camera,target);camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);supplement.append(name+'.png')
if args.asset=='m303':
    scene.cycles.samples=48;camera.location=(0,-2,1.70);look_at(camera,(0,0,1.70));camera.data.ortho_scale=.38;scene.render.filepath=str(out/'face_detail.png');bpy.ops.render.render(write_still=True);supplement.append('face_detail.png')
if args.asset=='bg23':
    camera.location=(6,-7,3);camera.data.ortho_scale=3.8;look_at(camera,(1.25,-.9,.35));scene.render.filepath=str(out/'root_detail.png');bpy.ops.render.render(write_still=True);supplement.append('root_detail.png');print('RENDERED root_detail.png',flush=True)
    if bpy.data.objects.get('Hook_to_globe_cradle_structural_bracket'):
        camera.location=(8,1.0,4.55);camera.data.ortho_scale=1.5;look_at(camera,(1.1,1.0,4.45));scene.render.filepath=str(out/'hook_side_detail.png');bpy.ops.render.render(write_still=True);supplement.append('hook_side_detail.png');print('RENDERED hook_side_detail.png',flush=True)
        if bpy.data.objects.get('Continuous_round_hook_and_cradle_return'):
            ball=max((o for o in bpy.data.collections['ASSET_bg23'].objects if not o.hide_render and o.name.startswith('Reference_mirror_sphere')),key=lambda o:o.matrix_world.translation.z);original_mats=list(ball.data.materials);diagnostic=bpy.data.materials.new('Diagnostic_matte_clearance_control');diagnostic.use_nodes=True;shader=diagnostic.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=(.35,.35,.35,1);shader.inputs['Roughness'].default_value=.85;shader.inputs['Metallic'].default_value=0;ball.data.materials.clear();ball.data.materials.append(diagnostic)
            scene.render.filepath=str(out/'hook_matte_clearance_control.png');bpy.ops.render.render(write_still=True);supplement.append('hook_matte_clearance_control.png')
            ball.data.materials.clear()
            for mat in original_mats:ball.data.materials.append(mat)
if args.asset=='m1':
    camera.data.ortho_scale=1.25;camera.location=(0,0,4);look_at(camera,(0,0,1.4));scene.render.filepath=str(out/'top.png');bpy.ops.render.render(write_still=True);supplement.append('top.png')
if args.asset=='m306':
    for name,loc in [('top',(0,0,4)),('bottom',(0,0,.2))]:
        camera.data.ortho_scale=.8;camera.location=loc;look_at(camera,(0,.05,1));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);supplement.append(name+'.png');print('RENDERED',name,flush=True)
    # Demonstrate illumination from the asset itself on a rough surface.
    asset_objects=set(bpy.data.collections['ASSET_m306'].all_objects)
    studio_lights=[o for o in scene.objects if o.type=='LIGHT' and o not in asset_objects]
    states={o:o.hide_render for o in studio_lights}
    for ob in studio_lights:ob.hide_render=True
    bg=scene.world.node_tree.nodes.get('Background');world_strength=bg.inputs[1].default_value;bg.inputs[1].default_value=.015
    floor=bpy.data.objects.get('Studio_floor');old_floor=list(floor.data.materials) if floor else []
    if floor:
        mat=bpy.data.materials.new('Night_test_rough_ground');mat.use_nodes=True;nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.07,.055,.035,1);bs.inputs['Roughness'].default_value=.9
        noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=75;bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.005;bump.inputs['Strength'].default_value=.5;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal']);floor.data.materials.clear();floor.data.materials.append(mat)
    camera.data.ortho_scale=1.8;camera.location=(1.4,-2.4,1.7);look_at(camera,(0,.03,.62));scene.render.filepath=str(out/'night_self_illumination.png');bpy.ops.render.render(write_still=True);supplement.append('night_self_illumination.png')
    if floor:
        # A neutral reflectance control separates emitted light colour from the
        # deliberate warm brown reflectance of the preceding ground test.
        bs.inputs['Base Color'].default_value=(.18,.18,.18,1)
        scene.render.filepath=str(out/'night_neutral_ground_control.png');bpy.ops.render.render(write_still=True);supplement.append('night_neutral_ground_control.png')
    for ob,state in states.items():ob.hide_render=state
    bg.inputs[1].default_value=world_strength
    if floor:
        floor.data.materials.clear()
        for mat in old_floor:floor.data.materials.append(mat)
scene['production_status']='DETAILED_CANDIDATE_NOT_INDEPENDENTLY_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
# Recompute current mesh evidence instead of inheriting stale face counts from
# the AI source or an earlier manual revision. Hidden archive objects are excluded.
coll=bpy.data.collections['ASSET_'+args.asset];visible=[o for o in coll.all_objects if not o.hide_render];counts={}
for ob in visible:
    if ob.type!='MESH':continue
    for poly in ob.data.polygons:
        mat=ob.data.materials[poly.material_index] if poly.material_index<len(ob.data.materials) else None
        key=mat.name if mat else '(none)';counts[key]=counts.get(key,0)+1
author=json.loads((folder/args.revision/'authoring.json').read_text())
materials={}
used_materials={slot.material for ob in visible if hasattr(ob,'material_slots') for slot in ob.material_slots if slot.material}
def shader_nodes(tree,path='',stack=()):
    if tree in stack:return []
    result=[]
    for node in tree.nodes:
        current=path+'/'+node.name
        if node.type=='GROUP' and node.node_tree:result.extend(shader_nodes(node.node_tree,current,stack+(tree,)))
        elif any(t in node.type for t in ('BSDF','EMISSION','VOLUME')):result.append((current,node))
    return result
def input_value(node,key):
    socket=node.inputs.get(key)
    if socket is None:return 'not_available'
    if socket.is_linked:return 'linked'
    value=socket.default_value
    return value if isinstance(value,(float,int,bool,str)) else list(value)
for mat in used_materials:
    if not mat or not mat.use_nodes:continue
    nodes=shader_nodes(mat.node_tree)
    materials[mat.name]={'shader_nodes':[n.type for path,n in nodes],'principled_values':[dict(path=path,**{key:input_value(n,key) for key in ['Roughness','Metallic','Transmission Weight','IOR','Emission Strength','Emission Color']}) for path,n in nodes if n.type=='BSDF_PRINCIPLED'],'volume_values':[dict(path=path,**{key:input_value(n,key) for key in ['Density','Emission Strength']}) for path,n in nodes if n.type=='PRINCIPLED_VOLUME'],'nested_groups_included':True}
optics={'lights':[{'name':o.name,'type':o.data.type,'watts':o.data.energy,'position':list(o.location)} for o in visible if o.type=='LIGHT'],'curves':[{'name':o.name,'splines':len(o.data.splines),'bevel_depth_m':o.data.bevel_depth} for o in visible if o.type=='CURVE']}
optics['hair_curves']=[{'name':o.name,'strands':len(o.data.curves),'points':len(o.data.points),'materials':[m.name for m in o.data.materials]} for o in visible if o.type=='CURVES']
for row in optics['curves']:
    ob=bpy.data.objects[row['name']];radii=[p.radius for sp in ob.data.splines for p in (sp.bezier_points if sp.type=='BEZIER' else sp.points)]
    row['control_point_radius_range']=[min(radii),max(radii)] if radii else None
    row['radius_note']='Point radius multiplies bevel_depth; world object scaling is additional. Visibility and actual connections still require image/geometry checks.'
modifiers={}
for ob in visible:
    for m in ob.modifiers:
        if m.show_render:modifiers[m.type]=modifiers.get(m.type,0)+1
report=dict(author,asset_id=args.asset,revision=args.revision,status='candidate_not_reviewed',sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),views=['south.png','east.png','north.png','west.png','perspective.png'],supplemental_views=supplement,visible_object_count=len(visible),visible_mesh_faces_by_material=counts,material_shader_evidence=materials,optical_geometry=optics,enabled_render_modifiers=modifiers,render_settings={'samples':scene.cycles.samples,'denoising':scene.cycles.use_denoising,'transparent_bounces':scene.cycles.transparent_max_bounces},metrics_note='Current revision base meshes and recursive shader nodes. Modifiers and instances are not expanded. Low base face counts do not mean texture-only construction. Names do not specify shader behavior. No topology acceptance is implied.',base_source_inspection=str(folder/args.base_revision/'inspection/inspection.json'))
points=[ob.matrix_world@Vector(corner) for ob in visible if ob.type in ('MESH','CURVE','CURVES') for corner in ob.bound_box]
if points:
 low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)];report['asset_bounds_m']=[low,high];report['asset_dimensions_m']=[high[i]-low[i] for i in range(3)]
report['render_settings']['studio_lights']=[{'name':ob.name,'watts':ob.data.energy,'type':ob.data.type} for ob in scene.objects if ob.type=='LIGHT' and ob not in visible and not ob.hide_render]
report['inspection_copy_cleanup']=inspection_cleanup
(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
