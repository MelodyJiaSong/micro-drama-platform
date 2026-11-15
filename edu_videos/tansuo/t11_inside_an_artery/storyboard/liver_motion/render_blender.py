import bpy,math,random,sys,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
SID=args[0] if args else 'V26'
MODE=args[1] if len(args)>1 else 'still'
FPS=12
DUR={'V23':7,'V24':7,'V25':9,'V26':7,'V27':10}[SID]
random.seed(59)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
sc.render.engine='BLENDER_EEVEE'
sc.render.use_persistent_data=True
sc.cycles.samples=12
sc.cycles.use_denoising=True
sc.eevee.taa_render_samples=16
sc.render.resolution_x=960;sc.render.resolution_y=540;sc.render.resolution_percentage=100
sc.render.image_settings.file_format='PNG'
sc.render.fps=FPS;sc.frame_start=1;sc.frame_end=DUR*FPS
sc.world=bpy.data.worlds.new('Deep teal ambience');sc.world.use_nodes=True
sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.035,.065,.09,1)
sc.world.node_tree.nodes['Background'].inputs[1].default_value=.35
sc.view_settings.view_transform='AgX'
sc.render.film_transparent=False
# Prefer GPU when Cycles reports an available CUDA or OptiX device.
try:
 prefs=bpy.context.preferences.addons['cycles'].preferences
 for backend in ['OPTIX','CUDA']:
  try:
   prefs.compute_device_type=backend;prefs.get_devices()
   gpu=[d for d in prefs.devices if d.type!='CPU']
   if gpu:
    for d in prefs.devices:d.use=d.type!='CPU'
    sc.cycles.device='GPU';break
  except Exception:pass
except Exception:pass

def mat(name,color,metal=.0,rough=.35,emission=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
 p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if emission:p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emission
 return m
AMBER=mat('LDL / amber coding',(.82,.35,.055),.35,.22)
WHITE=mat('ApoB / pearl coding',(.75,.82,.74),.1,.3)
TEAL=mat('membrane / teal coding',(.025,.21,.24),.22,.32)
HEAD=mat('phospholipid head',(.06,.39,.42),.25,.32)
TAIL=mat('lipid tail',(.025,.11,.14),.05,.4)
RECEPTOR=mat('functional receptor / not atomic shape',(.3,.7,.65),.2,.28)
LIVER=mat('liver / location model',(.29,.045,.032),.05,.34)
LIGHT=mat('focus trace',(.95,.46,.09),.1,.2,1.4)
BLUE=mat('cool trace',(.12,.52,.6),.1,.25,.8)

SPHERES={}
def sphere(name,loc,r,material,scale=(1,1,1),segments=20):
 cache_key=(r,material.name,segments)
 if cache_key not in SPHERES:
  bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=12,radius=r,location=loc)
  ob=bpy.context.object;ob.data.materials.append(material)
  for p in ob.data.polygons:p.use_smooth=True
  SPHERES[cache_key]=ob.data
 else:
  ob=bpy.data.objects.new(name,SPHERES[cache_key]);bpy.context.collection.objects.link(ob)
 ob.name=name;ob.location=loc;ob.scale=scale
 return ob

def curve(name,pts,r,material):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.resolution_u=12;c.bevel_depth=r;c.bevel_resolution=3
 sp=c.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
 for bp,co in zip(sp.bezier_points,pts):bp.co=co;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
 ob=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(ob);ob.data.materials.append(material)
 return ob

def empty(name,loc=(0,0,0)):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.location=loc;return o

def particle(name,loc,r=.33):
 root=empty(name,loc)
 core=sphere(name+' cargo',(0,0,0),r,AMBER);core.parent=root
 for i in range(48):
  z=1-2*(i+.5)/48;a=2.399963*i;rr=math.sqrt(1-z*z)
  dot=sphere('surface lipid',((r*.99)*rr*math.cos(a),(r*.99)*rr*math.sin(a),r*.99*z),r*.105,AMBER,segments=8);dot.parent=root
 pts=[(r*1.03*math.cos(a),r*1.03*math.sin(a),.08*math.sin(2*a)) for a in [i*math.tau/16 for i in range(17)]]
 belt=curve('one continuous ApoB concept',pts,r*.055,WHITE);belt.parent=root
 return root

def key(ob,frame,loc=None,scale=None):
 if loc is not None:ob.location=loc;ob.keyframe_insert(data_path='location',frame=frame)
 if scale is not None:ob.scale=scale;ob.keyframe_insert(data_path='scale',frame=frame)

def camera(loc,target,lens=44):
 bpy.ops.object.camera_add(location=loc);cam=bpy.context.object;sc.camera=cam;cam.data.lens=lens
 aim=empty('camera gaze',target);con=cam.constraints.new(type='TRACK_TO');con.target=aim;con.track_axis='TRACK_NEGATIVE_Z';con.up_axis='UP_Y'
 cam.data.dof.use_dof=True;cam.data.dof.focus_object=aim;cam.data.dof.aperture_fstop=6.3
 return cam,aim

