"""Add explicit groomed fur curves to sampled pale body surfaces; retain raw model."""
from pathlib import Path
import bpy,bmesh,numpy as np,json,sys,argparse
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
p=argparse.ArgumentParser();p.add_argument('--revision',default='r03');args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m21_Polar_Furbolg/model_3d'));out=folder/args.revision;out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r01/inspection/m21_r01.blend'));coll=bpy.data.collections['ASSET_m21'];body=max((o for o in coll.all_objects if o.type=='MESH'),key=lambda o:len(o.data.polygons));me=body.data
me.transform(body.matrix_world);body.parent=None;body.matrix_world.identity();me.update()
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001);bm.to_mesh(me);bm.free();me.update();print('WELDED_FOR_GROOM',len(me.vertices),flush=True)
co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3)
loops=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',loops);uv=np.empty(len(me.loops)*2,np.float32);me.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2);vuv=np.zeros((len(co),2),np.float32);vuv[loops]=uv
mat=me.materials[0];nt=mat.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');colour=bs.inputs['Base Color'].links[0].from_socket
source=colour.node
if source.type!='TEX_IMAGE':raise RuntimeError('Inspect base colour graph before sampling')
image=source.image;w,h=image.size;pixels=np.empty(w*h*4,np.float32);image.pixels.foreach_get(pixels);pixels=pixels.reshape(h,w,4)
rgb=pixels[np.clip((vuv[:,1]*(h-1)).astype(int),0,h-1),np.clip((vuv[:,0]*(w-1)).astype(int),0,w-1),:3]
brightness=rgb.mean(axis=1);chroma=rgb.max(axis=1)-rgb.min(axis=1)
print('COLOUR_QUANTILES',np.quantile(brightness,[.1,.3,.5,.7,.9]).tolist(),'BOUNDS',co.min(axis=0).tolist(),co.max(axis=0).tolist(),flush=True)
def smooth(value,lo,hi):
 t=np.clip((value-lo)/(hi-lo),0,1);return t*t*(3-2*t)
cape=smooth(co[:,2],1.25,1.55)
fur=np.clip((brightness-.50)/.20,0,1)*np.clip((.25-chroma)/.14,0,1)
fur*=1-cape*(1-smooth(brightness,.65,.78))
# Mouth, claws and projecting wooden posts must remain free of generated hair.
face=(np.abs(co[:,0])<.16)&(co[:,1]<-.30)&(co[:,2]>1.22)&(co[:,2]<1.55)
coat=cape*(1-fur);coat[face]=0
fur[face]=0;fur[(co[:,2]>2.01)|(co[:,2]<.04)]=0
# Smooth only fur-bearing skin, after welding UV seam duplicates, to reduce clay-like fins.
edges=np.empty(len(me.edges)*2,np.int32);me.edges.foreach_get('vertices',edges);edges=edges.reshape(-1,2);degree=np.bincount(edges.ravel(),minlength=len(co)).astype(np.float32)
for iteration in range(4):
 sums=np.zeros_like(co);np.add.at(sums,edges[:,0],co[edges[:,1]]);np.add.at(sums,edges[:,1],co[edges[:,0]]);mean=sums/np.maximum(degree[:,None],1);co+=(mean-co)*(fur*.52)[:,None]
co[:,1]-=.10*smooth(co[:,2],.9,1.8)
co[:,2]=np.where(co[:,2]<.72,co[:,2]*1.22,co[:,2]+.72*.22);co*=2.3/co[:,2].max();me.vertices.foreach_set('co',co.ravel());me.update()
if me.has_custom_normals:me.normals_split_custom_set([(0,0,0)]*len(me.loops))
for name,values in [('FurCoverage',fur),('LeatherCoverage',coat)]:
 a=me.attributes.new(name,'FLOAT','POINT');a.data.foreach_set('value',values.astype(np.float32))
