"""Real leaf instances, crossed bark fibres and physically sourced base lights."""
from pathlib import Path
import bpy,bmesh,json,sys,math,random,numpy as np
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at,material
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));MAP=WORLD/'background/map_3d';SRC=MAP/'environment_sources';folder=next(WORLD.glob('background/*/bg2_*/model_3d'));out=folder/'r05';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r03/inspection/bg2_r03.blend'));coll=bpy.data.collections['ASSET_bg2'];body=next(o for o in coll.objects if o.type=='MESH');me=body.data;me.transform(Matrix.Rotation(-math.pi/4,4,'Z')@body.matrix_world);body.matrix_world=Matrix.Identity(4)
v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);loops=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',loops);uv=np.empty(len(me.loops)*2,np.float32);me.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2);base=me.materials[0];im=next(n.image for n in base.node_tree.nodes if n.type=='TEX_IMAGE' and n.image.colorspace_settings.name=='sRGB');pixels=np.empty(im.size[0]*im.size[1]*4,np.float32);im.pixels.foreach_get(pixels);pixels=pixels.reshape(im.size[1],im.size[0],4);rgb=pixels[np.clip((uv[:,1]*im.size[1]).astype(int),0,im.size[1]-1),np.clip((uv[:,0]*im.size[0]).astype(int),0,im.size[0]-1),:3];color=np.zeros((len(v),3),np.float32);color[loops]=rgb
leafmask=((v[:,2]>10.5)|((v[:,2]>8.5)&(np.linalg.norm(v[:,:2],axis=1)>3)))&(color[:,1]>color[:,0]*.86)&(color[:,1]>color[:,2]*.98)&(color.sum(1)>.7);points=v[leafmask].copy();rng=random.Random(204);nr=np.random.default_rng(204)
if len(points)<10000:raise RuntimeError('Canopy selection too small')
# Identify the blue glass panels before changing bark, preserving original frames.
glass=material('World_tree_cyan_lantern_glass',(.035,.23,.19),.22);gb=glass.node_tree.nodes.get('Principled BSDF');gb.inputs['Transmission Weight'].default_value=.25;gb.inputs['Emission Color'].default_value=(.045,.7,.45,1);gb.inputs['Emission Strength'].default_value=2.5;me.materials.append(glass)
cc=v[loops].reshape(-1,3,3).mean(1);face_rgb=rgb.reshape(-1,3,3).mean(1);isglass=(cc[:,2]>4)&(cc[:,2]<10.5)&(face_rgb[:,2]>face_rgb[:,0]*1.08)&(face_rgb[:,1]>face_rgb[:,0]*1.04)
labels=np.zeros(len(me.polygons),np.int32);labels[isglass]=1;me.polygons.foreach_set('material_index',labels)
# Preserve structural roots. The low AI ground wafer is buried beneath actual soil.
v[:,2]-=.8*np.clip((2-v[:,2])/1.5,0,1);trunk=(v[:,2]>4)&(v[:,2]<10.5)&(np.linalg.norm(v[:,:2],axis=1)<3);v[trunk,:2]*=(1-.22*np.clip((v[trunk,2]-4)/2,0,1))[:,None];me.vertices.foreach_set('co',v.ravel());bm=bmesh.new();bm.from_mesh(me);bm.verts.ensure_lookup_table();bmesh.ops.delete(bm,geom=[p for p in bm.verts if p.co.z>10.5 or leafmask[p.index]],context='VERTS');bm.to_mesh(me);bm.free();me.update()
nt=base.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');source=bs.inputs['Base Color'].links[0].from_socket;tint=nt.nodes.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.65,.38,.25,1);nt.links.new(source,tint.inputs[1]);nt.links.new(tint.outputs[0],bs.inputs['Base Color'])
with bpy.data.libraries.load(str(next((SRC/'tree_small_02').glob('*.blend'))),link=False) as (s,d):d.objects=[f'tree_small_02_leaves_{x}_LOD1' for x in 'abcd']
lib=bpy.data.collections.new('World_tree_actual_leaf_prototypes')
leafmats=set()
for o in d.objects:
    o.location=(0,0,0);lib.objects.link(o)
    for m in o.data.materials:
        if not m or m.name in leafmats:continue
        leafmats.add(m.name);nt=m.node_tree;bs=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if bs:bs.inputs['Roughness'].default_value=.72
        for tex in list(nt.nodes):
            if tex.type!='TEX_IMAGE' or not tex.image or tex.image.colorspace_settings.name!='sRGB':continue
            links=list(tex.outputs['Color'].links);h=nt.nodes.new('ShaderNodeHueSaturation');h.inputs['Saturation'].default_value=1.15;h.inputs['Value'].default_value=1.35;nt.links.new(tex.outputs['Color'],h.inputs['Color'])
            for link in links:nt.links.new(h.outputs[0],link.to_socket)
