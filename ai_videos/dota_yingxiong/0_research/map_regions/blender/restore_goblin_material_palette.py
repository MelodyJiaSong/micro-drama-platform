"""Use sampled texture hues and world regions for inspectable goblin palette masks."""
from pathlib import Path
import bpy,numpy as np,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m309_*/model_3d'));out=folder/'r02';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r01/inspection/m309_r01.blend'));coll=bpy.data.collections['ASSET_m309'];body=max((o for o in coll.all_objects if o.type=='MESH' and not o.hide_render),key=lambda o:len(o.data.polygons));me=body.data;me.transform(body.matrix_world);body.parent=None;body.matrix_world.identity();me.update();body.name='Goblin_merchant_body'
co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3);indices=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',indices);uv=np.empty(len(me.loops)*2,np.float32);me.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2);image=next(n.image for m in me.materials for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and n.image.colorspace_settings.name=='sRGB');pixels=np.empty(len(image.pixels),np.float32);image.pixels.foreach_get(pixels);w,h=image.size;pixels=pixels.reshape(h,w,4);rgb=pixels[np.clip((uv[:,1]*h).astype(int),0,h-1),np.clip((uv[:,0]*w).astype(int),0,w-1),:3]
maximum=rgb.max(1);minimum=rgb.min(1);diff=np.maximum(maximum-minimum,1e-8);sat=(maximum-minimum)/np.maximum(maximum,1e-8);channel=rgb.argmax(1);hue=np.where(channel==0,(rgb[:,1]-rgb[:,2])/diff,np.where(channel==1,(rgb[:,2]-rgb[:,0])/diff+2,(rgb[:,0]-rgb[:,1])/diff+4))/6;hue%=1;x,y,z=co[indices].T
def smooth(v,lo,hi):t=np.clip((v-lo)/(hi-lo),0,1);return t*t*(3-2*t)
skin=smooth(hue,.082,.098)*(1-smooth(hue,.15,.18))*smooth(sat,.20,.35);skin*=np.maximum(np.maximum(smooth(z,.70,.74),1-smooth(z,.245,.27)),smooth(z,.42,.46))
coat=(1-smooth(hue,.075,.09))*smooth(sat,.12,.24)*(1-smooth(maximum,.35,.52))*smooth(z,.46,.50)*(1-smooth(z,.71,.75))
trim=(1-smooth(hue,.075,.095))*smooth(maximum,.30,.48)*smooth(z,.46,.50)*(1-smooth(z,.70,.74))
hair=(1-smooth(sat,.12,.28))*smooth(maximum,.20,.42)*smooth(z,.72,.76)*np.maximum(smooth(y,.005,.035),smooth(np.abs(x),.065,.085))
masks={'Goblin_skin':skin,'Goblin_coat':coat,'Goblin_trim':trim,'Goblin_hair':hair}
for name,values in masks.items():
 a=me.attributes.new(name,'FLOAT','CORNER');a.data.foreach_set('value',values.astype(np.float32))
for mat in me.materials:
 nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED');source=bs.inputs['Base Color'].links[0].from_socket;color=source
 for attrname,tint in [('Goblin_skin',(.65,.83,.37,1)),('Goblin_coat',(.85,.31,1.12,1)),('Goblin_trim',(.70,.44,.12,1)),('Goblin_hair',(.022,.024,.020,1))]:
  a=n.new('ShaderNodeAttribute');a.attribute_name=attrname;mul=n.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=tint;l.new(source,mul.inputs[1]);mix=n.new('ShaderNodeMixRGB');l.new(a.outputs['Fac'],mix.inputs[0]);l.new(color,mix.inputs[1]);l.new(mul.outputs[0],mix.inputs[2]);color=mix.outputs[0]
 l.new(color,bs.inputs['Base Color']);original_spec=bs.inputs['Specular IOR Level'].default_value
 # Preserve the metallic key/buckle branch; suppress metallic response only in
 # measured organic/fabric regions, and leave unclassified pixels untouched.
 a=n.new('ShaderNodeAttribute');a.attribute_name='Goblin_skin';b=n.new('ShaderNodeAttribute');b.attribute_name='Goblin_coat';c=n.new('ShaderNodeMath');c.operation='MAXIMUM';l.new(a.outputs['Fac'],c.inputs[0]);l.new(b.outputs['Fac'],c.inputs[1]);inverse=n.new('ShaderNodeMath');inverse.operation='SUBTRACT';inverse.inputs[0].default_value=1;l.new(c.outputs[0],inverse.inputs[1])
 if bs.inputs['Metallic'].is_linked:
  metal=bs.inputs['Metallic'].links[0].from_socket;mult=n.new('ShaderNodeMath');mult.operation='MULTIPLY';l.new(metal,mult.inputs[0]);l.new(inverse.outputs[0],mult.inputs[1]);l.new(mult.outputs[0],bs.inputs['Metallic'])
 bs.inputs['Specular IOR Level'].default_value=.20
scene=bpy.context.scene;scene['production_status']='GOBLIN_PALETTE_AUTHOR_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report={'asset_id':'m309','revision':'r02','source':'r01 inspection','status':'author_trial_pending_view','evidence':'material_region_probe.json and pbr_channel_diagnosis.json','mask_corner_counts':{k:int((v>.5).sum()) for k,v in masks.items()},'geometry_changed':False,'metallic_policy':'Original metallic retained outside skin and coat masks; dry specular reduced from .5 to .2','remaining':['Inspect masks for spill onto accessories and face','Hair fragment cleanup and sparse groom','Yellow eyes','Independent review']};(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SAVED',json.dumps(report),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('author_preview',(2.5,-4,1.8),(0,0,.475),1.23),('face_detail',(0,-2,.82),(0,0,.82),.42),('back_detail',(0,2,.79),(0,0,.79),.48)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
