"""Resumable face-wise UV projection; avoids the slow built-in UV transfer path."""
from pathlib import Path
import json,time,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

def transfer_uv(source,target,out):
    started=time.monotonic();src=source.data;dst=target.data;src.calc_loop_triangles()
    positions=np.empty(len(src.vertices)*3,np.float32);src.vertices.foreach_get('co',positions);positions=positions.reshape(-1,3)
    triangles=np.empty(len(src.loop_triangles)*3,np.int32);src.loop_triangles.foreach_get('vertices',triangles);triangles=triangles.reshape(-1,3)
    tri_loops=np.empty(len(src.loop_triangles)*3,np.int32);src.loop_triangles.foreach_get('loops',tri_loops);tri_loops=tri_loops.reshape(-1,3)
    src_uv=np.empty(len(src.loops)*2,np.float32);src.uv_layers.active.data.foreach_get('uv',src_uv);src_uv=src_uv.reshape(-1,2)
    print('BUILD_SOURCE_BVH',len(triangles),flush=True)
    tree=BVHTree.FromPolygons(positions,triangles,all_triangles=True)
    print('SOURCE_BVH_READY',round(time.monotonic()-started,1),flush=True)
    target_positions=np.empty(len(dst.vertices)*3,np.float32);dst.vertices.foreach_get('co',target_positions);target_positions=target_positions.reshape(-1,3)
    loop_vertices=np.empty(len(dst.loops),np.int32);dst.loops.foreach_get('vertex_index',loop_vertices)
    starts=np.empty(len(dst.polygons),np.int32);totals=np.empty(len(dst.polygons),np.int32);dst.polygons.foreach_get('loop_start',starts);dst.polygons.foreach_get('loop_total',totals)
    uv_path=out/'projected_uv.npy';progress_path=out/'uv_transfer_progress.json';done=0
    if progress_path.exists():
        old=json.loads(progress_path.read_text());assert old['target_loops']==len(dst.loops) and old['source_triangles']==len(triangles);done=old['completed_faces'];uv=np.lib.format.open_memmap(uv_path,mode='r+')
    else:uv=np.lib.format.open_memmap(uv_path,mode='w+',dtype=np.float32,shape=(len(dst.loops),2))
    max_distance=0.;far_faces=0
    for first in range(done,len(dst.polygons),25000):
        last=min(first+25000,len(dst.polygons));lo=int(starts[first]);hi=int(starts[last-1]+totals[last-1]);points=target_positions[loop_vertices[lo:hi]];centers=np.add.reduceat(points,starts[first:last]-lo,axis=0)/totals[first:last,None]
        nearest=[tree.find_nearest(Vector(p)) for p in centers];indices=np.array([hit[2] for hit in nearest],np.int32);distances=np.array([hit[3] for hit in nearest]);max_distance=max(max_distance,float(distances.max()));far_faces+=int((distances>.015).sum())
        expanded=np.repeat(indices,totals[first:last]);a,b,c=positions[triangles[expanded]].transpose(1,0,2);v0=b-a;v1=c-a;v2=points-a;d00=np.einsum('ij,ij->i',v0,v0);d01=np.einsum('ij,ij->i',v0,v1);d11=np.einsum('ij,ij->i',v1,v1);d20=np.einsum('ij,ij->i',v2,v0);d21=np.einsum('ij,ij->i',v2,v1);den=np.maximum(d00*d11-d01*d01,1e-24);v=(d11*d20-d01*d21)/den;w=(d00*d21-d01*d20)/den;weights=np.maximum(np.column_stack((1-v-w,v,w)),0);weights/=weights.sum(1)[:,None]
        uv[lo:hi]=np.einsum('ij,ijk->ik',weights,src_uv[tri_loops[expanded]]);uv.flush()
        progress={'completed_faces':last,'total_faces':len(dst.polygons),'target_loops':len(dst.loops),'source_triangles':len(triangles),'elapsed_seconds':round(time.monotonic()-started,2),'max_nearest_face_distance_m_this_run':max_distance,'faces_over_15mm_this_run':far_faces,'method':'One nearest source triangle per target face; barycentric corner weights clamped to the selected chart. No topology changes; texture seam/blur review required.'};progress_path.write_text(json.dumps(progress,indent=2),encoding='utf-8')
        if first==done or last==len(dst.polygons) or (first//25000)%10==0:print('UV_PROGRESS',last,len(dst.polygons),round(time.monotonic()-started,1),flush=True)
    layer=dst.uv_layers.get(src.uv_layers.active.name) or dst.uv_layers.new(name=src.uv_layers.active.name);layer.data.foreach_set('uv',np.asarray(uv).reshape(-1));dst.update();return json.loads(progress_path.read_text())
