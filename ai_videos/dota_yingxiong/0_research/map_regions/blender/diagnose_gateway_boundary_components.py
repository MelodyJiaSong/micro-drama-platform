"""Locate residual scan boundaries around measured face and collar holes."""
from pathlib import Path
import bpy, bmesh, json, numpy as np
from collections import Counter

ROOT = Path(__file__).resolve().parents[3]
folder = next(next(ROOT.glob('2_*')).glob('characters/*/m303_*/model_3d/r07'))
bpy.ops.wm.open_mainfile(filepath=str(folder / 'authoring.blend'))
body = bpy.data.objects['Gateway_merchant_body']
bm = bmesh.new(); bm.from_mesh(body.data)
print('EDGE_FACE_MULTIPLICITY', dict(Counter(len(e.link_faces) for e in bm.edges)), flush=True)
print('DEGENERATE_FACES', sum(f.calc_area() < 1e-12 for f in bm.faces), flush=True)
remaining = {e for e in bm.edges if e.is_boundary}
groups = []
while remaining:
    stack = [remaining.pop()]; part = list(stack)
    while stack:
        for v in stack.pop().verts:
            for e in v.link_edges:
                if e in remaining:
                    remaining.remove(e); stack.append(e); part.append(e)
    vs = {v for e in part for v in e.verts}
    co = np.array([tuple(v.co) for v in vs])
    degree = {v: sum(e.is_boundary for e in v.link_edges) for v in vs}
    groups.append({'edges': len(part), 'bounds': [co.min(0).tolist(), co.max(0).tolist()],
                   'dimensions': np.ptp(co, axis=0).tolist(), 'centre': co.mean(0).tolist(),
                   'degree_two': all(d == 2 for d in degree.values()),
                   'branch_vertices': sum(d != 2 for d in degree.values())})
simple_extents = [max(g['dimensions']) for g in groups if g['degree_two']]
remaining = {e for e in bm.edges if e.is_boundary}; cycles = []; failed = 0
while remaining:
    start = next(iter(remaining)); edge = start; cycle = []; seen = set(); broken = False
    while edge not in seen:
        seen.add(edge); cycle.append(edge)
        loop = edge.link_loops[0].link_loop_next
        rotated = set()
        while not loop.edge.is_boundary and loop not in rotated and loop.edge.is_manifold:
            rotated.add(loop); loop = loop.link_loop_radial_next.link_loop_next
        if not loop.edge.is_boundary:
            broken = True
            break
        edge = loop.edge
    remaining.difference_update(seen)
    if broken or edge != start:
        failed += 1; continue
    co = np.array([tuple(e.link_loops[0].vert.co) for e in cycle])
    cycles.append({'edges': len(cycle), 'dimensions': np.ptp(co, axis=0).tolist(),
                   'centre': co.mean(0).tolist(), 'bounds': [co.min(0).tolist(), co.max(0).tolist()]})
report = {'boundary_edges': sum(e.is_boundary for e in bm.edges), 'groups': groups,
          'head_front': [g for g in groups if g['bounds'][1][2] > 1.53 and g['bounds'][0][1] < 0],
          'simple_loop_extent_quantiles': np.quantile(simple_extents, [0,.25,.5,.75,.9,.99,1]).tolist() if simple_extents else [],
          'oriented_cycles': cycles, 'failed_cycle_walks': failed}
(folder / 'boundary_components.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps({'boundary_edges': report['boundary_edges'], 'groups': len(groups), 'oriented_cycles': len(cycles), 'failed_cycle_walks': failed}), flush=True)
bm.free()
