"""Repair the diagnosed cape gaps and separate beard/metal details."""
from pathlib import Path
import bpy,json,numpy as np,math,random,sys,hashlib
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import material,look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m300_*/model_3d'));out=folder/'r06/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'m300_r06.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r05/inspection/m300_r05.blend'));coll=bpy.data.collections['ASSET_m300'];ob=next(o for o in coll.objects if o.type=='MESH');me=ob.data;v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);loops=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',loops);centers=v[loops].reshape(-1,3,3).mean(1);x,y,z=centers.T;labels=np.empty(len(me.polygons),np.int32);me.polygons.foreach_get('material_index',labels)
uv=np.empty(len(me.loops)*2,np.float32);me.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2);original=me.materials[0];image=next(n.image for n in original.node_tree.nodes if n.type=='TEX_IMAGE' and n.image.colorspace_settings.name=='sRGB');pixels=np.empty(image.size[0]*image.size[1]*4,np.float32);image.pixels.foreach_get(pixels);pixels=pixels.reshape(image.size[1],image.size[0],4);rgb=pixels[np.clip((uv[:,1]*image.size[1]).astype(int),0,image.size[1]-1),np.clip((uv[:,0]*image.size[0]).astype(int),0,image.size[0]-1),:3].reshape(-1,3,3).mean(1)
redcloth=(rgb[:,0]>rgb[:,1]*1.12)&(rgb[:,2]>rgb[:,1]*.60)
cape=(((y>.04)&(z>.15)&(z<1.10))|((abs(x)>.23)&(y>-.14)&(z>.20)&(z<1.13))|((abs(x)>.15)&(y>-.20)&(z>1.02)&(z<1.14)))&redcloth&~((abs(x)<.23)&(z<.35));labels[cape]=1
helmet=(z>1.155)|((y>.01)&(z>1.10)&(abs(x)<.15));labels[helmet]=3
sidehair=(abs(x)>.09)&(abs(x)<.17)&(z>1.035)&(z<1.125)&(y>-.06)&(y<.12)&~helmet;labels[sidehair]=2;me.polygons.foreach_set('material_index',labels)
# Increase the beard's actual depth and keep its fibre roots on that surface.
beard=(abs(v[:,0])<np.clip((v[:,2]-.68)*.6+.035,.035,.155))&(v[:,1]<-.15)&(v[:,2]>.71)&(v[:,2]<1.065);offset=.035*np.sin(np.clip((v[:,2]-.70)/.38,0,1)*math.pi);v[beard,1]-=offset[beard];me.vertices.foreach_set('co',v.ravel());me.update()
for o in coll.objects:
    if o.type=='CURVE':
        for s in o.data.splines:
            for p in s.points:
                t=max(0,min(1,(p.co.z-.70)/.38));p.co.y-=.035*math.sin(t*math.pi)
        for m in o.data.materials:
            for n in m.node_tree.nodes:
                if n.type=='BSDF_HAIR_PRINCIPLED':n.inputs['Color'].default_value=(.26,.085,.012,1);n.inputs['Roughness'].default_value=.48
steel=me.materials[3];nt=steel.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.4
for n in nt.nodes:
    if n.type=='VALTORGB':n.color_ramp.elements[0].color=(.07,.075,.08,1);n.color_ramp.elements[-1].color=(.22,.24,.26,1)
skin=me.materials[4].node_tree.nodes.get('Principled BSDF');skin.inputs['Subsurface Radius'].default_value=(.015,.006,.003);skin.inputs['Subsurface Weight'].default_value=.06
brass=material('Merchant_worn_brass_details',(.34,.20,.055),.34);brass.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=.87
def attach(o,name,mat):
    for c in list(o.users_collection):c.objects.unlink(o)
    coll.objects.link(o);o.name=name;o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    return o
def sphere(name,loc,r,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=r,location=loc);return attach(bpy.context.object,name,mat)
def curve(name,points,r,mat):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=2;s=cu.splines.new('POLY');s.points.add(len(points)-1)
    for p,co in zip(s.points,points):p.co=(*co,1)
    o=bpy.data.objects.new(name,cu);coll.objects.link(o);cu.materials.append(mat);return o
curve('Helmet_brass_rim',[(.124*math.cos(a),.108*math.sin(a),1.167) for a in np.linspace(0,math.tau,129)],.004,brass)
for a in np.linspace(0,math.tau,24,endpoint=False):sphere('Helmet_small_rivet',(.125*math.cos(a),.109*math.sin(a),1.173),.003,brass)
# Medallions are real relief, positioned by ray intersection with the old body.
hits=[]
for name,xx,zz,radius in [('Belt',0,.665,.044),('Left_hammer',-.34,.30,.045),('Right_hammer',.34,.30,.045)]:
    hit,loc,normal,idx=ob.ray_cast(Vector((xx,-3,zz)),Vector((0,1,0)))
    if not hit:continue
    loc+=normal*.003;hits.append({'part':name,'location':list(loc),'normal':list(normal)});bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=radius,depth=.004,location=loc);o=attach(bpy.context.object,name+'_brass_medallion',brass);o.rotation_euler=normal.to_track_quat('Z','Y').to_euler();bevel=o.modifiers.new('Cast_edge','BEVEL');bevel.width=.001;bevel.segments=2
    u=normal.cross(Vector((0,0,1))).normalized();w=normal.cross(u).normalized()
    for rr in [.52,.89]:curve(name+'_cast_ring',[loc+normal*.003+radius*rr*(u*math.cos(a)+w*math.sin(a)) for a in np.linspace(0,math.tau,65)],.0012,brass)
    for a in np.linspace(0,math.tau,10,endpoint=False):sphere(name+'_rivet',loc+normal*.004+radius*.72*(u*math.cos(a)+w*math.sin(a)),.0018,brass)
scene=bpy.context.scene;scene.cycles.samples=24;camera=scene.camera;bpy.data.objects['Studio_floor'].location.z=0
for name,x,y,z in [('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22),('perspective',1,-1,.7)]:
    camera.location=(x*4.05,y*4.05,.675+z*1.35);look_at(camera,(0,0,.675));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report=json.loads((folder/'r05/inspection/inspection.json').read_text());report.update(revision='r06',source='r05; verified cape selection repair, depth-corrected beard, hair and steel separation, physically scaled skin scattering, cast brass details',sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),status='candidate_not_reviewed',detail_surface_hits=hits);(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