def light(name,loc,power,color,size):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.color=color;o.data.shape='DISK';o.data.size=size
 o.rotation_euler=(Vector((0,0,0))-o.location).to_track_quat('-Z','Y').to_euler()

light('large warm key',(-4,-5,8),650,(1,.71,.43),7)
light('cool rim',(5,3,5),1000,(.22,.72,1),5)
light('soft fill',(-5,4,1),350,(.2,.5,.7),6)

def membrane(extent=7,pit=False):
 verts=[];faces=[];N=55
 for y in range(N):
  for x in range(N):
   xx=(x/(N-1)-.5)*extent*2
   yy=y/(N-1)*extent*.65 if pit else (y/(N-1)-.5)*extent*1.3
   verts.append((xx,yy,.02*math.sin(xx*2+yy)))
 for y in range(N-1):
  for x in range(N-1):
   k=y*N+x;faces.append((k,k+1,k+1+N,k+N))
 me=bpy.data.meshes.new('lipid membrane surface');me.from_pydata(verts,[],faces);me.update()
 ob=bpy.data.objects.new('continuous membrane',me);bpy.context.collection.objects.link(ob);ob.data.materials.append(TEAL)
 for p in me.polygons:p.use_smooth=True
 if pit:
  ob.shape_key_add(name='Basis');s=ob.shape_key_add(name='Invagination')
  for v in s.data:
   rr=v.co.x*v.co.x+v.co.y*v.co.y
   v.co.z-=2.35*math.exp(-rr/1.05)
  for frame,value in [(1,0),(FPS*2,0),(FPS*4.8,1),(FPS*5.8,1),(FPS*6.8,0)]:s.value=value;s.keyframe_insert(data_path='value',frame=frame)
 # Linked heads make a tactile bilayer, leaving the central moving patch unobscured.
 template=sphere('phospholipid',(-20,0,0),.105,HEAD,segments=10)
 for ix in range(-18,19):
  for iy in range(-10,11):
   x=ix*.34;y=iy*.34
   if pit and (y<.3 or x*x+y*y<3):continue
   for z in [.035,-.21]:
    o=bpy.data.objects.new('lipid head',template.data);bpy.context.collection.objects.link(o);o.location=(x,y,z)
 return ob

def receptor(x,y,number):
 root=empty('LDLR functional site '+str(number),(x,y,0))
 # A folded curved binding site, not an antibody Y and not a claim of atomic accuracy.
 tube=curve('receptor fold',[(0,0,-.18),(.02,0,.18),(-.07,.015,.48),(.1,.04,.7),(.23,.035,.62),(.17,.02,.48)],.065,RECEPTOR);tube.parent=root
 return root

if SID=='V23':
 # Organ location only. LDL particles are not drawn at organ scale.
 outline=[(-2.8,.1),(-2.5,1.0),(-1.7,1.45),(-.5,1.4),(.5,1.05),(2.4,.55),(2.9,.1),(2.5,-.45),(1.1,-.5),(.25,-.65),(-.2,-1.25),(-1.5,-1.35),(-2.5,-.8)]
 rings=[(.02,.55),(.35,.61),(.72,.43),(1,0),(.72,-.4),(.35,-.51),(.02,-.48)]
 verts=[(x*r,y*r,z+.06*x) for r,z in rings for x,y in outline];faces=[];n=len(outline)
 for k in range(len(rings)-1):
  for i in range(n):faces.append((k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i))
 faces.extend([tuple(range(n-1,-1,-1)),tuple((len(rings)-1)*n+i for i in range(n))])
 mesh=bpy.data.meshes.new('liver location silhouette');mesh.from_pydata(verts,[],faces);mesh.update()
 ob=bpy.data.objects.new('liver location model',mesh);bpy.context.collection.objects.link(ob);ob.data.materials.append(LIVER)
 for face in mesh.polygons:face.use_smooth=True
 mod=ob.modifiers.new('soft organ contour','SUBSURF');mod.levels=3
 # A scale-change ripple is an editorial transition, not an anatomical feature.
 for i in range(3):
  ring=curve('scale transition',[(math.cos(a)*3.6,math.sin(a)*2.1,-.8) for a in [j*math.tau/48 for j in range(49)]],.012,LIGHT)
  key(ring,1,scale=(.7+i*.15,)*3);key(ring,sc.frame_end,scale=(1.05+i*.18,)*3)
 cam,aim=camera((3,-5,10),(0,0,0),48);key(cam,1,(3,-5,10));key(cam,DUR*FPS,(1.3,-2.9,6.5));key(aim,DUR*FPS,(-.4,0,.2))
