"""Separate shop materials and add actual tapered straw over the retained roof."""
from pathlib import Path
import bpy,json,numpy as np,sys,random,math
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'))
a=next(a for a in json.loads((WORLD/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'))['assets'] if a['id']=='bg12')
folder=ROOT/a['model_directory'];out=folder/'r07';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r05/inspection/bg12_r05.blend'))
coll=bpy.data.collections['ASSET_bg12'];ob=next(o for o in coll.objects if o.type=='MESH');me=ob.data
me.transform(ob.matrix_world);ob.matrix_world=Matrix.Identity(4)
v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3)
vi=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',vi);tri=vi.reshape(-1,3);centres=v[tri].mean(1)
uv=np.empty(len(me.loops)*2,np.float32);me.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,3,2).mean(1)
base=me.materials[0];bs=base.node_tree.nodes.get('Principled BSDF');tex=next(n for n in base.node_tree.nodes if n.type=='TEX_IMAGE' and any(l.to_socket.name=='Base Color' for l in n.outputs['Color'].links));img=tex.image
pixels=np.empty(img.size[0]*img.size[1]*4,np.float32);img.pixels.foreach_get(pixels);pixels=pixels.reshape(img.size[1],img.size[0],4)
colors=pixels[(uv[:,1]*img.size[1]).astype(int).clip(0,img.size[1]-1),(uv[:,0]*img.size[0]).astype(int).clip(0,img.size[0]-1),:3]
def tinted(name,tint,rough,scale=(1,1,1),bump=.002):
 mat=base.copy();mat.name=name;nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');original=bs.inputs['Base Color'].links[0].from_socket
 mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);nt.links.new(original,mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
 for key,value in [('Roughness',rough),('Metallic',0)]:
  for l in list(bs.inputs[key].links):nt.links.remove(l)
  bs.inputs[key].default_value=value
 tc=nt.nodes.new('ShaderNodeTexCoord');mapping=nt.nodes.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=scale;nt.links.new(tc.outputs['Object'],mapping.inputs[0]);noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=160;nt.links.new(mapping.outputs[0],noise.inputs['Vector']);bn=nt.nodes.new('ShaderNodeBump');bn.inputs['Distance'].default_value=bump;bn.inputs['Strength'].default_value=.35;nt.links.new(noise.outputs['Fac'],bn.inputs['Height']);nt.links.new(bn.outputs[0],bs.inputs['Normal']);me.materials.append(mat);return len(me.materials)-1
bamboo=tinted('bg12_Aged_golden_bamboo',(.62,.39,.14),.72,(1,1,.045),.003)
straw=tinted('bg12_Olive_straw_underlayer',(.38,.31,.075),.92,(1,1,1),.003)
red=tinted('bg12_Crimson_woven_cloth',(.48,.13,.15),.91,(1,1,1),.001)
purple=tinted('bg12_Purple_woven_cloth',(.18,.07,.32),.91,(1,1,1),.001)
gold=tinted('bg12_Worn_gold_border',(.65,.42,.09),.76,(1,1,1),.001)
stone=tinted('bg12_Grey_paving',(.45,.47,.42),.9,(1,1,1),.004)
bronze=bpy.data.materials.new('bg12_Oxidised_bronze');bronze.use_nodes=True;nt=bronze.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Metallic'].default_value=.65;bs.inputs['Roughness'].default_value=.56
noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=14;noise.inputs['Detail'].default_value=4;ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.38;ramp.color_ramp.elements[0].color=(.075,.033,.008,1);ramp.color_ramp.elements[1].position=.60;ramp.color_ramp.elements[1].color=(.035,.23,.16,1);nt.links.new(noise.outputs[0],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color']);me.materials.append(bronze);bronzeidx=len(me.materials)-1
x,y,z=centres.T
left=((x+1.05)**2+(y-.46)**2<2.05**2)&(z>3.55)&(z<5.43)
right=((x-1.65)**2+(y-.9)**2<2.1**2)&(z>4.05)&(z<6.48)
roof=left|right
pole=(x>2.85)&(z>4.75)
roof &= ~pole
labels=np.full(len(tri),bamboo,np.int32);labels[z<.22]=stone;labels[roof]=straw
cloth=(z>1.85)&(z<2.68)&(colors[:,0]>colors[:,1]*1.3)&(colors[:,0]>.12)
# Panel-sized alternating colours around the complete platform, retaining UV detail.
panels=np.floor((x+4)/1.0).astype(int)%2
labels[cloth&(panels==0)]=red;labels[cloth&(panels==1)]=purple
border=(z>1.85)&(z<2.2)&(colors[:,0]>colors[:,2]*1.3)&(colors[:,1]>colors[:,0]*.69);labels[border]=gold
finials=(((x+1.05)**2+(y-.46)**2<.38**2)&(z>5.43))|(((x-1.65)**2+(y-.9)**2<.48**2)&(z>6.48))
labels[finials]=bronzeidx;me.polygons.foreach_set('material_index',labels)
# Use original texture luminance for cloth wear; retain a clear dyed hue.
for index,color in [(red,(.20,.012,.018)),(purple,(.065,.012,.10))]:
 nt=me.materials[index].node_tree;bs=nt.nodes.get('Principled BSDF');original=next(n for n in nt.nodes if n.type=='MIX_RGB').inputs[1].links[0].from_socket
 grey=nt.nodes.new('ShaderNodeRGBToBW');nt.links.new(original,grey.inputs[0]);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=tuple(c*.3 for c in color)+(1,);ramp.color_ramp.elements[1].color=(*color,1);nt.links.new(grey.outputs[0],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color'])
nt=bronze.node_tree;tc=nt.nodes.new('ShaderNodeTexCoord');nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);noise.inputs['Scale'].default_value=18
normals=np.cross(v[tri[:,1]]-v[tri[:,0]],v[tri[:,2]]-v[tri[:,0]]);area=np.linalg.norm(normals,axis=1)/2
valid=roof&(normals[:,2]>0)&(area>1e-8)
rooftri=tri[valid];bvh=BVHTree.FromPolygons(v.tolist(),rooftri.tolist(),all_triangles=True)
rng=np.random.default_rng(28712);count=65000;chosen=rng.choice(np.flatnonzero(valid),count,p=area[valid]/area[valid].sum());r=rng.random((count,2));r[:,0]=np.sqrt(r[:,0]);roots=(1-r[:,0,None])*v[tri[chosen,0]]+(r[:,0]*(1-r[:,1]))[:,None]*v[tri[chosen,1]]+(r[:,0]*r[:,1])[:,None]*v[tri[chosen,2]]
palettes=[(.10,.075,.017),(.18,.13,.035),(.08,.095,.02),(.24,.17,.055),(.12,.115,.03)]
curves=[]
for i,color in enumerate(palettes):
 mat=bpy.data.materials.new(f'bg12_Individual_straw_{i}');mat.use_nodes=True;b=mat.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*color,1);b.inputs['Roughness'].default_value=.88;b.inputs['Subsurface Weight'].default_value=.04
 data=bpy.data.curves.new(f'Roof_straw_fibres_{i}','CURVE');data.dimensions='3D';data.resolution_u=1;data.bevel_depth=.0034;data.bevel_resolution=0;data.materials.append(mat);obj=bpy.data.objects.new(data.name,data);coll.objects.link(obj);curves.append(data)
for j,root in enumerate(roots):
 dl=(root[0]+1.05)**2+(root[1]-.46)**2;dr=(root[0]-1.65)**2+(root[1]-.9)**2
 center=np.array([-1.05,.46]) if dl<dr else np.array([1.65,.9]);direction=root[:2]-center;direction/=max(np.linalg.norm(direction),.01);length=rng.uniform(.12,.38);side=np.array([-direction[1],direction[0]])*rng.uniform(-.025,.025)
 points=[];last=root.copy();lift=rng.uniform(.018,.065)
 for t in np.linspace(0,1,5):
  xy=root[:2]+direction*length*t+side*math.sin(t*math.pi);hit=bvh.ray_cast(Vector((float(xy[0]),float(xy[1]),8)),Vector((0,0,-1)),6)
  hz=hit[0].z if hit[0] is not None and abs(hit[0].z-root[2])<1.2 else last[2]-.10
  point=np.array([xy[0],xy[1],hz+lift+.025*math.sin(t*math.pi)]);last=point;points.append((*point,1))
 spline=curves[j%len(curves)].splines.new('POLY');spline.points.add(4);spline.points.foreach_set('co',np.array(points).ravel());spline.points.foreach_set('radius',[.6,1,.9,.65,.12])
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=1000;scene.render.resolution_y=1000;camera=scene.camera;camera.data.ortho_scale=11.4;camera.location=(14,-25,11);look_at(camera,(0,0,3.5))
bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset':'bg12','revision':'r07','status':'author_preview_pending','source':'r05','changes':['Separate bamboo, straw, crimson and purple cloth, gold trim and oxidised bronze materials','65000 actual tapered straw strands over both roofs','Exclude tall sign pole from roof fibres; shorter varied straw; cloth luminance preserves wear without red tint contaminating purple'],'remaining':['Hanging sign intersects roof','Platform stone layout and thin base require rebuilding','Material boundaries need all-view inspection'],'straw_strands':count},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'shop_preview.png');bpy.ops.render.render(write_still=True)
