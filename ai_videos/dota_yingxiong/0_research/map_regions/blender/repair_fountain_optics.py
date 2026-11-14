"""Remove radial water normal artifacts and seat the falling water in its gorge."""
from pathlib import Path
import bpy,bmesh,json,sys,math,random
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('background/*/bg15_*/model_3d'));out=folder/'r06';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r05/authoring.blend'));coll=bpy.data.collections['ASSET_bg15'];rng=random.Random(1506)
water=bpy.data.objects['Refractive_reservoir_water'];me=water.data
for v in me.vertices:
    if v.co.z>.9:v.co.z=1.04
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
# Keep the horizontal top normals distinct from the vertical perimeter normals.
for p in me.polygons:p.use_smooth=False
mat=me.materials[0];nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.98,.995,1,1);bs.inputs['Roughness'].default_value=.012;vol=next(n for n in nt.nodes if n.type=='VOLUME_ABSORPTION');vol.inputs['Color'].default_value=(.025,.35,.78,1);vol.inputs['Density'].default_value=.7
tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=7;noise.inputs['Detail'].default_value=2;noise.inputs['Roughness'].default_value=.4;nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.0013;bump.inputs['Strength'].default_value=.3;nt.links.new(noise.outputs[0],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
# Use a complete stone volume for the submerged pebbles; the old scan was a cut wall.
source=next(o for o in coll.objects if o.name.startswith('Rear_spire'));pebble=source.data.copy();pebble.materials.clear();pebble.materials.append(bpy.data.materials['Pale_calcite_basin'])
for p in pebble.polygons:p.material_index=0
for o in coll.objects:
    if o.name.startswith('Submerged_calcite_pebble'):
        o.data=pebble;o.scale=(rng.uniform(.08,.22),rng.uniform(.06,.15),rng.uniform(.018,.045));o.location.z=max(.48,o.location.z+.02)
fall=bpy.data.objects['Continuous_falling_water_sheet']
for v in fall.data.vertices:
    t=max(0,min(1,max(0,(3.45-v.co.z)/2.41)**(1/1.35)));v.co.y=3.35-.45*t+.014*math.sin(t*35+v.co.x*22)
    v.co.x*=.7+.17*math.sin(t*math.pi)
for o in coll.objects:
    if o.name.startswith('Aerated_water_thread'):
        for s in o.data.splines:
            for p in s.points:
                t=max(0,min(1,max(0,(3.45-p.co.z)/2.41)**(1/1.35)));p.co.y=3.33-.45*t;p.co.x*=.75
    if o.name.startswith(('Splash_drop','Soft_waterfall_impact_mist')):o.location.y+=1.12
nt=fall.data.materials[0].node_tree;mix=next(n for n in nt.nodes if n.type=='MIX_SHADER');src=mix.inputs[0].links[0].from_socket;atten=nt.nodes.new('ShaderNodeMath');atten.operation='MULTIPLY';atten.inputs[1].default_value=.36;nt.links.new(src,atten.inputs[0]);nt.links.new(atten.outputs[0],mix.inputs[0])
# Close the rear of the gorge with an actual scanned rock mass.
for x,z,s in [(-.45,.65,(1.9,1.3,3.5)),(.75,.55,(1.5,1.4,3.1))]:
    o=source.copy();o.data=source.data;coll.objects.link(o);o.name='Closed_rear_fountain_rock';o.location=(x,4.0,z);o.scale=s
tex=bpy.data.textures.new('Fountain_step_edge_weathering',type='CLOUDS');tex.noise_scale=.12;tex.noise_depth=2
for o in coll.objects:
    if o.name.startswith(('Weathered_entry_stair','Lantern_stone')):
        sub=o.modifiers.new('Weathered_stone_subdivision','SUBSURF');sub.subdivision_type='SIMPLE';sub.levels=3;sub.render_levels=3;dis=o.modifiers.new('Eroded_stone_edges','DISPLACE');dis.texture=tex;dis.texture_coords='GLOBAL';dis.strength=.025;dis.mid_level=.5
scene=bpy.context.scene;nt=scene.world.node_tree;env=next(n for n in nt.nodes if n.type=='TEX_ENVIRONMENT');bg=nt.nodes.get('Background');nt.links.new(env.outputs[0],bg.inputs['Color']);bg.inputs['Strength'].default_value=.70;scene.view_settings.exposure=0;bpy.data.lights['Daylight_key'].energy=1800;scene.cycles.samples=32;scene.cycles.transmission_bounces=16;scene.cycles.max_bounces=20;scene.render.resolution_x=1000;scene.render.resolution_y=1000;camera=scene.camera;camera.data.ortho_scale=12.5;camera.location=(19,-25,20);look_at(camera,(0,0,2.3));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'perspective_preview.png');bpy.ops.render.render(write_still=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r06','status':'author_preview_pending','source':'r05 with flat water surface normals and micro bump, closed volumetric basin stones, rear rock closure and re-seated falling water','water_surface_height_m':1.04,'water_body_closed':True,'waterfall_impact_y':2.9},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
