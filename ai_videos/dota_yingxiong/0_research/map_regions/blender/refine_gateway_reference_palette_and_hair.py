"""Refine the locally patched merchant's buzzcut, skin and reference clothing."""
from pathlib import Path
import bpy,json,sys,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m303_*/model_3d'));out=folder/'r11';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r10/authoring.blend'));coll=bpy.data.collections['ASSET_m303'];body=bpy.data.objects['Gateway_merchant_body'];me=body.data;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3)
def smooth(v,lo,hi):t=np.clip((v-lo)/(hi-lo),0,1);return t*t*(3-2*t)
front=np.clip((.04-co[:,1])/.09,0,1);temple=np.clip(np.abs(co[:,0]+.007)/.09,0,1);hairline=1.72+(.082-.024*temple)*front;scalp=smooth(co[:,2]-hairline,-.003,.005)*(co[:,2]>1.70);me.attributes['ScalpHair'].data.foreach_set('value',scalp.astype(np.float32))
mat=me.materials[0];nt=mat.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');tex=next(n.image for n in nt.nodes if n.type=='TEX_IMAGE' and n.image and n.image.colorspace_settings.name=='sRGB');pixels=np.empty(len(tex.pixels),np.float32);tex.pixels.foreach_get(pixels);pixels=pixels.reshape(tex.size[1],tex.size[0],4);mask_counts={}
for ob in [body]+[o for o in coll.objects if o.name.startswith('Measured_pinhole_')]:
 mesh=ob.data;pos=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('co',pos);pos=pos.reshape(-1,3);ids=np.empty(len(mesh.loops),np.int32);mesh.loops.foreach_get('vertex_index',ids);uv=np.empty(len(ids)*2,np.float32);mesh.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2);rgb=pixels[np.clip((uv[:,1]*tex.size[1]).astype(int),0,tex.size[1]-1),np.clip((uv[:,0]*tex.size[0]).astype(int),0,tex.size[0]-1),:3];x,y,z=pos[ids].T;hi=rgb.max(1);lo=rgb.min(1);sat=(hi-lo)/np.maximum(hi,1e-6);warm=smooth(rgb[:,0]-rgb[:,2],.025,.10)*smooth(sat,.12,.35)
 head=smooth(z,1.48,1.55);arms=smooth(np.abs(x),.18,.27)*smooth(z,.72,.80)*(1-smooth(z,1.26,1.34));skin=np.maximum(head,arms*warm);shirt=smooth(z,.91,.94)*(1-smooth(z,1.54,1.59))*(1-skin)*(1-smooth(sat,.20,.45));pants=smooth(z,.23,.30)*(1-smooth(z,.89,.94))*(1-arms*warm)
 for name,values in [('Merchant_skin_region',skin),('Merchant_linen_region',shirt),('Merchant_trousers_region',pants)]:
  attr=mesh.attributes.get(name) or mesh.attributes.new(name,'FLOAT','CORNER');attr.data.foreach_set('value',values.astype(np.float32));mask_counts[ob.name+':'+name]=int((values>.5).sum())
colour=bs.inputs['Base Color'].links[0].from_socket
for name,tint in [('Merchant_skin_region',(.72,.56,.45,1)),('Merchant_linen_region',(.62,.58,.52,1)),('Merchant_trousers_region',(.60,.48,.34,1))]:
 attr=nt.nodes.new('ShaderNodeAttribute');attr.attribute_name=name;mul=nt.nodes.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=tint;nt.links.new(colour,mul.inputs[1]);mix=nt.nodes.new('ShaderNodeMixRGB');nt.links.new(attr.outputs['Fac'],mix.inputs[0]);nt.links.new(colour,mix.inputs[1]);nt.links.new(mul.outputs[0],mix.inputs[2]);colour=mix.outputs[0]
nt.links.new(colour,bs.inputs['Base Color'])
for node in nt.nodes:
 if node.type=='ATTRIBUTE' and node.attribute_name=='ScalpHair':
  for link in node.outputs['Fac'].links:
   if link.to_node.type=='MATH' and link.to_node.operation=='MULTIPLY':link.to_node.inputs[1].default_value=.84
