"""Replace fused crest and dental blocks with independently modeled geometry."""
from pathlib import Path
import bpy,json,numpy as np,sys,math,hashlib,random
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import material,look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m4_Ghoul/model_3d'));out=folder/'r10/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'m4_r10.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r09/inspection/m4_r09.blend'));coll=bpy.data.collections['ASSET_m4'];body=next(o for o in coll.objects if o.type=='MESH' and len(o.data.polygons)>100000);me=body.data;v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);loops=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',loops);labels=np.empty(len(me.polygons),np.int32);me.polygons.foreach_get('material_index',labels);centers=v[loops].reshape(-1,3,3).mean(1)
report=json.loads((folder/'r09/inspection/inspection.json').read_text());scale=report['uniform_scale'];scalp_center=np.array([0,-.31,1.13]);radii=np.array([.145,.16,.15]);hairfaces=(labels==1)&(centers[:,1]<-.21)&(centers[:,2]>1.03)&(abs(centers[:,0])<.20)
hairverts=np.unique(loops.reshape(-1,3)[hairfaces]);delta=v[hairverts]-scalp_center;length=np.linalg.norm(delta/radii,axis=1);v[hairverts]=scalp_center+delta/np.maximum(length[:,None],1e-6)*.72;labels[(labels==1)&~hairfaces]=0
# Sink the reconstructed dental surface into the mouth, leaving original gums.
probe=np.load(folder/'r04/material_probe.npz');pc=probe['co'];rgb=probe['colors'];tooth=(abs(pc[:,0])<.10)&(pc[:,1]<-.37)&(pc[:,2]>.665)&(pc[:,2]<.815)&(rgb[:,2]<rgb[:,0]*.55)&(rgb[:,0]>.18);tf=tooth.reshape(-1,3).sum(1)>=2;tv=np.unique(loops.reshape(-1,3)[tf]);v[tv,1]+=.055;labels[tf]=0;me.vertices.foreach_set('co',v.ravel());me.polygons.foreach_set('material_index',labels);me.update()
for o in coll.objects:
    if o.name.startswith('Black_bristle_hair'):o.hide_render=True
hairmat=material('Coarse_black_crest_undercoat',(.002,.0015,.001),.88);hairmat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.08
def mesh(name,verts,faces,mat):
    data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);o=bpy.data.objects.new(name,data);coll.objects.link(o);data.materials.append(mat)
    for p in data.polygons:p.use_smooth=True
    return o
verts=[];faces=[];N=96
for j in range(17):
    th=j/16*math.pi/2
    for k in range(N):
        a=k*math.tau/N;verts.append(tuple(scalp_center+np.array([radii[0]*math.sin(th)*math.cos(a),radii[1]*math.sin(th)*math.sin(a),radii[2]*math.cos(th)])))
for j in range(16):
    for k in range(N):i=j*N+k;faces.append((i,j*N+(k+1)%N,(j+1)*N+(k+1)%N,i+N))
mesh('Continuous_crest_scalp',verts,faces,hairmat)
fibremat=bpy.data.materials.new('Black_anatomical_hair_fibres');fibremat.use_nodes=True;nt=fibremat.node_tree;nt.nodes.clear();hair=nt.nodes.new('ShaderNodeBsdfHairPrincipled');hair.parametrization='COLOR';hair.inputs['Color'].default_value=(.006,.0035,.0018,1);hair.inputs['Roughness'].default_value=.53;output=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(hair.outputs[0],output.inputs['Surface']);cu=bpy.data.curves.new('Groomed_black_crest','CURVE');cu.dimensions='3D';cu.bevel_depth=.00020;cu.bevel_resolution=1;cu.materials.append(fibremat);rng=random.Random(410)
for i in range(28000):
    theta=math.acos(rng.uniform(.05,1));a=rng.random()*math.tau;normal=Vector((math.sin(theta)*math.cos(a),math.sin(theta)*math.sin(a),math.cos(theta)));root=Vector(scalp_center)+Vector((radii[0]*normal.x,radii[1]*normal.y,radii[2]*normal.z));direction=(normal*.45+Vector((normal.x*.12,.68,.7))).normalized();length=rng.uniform(.045,.14);phase=rng.random()*math.tau;s=cu.splines.new('POLY');s.points.add(8)
    for j,p in enumerate(s.points):
        t=j/8;co=root+direction*length*t+Vector((math.sin(t*9+phase)*.003*t,.008*t*t,-.025*t*t));p.co=(*co,1);p.radius=max(.015,(1-t)**1.2)
o=bpy.data.objects.new('Individual_crest_hairs',cu);coll.objects.link(o)
enamel=material('Aged_individual_teeth',(.52,.43,.28),.34);eb=enamel.node_tree.nodes.get('Principled BSDF');eb.inputs['Subsurface Weight'].default_value=.05;eb.inputs['Subsurface Radius'].default_value=(.002,.0015,.001)
# Pointed irregular dentition is fully separate from the gum and jaw mesh.
def tooth_mesh(name,x,rootz,length,direction,canine=False):
    vertices=[];faces=[];N=20
    for j in range(13):
        t=j/12;r=(.009 if not canine else .011)*(1-t*.82)*(1+.08*math.sin(t*math.pi));yy=-.500+.014*(abs(x)/.10)**2+.006*t*t;zz=rootz+direction*length*t
        for k in range(N):a=k*math.tau/N;vertices.append((x+r*math.cos(a),yy+r*.62*math.sin(a),zz))
    for j in range(12):
        for k in range(N):i=j*N+k;faces.append((i,j*N+(k+1)%N,(j+1)*N+(k+1)%N,i+N))
    faces.extend([tuple(range(N-1,-1,-1)),tuple(12*N+k for k in range(N))]);mesh(name,vertices,faces,enamel)
for i in range(8):
    x=(i-3.5)*.021;tooth_mesh('Upper_separate_tooth',x,.926-.014*(abs(x)/.08),rng.uniform(.047,.057),-1);tooth_mesh('Lower_separate_tooth',x,.816+.006*(abs(x)/.08),rng.uniform(.033,.043),1)
for side in [-1,1]:tooth_mesh('Long_lateral_fang',side*.092,.939,.080,-1,True)
# Fit both irises symmetrically behind the brow, correcting the recessed left eye.
for prefix in ['Recessed_eyeball','Amber_iris','Dark_pupil']:
    for o in [o for o in coll.objects if o.name.startswith(prefix)]:
        side=-1 if o.location.x<0 else 1;offset=0 if prefix=='Recessed_eyeball' else -.008 if prefix=='Amber_iris' else -.010;o.location=(side*.056,-.459+offset,.975)
scene=bpy.context.scene;scene.cycles.samples=24;camera=scene.camera;camera.data.ortho_scale=1.3*scale*1.28
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(folder/'r10/authoring.blend'))
for name,x,y,z in [('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22),('perspective',1,-1,.7)]:
    camera.location=(x*4.5,y*4.5,.72+z*1.5);look_at(camera,(0,0,.72));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
camera.data.ortho_scale=.55;camera.location=(0,-2,1.25);look_at(camera,(0,-.42,1.05));scene.render.filepath=str(out/'face_detail.png');bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(dest));report.update(revision='r10',source='r09 with actual groomed hair and independent dentition, corrected recessed eye symmetry',sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),status='candidate_not_reviewed',hair_strands=28000,separate_teeth=18);(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
