"""Revision 21 balances the overly bright hooked fibres in author-only r20."""
from pathlib import Path
import bpy,json,sys,math
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m306_*/model_3d'));out=folder/'r21';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r20/authoring.blend'))
ob=bpy.data.objects['Six_organic_bent_light_filaments'];cu=ob.data;cu.bevel_depth=.00009
directions=[(.45,.1,1),(-.8,-.15,.4),(1,.35,.1),(.15,.75,-.7),(-.55,.25,-.4),(.55,-.6,.4)];lengths=[.21,.15,.17,.16,.14,.15];center=Vector((0,0,1))
for i,(s,direction,length) in enumerate(zip(cu.splines,directions,lengths)):
 d=Vector(direction).normalized();u=d.cross(Vector((0,1,0))).normalized();v=d.cross(u).normalized()
 for j,p in enumerate(s.points):
  t=j/(len(s.points)-1);sign=1 if i%2 else -1
  co=center+d*length*t+u*length*sign*(.22*math.sin(t*math.pi)+.07*math.sin(t*math.pi*2.3))+v*length*.12*math.sin(t*math.pi*1.5)
  p.co=(*co,1);p.radius=max(.001,(1-t)**1.6)
nt=cu.materials[0].node_tree;e=next(n for n in nt.nodes if n.type=='EMISSION');e.inputs[0].default_value=(.28,.72,1,1)
tc=nt.nodes.new('ShaderNodeTexCoord');dist=nt.nodes.new('ShaderNodeVectorMath');dist.operation='DISTANCE';dist.inputs[1].default_value=(0,0,1);nt.links.new(tc.outputs['Object'],dist.inputs[0])
fade=nt.nodes.new('ShaderNodeMapRange');fade.inputs['From Min'].default_value=.025;fade.inputs['From Max'].default_value=.21;fade.inputs['To Min'].default_value=15;fade.inputs['To Max'].default_value=0;nt.links.new(dist.outputs['Value'],fade.inputs[0]);nt.links.new(fade.outputs[0],e.inputs[1])
for m in bpy.data.materials:
 if m.name.startswith('White_dust_fade_'):
  e=next(n for n in m.node_tree.nodes if n.type=='EMISSION');e.inputs[1].default_value*=.35;e.inputs[0].default_value=(.28,.72,1,1)
scene=bpy.context.scene;scene.render.filepath=str(out/'close_preview.png');bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'revision':'r21','source':'r20 author-only, not accepted','status':'author_preview_pending','changes':['Gentle asymmetric S-curves in place of hooked loops','Distance-faded thin cyan-white main fibres','Lower dust radiance with additive transparency'],'remaining':['Full multi-view independent review pending']},indent=2),encoding='utf-8');bpy.ops.render.render(write_still=True)