attr=nt.nodes.new('ShaderNodeAttribute');attr.attribute_name='LeatherCoverage';leather=nt.nodes.new('ShaderNodeMixRGB');leather.blend_type='MULTIPLY';leather.inputs[0].default_value=1;leather.inputs[2].default_value=(.17,.105,.055,1);nt.links.new(colour,leather.inputs[1]);mix=nt.nodes.new('ShaderNodeMixRGB');nt.links.new(attr.outputs['Fac'],mix.inputs[0]);nt.links.new(colour,mix.inputs[1]);nt.links.new(leather.outputs[0],mix.inputs[2])
furattr=nt.nodes.new('ShaderNodeAttribute');furattr.attribute_name='FurCoverage';cool=nt.nodes.new('ShaderNodeMixRGB');cool.blend_type='MULTIPLY';cool.inputs[0].default_value=1;cool.inputs[2].default_value=(.78,.86,.95,1);nt.links.new(colour,cool.inputs[1]);final=nt.nodes.new('ShaderNodeMixRGB');nt.links.new(furattr.outputs['Fac'],final.inputs[0]);nt.links.new(mix.outputs[0],final.inputs[1]);nt.links.new(cool.outputs[0],final.inputs[2]);nt.links.new(final.outputs[0],bs.inputs['Base Color'])
me.calc_loop_triangles();tri=np.empty(len(me.loop_triangles)*3,np.int32);me.loop_triangles.foreach_get('vertices',tri);tri=tri.reshape(-1,3)
a,b,c=co[tri[:,0]],co[tri[:,1]],co[tri[:,2]];cross=np.cross(b-a,c-a);area=np.linalg.norm(cross,axis=1)*.5;coverage=fur[tri].mean(axis=1);norm=cross/np.maximum(2*area[:,None],1e-10);centres=(a+b+c)/3
weight=area*coverage;weight[(centres[:,2]>1.5)&(norm[:,2]>.55)&(centres[:,1]>-.08)]=0
assert weight.sum()>.25,('Insufficient fur surface',float(weight.sum()))
rng=np.random.default_rng(21202);count=420000;selected=rng.choice(len(tri),count,p=weight/weight.sum());u=rng.random(count);v=rng.random(count);root_weights=np.column_stack((1-np.sqrt(u),np.sqrt(u)*(1-v),np.sqrt(u)*v)).astype(np.float32)
roots=(co[tri[selected]]*root_weights[:,:,None]).sum(axis=1);normal=norm[selected];roots+=normal*.001
length=rng.uniform(.040,.105,count).astype(np.float32);head=(roots[:,2]>1.45)&(roots[:,1]<-.15);length[head]*=.25
side=rng.normal(size=(count,3)).astype(np.float32);side-=normal*(side*normal).sum(axis=1)[:,None];side/=np.maximum(np.linalg.norm(side,axis=1)[:,None],1e-8)
points=np.empty((count,5,3),np.float32)
for j,t in enumerate(np.linspace(0,1,5)):
 points[:,j]=roots+normal*(length*t*.58)[:,None]+side*(np.sin(t*np.pi)*length*.13)[:,None];points[:,j,2]-=length*t*t*.78
curves=bpy.data.hair_curves.new('Individual_polar_guard_hairs');curves.add_curves([5]*count);curves.set_types(type='CATMULL_ROM');curves.attributes['position'].data.foreach_set('vector',points.ravel())
radius=curves.attributes.new('radius','FLOAT','POINT');radii=(rng.uniform(.00010,.00019,count)[:,None]*np.array([1,.93,.76,.42,.025],np.float32)).astype(np.float32);radius.data.foreach_set('value',radii.ravel())
hair=bpy.data.objects.new('Groomed_polar_fur_curves',curves);coll.objects.link(hair)
furmat=bpy.data.materials.new('Cool_white_polar_fur');furmat.use_nodes=True;hn,hl=furmat.node_tree.nodes,furmat.node_tree.links;hn.clear();output=hn.new('ShaderNodeOutputMaterial');hairbs=hn.new('ShaderNodeBsdfHairPrincipled');hairbs.parametrization='COLOR';hairbs.inputs['Color'].default_value=(.54,.57,.60,1);hairbs.inputs['Roughness'].default_value=.36
if 'Radial Roughness' in hairbs.inputs:hairbs.inputs['Radial Roughness'].default_value=.44
hl.new(hairbs.outputs[0],output.inputs['Surface']);curves.materials.append(furmat)
scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=64;scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';scene.camera.location=(6,-7,3.0);scene.camera.data.ortho_scale=2.9;look_at(scene.camera,(0,0,1.15))
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m21','revision':args.revision,'source':'r01','status':'author_preview_not_accepted','hair_curves':count,'points_per_strand':5,'hair_length_range_m':[float(length.min()),float(length.max())],'fur_surface_weight_m2':float(weight.sum()),'sampling':'Original UV texture brightness, chroma and smooth spatial exclusion masks; raw texture unchanged','changes':['Weld and smooth fur-bearing surface fins','Longer tapered Catmull-Rom fur strands','Slightly longer legs and forward upper-body posture, normalized to 2.3m','Cool white fur response and continuous leather transition'],'remaining':['Fur placement and clipping','Skin/cloth boundary accuracy','Body proportions and four-pole geometry','Author inspection and independent review']},indent=2),encoding='utf-8');print('GROOM_SAVED',count,flush=True)
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
