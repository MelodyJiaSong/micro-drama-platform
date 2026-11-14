"""Fit facial anatomy under the helmet and map the established skin reference."""
from pathlib import Path
import bpy,json,sys,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m300_*/model_3d'));out=folder/'r11';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r10/authoring.blend'));coll=bpy.data.collections['ASSET_m300'];head=bpy.data.objects['Anatomical_merchant_head']
for v in head.data.vertices:v.co.z+=.025
for o in coll.objects:
    if o.name.startswith(('Inset_anatomical_eye','Blue_iris','Natural_eye_pupil')):o.location.z+=.025
    if o.name.startswith('Volumetric_curly_'):
        for s in o.data.splines:
            for p in s.points:p.co.z+=.025 if 'beard' not in o.name else .025*max(0,min(1,(p.co.z-.70)/.30))
uv=head.data.uv_layers.new(name='Reference_face_projection')
for p in head.data.polygons:
    for li in p.loop_indices:
        co=head.data.vertices[head.data.loops[li].vertex_index].co;uv.data[li].uv=(.489+co.x*1.10,.77125+(co.z-1.132)*.80)
image=bpy.data.images.load(str(folder.parent/'m300_Weapons_Dealer.png'),check_existing=True)
mat=head.data.materials[0];nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');old=bs.inputs['Base Color'].links[0].from_socket;tex=nt.nodes.new('ShaderNodeTexImage');tex.image=image;tex.extension='EXTEND';uvnode=nt.nodes.new('ShaderNodeUVMap');uvnode.uv_map=uv.name;nt.links.new(uvnode.outputs[0],tex.inputs[0])
# Only the frontal skin uses the established face photograph. Ears and back
# retain a skin shader instead of projecting a second face onto them.
geo=nt.nodes.new('ShaderNodeNewGeometry');vt=nt.nodes.new('ShaderNodeVectorTransform');vt.vector_type='NORMAL';vt.convert_from='WORLD';vt.convert_to='OBJECT';nt.links.new(geo.outputs['Normal'],vt.inputs[0]);sep=nt.nodes.new('ShaderNodeSeparateXYZ');nt.links.new(vt.outputs[0],sep.inputs[0]);r=nt.nodes.new('ShaderNodeMapRange');r.inputs['From Min'].default_value=-.18;r.inputs['From Max'].default_value=-.72;nt.links.new(sep.outputs['Y'],r.inputs['Value']);mix=nt.nodes.new('ShaderNodeMixRGB');nt.links.new(r.outputs[0],mix.inputs[0]);nt.links.new(old,mix.inputs[1]);nt.links.new(tex.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
# Smooth voxel-scale chatter on the helmet while retaining its main silhouette.
body=next(o for o in coll.objects if o.type=='MESH' and len(o.data.polygons)>100000);me=body.data;v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);ed=np.empty(len(me.edges)*2,np.int32);me.edges.foreach_get('vertices',ed);ed=ed.reshape(-1,2);a=np.concatenate([ed[:,0],ed[:,1]]);b=np.concatenate([ed[:,1],ed[:,0]]);degree=np.bincount(a,minlength=len(v));mask=v[:,2]>1.165
for _ in range(16):
    avg=np.stack([np.bincount(a,weights=v[b,j],minlength=len(v)) for j in range(3)],1)/np.maximum(degree[:,None],1);v[mask]+=.35*(avg[mask]-v[mask])
me.vertices.foreach_set('co',v.ravel());me.update()
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=900;scene.render.resolution_y=900;scene.camera.data.ortho_scale=.62;scene.camera.location=(.4,-1.8,1.18);look_at(scene.camera,(0,-.1,1.04));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'face_preview.png');bpy.ops.render.render(write_still=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r11','status':'author_preview_pending','source':'r10 anatomy fitted vertically, frontal skin uses the established character reference through explicit UVs; nonfrontal skin remains procedural','face_reference':'m300_Weapons_Dealer.png','note':'Single-view skin projection requires side-angle inspection; not accepted yet'},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
