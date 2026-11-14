"""Read shader connections and image-channel statistics without changing assets."""
from pathlib import Path
import bpy,json,numpy as np,argparse,sys
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'))
parser=argparse.ArgumentParser();parser.add_argument('--assets',nargs='+',default=['m303:r01','m26:r06']);args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
for aid,revision in [item.split(':') for item in args.assets]:
 folder=next(WORLD.glob(f'characters/*/{aid}_*/model_3d'));bpy.ops.wm.open_mainfile(filepath=str(folder/revision/'inspection'/f'{aid}_{revision}.blend'));ob=max((o for o in bpy.data.collections[f'ASSET_{aid}'].all_objects if o.type=='MESH' and not o.hide_render),key=lambda o:len(o.data.polygons));report={'asset':aid,'revision':revision,'materials':[],'images':[]}
 for mat in ob.data.materials:
  if not mat.use_nodes:continue
  bs=next(q for q in mat.node_tree.nodes if q.type=='BSDF_PRINCIPLED');report['materials'].append({'name':mat.name,'sockets':{k:({'source':bs.inputs[k].links[0].from_node.name,'socket':bs.inputs[k].links[0].from_socket.name} if bs.inputs[k].is_linked else bs.inputs[k].default_value) for k in ['Roughness','Metallic','Specular IOR Level']},'nodes':[{'name':q.name,'type':q.type,'image':q.image.name if q.type=='TEX_IMAGE' and q.image else None,'input_links':[(l.from_node.name,l.from_socket.name,l.to_socket.name) for s in q.inputs for l in s.links]} for q in mat.node_tree.nodes]})
 for im in bpy.data.images:
  if im.name.startswith(('Render Result','Viewer')) or not im.size[0]:continue
  px=np.empty(len(im.pixels),np.float32);im.pixels.foreach_get(px);px=px.reshape(-1,im.channels);report['images'].append({'name':im.name,'colorspace':im.colorspace_settings.name,'quantiles_0_10_50_90_100':np.quantile(px,[0,.1,.5,.9,1],axis=0).tolist()})
 (folder/'pbr_channel_diagnosis.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
