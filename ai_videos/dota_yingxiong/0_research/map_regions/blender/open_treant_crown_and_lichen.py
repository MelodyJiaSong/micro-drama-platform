"""Expose forehead, simplify leaf optics and use larger patchy lichen islands."""
from pathlib import Path
import bpy,json,sys,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m1_Treant/model_3d'));out=folder/'r24';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r23/authoring.blend'));coll=bpy.data.collections['ASSET_m1'];body=max((o for o in coll.objects if o.type=='MESH'),key=lambda o:len(o.data.polygons))
for node in body.data.materials[0].node_tree.nodes:
 if node.type=='TEX_NOISE':
  scale=node.inputs['Scale'].default_value
  if abs(scale-220)<.01:node.inputs['Scale'].default_value=42
  elif abs(scale-12)<.01:node.inputs['Scale'].default_value=8
 elif node.type=='MAP_RANGE':
  pair=tuple(round(node.inputs[k].default_value,3) for k in ['From Min','From Max'])
  changes={(.505,.545):(.50,.59),(.525,.57):(.39,.52),(.42,.58):(.56,.70)}
  if pair in changes:node.inputs['From Min'].default_value,node.inputs['From Max'].default_value=changes[pair]
 elif node.type=='MIX_RGB':
  c=node.inputs[2].default_value
  if abs(c[0]-.18)<.001 and abs(c[1]-.21)<.001:node.inputs[2].default_value=(.105,.12,.095,1)
for index,mat in enumerate(sorted((m for m in bpy.data.materials if m.name.startswith('Scanned_dark_living_maple')),key=lambda m:m.name)):
 nt=mat.node_tree;n,l=nt.nodes,nt.links;images={}
 for node in n:
  if node.type=='TEX_IMAGE' and node.image:
   for key in ['Color','NormalGL','Roughness']:
    if key in node.image.name:images[key]=node.image
 assert len(images)==3
 n.clear();output=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled');l.new(bs.outputs[0],output.inputs['Surface']);bs.inputs['Roughness'].default_value=.72;bs.inputs['Specular IOR Level'].default_value=.045;bs.inputs['Subsurface Weight'].default_value=.015;bs.inputs['Subsurface Scale'].default_value=.0004
 tex=n.new('ShaderNodeTexImage');tex.image=images['Color'];gray=n.new('ShaderNodeRGBToBW');l.new(tex.outputs['Color'],gray.inputs[0]);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.015;ramp.color_ramp.elements[1].position=.5
 palette=[((.002,.004,.001),(.018,.036,.010)),((.003,.004,.002),(.024,.030,.014)),((.003,.002,.004),(.025,.013,.027))][index%3]
 for element,color in zip(ramp.color_ramp.elements,palette):element.color=(*color,1)
 l.new(gray.outputs[0],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color']);tex=n.new('ShaderNodeTexImage');tex.image=images['NormalGL'];nm=n.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.45;l.new(tex.outputs['Color'],nm.inputs['Color']);l.new(nm.outputs[0],bs.inputs['Normal'])
prefixes=('Scanned_maple_leaf_','Supplementary_scanned_maple_leaf','Attached_foliage_twig','Connected_supplementary_petiole','Scanned_leaf_petiole','Native_crown_branch')
def warp(points):
 p=np.asarray(points,dtype=np.float32).copy();weight=np.clip((1.95-p[:,2])/.6,0,1);p[:,2]+=.13*weight;p[:,0]+=.010*np.sin(p[:,2]*21+p[:,1]*5);p[:,1]+=.010*np.sin(p[:,0]*19+p[:,2]*7);return p
changed=0
for ob in coll.objects:
 if not ob.name.startswith(prefixes):continue
 matrix=np.array(ob.matrix_world,dtype=np.float32);rotation=matrix[:3,:3];translation=matrix[:3,3];inv=np.linalg.inv(rotation)
 if ob.type=='MESH':
  co=np.empty(len(ob.data.vertices)*3,np.float32);ob.data.vertices.foreach_get('co',co);co=co.reshape(-1,3);co=(warp(co@rotation.T+translation)-translation)@inv.T;ob.data.vertices.foreach_set('co',co.ravel());ob.data.update()
  if ob.name.startswith(('Scanned_maple_leaf_','Supplementary_scanned_maple_leaf')):
   mod=ob.modifiers.new('Leaf_lamina_thickness','SOLIDIFY');mod.thickness=.00035/max(ob.scale);mod.offset=0
 elif ob.type=='CURVE':
  for sp in ob.data.splines:
   for p in sp.points:
    point=(warp(np.array([rotation@np.array(p.co[:3])+translation]))[0]-translation)@inv.T;p.co=(*point,p.co.w)
   for p in sp.bezier_points:
    for key in ['co','handle_left','handle_right']:
     point=(warp(np.array([rotation@np.array(getattr(p,key))+translation]))[0]-translation)@inv.T;setattr(p,key,Vector(point))
 changed+=1
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.camera.location=(0,-6,1.25);scene.camera.data.ortho_scale=2.25;look_at(scene.camera,(0,0,.95));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m1','revision':'r24','source':'r23','status':'author_preview_not_accepted','changes':['Lift lower crown with one coherent deformation for foliage and attached branches','Direct Principled leaf shader replaces translucent mix; green/plum variation','Thin solid leaf lamina','Coarser irregular gray lichen with less pervasive moss'],'crown_objects_deformed':changed,'remaining':['Head/branch attachment and silhouette','Leaf highlights and lichen appearance','Independent review']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.data.ortho_scale=.95;scene.camera.location=(.4,-3,1.9);look_at(scene.camera,(0,0,1.58));scene.render.filepath=str(out/'crown_detail.png');bpy.ops.render.render(write_still=True)
