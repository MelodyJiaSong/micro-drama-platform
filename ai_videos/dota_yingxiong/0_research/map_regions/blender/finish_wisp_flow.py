"""Use instance-local light shaders and a continuous curved Gaussian wake."""
from pathlib import Path
import bpy,json,math,sys,time,hashlib
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m306_*/model_3d'));source=folder/'r10/inspection/m306_r10.blend';out=folder/'r11/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'m306_r11.blend'
if dest.exists():raise FileExistsError(dest)
while not source.exists():time.sleep(10)
bpy.ops.wm.open_mainfile(filepath=str(source));coll=bpy.data.collections['ASSET_m306']
# World-space coordinates broke distance fades when the collection was placed on
# the map. Every optical field now follows its own instance-local geometry.
for mat in bpy.data.materials:
    if not mat.use_nodes:continue
    nt=mat.node_tree
    for n in list(nt.nodes):
        if n.type=='NEW_GEOMETRY':
            coord=nt.nodes.new('ShaderNodeTexCoord')
            for link in list(n.outputs['Position'].links):nt.links.new(coord.outputs['Object'],link.to_socket)
old=bpy.data.objects['Continuous_soft_light_trail'];old.hide_render=True
verts=[(x,y,z) for z in [.82,1.16] for y in [-.02,.43] for x in [-.10,.10]];faces=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];me=bpy.data.meshes.new('Curved_wake_domain');me.from_pydata(verts,[],faces);ob=bpy.data.objects.new('Curved_volumetric_light_wake',me);coll.objects.link(ob)
mat=bpy.data.materials.new('Local_curved_Gaussian_wake');mat.use_nodes=True;nt=mat.node_tree;n,l=nt.nodes,nt.links;n.clear();output=n.new('ShaderNodeOutputMaterial');vol=n.new('ShaderNodeVolumePrincipled');vol.inputs['Density'].default_value=0;vol.inputs['Emission Color'].default_value=(.30,.84,1,1);l.new(vol.outputs[0],output.inputs['Volume']);tc=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Object'],sep.inputs[0])
def calc(op,a,b=None):
    node=n.new('ShaderNodeMath');node.operation=op
    for i,v in enumerate([a,b]):
        if v is None:continue
        if isinstance(v,(float,int)):node.inputs[i].default_value=v
        else:l.new(v,node.inputs[i])
    return node.outputs[0]
y=sep.outputs['Y'];t=calc('DIVIDE',y,.38);curve_x=calc('MULTIPLY',calc('SINE',calc('MULTIPLY',t,math.pi)),.025);curve_z=calc('ADD',calc('SUBTRACT',1,calc('MULTIPLY',y,.18)),calc('MULTIPLY',calc('SINE',calc('MULTIPLY',t,math.pi)),.065));dx=calc('SUBTRACT',sep.outputs['X'],curve_x);dz=calc('SUBTRACT',sep.outputs['Z'],curve_z);r2=calc('ADD',calc('MULTIPLY',dx,dx),calc('MULTIPLY',dz,dz));width=calc('ADD',.004,calc('MULTIPLY',calc('SUBTRACT',1,t),.010));gaussian=calc('EXPONENT',calc('MULTIPLY',calc('DIVIDE',r2,calc('MULTIPLY',width,width)),-2));gate=calc('MULTIPLY',calc('GREATER_THAN',y,0),calc('LESS_THAN',y,.38));fade=calc('POWER',calc('MAXIMUM',calc('SUBTRACT',1,t),0),2);strength=calc('MULTIPLY',calc('MULTIPLY',gaussian,calc('MULTIPLY',fade,gate)),350);l.new(strength,vol.inputs['Emission Strength']);me.materials.append(mat)
for ob in coll.objects:
    if ob.name.startswith('Wisp_light_dust'):
        y=ob.location.y;t=max(0,min(1.1,y/.38));ob.location.x+=.025*math.sin(math.pi*t);ob.location.z=1-.18*y+.065*math.sin(math.pi*t)+(ob.location.z-(1-.18*y))*.25
cu=bpy.data.objects['Wisp_light_filaments'].data
for s in list(cu.splines)[:6]:
    end=Vector(s.points[-1].co[:3])-Vector((0,0,1));direction=end.normalized();bend=direction.cross(Vector((0,0,1))).normalized()
    for j,p in enumerate(s.points):t=j/(len(s.points)-1);point=Vector(p.co[:3])+bend*.014*math.sin(t*math.pi);p.co=(*point,1)
scene=bpy.context.scene;scene.cycles.samples=48;camera=scene.camera;camera.data.ortho_scale=1.7
bpy.ops.wm.save_as_mainfile(filepath=str(folder/'r11/authoring.blend'))
for name,x,y,z in [('south',0,-1,1),('east',1,0,1),('north',0,1,1),('west',-1,0,1),('perspective',.7,-.7,2.8)]:
    camera.location=(x*4,y*4,1+z);look_at(camera,(0,0,.65));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
for name,loc,target,size in [('close',(1.1,-1.6,1.25),(0,.05,1),.72),('top',(0,0,4),(0,.05,1),.8),('bottom',(0,0,.2),(0,.05,1),.8)]:
    camera.data.ortho_scale=size;camera.location=loc;look_at(camera,target);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(dest));report=json.loads((source.parent/'inspection.json').read_text());report.update(revision='r11',source='r10; curved continuous volumetric wake and instance-local optical fields',sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),status='candidate_not_reviewed',instance_local_shaders=True);(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
