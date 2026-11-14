"""Rebuild the reference's ridged stitched hide cape as a continuous surface."""
from pathlib import Path
import bpy,math,json,sys,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at,material
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m21_Polar_Furbolg/model_3d'));out=folder/'r07';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r06/authoring.blend'));coll=bpy.data.collections['ASSET_m21'];old=bpy.data.objects['Reconstructed_leather_cape_shell'];old.hide_render=True;old.hide_viewport=True
def surface(u,v):
 width=.55+.035*math.sin(v*math.pi);x=u*width;y=-.51+1.18*v
 ridge=2.08-.17*v-.18*v*v;hem=1.60-.30*v-.60*v**3
 z=ridge-(ridge-hem)*abs(u)**.88
 z+=.016*math.sin(u*18+v*3)*math.sin(abs(u)*math.pi)+.009*math.sin(v*29+u*4)*abs(u)**2
 # Thick hide sags between stitch lines; irregularities stay below the fold scale.
 z-=.018*math.sin(v*math.pi*3)**2*math.sin(u*math.pi*2)**2
 y+=.016*math.sin(u*21)*((1-v)**8+v**8);z+=.012*math.sin(v*37+u*9)*abs(u)**12
 return Vector((x,y,z))
nu,nv=160,180;verts=[surface(-1+2*i/nu,j/nv) for j in range(nv+1) for i in range(nu+1)];faces=[]
for j in range(nv):
 for i in range(nu):k=j*(nu+1)+i;faces.append((k,k+1,k+nu+2,k+nu+1))
me=bpy.data.meshes.new('Continuous_stitched_hide');me.from_pydata(verts,[],faces);ob=bpy.data.objects.new(me.name,me);coll.objects.link(ob);mat=old.data.materials[0].copy();mat.name='Rugged_stitched_brown_hide';me.materials.append(mat)
for face in me.polygons:face.use_smooth=True
uv=me.uv_layers.new(name='Hide_metres')
for face in me.polygons:
 for li in face.loop_indices:
  vi=me.loops[li].vertex_index;j,i=divmod(vi,nu+1);uv.data[li].uv=(i/nu*1.25,j/nv*1.18)
for node in mat.node_tree.nodes:
 if node.type=='TEX_COORD':
  for link in list(node.outputs['Object'].links):mat.node_tree.links.new(node.outputs['UV'],link.to_socket)
 elif node.type=='TEX_IMAGE':node.projection='FLAT'
 elif node.type=='BUMP':node.inputs['Distance'].default_value=.003;node.inputs['Strength'].default_value=.8
 elif node.type=='BSDF_PRINCIPLED':node.inputs['Specular IOR Level'].default_value=.12
solid=ob.modifiers.new('Hide_thickness_6mm','SOLIDIFY');solid.thickness=.006;solid.offset=-1
thread=material('Worn_hide_stitch_cord',(.07,.052,.028),.91)
def curve(name,points,radius,mat):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=2;sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for p,c in zip(sp.points,points):p.co=(*c,1)
 o=bpy.data.objects.new(name,cu);coll.objects.link(o);cu.materials.append(mat);return o
seams=0
for u in [-1,-.52,0,.52,1]:
 curve('Raised_hide_panel_seam',[surface(u,v)+Vector((0,0,.004)) for v in np.linspace(0,1,101)],.0035,mat)
 for v in np.linspace(.025,.975,38):
  points=[surface(max(-1,min(1,u+t*.022)),v)+Vector((0,0,.007+.003*math.sin((t+1)*math.pi/2))) for t in np.linspace(-1,1,7)];curve('Cross_laced_hide_stitch',points,.0021,thread);seams+=1
for v in [.36,.70]:
 curve('Cross_hide_panel_seam',[surface(u,v)+Vector((0,0,.004)) for u in np.linspace(-1,1,141)],.0035,mat)
 for u in np.linspace(-.96,.96,48):
  points=[surface(u,v+t*.012)+Vector((0,0,.007+.003*math.sin((t+1)*math.pi/2))) for t in np.linspace(-1,1,7)];curve('Cross_laced_hide_stitch',points,.0021,thread);seams+=1
# Uneven fur fringe belongs to the front hide edge, rather than extending the scalp.
rng=np.random.default_rng(2107);count=16000;points=np.empty((count,5,3),np.float32)
for i,u in enumerate(rng.uniform(-1,1,count)):
 root=surface(u,0)+Vector((0,-.006,-.003));length=rng.uniform(.024,.052);drift=rng.normal(0,.007,3)
 for j,t in enumerate(np.linspace(0,1,5)):points[i,j]=root+Vector((drift[0]*t,-.014*t+drift[1]*t,-length*t))+Vector((0,-.004*math.sin(t*math.pi),0))
cu=bpy.data.hair_curves.new('Hide_front_fur_fringe');cu.add_curves([5]*count);cu.set_types(type='CATMULL_ROM');cu.attributes['position'].data.foreach_set('vector',points.ravel());radius=cu.attributes.new('radius','FLOAT','POINT');radius.data.foreach_set('value',np.tile(np.array([.00016,.00014,.00011,.00006,.000003],np.float32),count));cu.materials.append(bpy.data.materials['Cool_white_polar_fur']);hair=bpy.data.objects.new(cu.name,cu);coll.objects.link(hair)
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.camera.location=(6,-7,3);scene.camera.data.ortho_scale=2.9;look_at(scene.camera,(0,0,1.15));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m21','revision':'r07','source':'r06','status':'author_preview_not_accepted','changes':['Replace pitted generated cape with a continuous ridged hide surface','Separate sewn panels, actual lacing and fur fringe','Preserve existing body and three poles'],'hide_faces':len(faces),'stitches':seams,'fringe_strands':count,'remaining':['Silhouette and pole intersection','Body exposure and cape length','Author and independent inspection']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.location=(3,4,3.2);scene.camera.data.ortho_scale=1.5;look_at(scene.camera,(0,.1,1.8));scene.render.filepath=str(out/'roof_poles_preview.png');bpy.ops.render.render(write_still=True)