patch=bpy.data.objects['MPFB_orbital_skin_patches'];pc=np.empty(len(patch.data.vertices)*3,np.float32);patch.data.vertices.foreach_get('co',pc);pc=pc.reshape(-1,3);d=np.minimum(*[np.sqrt(((pc[:,0]-cx)/.034)**2+((pc[:,2]-1.73)/.028)**2) for cx in [-.0494,.02394]]);weight=smooth(d,.42,.60)*(1-smooth(d,.85,1.12));pc[:,1]+=.0022*weight;patch.data.vertices.foreach_set('co',pc.ravel());patch.data.update()
for pm in patch.data.materials:
 tree=pm.node_tree;p=next(n for n in tree.nodes if n.type=='BSDF_PRINCIPLED');source=p.inputs['Base Color'].links[0].from_socket;mul=tree.nodes.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=(.72,.56,.45,1);tree.links.new(source,mul.inputs[1]);tree.links.new(mul.outputs[0],p.inputs['Base Color']);p.inputs['Roughness'].default_value=.60
 noise=tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1800;noise.inputs['Detail'].default_value=2;bump=tree.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.00007;bump.inputs['Strength'].default_value=.35;tree.links.new(noise.outputs['Fac'],bump.inputs['Height']);tree.links.new(bump.outputs[0],p.inputs['Normal'])
for index,cx in enumerate([-.0494,.02394]):
 iris=bpy.data.objects.get(f'Iris_{index}')
 if iris:
  for v in iris.data.vertices:v.co.x=cx+(v.co.x-cx)*1.16;v.co.z=1.730+(v.co.z-1.730)*1.16
  iris.data.update()
# Replant short hairs on the new hairline; old geometry remains hidden as evidence.
old=bpy.data.objects['Buzzcut_individual_hairs'];old.hide_render=True;old.hide_viewport=True;me.calc_loop_triangles();tri=np.empty(len(me.loop_triangles)*3,np.int32);me.loop_triangles.foreach_get('vertices',tri);tri=tri.reshape(-1,3);cross=np.cross(co[tri[:,1]]-co[tri[:,0]],co[tri[:,2]]-co[tri[:,0]]);area=np.linalg.norm(cross,axis=1)*.5;weights=area*scalp[tri].mean(1);weights[area<1e-12]=0;rng=np.random.default_rng(30311);count=65000;selected=rng.choice(len(tri),count,p=weights/weights.sum());u,v=rng.random(count),rng.random(count);bary=np.column_stack((1-np.sqrt(u),np.sqrt(u)*(1-v),np.sqrt(u)*v));roots=(co[tri[selected]]*bary[:,:,None]).sum(1);normal=cross[selected]/np.maximum(area[selected,None]*2,1e-12);flow=np.tile([0,1,0],(count,1)).astype(float);flow-=normal*(flow*normal).sum(1)[:,None];flow/=np.maximum(np.linalg.norm(flow,axis=1)[:,None],1e-8);length=rng.uniform(.001,.0024,count);points=np.empty((count,4,3),np.float32)
for j,t in enumerate([0,1/3,2/3,1]):points[:,j]=roots+normal*(.00008+length*t*.55)[:,None]+flow*(length*t*.65)[:,None]
curves=bpy.data.hair_curves.new('Natural_short_buzzcut');curves.add_curves([4]*count);curves.set_types(type='CATMULL_ROM');curves.attributes['position'].data.foreach_set('vector',points.ravel());radius=curves.attributes.new('radius','FLOAT','POINT');radius.data.foreach_set('value',(rng.uniform(.000020,.000032,count)[:,None]*np.array([1,.85,.50,.01])).astype(np.float32).ravel());ob=bpy.data.objects.new('Natural_short_buzzcut',curves);coll.objects.link(ob)
for hm in old.data.materials:curves.materials.append(hm)
report={'asset_id':'m303','revision':'r11','source':'r10','status':'author_trial_pending_view','changes':['Less angular hairline with 65000 replanted 1–2.4 mm hairs and partial scalp visibility','Warm skin, grey-taupe linen and dark brown trousers using geometry/colour masks','Orbital annulus recessed by at most 2.2 mm; 70 micron pore bump','Iris radius increased 16 percent'],'mask_corner_counts':mask_counts,'remaining':['Mask spill and collar continuity','Natural hair silhouette and skin','Eye expression and remaining source holes','Independent review']};scene=bpy.context.scene;scene['production_status']='MERCHANT_REFERENCE_PALETTE_GROOM_AUTHOR_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SAVED_REFERENCE_PALETTE_GROOM',flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('face_detail',(0,-2,1.7),(0,0,1.7),.38),('face_side',(1.3,-2,1.7),(0,0,1.7),.38),('author_preview',(4,-6,2),(0,0,.925),2.37)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
