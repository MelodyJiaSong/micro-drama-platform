"""Fit helmet trim to the surface and restore distinct hands and paired steel."""
from pathlib import Path
import bpy,json,numpy as np,sys,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at,material
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m300_*/model_3d'));out=folder/'r07';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r06/inspection/m300_r06.blend'));coll=bpy.data.collections['ASSET_m300'];body=next(o for o in coll.objects if o.type=='MESH' and len(o.data.polygons)>100000);me=body.data;v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);loops=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',loops);centers=v[loops].reshape(-1,3,3).mean(1);x,y,z=centers.T;labels=np.empty(len(me.polygons),np.int32);me.polygons.foreach_get('material_index',labels)
hands=(abs(x)>.285)&(abs(x)<.43)&(y<.025)&(z>.385)&(z<.565);labels[hands]=4
hammers=(abs(x)>.24)&(y<.055)&(z>.18)&(z<.385);labels[hammers]=3
collar=(z>1.035)&(z<1.135)&(y>-.025)&(abs(x)<.25);labels[collar]=1
shoulders=(abs(x)>.24)&(z>.94)&(z<1.10)&(y>-.07);labels[shoulders]=1;me.polygons.foreach_set('material_index',labels)
# A physical beard shader avoids the specular tube appearance of a hair-only BSDF.
hairmat=material('Merchant_true_golden_fibres',(.16,.065,.013),.86);hb=hairmat.node_tree.nodes.get('Principled BSDF');hb.inputs['Specular IOR Level'].default_value=.18
for o in coll.objects:
    if o.name.startswith('Beard_individual_fibres'):o.data.materials.clear();o.data.materials.append(hairmat)
    if o.name.startswith(('Helmet_brass_rim','Helmet_small_rivet')):o.hide_render=True
# Fit the rim by ray intersection, never by an assumed helmet radius.
bvh=BVHTree.FromPolygons([p.co.copy() for p in me.vertices],[list(p.vertices) for p in me.polygons]);section=v[(v[:,2]>1.16)&(v[:,2]<1.175)];center=Vector((float(np.median(section[:,0])),float(np.median(section[:,1])),1.167));points=[];normals=[]
for a in np.linspace(0,math.tau,129):
    direction=Vector((math.cos(a),math.sin(a),0));p,n,idx,dist=bvh.ray_cast(center+direction*.5,-direction)
    if p is None:raise RuntimeError('Helmet rim did not hit the body')
    points.append(p+n*.002);normals.append(n)
brass=bpy.data.materials['Merchant_worn_brass_details'];cu=bpy.data.curves.new('Surface_fitted_helmet_trim','CURVE');cu.dimensions='3D';cu.bevel_depth=.0025;cu.bevel_resolution=2;s=cu.splines.new('POLY');s.points.add(len(points)-1)
for p,co in zip(s.points,points):p.co=(*co,1)
cu.materials.append(brass);o=bpy.data.objects.new('Fitted_helmet_brass_edge',cu);coll.objects.link(o)
for i in range(0,128,8):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=.0025,location=points[i]);o=bpy.context.object
    for c in list(o.users_collection):c.objects.unlink(o)
    coll.objects.link(o);o.name='Fitted_helmet_rivet';o.data.materials.append(brass)
scene=bpy.context.scene;scene.cycles.samples=16;scene.render.resolution_x=800;scene.render.resolution_y=800;camera=scene.camera;camera.data.ortho_scale=1.72;camera.location=(4.05,-4.05,1.62);look_at(camera,(0,0,.675));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'perspective_preview.png');bpy.ops.render.render(write_still=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r07','status':'author_preview_pending','hands_faces':int(hands.sum()),'steel_hammer_faces':int(hammers.sum()),'helmet_rim_center':list(center),'source':'r06, fitted trim and differentiated hands, hammer steel, collar cloth and beard response'},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