elif SID=='V24':
 # Endoplasmic reticulum context; particles stand for synthesis output only.
 for i in range(9):
  x=-4+i
  curve('ER folded membrane',[(x,-3,.1),(x+.4,-1,math.sin(i)*.4),(x-.2,1,.4),(x+.3,3,.0)],.16,TEAL)
 enzyme=sphere('enzyme functional node',(0,0,.8),.55,RECEPTOR,(1.2,.7,1))
 inhibitor=sphere('statin functional marker',(1.7,-.4,1.4),.2,WHITE)
 key(inhibitor,1,(1.7,-.4,1.4));key(inhibitor,FPS*2.5,(.45,-.15,1.05))
 for i in range(20):
  o=sphere('new synthesis output',(0,0,0),.115,AMBER)
  start=1+i*3 if i<12 else FPS*3+(i-12)*9
  key(o,1,(0,.1,.9),(.001,)*3);key(o,start,(0,.1,.9),(1,)*3)
  key(o,start+FPS*2,(3.5,.2+math.sin(i)*.7,1.1),(1,)*3)
  key(o,start+FPS*2+2,scale=(.001,)*3)
 cam,aim=camera((6,-8,6),(.3,0,.5),48);key(cam,1,(6,-8,6));key(cam,sc.frame_end,(4.5,-7,4.8))
elif SID=='V25':
 membrane()
 for i in range(21):
  x=(i%7-3)*1.5;y=(i//7-1)*1.4;r=receptor(x,y,i)
  if i%4:
   start=FPS*2+(i%7)*5;key(r,1,scale=(.001,)*3);key(r,start,scale=(.001,)*3);key(r,start+FPS*2,scale=(1,)*3)
 for i in range(14):
  x=-6+(i%7)*1.7;y=-1.5+(i//7)*2.6;p=particle('circulating LDL',(x,y,2.4),.25)
  key(p,1,(x,y,2.4));key(p,sc.frame_end,(x+1.5,y,1.45))
 cam,aim=camera((7,-10,5),(0,0,.5),46);key(cam,1,(7,-10,5));key(cam,sc.frame_end,(4.8,-8,3.8))
elif SID=='V26':
 membrane(pit=True)
 for i,(x,y) in enumerate([(-3,1),(3,1),(-3,2.5),(3,2.5)]):receptor(x,y,i)
 r=receptor(.1,0,'target');p=particle('single tracked LDL',(.1,0,2.2),.4)
 key(p,1,(.1,0,2.2));key(p,FPS*2,(.1,0,1.05));key(p,FPS*4.8,(.1,0,-1.2));key(p,FPS*5.8,(.1,0,-1.2));key(p,sc.frame_end,(.1,0,-2.4))
 key(r,1,(.1,0,0));key(r,FPS*2,(.1,0,0));key(r,FPS*4.8,(.1,0,-2.1));key(r,FPS*5.8,(.1,0,-2.1));key(r,sc.frame_end,(.1,0,-3.2))
 # Vesicle represented by a cutaway ring cage so cargo remains visible.
 ves=empty('vesicle membrane envelope',(.1,0,-1.3))
 for axis in range(3):
  pts=[]
  for i in range(33):
   a=i*math.tau/32;co=[.83*math.cos(a),.83*math.sin(a),0]
   if axis==1:co=[co[0],0,co[1]]
   if axis==2:co=[0,co[0],co[1]]
   pts.append(co)
  c=curve('vesicle outline',pts,.035,BLUE);c.parent=ves
 key(ves,1,scale=(.001,)*3);key(ves,FPS*5.3,scale=(.001,)*3);key(ves,FPS*5.8,scale=(1,)*3);key(ves,sc.frame_end,(.1,0,-2.4))
 cam,aim=camera((7.5,-10,4.8),(0,0,.7),44);key(cam,1,(7.5,-10,4.8));key(cam,sc.frame_end,(7,-10,1));key(aim,1,(0,0,.7));key(aim,sc.frame_end,(0,0,-1.1))
else:
 membrane()
 for i in range(15):receptor((i%5-2)*2,(i//5-1)*2,i)
 for i in range(6):
  x=-5+(i%3)*3.5;y=(i//3-.5)*2.5
  p=particle('LDL clearance population',(x,y,2.3),.24)
  key(p,1,(x,y,2.3));key(p,sc.frame_end,(x+2.2,y,2.2))
 cam,aim=camera((6,-9,4),(0,0,1),45);key(cam,1,(6,-9,4));key(cam,sc.frame_end,(10,-14,7))

# Keep motion slow and intentional rather than bouncing through easing overshoot.
for ob in bpy.data.objects:
 if ob.animation_data and ob.animation_data.action:
  try:
   for fc in ob.animation_data.action.fcurves:
    for kp in fc.keyframe_points:kp.interpolation='LINEAR'
  except AttributeError:pass

folder=OUT/'frames_eevee'/SID;folder.mkdir(parents=True,exist_ok=True)
if MODE=='still':
 sc.frame_set(int(sc.frame_end*.56));sc.render.filepath=str(OUT/f'{SID}_test.png');bpy.ops.render.render(write_still=True)
else:
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/f'{SID}.blend'))
 for frame in range(1,sc.frame_end+1):
  target=folder/f'{frame:04d}.png'
  if target.exists():continue
  sc.frame_set(frame);sc.render.filepath=str(target);bpy.ops.render.render(write_still=True)
 (OUT/f'{SID}_render.json').write_text(json.dumps({'shot':SID,'frames':sc.frame_end,'fps':FPS,'duration':DUR,'engine':sc.render.engine,'stage':'local motion previz, not molecular model validation'},indent=2),encoding='utf-8')
