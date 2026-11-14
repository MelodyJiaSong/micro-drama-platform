"""Replace blade-like moss and bead-like crystal clusters with low moss and inset geodes."""
from pathlib import Path
import bpy,json,sys,math,random,bmesh
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r43';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r42/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];parent=bpy.data.objects['Asset_metre_calibration'];bpy.context.view_layer.update();inverse=parent.matrix_world.inverted();rng=random.Random(2343)
moss=bpy.data.materials['Damp_cornice_moss'];bs=moss.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.045,.065,.012,1)
bm=bmesh.new()
for j in range(9):
 a=rng.uniform(0,math.tau);r=rng.uniform(0,.035);result=bmesh.ops.create_icosphere(bm,subdivisions=2,radius=1)
 for v in result['verts']:v.co=Vector((v.co.x*.022+r*math.cos(a),v.co.y*.018+r*math.sin(a),v.co.z*.008+.004))
mesh=bpy.data.meshes.new('Low_cushion_moss_shared');bm.to_mesh(mesh);bm.free();mesh.materials.append(moss)
for p in mesh.polygons:p.use_smooth=True
count=0
for ob in coll.objects:
 if ob.name.startswith('Cornice_moss_tuft'):ob.data=mesh;count+=1
materials=[]
for j,color in enumerate([(.085,.025,.17,1),(.14,.045,.24,1),(.045,.012,.10,1)]):
 mat=bpy.data.materials.new(f'Inset_quartz_amethyst_{j}');mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=color;bs.inputs['Roughness'].default_value=.20+j*.035;bs.inputs['Transmission Weight'].default_value=.25;bs.inputs['IOR'].default_value=1.54;bs.inputs['Coat Weight'].default_value=.12;materials.append(mat)
for ob in coll.objects:
 if ob.name.startswith('Raw_amethyst_cluster_crystal'):ob.hide_render=True;ob.hide_viewport=True
slabs=[ob for ob in coll.objects if ob.name.startswith('Inset_amethyst_plinth_slab')];geodes=0
for slab in slabs:
 center=sum((inverse@slab.matrix_world@v.co for v in slab.data.vertices),Vector())/len(slab.data.vertices);angle=round(math.atan2(center.y,center.x)/(math.pi/4))*math.pi/4;n=Vector((math.cos(angle),math.sin(angle),0));t=Vector((-n.y,n.x,0));up=Vector((0,0,1));verts=[];faces=[];sides=12
 for ring in range(3):
  scale=[1,.72,.28][ring]
  for k in range(sides):
   a=k*math.tau/sides;w=.145*scale*rng.uniform(.90,1.06);h=.105*scale*rng.uniform(.90,1.06);depth=[-.035,.012,.045][ring]+rng.uniform(-.012,.012);verts.append(tuple(center+t*math.cos(a)*w+up*math.sin(a)*h+n*depth))
 verts.append(tuple(center+n*.025));tip=len(verts)-1
 for ring in range(2):
  for k in range(sides):
   a=ring*sides+k;b=ring*sides+(k+1)%sides;c=(ring+1)*sides+(k+1)%sides;d=(ring+1)*sides+k;faces.extend([(a,b,c),(a,c,d)])
 for k in range(sides):faces.append((2*sides+k,2*sides+(k+1)%sides,tip))
 faces.append(tuple(range(sides-1,-1,-1)));mesh=bpy.data.meshes.new('Inset_faceted_amethyst_geode');mesh.from_pydata(verts,[],faces);mesh.update();ob=bpy.data.objects.new(mesh.name,mesh);coll.objects.link(ob);ob.parent=parent
 for mat in materials:mesh.materials.append(mat)
 for p in mesh.polygons:p.material_index=rng.randrange(3)
 geodes+=1
scene=bpy.context.scene;scene['production_status']='OBSERVATORY_MOSS_GEODE_AUTHOR_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report=json.loads((folder/'r42/authoring.json').read_text());report.update(revision='r43',source='r42',status='author_trial_pending_view',moss_cushion_instances=count,inset_closed_amethyst_geodes=geodes,remaining=['Moss density and silhouette','Geode shape, inset depth and purple response','Root/soil integration','Independent review']);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('MOSS_GEODES_SAVED',count,geodes,flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
