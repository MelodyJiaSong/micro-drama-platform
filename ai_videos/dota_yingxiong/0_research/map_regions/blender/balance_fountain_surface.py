"""Moderate mineral absorption, readable ripples and continuous stone treads."""
from pathlib import Path
import bpy,json,sys,random
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg15_*/model_3d'));out=folder/'r08';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r07/authoring.blend'));coll=bpy.data.collections['ASSET_bg15'];rng=random.Random(1508)
nt=bpy.data.materials['Clear_cyan_spring_water'].node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.018;vol=next(n for n in nt.nodes if n.type=='VOLUME_ABSORPTION');vol.inputs['Color'].default_value=(.035,.42,.78,1);vol.inputs['Density'].default_value=1.8
for n in nt.nodes:
    if n.type=='BUMP':n.inputs['Distance'].default_value=.009;n.inputs['Strength'].default_value=.45
    if n.type=='TEX_NOISE':n.inputs['Scale'].default_value=4;n.inputs['Detail'].default_value=3
for o in coll.objects:
    if o.name.startswith('Individual_worn_entry_stone'):o.hide_render=True
steps=[o for o in coll.objects if o.name.startswith('Weathered_entry_stair')]
for old in steps:
    for k in range(3):
        o=old.copy();o.data=old.data.copy();coll.objects.link(o);o.name='Worn_continuous_stone_tread';o.hide_render=False
        for v in o.data.vertices:v.co.x*=.328
        o.location.x+=(k-1)*.58;o.location.y+=rng.uniform(-.018,.018);o.location.z+=rng.uniform(-.006,.006)
        for m in o.modifiers:
            if m.type=='DISPLACE':m.strength=.055
st=bpy.data.materials['Fountain_weathered_stair_limestone']
for n in st.node_tree.nodes:
    if n.type=='VALTORGB':n.color_ramp.elements[0].color=(.018,.025,.018,1);n.color_ramp.elements[-1].color=(.12,.15,.10,1)
scene=bpy.context.scene;scene.cycles.samples=32;scene.camera.location=(12,-25,16);scene.camera.data.ortho_scale=12.2;look_at(scene.camera,(0,0,2.3));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));scene.render.filepath=str(out/'perspective_preview.png');bpy.ops.render.render(write_still=True)
(out/'authoring.json').write_text(json.dumps({'revision':'r08','status':'author_preview_pending','source':'r07 with moderate cyan absorption, physical ripple normals and contiguous three-stone stair treads','water_surface_height_m':1.04,'waterfall_impact_y':2.9},indent=2));print('PREVIEW',scene.render.filepath,flush=True)