indices=nr.choice(len(points),40000,replace=len(points)<40000);scatter=points[indices]+nr.uniform(-.25,.25,(len(indices),3));mesh=bpy.data.meshes.new('Detailed_world_tree_canopy_points');mesh.vertices.add(len(scatter));mesh.vertices.foreach_set('co',scatter.astype(np.float32).ravel());mesh.update();ob=bpy.data.objects.new('Individual_world_tree_leaves',mesh);coll.objects.link(ob)
for name,data in [('scale',np.repeat(nr.uniform(1.1,1.8,len(scatter)),3)),('rotation',nr.uniform(-math.pi,math.pi,len(scatter)*3))]:attr=mesh.attributes.new(name,'FLOAT_VECTOR','POINT');attr.data.foreach_set('vector',data.astype(np.float32))
ng=bpy.data.node_groups.new('World_tree_leaf_instancing','GeometryNodeTree');ng.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');ng.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');n,l=ng.nodes,ng.links;inp=n.new('NodeGroupInput');output=n.new('NodeGroupOutput');info=n.new('GeometryNodeCollectionInfo');info.inputs['Collection'].default_value=lib;info.inputs['Separate Children'].default_value=True;info.inputs['Reset Children'].default_value=True;inst=n.new('GeometryNodeInstanceOnPoints');inst.inputs['Pick Instance'].default_value=True;l.new(inp.outputs['Geometry'],inst.inputs['Points']);l.new(info.outputs['Instances'],inst.inputs['Instance']);l.new(inst.outputs['Instances'],output.inputs['Geometry'])
for name,socket in [('scale','Scale'),('rotation','Rotation')]:attr=n.new('GeometryNodeInputNamedAttribute');attr.data_type='FLOAT_VECTOR';attr.inputs['Name'].default_value=name;l.new(attr.outputs['Attribute'],inst.inputs[socket])
mod=ob.modifiers.new('True_leaf_geometry','NODES');mod.node_group=ng
bark=material('World_tree_fibrous_red_brown_bark',(.12,.045,.018),.92);nt=bark.node_tree;bs=nt.nodes.get('Principled BSDF');tc=nt.nodes.new('ShaderNodeTexCoord');mapping=nt.nodes.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(5,5,.16);nt.links.new(tc.outputs['Object'],mapping.inputs[0]);noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=4;noise.inputs['Detail'].default_value=6;nt.links.new(mapping.outputs[0],noise.inputs['Vector']);r=nt.nodes.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.025,.012,.006,1);r.color_ramp.elements[1].color=(.20,.09,.035,1);nt.links.new(noise.outputs[0],r.inputs[0]);nt.links.new(r.outputs[0],bs.inputs['Base Color']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.055;bump.inputs['Strength'].default_value=.7;nt.links.new(noise.outputs[0],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
def curve(name,points,radii,mat):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=1;cu.bevel_resolution=3;s=cu.splines.new('POLY');s.points.add(len(points)-1)
    for p,co,r in zip(s.points,points,radii):p.co=(*co,1);p.radius=r
    o=bpy.data.objects.new(name,cu);coll.objects.link(o);cu.materials.append(mat);return o
for strand in range(6):
    path=[];radii=[]
    for j in range(81):t=j/80;a=strand*math.tau/6+t*math.tau*.65;rr=1.85-.25*t;path.append((rr*math.cos(a),rr*math.sin(a),6.3+5.5*t));radii.append(.38-.12*t)
    curve('Crossed_bark_strand',path,radii,bark)
centers=points[np.linspace(0,len(points)-1,18,dtype=int)].copy();sample=points[::max(1,len(points)//10000)]
for _ in range(10):
    labels=np.argmin(((sample[:,None]-centers[None])**2).sum(2),axis=1)
    for k in range(len(centers)):
        if np.any(labels==k):centers[k]=sample[labels==k].mean(0)
for k,end in enumerate(centers):
    start=Vector((math.cos(k)*1.4,math.sin(k)*1.4,10));end=Vector(end);path=[start.lerp(end,j/60)+Vector((0,0,-.6*math.sin(j/60*math.pi))) for j in range(61)];curve('Connected_crown_branch',path,[.48*(1-j/60)+.025 for j in range(61)],bark)
stone=material('World_tree_weathered_platform',(.32,.35,.30),.85);nt=stone.node_tree;bs=nt.nodes.get('Principled BSDF');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=18;noise.inputs['Detail'].default_value=5;bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.025;nt.links.new(noise.outputs[0],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
def attach(o,name,mat):
    for c in list(o.users_collection):c.objects.unlink(o)
    coll.objects.link(o);o.name=name;o.data.materials.append(mat);return o
bpy.ops.mesh.primitive_cylinder_add(vertices=192,radius=4.5,depth=.28,location=(0,0,.15));platform=attach(bpy.context.object,'Circular_engraved_stone_platform',stone);bev=platform.modifiers.new('Worn_stone_edge','BEVEL');bev.width=.06;bev.segments=3
moss=material('Bioluminescent_blue_green_moss',(.02,.12,.08),.8);mb=moss.node_tree.nodes.get('Principled BSDF');mb.inputs['Emission Color'].default_value=(.015,.60,.32,1);mb.inputs['Emission Strength'].default_value=2.2
for rr in [1.3,2.15,2.95,3.70,4.22]:curve('Cold_moss_inset_ring',[(rr*math.cos(a),rr*math.sin(a),.294) for a in np.linspace(0,math.tau,257)],[.015]*257,moss)
for j in range(3):
    bpy.ops.mesh.primitive_cube_add(size=1,location=(0,-4.45-j*.40,.22-j*.065));o=attach(bpy.context.object,'World_tree_entry_step',stone);o.scale=(3.5+j*.25,.5,.15);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);b=o.modifiers.new('Worn_step','BEVEL');b.width=.035;b.segments=3
for i in range(70):
    a=rng.random()*math.tau;rr=rng.uniform(3.1,5.8)
    if math.sin(a)<-.9:continue
    x,y=rr*math.cos(a),rr*math.sin(a);r0=rng.uniform(.10,.28);bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=r0,location=(x,y,.30+r0));o=attach(bpy.context.object,'Living_luminous_fungus',moss);o.scale.z=.65
    for p in o.data.polygons:p.use_smooth=True
for im in bpy.data.images:
    if im.source=='FILE' and not im.packed_file:
        paths=list(SRC.glob('*/textures/'+Path(im.filepath.replace('\\','/')).name))
        if paths:im.filepath=str(paths[0]);im.reload()
scene=bpy.context.scene;scene.cycles.samples=16;scene.render.resolution_x=900;scene.render.resolution_y=900;camera=scene.camera;camera.data.ortho_scale=27;camera.location=(0,-70,22);look_at(camera,(0,0,10));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'south_preview.png');bpy.ops.render.render(write_still=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r05','status':'author_preview_pending','leaf_cluster_instances':40000,'platform_diameter_m':9,'glass_faces':int(isglass.sum()),'source':'r03 with independent leaves, exposed platform, properly visible crossed trunk fibres and physical base light sources'},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
