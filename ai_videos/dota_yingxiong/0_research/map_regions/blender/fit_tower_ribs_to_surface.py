"""Fit authored ribs to measured tower surface instead of nominal radii."""
from pathlib import Path
import bpy,json,math,sys
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg26_*/model_3d'));out=folder/'r10';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r09/authoring.blend'));coll=bpy.data.collections['ASSET_bg26'];body=max((o for o in coll.objects if o.type=='MESH' and not o.name.startswith('Scanned_skull')),key=lambda o:len(o.data.polygons));measurements=[]
def surface(direction,z):
 hit,pos,n,face=body.ray_cast(direction*15+Vector((0,0,z)),-direction)
 if not hit:raise RuntimeError('No tower surface at '+str(z))
 return math.hypot(pos.x,pos.y)
for ob in coll.objects:
 if ob.name.startswith('Continuous_structural_bronze_rib'):
  points=ob.data.splines[0].bezier_points;d=Vector((points[0].co.x,points[0].co.y,0)).normalized()
  for p in points:
   radius=surface(d,min(p.co.z,8.0))+.17;p.co=d*radius+Vector((0,0,p.co.z));measurements.append({'z':p.co.z,'r':radius})
  ob.data.bevel_depth=.23
 elif ob.name.startswith('Large_outward_basal_bone_claw'):
  points=ob.data.splines[0].bezier_points;d=Vector((points[0].co.x,points[0].co.y,0)).normalized();radius=surface(d,1.4)
  for p,offset,z in zip(points,[.10,.35,.75,1.15],[1.45,.95,.32,.10]):p.co=d*(radius+offset)+Vector((0,0,z))
  ob.data.bevel_depth=.35
 elif ob.name.startswith('Bronze_rib_retaining_cuff'):
  d=Vector((ob.location.x,ob.location.y,0)).normalized();z=ob.location.z;ob.location=d*(surface(d,z)+.17)+Vector((0,0,z));ob.scale=(1.18,1.18,1)
nt=bpy.data.materials['Tower_faceted_fluorite_shell'].node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.13
tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=18;noise.inputs['Detail'].default_value=3;nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.003;bump.inputs['Strength'].default_value=.16;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
for n in list(nt.nodes):
 if n.type=='EMISSION' and n.inputs['Strength'].is_linked:
  source=n.inputs['Strength'].links[0].from_socket;mul=nt.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=3.5;nt.links.new(source,mul.inputs[0]);nt.links.new(mul.outputs[0],n.inputs['Strength'])
fractures=[o for o in coll.objects if o.name.startswith('Internal_mineral_fissure')]
for i,ob in enumerate(fractures):ob.hide_render=(i%3!=0)
fmat=bpy.data.materials['Fluorite_internal_fracture_planes'];p=fmat.node_tree.nodes.get('Principled BSDF');p.inputs['IOR'].default_value=1.025;p.inputs['Transmission Weight'].default_value=1;p.inputs['Roughness'].default_value=.12;p.inputs['Base Color'].default_value=(.30,.52,.43,1)
scene=bpy.context.scene;scene.cycles.samples=64;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'bg26','revision':'r10','source':'r09','status':'author_preview_not_accepted','changes':['Ray-fitted structural ribs and claws outside the measured tower surface','Rougher teal mineral, subtle internal fissures and stronger distributed core emission'],'surface_measurements':measurements,'remaining':['Panel seams and stairs','Full independent review']},indent=2),encoding='utf-8');scene.render.filepath=str(out/'tower_preview.png');bpy.ops.render.render(write_still=True)
