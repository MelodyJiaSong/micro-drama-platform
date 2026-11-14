"""Fit local MPFB orbital topology and transfer actual baked skin colour."""
from pathlib import Path
import bpy,json,sys,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('characters/*/m303_Gateway_Relics/model_3d'));out=folder/'r04';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r03/authoring.blend'));coll=bpy.data.collections['ASSET_m303'];source=bpy.data.objects['geometry_0'];source.data.transform(source.matrix_world);source.parent=None;source.matrix_world.identity();me=source.data;me.update();source.name='Archive_r03_original_face_skin'
layer=me.color_attributes.new(name='BakedSkin',type='FLOAT_COLOR',domain='CORNER');me.color_attributes.active_color=layer;original=list(me.materials)
for i,mat in enumerate(original):
 copy=mat.copy();me.materials[i]=copy;nt=copy.node_tree;bs=next(q for q in nt.nodes if q.type=='BSDF_PRINCIPLED');em=nt.nodes.new('ShaderNodeEmission');nt.links.new(bs.inputs['Base Color'].links[0].from_socket,em.inputs[0]);nt.links.new(em.outputs[0],next(q for q in nt.nodes if q.type=='OUTPUT_MATERIAL').inputs['Surface'])
bpy.ops.object.select_all(action='DESELECT');source.select_set(True);bpy.context.view_layer.objects.active=source;scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=1;scene.render.bake.target='VERTEX_COLORS';bpy.ops.object.bake(type='EMIT');me.materials.clear()
for mat in original:me.materials.append(mat)
print('SKIN_COLOUR_BAKED',flush=True)
body=source.copy();body.data=me.copy();body.name='Gateway_merchant_body';coll.objects.link(body);source.hide_render=True;source.hide_viewport=True;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3);loops=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',loops);colours=np.empty(len(layer.data)*4,np.float32);layer.data.foreach_get('color',colours);colours=colours.reshape(-1,4)
centres=[-.0494,.02394]
def smooth(a,lo,hi):
 t=np.clip((a-lo)/(hi-lo),0,1);return t*t*(3-2*t)
def distance(p):return np.minimum(*[np.sqrt(((p[:,0]-cx)/.034)**2+((p[:,2]-1.73)/.028)**2) for cx in centres])
rim=(distance(co[loops])>.65)&(distance(co[loops])<1.05)&(co[loops,1]<-.025)&(co[loops,2]<1.744);skinmean=np.median(colours[rim,:3],axis=0);print('ORBITAL_SKIN_LINEAR',skinmean.tolist(),flush=True)
# Keep the original head, jaw, nose and mouth. Only the two failed orbital patches
# are recessed underneath a continuous anatomical lid/cheek patch.
d=distance(co);co[:,1]+=.025*(1-smooth(d,.70,1.02))*(co[:,1]<.015);body.data.vertices.foreach_set('co',co.ravel());body.data.update()
with bpy.data.libraries.load(str(WORLD/'background/map_3d/anatomy_sources/mpfb_merchant_source.blend'),link=False) as (src,dst):dst.objects=[src.objects[0]]
human=dst.objects[0];coll.objects.link(human)
for mod in human.modifiers:mod.show_viewport=False;mod.show_render=False
bpy.context.view_layer.update();ev=human.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh();gi=human.vertex_groups['body'].index;bodyids={v.index for v in human.data.vertices if any(g.group==gi and g.weight>.1 for g in v.groups)};sx=(centres[1]-centres[0])/(2*.03193683782592416)
positions=np.array([(v.co.x*sx-.01273,(v.co.y+.12483159638941288)*.90-.0545,v.co.z-1.6168598681688309+1.73) for v in mesh.vertices]);dd=distance(positions);polys=[list(p.vertices) for p in mesh.polygons if all(i in bodyids and dd[i]<1.25 and positions[i,1]<.018 for i in p.vertices)];used=sorted({i for p in polys for i in p});mapping={old:new for new,old in enumerate(used)};vv=[]
source.hide_viewport=False;bpy.context.view_layer.update()
for i in used:
 point=Vector(positions[i]);hit,p,n,face=source.ray_cast(Vector((point.x,-.4,point.z)),Vector((0,1,0)));blend=float(smooth(np.array([dd[i]]),.58,1.08)[0])
 if hit and p.y<.015:point.y=point.y*(1-blend)+(p.y-.00035)*blend
 vv.append(tuple(point))
