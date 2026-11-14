"""Use current geometry/UVs for enamel selection, not a stale pre-calibration probe."""
from pathlib import Path
import bpy,numpy as np,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m4_Ghoul/model_3d'));out=folder/'r17';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r15/inspection/m4_r15.blend'));coll=bpy.data.collections['ASSET_m4'];ob=next(o for o in coll.objects if o.type=='MESH' and len(o.data.polygons)>100000);me=ob.data
v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);idx=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',idx);co=v[idx].reshape(-1,3,3).mean(1)
uv=np.empty(len(me.loops)*2,np.float32);me.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,3,2).mean(1);im=next(n.image for n in me.materials[0].node_tree.nodes if n.type=='TEX_IMAGE' and n.image.colorspace_settings.name=='sRGB');pix=np.empty(len(im.pixels),np.float32);im.pixels.foreach_get(pix);pix=pix.reshape(im.size[1],im.size[0],4);rgb=pix[(uv[:,1]*im.size[1]).astype(int).clip(0,im.size[1]-1),(uv[:,0]*im.size[0]).astype(int).clip(0,im.size[0]-1),:3]
x,y,z=co.T;mask=(abs(x)<.11)&(y<-.355)&(z>.815)&(z<.915)&(rgb[:,2]<rgb[:,0]*.30)&(rgb[:,0]>.20)
labels=np.empty(len(me.polygons),np.int32);me.polygons.foreach_get('material_index',labels);labels[mask]=2;me.polygons.foreach_set('material_index',labels)
skin=me.materials[0].node_tree;bs=skin.nodes.get('Principled BSDF');source=bs.inputs['Base Color'].links[0].from_socket;mix=skin.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(.72,.57,.34,1);skin.links.new(source,mix.inputs[1]);skin.links.new(mix.outputs[0],bs.inputs['Base Color'])
for link in list(bs.inputs['Roughness'].links):skin.links.remove(link)
bs.inputs['Roughness'].default_value=.84;bs.inputs['Subsurface Weight'].default_value=.015
# Enlarge the lower jaw continuously, including the lower dentition.
weight=np.exp(-((v[:,2]-.815)/.046)**2)*np.clip((-.34-v[:,1])/.08,0,1)*np.clip((.16-abs(v[:,0]))/.035,0,1);v[:,0]*=1+.23*weight;v[:,1]-=.025*weight;me.vertices.foreach_set('co',v.ravel());me.update();me.normals_split_custom_set(np.zeros((len(me.loops),3),np.float32))
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=900;scene.render.resolution_y=900;scene.camera.data.ortho_scale=.57;scene.camera.location=(0,-2,1.2);look_at(scene.camera,(0,-.38,1.04))
bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'revision':'r17','status':'author_preview_pending','source':'r15','changes':['Narrow highly saturated side-tooth mask from CURRENT geometry/UVs','Preserve existing correct front tooth assignments and textured enamel shader','Dry yellow-brown skin response; wider projecting lower jaw'],'additional_tooth_faces':int(mask.sum()),'stale_probe_not_used':True,'remaining':['Shoulder surface tears, fibrous cloth ends and hair silhouette still need repair']},indent=2),encoding='utf-8');scene.render.filepath=str(out/'face_preview.png');bpy.ops.render.render(write_still=True)
