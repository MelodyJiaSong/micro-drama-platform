"""Replace the opaque AI crystal interior with a solid transmissive mineral."""
from pathlib import Path
import bpy,bmesh,json,math,random,sys
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg26_*/model_3d'));out=folder/'r06';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r05/authoring.blend'));coll=bpy.data.collections['ASSET_bg26'];body=max((o for o in coll.objects if o.type=='MESH' and not o.name.startswith('Scanned_skull')),key=lambda o:len(o.data.polygons));me=body.data;idx={m.name:i for i,m in enumerate(me.materials)}
bm=bmesh.new();bm.from_mesh(me);faces=[]
for f in bm.faces:
 c=f.calc_center_median()
 if f.material_index==idx['Tower_internal_luminous_fluorite'] or (c.z>8.2 and math.hypot(c.x,c.y)<1.45 and f.material_index!=idx['Tower_weathered_ivory_bone']):faces.append(f)
bmesh.ops.delete(bm,geom=faces,context='FACES');bm.to_mesh(me);bm.free()
mat=bpy.data.materials['Tower_faceted_fluorite_shell'];nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.24,.60,.35,1);bs.inputs['Transmission Weight'].default_value=1;bs.inputs['Roughness'].default_value=.055;bs.inputs['IOR'].default_value=1.434
vol=nt.nodes.new('ShaderNodeVolumeAbsorption');vol.inputs['Color'].default_value=(.025,.48,.12,1);vol.inputs['Density'].default_value=.6;output=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL');nt.links.new(vol.outputs[0],output.inputs['Volume'])
# Warp the mineral fracture field to avoid a regular polygon grid.
vor=next(n for n in nt.nodes if n.type=='TEX_VORONOI');tc=next(n for n in nt.nodes if n.type=='TEX_COORD');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=2;noise.inputs['Detail'].default_value=4;nt.links.new(tc.outputs['Object'],noise.inputs[0]);scale=nt.nodes.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs['Scale'].default_value=.28;nt.links.new(noise.outputs['Color'],scale.inputs[0]);add=nt.nodes.new('ShaderNodeVectorMath');add.operation='ADD';nt.links.new(tc.outputs['Object'],add.inputs[0]);nt.links.new(scale.outputs[0],add.inputs[1]);nt.links.new(add.outputs[0],vor.inputs[0])
for n in nt.nodes:
 if n.type=='MATH' and n.operation=='MULTIPLY' and n.inputs[1].default_value==.75:n.inputs[1].default_value=.10
def light(name,pos,power):
 data=bpy.data.lights.new(name,'POINT');data.energy=power;data.color=(.05,1,.18);data.shadow_soft_size=.25;o=bpy.data.objects.new(name,data);coll.objects.link(o);o.location=pos
light('Fluorite_internal_base_light',(0,0,7.8),420);light('Fluorite_internal_upper_light',(0,0,10.0),85)
fracture=bpy.data.materials.new('Fluorite_internal_fracture_planes');fracture.use_nodes=True;nt=fracture.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.18,.46,.28,1);bs.inputs['Transmission Weight'].default_value=.94;bs.inputs['Roughness'].default_value=.18;bs.inputs['IOR'].default_value=1.15
rng=random.Random(2606)
for i in range(24):
 z=rng.uniform(7.7,11.6);radius=1.0 if z<10.5 else .6;cx,cy=rng.uniform(-radius*.6,radius*.6),rng.uniform(-radius*.6,radius*.6);length=rng.uniform(.2,.7);v=[(cx-length,cy,z-rng.uniform(.1,.4)),(cx+length,cy+rng.uniform(-.3,.3),z),(cx,cy+rng.uniform(-.4,.4),z+length)]
 data=bpy.data.meshes.new('Internal_mineral_fissure');data.from_pydata(v,[],[(0,1,2)]);data.materials.append(fracture);o=bpy.data.objects.new(data.name,data);coll.objects.link(o)
# Add fine physical pores and narrow dark weather cracks to the large ribs.
mat=bpy.data.materials['Tower_weathered_ivory_bone'];nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');src=bs.inputs['Base Color'].links[0].from_socket;tc=nt.nodes.new('ShaderNodeTexCoord');vor=nt.nodes.new('ShaderNodeTexVoronoi');vor.feature='DISTANCE_TO_EDGE';vor.inputs['Scale'].default_value=8;nt.links.new(tc.outputs['Object'],vor.inputs[0]);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.005;ramp.color_ramp.elements[0].color=(.08,.05,.022,1);ramp.color_ramp.elements[1].position=.022;ramp.color_ramp.elements[1].color=(1,1,1,1);nt.links.new(vor.outputs['Distance'],ramp.inputs[0]);mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.58;nt.links.new(src,mix.inputs[1]);nt.links.new(ramp.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.transmission_bounces=12;scene.render.filepath=str(out/'tower_preview.png');bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'revision':'r06','source':'r05','status':'author_preview_pending','changes':['Opaque AI crystal skin removed inside retained closed faceted shell','Green mineral absorption with internal emitters and 24 real fracture planes','Fine weather cracks on ivory ribs'],'removed_ai_crystal_faces':len(faces),'remaining':['Inspect refraction, light noise, rear geometry and weathering at full views']},indent=2),encoding='utf-8');bpy.ops.render.render(write_still=True)
