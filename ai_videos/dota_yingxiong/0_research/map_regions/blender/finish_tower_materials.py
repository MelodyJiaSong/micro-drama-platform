"""Revision 3 fixes upper bone selection and places treads in recessed wall bays."""
from pathlib import Path
import bpy, json, math, numpy as np, sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg26_*/model_3d'));out=folder/'r03';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r02/authoring.blend'));coll=bpy.data.collections['ASSET_bg26']
ob=max((o for o in coll.objects if o.type=='MESH'),key=lambda o:len(o.data.polygons));me=ob.data
vs=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',vs);vs=vs.reshape(-1,3);vi=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',vi);co=vs[vi.reshape(-1,3)].mean(1)
labels=np.empty(len(me.polygons),np.int32);me.polygons.foreach_get('material_index',labels)
bone=next(i for i,m in enumerate(me.materials) if m.name=='Tower_weathered_ivory_bone');crystal=next(i for i,m in enumerate(me.materials) if m.name=='Tower_internal_luminous_fluorite')
r=np.linalg.norm(co[:,:2],axis=1);z=co[:,2]
# Include the shaded sides of the ribs; colour-only thresholding had painted
# these metal and produced mottled ivory/black fragments.
mask=(z>7.55)&(r>1.65)&(labels!=crystal);labels[mask]=bone;me.polygons.foreach_set('material_index',labels)
nt=me.materials[bone].node_tree;bs=nt.nodes.get('Principled BSDF');tex=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and n.image.colorspace_settings.name=='sRGB')
lum=nt.nodes.new('ShaderNodeRGBToBW');nt.links.new(tex.outputs['Color'],lum.inputs[0]);ramp=nt.nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].position=.10;ramp.color_ramp.elements[0].color=(.12,.085,.045,1);ramp.color_ramp.elements[1].position=.85;ramp.color_ramp.elements[1].color=(.68,.60,.44,1)
e=ramp.color_ramp.elements.new(.40);e.color=(.38,.32,.22,1);nt.links.new(lum.outputs[0],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color'])
bs.inputs['Subsurface Weight'].default_value=.025
# Reposition the replacement treads from protruding ribs to four recessed bays.
treads=[o for o in coll.objects if o.name.startswith('Separate_copper_stair_tread')]
mat=bpy.data.materials['Tower_copper_green_treads']
for o in treads:bpy.data.objects.remove(o,do_unlink=True)
count=0
for deg in [22.5,112.5,202.5,292.5]:
 a=math.radians(deg);d=Vector((math.cos(a),math.sin(a),0))
 for zz in np.arange(.36,4.55,.25):
  hit,loc,normal,face=ob.ray_cast(d*15+Vector((0,0,float(zz))),-d)
  if not hit:continue
  loc+=d*.035;bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object
  for c in list(o.users_collection):c.objects.unlink(o)
  coll.objects.link(o);o.name='Recessed_copper_stair_tread';o.scale=(.79,.17,.048);o.rotation_euler.z=a+math.pi/2
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat);b=o.modifiers.new('Cast_edge_rounding','BEVEL');b.width=.012;b.segments=2;count+=1
# Dark green transparent crystal with fine internal fracture boundaries.
nt=me.materials[crystal].node_tree;bs=nt.nodes.get('Principled BSDF')
for link in list(bs.inputs['Emission Strength'].links):nt.links.remove(link)
bs.inputs['Emission Strength'].default_value=.22;bs.inputs['Base Color'].default_value=(.012,.07,.025,1)
shell=bpy.data.materials['Tower_faceted_fluorite_shell'];nt=shell.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.08,.28,.15,1);bs.inputs['Transmission Weight'].default_value=.97
tc=nt.nodes.new('ShaderNodeTexCoord');vor=nt.nodes.new('ShaderNodeTexVoronoi');vor.feature='DISTANCE_TO_EDGE';vor.inputs['Scale'].default_value=3.5;nt.links.new(tc.outputs['Object'],vor.inputs['Vector'])
bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.007;bump.inputs['Strength'].default_value=.35;nt.links.new(vor.outputs['Distance'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
scene=bpy.context.scene;scene.cycles.samples=32;scene.render.filepath=str(out/'tower_preview.png');bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'revision':'r03','source':'r02','status':'author_preview_pending','changes':['Upper bone selection includes shaded rib surfaces','Ivory colour remap preserves texture without metal blotches','Four recessed stair bays instead of ladders on structural ribs','Darker transparent crystal and fracture bump'],'treads':count,'remaining':['Skull topology and material boundaries need independent visual review']},indent=2),encoding='utf-8');bpy.ops.render.render(write_still=True)
