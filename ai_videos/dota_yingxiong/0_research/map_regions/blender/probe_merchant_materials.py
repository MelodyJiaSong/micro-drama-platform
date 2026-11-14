from pathlib import Path
import bpy,json,collections
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m300_*/model_3d'));bpy.ops.wm.open_mainfile(filepath=str(folder/'r13/authoring.blend'));coll=bpy.data.collections['ASSET_m300'];report=[]
for ob in coll.objects:
    if ob.type!='MESH' or len(ob.data.polygons)<100000:continue
    row={'object':ob.name,'hidden':ob.hide_render,'matrix':list(map(list,ob.matrix_world)),'counts':dict(collections.Counter(p.material_index for p in ob.data.polygons)),'slots':[]}
    for i,slot in enumerate(ob.material_slots):
        m=slot.material;bs=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None) if m.use_nodes else None
        row['slots'].append({'index':i,'name':m.name,'link':slot.link,'base_color':list(bs.inputs['Base Color'].default_value) if bs else None,'color_input':[(l.from_node.name,l.from_socket.name) for l in bs.inputs['Base Color'].links] if bs else [],'ramps':[[list(e.color) for e in n.color_ramp.elements] for n in m.node_tree.nodes if n.type=='VALTORGB']})
    report.append(row)
(folder/'r13/material_probe.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)

print('LIGHTING',json.dumps({'exposure':bpy.context.scene.view_settings.exposure,'look':bpy.context.scene.view_settings.look,'lights':[{'name':o.name,'power':o.data.energy,'position':list(o.matrix_world.translation),'size':getattr(o.data,'size',0)} for o in bpy.context.scene.objects if o.type=='LIGHT']}),flush=True)
