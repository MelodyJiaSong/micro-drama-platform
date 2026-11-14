"""Separate and rebuild the coarse cape shell; retain the groomed body and three poles."""
from pathlib import Path
import bpy,bmesh,numpy as np,json,sys,math,random
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('characters/*/m21_Polar_Furbolg/model_3d'));out=folder/'r04';out.mkdir(exist_ok=True);scan=WORLD/'background/map_3d/environment_sources/brown_leather'
if (out/'authoring.blend').exists():raise FileExistsError(out)
assert json.loads((scan/'provenance.json').read_text())['status']=='downloaded_hash_verified'
bpy.ops.wm.open_mainfile(filepath=str(folder/'r03/authoring.blend'));coll=bpy.data.collections['ASSET_m21'];body=max((o for o in coll.objects if o.type=='MESH'),key=lambda o:len(o.data.polygons));me=body.data
def cape_region(x,y,z):return z>1.70 or (y>.13 and z>.85) or (y>.34 and z>.63)
def old_pole(x,y,z):return (x<-.25 and z>1.87) or (x>.23 and y>.10 and z>1.90) or (-.30<x<-.08 and -.15<y<.08 and z>2.07)
bm=bmesh.new();bm.from_mesh(me);cloth_ids=[];pole_ids=[]
for f in bm.faces:
 p=f.calc_center_median()
 if old_pole(*p):pole_ids.append(f.index)
 elif cape_region(*p):cloth_ids.append(f.index)
cloth_set=set(cloth_ids);pole_set=set(pole_ids);cloth_data=me.copy();cb=bmesh.new();cb.from_mesh(cloth_data);bmesh.ops.delete(cb,geom=[f for f in cb.faces if f.index not in cloth_set],context='FACES');bmesh.ops.recalc_face_normals(cb,faces=list(cb.faces));cb.to_mesh(cloth_data);cb.free()
bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.index in cloth_set or f.index in pole_set],context='FACES');bm.to_mesh(me);bm.free();me.update();print('CAPE_SPLIT',len(cloth_ids),'POLE_FACES_REMOVED',len(pole_ids),flush=True)
cloth=bpy.data.objects.new('Reconstructed_leather_cape_shell',cloth_data);coll.objects.link(cloth);cloth_data.materials.clear()
bpy.ops.object.select_all(action='DESELECT');cloth.select_set(True);bpy.context.view_layer.objects.active=cloth
solid=cloth.modifiers.new('Leather_shell_thickness','SOLIDIFY');solid.thickness=.008;solid.offset=-.5;solid.use_quality_normals=True;bpy.ops.object.modifier_apply(modifier=solid.name)
remesh=cloth.modifiers.new('Close_pitted_leather_surface','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.0045;remesh.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=remesh.name)
smooth=cloth.modifiers.new('Smooth_coarse_cape_noise','SMOOTH');smooth.factor=.65;smooth.iterations=5;bpy.ops.object.modifier_apply(modifier=smooth.name)
mat=bpy.data.materials.new('Scanned_worn_brown_leather');mat.use_nodes=True;nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=n.get('Principled BSDF');tc=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=2.5;l.new(tc.outputs['Object'],mapping.inputs[0]);maps={}
for key,pattern in [('color','*albedo*jpg'),('rough','*rough*jpg'),('height','*disp*png')]:
 tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(next(scan.glob(pattern))),check_existing=True);tex.projection='BOX';tex.projection_blend=.25;l.new(mapping.outputs[0],tex.inputs['Vector'])
 if key!='color':tex.image.colorspace_settings.name='Non-Color'
 maps[key]=tex.outputs['Color']
