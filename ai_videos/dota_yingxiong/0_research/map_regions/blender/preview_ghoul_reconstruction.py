"""Rebuild the crown and teeth from the intact body, then inspect a close preview."""
from pathlib import Path
import bpy,bmesh,json,numpy as np,sys,math,random
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import material,look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m4_Ghoul/model_3d'));out=folder/'r11';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r09/inspection/m4_r09.blend'));coll=bpy.data.collections['ASSET_m4'];body=next(o for o in coll.objects if o.type=='MESH' and len(o.data.polygons)>100000);me=body.data;v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);loops=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',loops);labels=np.empty(len(me.polygons),np.int32);me.polygons.foreach_get('material_index',labels);c=v[loops].reshape(-1,3,3).mean(1);x,y,z=c.T
report=json.loads((folder/'r09/inspection/inspection.json').read_text());scale=report['uniform_scale']
hair_region=(abs(x)<.18)&(y<-.20)&(z>1.045)&(z<1.32)
dental=(abs(x)<.103)&(y<-.45)&(z>.835)&(z<.928)
# Keep a separate skin material on formerly black border polygons.
skin=material('Ghoul_repaired_border_skin',(.26,.225,.17),.8);nt=skin.node_tree;bs=nt.nodes.get('Principled BSDF');tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=110;noise.inputs['Detail'].default_value=4;nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);r=nt.nodes.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.10,.085,.06,1);r.color_ramp.elements[1].color=(.37,.32,.24,1);nt.links.new(noise.outputs[0],r.inputs[0]);nt.links.new(r.outputs[0],bs.inputs['Base Color']);b=nt.nodes.new('ShaderNodeBump');b.inputs['Distance'].default_value=.001;nt.links.new(noise.outputs[0],b.inputs['Height']);nt.links.new(b.outputs[0],bs.inputs['Normal']);me.materials.append(skin);labels[(labels==1)&~hair_region]=len(me.materials)-1;me.polygons.foreach_set('material_index',labels)
bm=bmesh.new();bm.from_mesh(me);bm.faces.ensure_lookup_table();remove=np.flatnonzero(hair_region|dental);bmesh.ops.delete(bm,geom=[bm.faces[int(i)] for i in remove],context='FACES');bm.to_mesh(me);bm.free();me.update()
for ob in coll.objects:
    if ob.name.startswith('Black_bristle_hair'):ob.hide_render=True
hairmat=material('Black_rough_actual_strands',(.002,.0015,.001),.94);hairmat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.06
def mesh(name,verts,faces,mat):
    data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);ob=bpy.data.objects.new(name,data);coll.objects.link(ob);data.materials.append(mat)
    for p in data.polygons:p.use_smooth=True
    return ob
center=Vector((0,-.355,1.065));radii=Vector((.130,.125,.075));verts=[];faces=[];N=64
for j in range(17):
    th=j/16*math.pi/2
    for k in range(N):a=k*math.tau/N;verts.append(tuple(center+Vector((radii.x*math.sin(th)*math.cos(a),radii.y*math.sin(th)*math.sin(a),radii.z*math.cos(th)))))
for j in range(16):
    for k in range(N):faces.append((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k))
mesh('Small_natural_scalp',verts,faces,hairmat);rng=random.Random(411);cu=bpy.data.curves.new('Anatomical_black_groom','CURVE');cu.dimensions='3D';cu.bevel_depth=.00022;cu.bevel_resolution=1;cu.materials.append(hairmat)
for i in range(21000):
    th=math.acos(rng.uniform(.05,1));a=rng.random()*math.tau;n=Vector((math.sin(th)*math.cos(a),math.sin(th)*math.sin(a),math.cos(th)));root=center+Vector((radii.x*n.x,radii.y*n.y,radii.z*n.z));direction=(n*.24+Vector((0,.65,.6))).normalized();length=rng.uniform(.035,.095);s=cu.splines.new('POLY');s.points.add(8);phase=rng.random()*math.tau
    for j,p in enumerate(s.points):t=j/8;co=root+direction*length*t+Vector((.002*math.sin(t*8+phase)*t,0,-.02*t*t));p.co=(*co,1);p.radius=max(.01,1-t)
ob=bpy.data.objects.new('Black_individual_groom',cu);coll.objects.link(ob)
enamel=material('Ghoul_varied_old_enamel',(.36,.29,.18),.45);nt=enamel.node_tree;bs=nt.nodes.get('Principled BSDF');tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=50;nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);r=nt.nodes.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.20,.14,.065,1);r.color_ramp.elements[1].color=(.52,.45,.29,1);nt.links.new(noise.outputs[0],r.inputs[0]);nt.links.new(r.outputs[0],bs.inputs['Base Color'])
def tooth(x,z,length,direction,fang=False):
    vv=[];ff=[];width=.008 if not fang else .009
    for j in range(12):
        t=j/11;rad=width*(1-.62*t)*(1+.12*math.sin(t*math.pi));yy=-.487+.018*(abs(x)/.10)**2+.005*t*t
        for k in range(20):a=k*math.tau/20;vv.append((x+rad*math.cos(a),yy+rad*.6*math.sin(a),z+direction*length*t))
    for j in range(11):
        for k in range(20):ff.append((j*20+k,j*20+(k+1)%20,(j+1)*20+(k+1)%20,(j+1)*20+k))
    ff.extend([tuple(range(19,-1,-1)),tuple(220+k for k in range(20))]);mesh('Individual_anatomical_tooth',vv,ff,enamel)
for j in range(8):
    x=(j-3.5)*.020;tooth(x,.914-.006*abs(x)/.08,rng.uniform(.029,.036),-1);tooth(x,.843+.005*abs(x)/.08,rng.uniform(.023,.029),1)
for side in [-1,1]:tooth(side*.09,.924,.050,-1,True)
for prefix in ['Recessed_eyeball','Amber_iris','Dark_pupil']:
    for o in [o for o in coll.objects if o.name.startswith(prefix)]:
        side=-1 if o.location.x<0 else 1;offset=0 if prefix=='Recessed_eyeball' else -.008 if prefix=='Amber_iris' else -.010;o.location=(side*.056,-.459+offset,.975)
scene=bpy.context.scene;scene.cycles.samples=16;scene.render.resolution_x=720;scene.render.resolution_y=720;camera=scene.camera;camera.data.ortho_scale=.57;camera.location=(0,-2,1.20);look_at(camera,(0,-.38,1.04));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'face_preview.png');bpy.ops.render.render(write_still=True);print('PREVIEW',scene.render.filepath,flush=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r11','status':'author_preview_pending','removed_fused_faces':len(remove),'source':'r09 with actual hair and dentition replacement'},indent=2))
