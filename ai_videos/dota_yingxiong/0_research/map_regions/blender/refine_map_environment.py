"""在原版坐标底稿上细化地表；保留 v001，单独保存 v002。"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = next(ROOT.glob('2_*')) / 'background/map_3d'
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_production_map import surface


def sample(array, x, y):
    u, v = np.clip((x+8192)/128,0,127.9999), np.clip((y+8192)/128,0,127.9999)
    i, j = u.astype(int), v.astype(int)
    u, v = u-i, v-j
    return (array[j,i]*(1-u)+array[j,i+1]*u)*(1-v)+(array[j+1,i]*(1-u)+array[j+1,i+1]*u)*v


def main():
    dest = OUT/'foundation_v002.blend'
    if dest.exists():
        raise FileExistsError(dest)
    bpy.ops.wm.open_mainfile(filepath=str(OUT/'foundation_v001.blend'))
    data=json.loads((ROOT/'0_research/base_layout_refs/terrain_samples.json').read_text())
    common=json.loads(Path(__file__).with_name('common.json').read_text(encoding='utf-8'))
    flags=np.array(data['flags'])
    layers=np.array(data['cliff_layers'],dtype=float)
    residual=(np.array(data['ground_world_z'])-((layers-2)*128))/common['units_per_m']
    mesh=bpy.data.objects['Terrain_683d'].data
    coords=np.empty(len(mesh.vertices)*3,dtype=np.float32)
    mesh.vertices.foreach_get('co',coords)
    coords=coords.reshape(-1,3)
    x,y=coords[:,0]*common['units_per_m'],coords[:,1]*common['units_per_m']
    coords[:,2]+=sample(residual,x,y)
    mesh.vertices.foreach_set('co',coords.ravel())
    # Original ground tile categories become continuous masks, avoiding square seams.
    tile=flags&15
    masks={
        'Grass':np.isin(tile,[2,3,4,5]).astype(float),
        'Blight':((flags&32)>0).astype(float),
        'Paving':(tile==6).astype(float),
    }
    for name,array in masks.items():
        padded=np.pad(array,1,mode='edge')
        array=(padded[1:-1,1:-1]*4+padded[:-2,1:-1]+padded[2:,1:-1]+padded[1:-1,:-2]+padded[1:-1,2:])/8
        attribute=mesh.attributes.new(name,'FLOAT','POINT')
        attribute.data.foreach_set('value',sample(array,x,y).astype(np.float32))
    z=coords[:,2].reshape(1025,1025)
    dzdy,dzdx=np.gradient(z,16/common['units_per_m'])
    slope=np.clip(np.sqrt(dzdy**2+dzdx**2)-.4,0,1).astype(np.float32).ravel()
    attr=mesh.attributes.new('Rock','FLOAT','POINT')
    attr.data.foreach_set('value',slope)
    mat=surface('Continuous_ground',(.025,.017,.009),(.12,.07,.035),1.1,bump=.06)
    nt=mat.node_tree
    nodes,links=nt.nodes,nt.links
    bsdf=nodes.get('Principled BSDF')
    original=bsdf.inputs['Base Color'].links[0].from_socket
    coord=next(n for n in nodes if n.type=='TEX_COORD')
    fine=nodes.new('ShaderNodeTexNoise')
    fine.inputs['Scale'].default_value=1.5
    fine.inputs['Detail'].default_value=5
    links.new(coord.outputs['Object'],fine.inputs['Vector'])
    for name,dark,light in [
        ('Grass',(.012,.025,.005),(.055,.095,.018)),
        ('Blight',(.007,.006,.009),(.045,.035,.047)),
        ('Paving',(.045,.042,.035),(.15,.14,.12)),
        ('Rock',(.038,.035,.029),(.18,.16,.13)),
    ]:
        attribute=nodes.new('ShaderNodeAttribute');attribute.attribute_name=name
        ramp=nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].color=(*dark,1)
        ramp.color_ramp.elements[1].color=(*light,1)
        links.new(fine.outputs['Fac'],ramp.inputs[0])
        mix=nodes.new('ShaderNodeMixRGB')
        links.new(attribute.outputs['Fac'],mix.inputs[0])
        links.new(original,mix.inputs[1]);links.new(ramp.outputs[0],mix.inputs[2])
        original=mix.outputs[0]
    links.new(original,bsdf.inputs['Base Color'])
    mesh.materials.clear();mesh.materials.append(mat)
    mesh.polygons.foreach_set('material_index',np.zeros(len(mesh.polygons),dtype=np.int32))
    mesh.update()
    for collname in ('02_Forest','03_Asset_Placement'):
        for obj in bpy.data.collections[collname].objects:
            tx,ty=np.array([obj.location.x*common['units_per_m']]),np.array([obj.location.y*common['units_per_m']])
            obj.location.z+=float(sample(residual,tx,ty)[0])
    bpy.context.scene.view_settings.look='AgX - Medium High Contrast'
    bpy.context.scene.view_settings.exposure=-.8
    bpy.context.scene['production_status']='FOUNDATION V002: continuous ground materials; precision assets pending'
    bpy.ops.wm.save_as_mainfile(filepath=str(dest))
    report={'status':'foundation_pending_assets','file':dest.name,
            'changes':['原版 ground_world_z 的层内微地形','草地、泥土、腐地、石面的连续过渡','按坡度赋予岩石材质','树木与资产点位同步接地'],
            'review':'not_independently_reviewed','remaining':['精细建筑和 NPC','悬崖自然化','地面植被与散石','逐区近景验收']}
    (OUT/'foundation_v002_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')


if __name__=='__main__':main()
