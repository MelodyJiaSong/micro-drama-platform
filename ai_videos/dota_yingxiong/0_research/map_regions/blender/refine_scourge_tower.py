"""Separate tower materials, add copper treads and a real faceted crystal shell."""
from pathlib import Path
import bpy,json,numpy as np,math,sys
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
from build_production_map import surface
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('background/*/bg26_*/model_3d'));out=folder/'r02';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r01/inspection/bg26_r01.blend'));coll=bpy.data.collections['ASSET_bg26'];ob=next(o for o in coll.objects if o.type=='MESH');me=ob.data;me.transform(ob.matrix_world);ob.matrix_world=Matrix.Identity(4)
v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);vi=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',vi);tri=vi.reshape(-1,3);co=v[tri].mean(1);uv=np.empty(len(me.loops)*2,np.float32);me.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,3,2).mean(1)
base=me.materials[0];im=next(n.image for n in base.node_tree.nodes if n.type=='TEX_IMAGE' and n.image.colorspace_settings.name=='sRGB');pix=np.empty(len(im.pixels),np.float32);im.pixels.foreach_get(pix);pix=pix.reshape(im.size[1],im.size[0],4);rgb=pix[(uv[:,1]*im.size[1]).astype(int).clip(0,im.size[1]-1),(uv[:,0]*im.size[0]).astype(int).clip(0,im.size[0]-1),:3]
def variant(name,tint,metallic,rough):
 mat=base.copy();mat.name=name;nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');src=bs.inputs['Base Color'].links[0].from_socket;mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);nt.links.new(src,mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
 for key,value in [('Metallic',metallic),('Roughness',rough)]:
  for link in list(bs.inputs[key].links):nt.links.remove(link)
  bs.inputs[key].default_value=value
 tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=45;noise.inputs['Detail'].default_value=4;nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.006;bump.inputs['Strength'].default_value=.28;nt.links.new(noise.outputs[0],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal']);me.materials.append(mat);return len(me.materials)-1
metal=variant('Tower_hammered_purple_grey_metal',(.36,.25,.39),.84,.43)
bronze=variant('Tower_dark_oxidised_bronze',(.30,.20,.095),.80,.48)
bone=variant('Tower_weathered_ivory_bone',(.75,.69,.51),0,.79)
stone=variant('Tower_dark_lava_foundation',(.24,.26,.19),0,.92)
crystal=variant('Tower_internal_luminous_fluorite',(.07,.55,.17),.05,.3)
nt=me.materials[crystal].node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Emission Color'].default_value=(.025,.70,.12,1);noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=6;noise.inputs['Detail'].default_value=5;ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.25;ramp.color_ramp.elements[0].color=(.08,.08,.08,1);ramp.color_ramp.elements[1].position=.68;ramp.color_ramp.elements[1].color=(2.8,2.8,2.8,1);nt.links.new(noise.outputs[0],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Emission Strength'])
x,y,z=co.T;r=np.hypot(x,y);theta=np.arctan2(y,x);labels=np.full(len(co),metal,np.int32);labels[z<.4]=stone
bright=rgb.mean(1)>.56;labels[bright&((z>6.05)|(z<1.4))]=bone
ribphase=np.abs(np.sin((theta-math.pi/8)*4));labels[(ribphase<.20)&(z>.8)&(z<7.35)]=bronze
green=(rgb[:,1]>rgb[:,0]*1.10)&(rgb[:,2]>rgb[:,0]*1.05);crystalmask=(z>7)&(r<2.2)&green;labels[crystalmask]=crystal;me.polygons.foreach_set('material_index',labels)
# Material corrosion varies over physical metres, not across a flat colour plate.
nt=me.materials[metal].node_tree;bs=nt.nodes.get('Principled BSDF');src=bs.inputs['Base Color'].links[0].from_socket;tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=2.8;noise.inputs['Detail'].default_value=5;nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.55;ramp.color_ramp.elements[1].position=.70;nt.links.new(noise.outputs[0],ramp.inputs[0]);mix=nt.nodes.new('ShaderNodeMixRGB');mix.inputs[2].default_value=(.12,.036,.012,1);nt.links.new(ramp.outputs[0],mix.inputs[0]);nt.links.new(src,mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
patina=surface('Tower_copper_green_treads',(.022,.07,.052),(.11,.23,.15),18,.57,.004);patina.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=.65
def block(name,loc,size,mat):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object
 for c in list(o.users_collection):c.objects.unlink(o)
 coll.objects.link(o);o.name=name;o.scale=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat);b=o.modifiers.new('Worn_cast_edges','BEVEL');b.width=.015;b.segments=2;return o
treads=[]
for angle in [-math.pi/2,0,math.pi/2,math.pi]:
 direction=Vector((math.cos(angle),math.sin(angle),0))
 for zz in np.arange(.40,6.45,.25):
  hit,loc,normal,face=ob.ray_cast(direction*15+Vector((0,0,float(zz))),-direction)
  if not hit:continue
  loc+=direction*.025;tread=block('Separate_copper_stair_tread',loc,(.85,.18,.035),patina);tread.rotation_euler.z=angle+math.pi/2;treads.append(tread.name)
# A closed shell with real planar facets, distinct from the luminous inclusions.
glass=bpy.data.materials.new('Tower_faceted_fluorite_shell');glass.use_nodes=True;bs=glass.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.34,.85,.52,1);bs.inputs['Roughness'].default_value=.065;bs.inputs['Transmission Weight'].default_value=.9;bs.inputs['IOR'].default_value=1.434
selected=co[crystalmask];center=selected[:,:2].mean(0) if len(selected) else np.array([0,0]);vs=[];fs=[];N=8
for radius,zz,phase in [(1.36,7.1,0),(1.50,9.2,.10),(.95,11.2,0),(.015,13.02,.02)]:
 for i in range(N):a=i*math.tau/N+phase;vs.append((center[0]+radius*math.cos(a),center[1]+radius*math.sin(a),zz))
for j in range(3):
 for i in range(N):fs.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i))
fs.extend([tuple(range(N-1,-1,-1)),tuple(3*N+i for i in range(N))]);data=bpy.data.meshes.new('Closed_fluorite_facets');data.from_pydata(vs,[],fs);o=bpy.data.objects.new(data.name,data);coll.objects.link(o);data.materials.append(glass)
for i in range(6):
 a=i*math.tau/6;data=bpy.data.lights.new('Fluorite_bounce_light','POINT');data.color=(.12,1,.25);data.energy=95;data.shadow_soft_size=.5;o=bpy.data.objects.new(data.name,data);coll.objects.link(o);o.location=(center[0]+1.75*math.cos(a),center[1]+1.75*math.sin(a),8.2)
scene=bpy.context.scene;scene.cycles.samples=32;scene.cycles.transmission_bounces=10;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.camera.data.ortho_scale=18;scene.camera.location=(18,-30,13.5);look_at(scene.camera,(0,0,6.5));bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'revision':'r02','status':'author_preview_pending','source':'r01','changes':['Separated purple-grey metal, oxidised bronze, weathered bone and green fluorite','Closed faceted transmissive crystal shell with luminous inclusions','Actual copper-green treads on four stair directions'],'copper_treads':len(treads),'crystal_faces':int(crystalmask.sum()),'remaining':['Material boundaries require visual verification','Skull, rivet and moss geometry remain low-frequency and need near-shot refinement']},indent=2),encoding='utf-8');scene.render.filepath=str(out/'tower_preview.png');bpy.ops.render.render(write_still=True)
