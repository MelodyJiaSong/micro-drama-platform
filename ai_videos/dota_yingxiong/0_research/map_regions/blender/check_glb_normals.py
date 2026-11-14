"""Read-only comparison of exported normals and geometric triangle normals."""
import json,struct,argparse
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'))
def inspect(path):
    data=path.read_bytes();n,kind=struct.unpack_from('<II',data,12);doc=json.loads(data[20:20+n]);off=20+n;blen,bkind=struct.unpack_from('<II',data,off);blob=memoryview(data)[off+8:off+8+blen]
    def accessor(index):
        a=doc['accessors'][index];v=doc['bufferViews'][a['bufferView']];dtype=np.dtype({5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]);width={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']];offset=v.get('byteOffset',0)+a.get('byteOffset',0);stride=v.get('byteStride',width*dtype.itemsize)
        return np.ndarray((a['count'],width),dtype=dtype,buffer=blob,offset=offset,strides=(stride,dtype.itemsize)).copy()
    rows=[]
    for m in doc['meshes']:
        for primitive in m['primitives']:
            att=primitive['attributes'];p=accessor(att['POSITION']);normal=accessor(att['NORMAL']);idx=accessor(primitive['indices']).ravel().reshape(-1,3);tri=p[idx];face=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);length=np.linalg.norm(face,axis=1);keep=length>1e-12;face=face[keep]/length[keep,None];vn=normal[idx].mean(1)[keep];vn/=np.maximum(np.linalg.norm(vn,axis=1,keepdims=True),1e-9)
            variants={'as_exported':vn,'normal_rot_x_plus90':vn[:,[0,2,1]]*np.array([1,-1,1]),'normal_rot_x_minus90':vn[:,[0,2,1]]*np.array([1,1,-1])}
            result={}
            for key,norm in variants.items():
                dots=np.sum(face*norm,axis=1);result[key]={'median_dot':float(np.median(dots)),'mean_dot':float(np.mean(dots)),'fraction_dot_below_zero':float(np.mean(dots<0)),'fraction_dot_above_0_8':float(np.mean(dots>.8))}
            rows.append({'vertices':len(p),'triangles':len(idx),'comparisons':result})
    return {'file':str(path),'results':rows}

def repair_exported_normals(path):
    """Correct only the empirically detected extra X rotation, in a copied GLB."""
    before=inspect(path)
    if not before['results']:return {'applied':False,'reason':'no mesh primitives'}
    repair_rows=[]
    for index,row in enumerate(before['results']):
        a=row['comparisons']['as_exported'];b=row['comparisons']['normal_rot_x_plus90']
        if a['median_dot']>.90:continue
        if b['median_dot']<.95 or b['fraction_dot_above_0_8']<.90:
            raise ValueError('Normal orientation is not the known exporter defect; manual diagnosis required')
        repair_rows.append(index)
    if not repair_rows:return {'applied':False,'reason':'normals already agree with geometry','before':before}
    data=bytearray(path.read_bytes());length,kind=struct.unpack_from('<II',data,12);doc=json.loads(data[20:20+length]);bin_offset=20+length+8;seen=set()
    primitives=[p for m in doc['meshes'] for p in m['primitives']]
    selected_accessors={primitives[i]['attributes']['NORMAL'] for i in repair_rows}
    correct_accessors={p['attributes']['NORMAL'] for i,p in enumerate(primitives) if i not in repair_rows}
    if selected_accessors & correct_accessors:raise ValueError('Mixed geometric interpretations of a shared normal accessor')
    for primitive in primitives:
            index=primitive['attributes']['NORMAL']
            if index in seen or index not in selected_accessors:continue
            seen.add(index);a=doc['accessors'][index];view=doc['bufferViews'][a['bufferView']]
            if a['componentType']!=5126 or a['type']!='VEC3':raise ValueError('Unexpected normal accessor')
            offset=bin_offset+view.get('byteOffset',0)+a.get('byteOffset',0);arr=np.ndarray((a['count'],3),dtype='<f4',buffer=data,offset=offset,strides=(view.get('byteStride',12),4));old=arr.copy();arr[:,0]=old[:,0];arr[:,1]=-old[:,2];arr[:,2]=old[:,1]
    temp=path.with_suffix('.normalfix.tmp');temp.write_bytes(data)
    after=inspect(temp)
    for index,row in enumerate(after['results']):
        threshold=.95 if index in repair_rows else .90
        if row['comparisons']['as_exported']['median_dot']<threshold:raise ValueError('Normal correction failed verification')
    temp.replace(path)
    return {'applied':True,'rotation':'X +90 degrees in GLB coordinates','before':before,'after':after}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('asset');p.add_argument('--revision',required=True);args=p.parse_args();folder=next(WORLD.glob('**/'+args.asset+'_*/model_3d'))/args.revision;path=next(folder.glob('*_pbr_*.glb'));result=inspect(path);(folder/'normal_diagnostic.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
