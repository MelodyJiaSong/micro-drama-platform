"""Fit facial anatomy under the helmet and map the established skin reference."""
from pathlib import Path
import bpy,json,sys,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m300_*/model_3d'));out=folder/'r12';out.mkdir(exist_ok=True)
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
        co=head.data.vertices[head.data.loops[li].vertex_index].co;uv.data[li].uv=(.489+co.x*1.10,.785+(co.z-1.132)*.80)
image=bpy.data.images.load(str(folder.parent/'m300_Weapons_Dealer.png'),check_existing=True)
mat=head.data.materials[0];nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');old=bs.inputs['Base Color'].links[0].from_socket;tex=nt.nodes.new('ShaderNodeTexImage');tex.image=image;tex.extension='EXTEND';uvnode=nt.nodes.new('ShaderNodeUVMap');uvnode.uv_map=uv.name;nt.links.new(uvnode.outputs[0],tex.inputs[0])
# Only the frontal skin uses the established face photograph. Ears and back
# retain a skin shader instead of projecting a second face onto them.
geo=nt.nodes.new('ShaderNodeNewGeometry');vt=nt.nodes.new('ShaderNodeVectorTransform');vt.vector_type='NORMAL';vt.convert_from='WORLD';vt.convert_to='OBJECT';nt.links.new(geo.outputs['Normal'],vt.inputs[0]);sep=nt.nodes.new('ShaderNodeSeparateXYZ');nt.links.new(vt.outputs[0],sep.inputs[0]);r=nt.nodes.new('ShaderNodeMapRange');r.inputs['From Min'].default_value=-.18;r.inputs['From Max'].default_value=-.72;nt.links.new(sep.outputs['Y'],r.inputs['Value']);mix=nt.nodes.new('ShaderNodeMixRGB');nt.links.new(r.outputs[0],mix.inputs[0]);nt.links.new(old,mix.inputs[1]);nt.links.new(tex.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
# Keep the archived generated helmet untouched; replace it with a closed shell.
import bmesh,math
body=next(o for o in coll.objects if o.type=='MESH' and len(o.data.polygons)>100000);me=body.data
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_center_median().z>1.16],context='FACES');bm.to_mesh(me);bm.free()
for o in coll.objects:
    if o.name.startswith(('Fitted_helmet','Helmet_')):o.hide_render=True
steel=me.materials[3];brass=bpy.data.materials['Merchant_worn_brass_details']
def mesh(name,verts,faces,mat):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);o=bpy.data.objects.new(name,me);coll.objects.link(o);me.materials.append(mat)
    for p in me.polygons:p.use_smooth=True
    return o
def curve(name,points,radius,mat):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=3;s=cu.splines.new('POLY');s.points.add(len(points)-1)
    for p,co in zip(s.points,points):p.co=(*co,1)
    o=bpy.data.objects.new(name,cu);coll.objects.link(o);cu.materials.append(mat)
profile=[(1.16,.142),(1.185,.139),(1.22,.124),(1.25,.100),(1.28,.064),(1.301,.025),(1.33,.010),(1.36,.001)];N=96;vv=[];ff=[]
for z,radius in profile:
    for k in range(N):a=k*math.tau/N;vv.append((radius*math.cos(a),-.025+radius*.92*math.sin(a),z))
for j in range(len(profile)-1):
    for k in range(N):a=j*N+k;b=j*N+(k+1)%N;ff.append((a,b,b+N,a+N))
ff.append(tuple(range(N-1,-1,-1)));ff.append(tuple((len(profile)-1)*N+k for k in range(N)));mesh('Closed_forged_spiked_helmet',vv,ff,steel)
curve('Forged_helmet_brass_rim',[(.143*math.cos(k*math.tau/128),-.025+.132*math.sin(k*math.tau/128),1.166) for k in range(129)],.003,brass)
for a in [-math.pi/2,0,math.pi/2,math.pi]:curve('Raised_helmet_rib',[(r*math.cos(a),-.025+r*.92*math.sin(a),z) for z,r in profile],.0015,brass)
for side in [-1,1]:
    vv=[];ff=[]
    for j in range(13):
        v=j/12
        for k in range(13):u=k/12;vv.append((side*(.127+.016*math.sin(v*math.pi)+.006*math.cos(u*math.pi)),-.12+.16*u,1.161-.135*v+.018*u+.01*(2*u-1)**2*v))
    for j in range(12):
        for k in range(12):a=j*13+k;ff.append((a,a+1,a+14,a+13))
    ob=mesh('Curved_hinged_helmet_cheek_guard',vv,ff,steel);solid=ob.modifiers.new('Forged_plate_thickness','SOLIDIFY');solid.thickness=.004
    curve('Cheek_guard_rolled_brass_edge',[vv[12*13+k] for k in range(13)],.0017,brass)
# The reference projection is restricted to central facial skin, excluding ears.
attr=head.data.attributes.new('CentralFaceMask','FLOAT','POINT')
for v,d in zip(head.data.vertices,attr.data):d.value=max(0,min(1,(.102-abs(v.co.x))/.026))
n=nt.nodes.new('ShaderNodeAttribute');n.attribute_name='CentralFaceMask';mul=nt.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';nt.links.new(r.outputs[0],mul.inputs[0]);nt.links.new(n.outputs['Fac'],mul.inputs[1]);nt.links.new(mul.outputs[0],mix.inputs[0])
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=900;scene.render.resolution_y=900;scene.camera.data.ortho_scale=.62;scene.camera.location=(.4,-1.8,1.18);look_at(scene.camera,(0,-.1,1.04));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'face_preview.png');bpy.ops.render.render(write_still=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r12','status':'author_preview_pending','source':'r10 anatomy fitted vertically, frontal skin uses the established character reference through explicit UVs; nonfrontal skin remains procedural','face_reference':'m300_Weapons_Dealer.png','note':'Single-view skin projection requires side-angle inspection; not accepted yet'},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