patchmesh=bpy.data.meshes.new('MPFB_anatomical_orbital_loops');patchmesh.from_pydata(vv,[],[[mapping[i] for i in p] for p in polys]);patch=bpy.data.objects.new('MPFB_orbital_skin_patches',patchmesh);coll.objects.link(patch);ev.to_mesh_clear();bpy.data.objects.remove(human,do_unlink=True)
for p in patchmesh.polygons:p.use_smooth=True
bpy.ops.object.select_all(action='DESELECT');patch.select_set(True);bpy.context.view_layer.objects.active=patch;sub=patch.modifiers.new('Anatomical_patch_subdivision','SUBSURF');sub.levels=sub.render_levels=2;bpy.ops.object.modifier_apply(modifier=sub.name);patch.data.color_attributes.new(name='BakedSkin',type='FLOAT_COLOR',domain='CORNER');transfer=patch.modifiers.new('Local_baked_skin_colour_transfer','DATA_TRANSFER');transfer.object=source;transfer.use_loop_data=True;transfer.data_types_loops={'COLOR_CORNER'};transfer.loop_mapping='POLYINTERP_NEAREST';transfer.layers_vcol_loop_select_src='ALL';transfer.layers_vcol_loop_select_dst='NAME';bpy.ops.object.modifier_apply(modifier=transfer.name)
source.hide_viewport=True
pc=np.empty(len(patch.data.vertices)*3,np.float32);patch.data.vertices.foreach_get('co',pc);pc=pc.reshape(-1,3);li=np.empty(len(patch.data.loops),np.int32);patch.data.loops.foreach_get('vertex_index',li);lc=np.empty(len(li)*4,np.float32);patch.data.color_attributes['BakedSkin'].data.foreach_get('color',lc);lc=lc.reshape(-1,4);weight=1-smooth(distance(pc[li]),.40,.85);lc[:,:3]=lc[:,:3]*(1-weight[:,None])+skinmean*weight[:,None];patch.data.color_attributes['BakedSkin'].data.foreach_set('color',lc.ravel())
skin=bpy.data.materials.new('Baked_local_skin_continuity');skin.use_nodes=True;nt=skin.node_tree;bs=nt.nodes.get('Principled BSDF');attr=nt.nodes.new('ShaderNodeVertexColor');attr.layer_name='BakedSkin';nt.links.new(attr.outputs[0],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.67;bs.inputs['Specular IOR Level'].default_value=.28;bs.inputs['Subsurface Weight'].default_value=.06;bs.inputs['Subsurface Radius'].default_value=(.012,.005,.002);patch.data.materials.append(skin)
# Use the source anatomy's actual ellipsoidal eye volume, fitted with the same
# transform as the lids. The earlier generic annular lid mesh is not reused.
white=bpy.data.materials.new('Natural_warm_sclera');white.use_nodes=True;wbs=white.node_tree.nodes.get('Principled BSDF');wbs.inputs['Base Color'].default_value=(.48,.44,.38,1);wbs.inputs['Roughness'].default_value=.24;wbs.inputs['IOR'].default_value=1.38
for j,cx in enumerate(centres):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=1,location=(cx,-.0545,1.73));eye=bpy.context.object
 for c in list(eye.users_collection):c.objects.unlink(eye)
 coll.objects.link(eye);eye.name=f'Anatomical_eye_volume_{j}';eye.scale=(.016*sx,.016*.90,.016);eye.data.materials.append(white)
 for p in eye.data.polygons:p.use_smooth=True
names=['Iris_0','Iris_1','Pupil_0','Pupil_1','Buzzcut_individual_hairs','Stubble_individual_hairs','Brows_individual_hairs','geometry_0']
with bpy.data.libraries.load(str(folder/'r02/authoring.blend'),link=False) as (src,dst):dst.objects=[name for name in names if name in src.objects]
grooms=[]
for ob in dst.objects:
 if ob.name.startswith('geometry_0'):
  assert len(ob.data.vertices)==len(body.data.vertices)
  for name in ['ScalpHair','BeardStubble','Eyebrows']:
   values=np.empty(len(body.data.vertices),np.float32);ob.data.attributes[name].data.foreach_get('value',values);attr=body.data.attributes.new(name,'FLOAT','POINT');attr.data.foreach_set('value',values)
  bpy.data.objects.remove(ob,do_unlink=True);continue
 coll.objects.link(ob)
 if ob.name.startswith(('Iris','Pupil')):ob.location.y+=.0021
 else:grooms.append(ob)
bodymat=body.data.materials[0].copy();body.data.materials[0]=bodymat;nt=bodymat.node_tree;bs=next(q for q in nt.nodes if q.type=='BSDF_PRINCIPLED');colour=bs.inputs['Base Color'].links[0].from_socket
for name,strength in [('ScalpHair',.98),('BeardStubble',.50),('Eyebrows',.80)]:
 attr=nt.nodes.new('ShaderNodeAttribute');attr.attribute_name=name;factor=nt.nodes.new('ShaderNodeMath');factor.operation='MULTIPLY';factor.inputs[1].default_value=strength;nt.links.new(attr.outputs['Fac'],factor.inputs[0]);mix=nt.nodes.new('ShaderNodeMixRGB');mix.inputs[2].default_value=(.002,.0015,.001,1);nt.links.new(factor.outputs[0],mix.inputs[0]);nt.links.new(colour,mix.inputs[1]);colour=mix.outputs[0]
nt.links.new(colour,bs.inputs['Base Color'])
hair=bpy.data.materials.new('Matte_black_short_hair');hair.use_nodes=True;hbs=hair.node_tree.nodes.get('Principled BSDF');hbs.inputs['Base Color'].default_value=(.003,.002,.0015,1);hbs.inputs['Roughness'].default_value=.82;hbs.inputs['Specular IOR Level'].default_value=.15
for ob in grooms:ob.data.materials.clear();ob.data.materials.append(hair)
scene.render.bake.target='IMAGE_TEXTURES';scene.cycles.samples=48;scene['production_status']='MPFB_ORBITAL_FIT_AUTHOR_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'asset_id':'m303','revision':'r04','source':'r03 body and local MPFB orbital topology','status':'author_trial_pending_view','rejected_prior':'r02 generic lid rings had UV streaks and protruding sclera','patch_faces':len(patch.data.polygons),'skin_colour_linear':skinmean.tolist(),'eyes_fitted_to_measured_world_landmarks':centres,'remaining':['Anatomical orbital fit and boundary continuity','Natural gaze and expression','Black hair/stubble coverage','Source holes away from eye regions','Independent review']},indent=2),encoding='utf-8');print('ANATOMICAL_ORBITAL_PATCH_SAVED',flush=True)
for name,loc in [('face_detail',(0,-2,1.70)),('face_side',(1.3,-2,1.70))]:
 scene.camera.location=loc;look_at(scene.camera,(0,0,1.70));scene.camera.data.ortho_scale=.38;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