l.new(maps['color'],bs.inputs['Base Color']);l.new(maps['rough'],bs.inputs['Roughness']);bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.0012;bump.inputs['Strength'].default_value=.7;l.new(maps['height'],bump.inputs['Height']);l.new(bump.outputs[0],bs.inputs['Normal']);bs.inputs['Specular IOR Level'].default_value=.25;cloth.data.materials.append(mat)
# Hair remains on the body; former cloth patches must not grow white fur.
hair=next(o for o in coll.objects if o.type=='CURVES');curves=hair.data;coords=np.empty(len(curves.attributes['position'].data)*3,np.float32);curves.attributes['position'].data.foreach_get('vector',coords);coords=coords.reshape(-1,5,3);roots=coords[:,0];keep=~((roots[:,2]>1.70)|((roots[:,1]>.13)&(roots[:,2]>.85))|((roots[:,1]>.34)&(roots[:,2]>.63)));radii=np.empty(len(curves.attributes['radius'].data),np.float32);curves.attributes['radius'].data.foreach_get('value',radii);radii=radii.reshape(-1,5)
new=bpy.data.hair_curves.new('Body_only_polar_guard_hairs');new.add_curves([5]*int(keep.sum()));new.set_types(type='CATMULL_ROM');new.attributes['position'].data.foreach_set('vector',coords[keep].ravel());radius=new.attributes.new('radius','FLOAT','POINT');radius.data.foreach_set('value',radii[keep].ravel())
for m in curves.materials:new.materials.append(m)
hair.data=new
wood=bpy.data.materials.new('Weathered_solid_wood_poles');wood.use_nodes=True;wn,wl=wood.node_tree.nodes,wood.node_tree.links;wb=wn.get('Principled BSDF');wt=wn.new('ShaderNodeTexImage');wt.image=bpy.data.images.load(str(WORLD/'background/map_3d/environment_sources/bark_brown_02/bark_brown_02_diff_4k.jpg'),check_existing=True);wt.projection='BOX';wt.projection_blend=.25;wc=wn.new('ShaderNodeTexCoord');wl.new(wc.outputs['Object'],wt.inputs['Vector']);wl.new(wt.outputs['Color'],wb.inputs['Base Color']);wb.inputs['Roughness'].default_value=.86
rope=bpy.data.materials.new('Dark_hide_pole_bindings');rope.use_nodes=True;rb=rope.node_tree.nodes.get('Principled BSDF');rb.inputs['Base Color'].default_value=(.025,.014,.006,1);rb.inputs['Roughness'].default_value=.9
rng=random.Random(214)
def tube(name,points,radius,material):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=3;cu.use_fill_caps=True;s=cu.splines.new('POLY');s.points.add(len(points)-1)
 for p,co in zip(s.points,points):p.co=(*co,1)
 ob=bpy.data.objects.new(name,cu);coll.objects.link(ob);cu.materials.append(material);return ob
for i,(start,end) in enumerate([((-.10,.0,1.90),(-.21,-.05,2.30)),((-.23,-.01,1.78),(-.39,-.03,2.135)),((.23,.17,1.78),(.31,.30,2.135))]):
 start,end=Vector(start),Vector(end);direction=(end-start).normalized();u=direction.cross(Vector((0,1,0))).normalized();v=direction.cross(u);points=[]
 for j in range(40):
  t=j/39;points.append(start.lerp(end,t)+u*.003*math.sin(t*11+i))
 tube('Three_structural_wood_poles_'+str(i),points,.026 if i else .032,wood)
 mid=start.lerp(end,.64)
 for wrap in range(3):
  loop=[mid+direction*(wrap-1)*.009+(u*math.cos(a)+v*math.sin(a))*.033 for a in np.linspace(0,math.tau,65)];tube('Tied_hide_binding',loop,.004,rope)
 tail=[mid+Vector((.008*math.sin(t*7+i),-.015,t*-.15)) for t in np.linspace(0,1,30)];tube('Hanging_hide_tie',tail,.004,rope)
scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=64;scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';scene.camera.location=(6,-7,3);scene.camera.data.ortho_scale=2.9;look_at(scene.camera,(0,0,1.15))
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m21','revision':'r04','source':'r03','status':'author_preview_not_accepted','changes':['Separate coarse cape, thicken and rebuild closed leather surface','Actual CC0 brown leather scan','Remove original duplicate poles and rebuild exactly three bound wooden supports','Restrict groom to body'],'cape_source_faces':len(cloth_ids),'removed_pole_faces':len(pole_ids),'remaining_hair_curves':int(keep.sum()),'remaining':['Cape/body boundary','Head and shoulder coverage','All-angle geometry and independent review']},indent=2),encoding='utf-8');print('CAPE_REPAIR_SAVED',flush=True)
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.location=(3,4,3.2);scene.camera.data.ortho_scale=1.5;look_at(scene.camera,(0,.1,1.8));scene.render.filepath=str(out/'roof_poles_preview.png');bpy.ops.render.render(write_still=True)
