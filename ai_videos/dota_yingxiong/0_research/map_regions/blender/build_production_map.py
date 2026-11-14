from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from region_blockout import Terrain, read_doodads


DRAMA = Path(__file__).resolve().parents[3]
WORLD = next(DRAMA.glob('2_*'))
OUT = WORLD / 'background/map_3d'
RESEARCH = DRAMA / '0_research'


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def collection(name: str, parent=None):
    result = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(result)
    return result


def mesh_object(name, vertices, faces, materials, indices, parent):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    for material in materials:
        mesh.materials.append(material)
    if indices:
        mesh.polygons.foreach_set('material_index', indices)
    obj = bpy.data.objects.new(name, mesh)
    parent.objects.link(obj)
    return obj


def surface(name, dark, light, scale=1.0, roughness=0.85, bump=0.08):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    bsdf = nodes.get('Principled BSDF')
    bsdf.inputs['Roughness'].default_value = roughness
    coord = nodes.new('ShaderNodeTexCoord')
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = scale
    noise.inputs['Detail'].default_value = 5
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (*dark, 1)
    ramp.color_ramp.elements[1].color = (*light, 1)
    links.new(coord.outputs['Object'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    fine = nodes.new('ShaderNodeTexNoise')
    fine.inputs['Scale'].default_value = scale * 18
    fine.inputs['Detail'].default_value = 3
    links.new(coord.outputs['Object'], fine.inputs['Vector'])
    normal = nodes.new('ShaderNodeBump')
    normal.inputs['Strength'].default_value = 0.65
    normal.inputs['Distance'].default_value = bump
    links.new(fine.outputs['Fac'], normal.inputs['Height'])
    links.new(normal.outputs['Normal'], bsdf.inputs['Normal'])
    mat.diffuse_color = (*light, 1)
    return mat


class Geometry:
    def __init__(self):
        self.vertices, self.faces, self.indices = [], [], []

    def branch(self, points, radii, material=0, segments=8):
        offset = len(self.vertices)
        for i, (point, radius) in enumerate(zip(points, radii)):
            tangent = (Vector(points[min(i + 1, len(points) - 1)]) - Vector(points[max(i - 1, 0)])).normalized()
            axis = tangent.cross(Vector((0, 1, 0))).normalized()
            across = tangent.cross(axis).normalized()
            for j in range(segments):
                angle = j * math.tau / segments
                self.vertices.append(Vector(point) + radius * (axis * math.cos(angle) + across * math.sin(angle)))
        for i in range(len(points) - 1):
            for j in range(segments):
                a = offset + i * segments + j
                b = offset + i * segments + (j + 1) % segments
                self.faces.append((a, b, b + segments, a + segments))
                self.indices.append(material)
        self.faces.append(tuple(offset + (len(points) - 1) * segments + j for j in range(segments)))
        self.indices.append(material)

    def leaf(self, center, direction, length, width, material):
        axis = Vector(direction).normalized()
        across = axis.cross(Vector((0, 0, 1)))
        if across.length < 0.01:
            across = Vector((1, 0, 0))
        across.normalize()
        normal = axis.cross(across).normalized()
        center = Vector(center)
        offset = len(self.vertices)
        self.vertices.extend([center - axis * length * 0.4,
                              center - across * width,
                              center + axis * length * 0.6,
                              center + across * width,
                              center + normal * width * 0.22])
        for tri in ((0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)):
            self.faces.append(tuple(offset + n for n in tri))
            self.indices.append(material)


class MapBuilder:
    def __init__(self):
        self.common = read(Path(__file__).with_name('common.json'))
        self.upm = self.common['units_per_m']
        self.samples = read(RESEARCH / 'base_layout_refs/terrain_samples.json')
        self.terrain = Terrain(self.samples, self.common['base_layer'], self.common['level_height_m'])
        self.asset_manifest = read(OUT / 'asset_manifest.json')
        self.base = read(RESEARCH / 'base_layout_refs/base_layout_manifest.json')
        self.features = read(RESEARCH / 'map_regions/map_features.json')
        self.report = {'followups': [287, 288], 'status': 'foundation_pending_assets', 'assets': [],
                       'missing_models': [], 'warnings': ['本文件是地形与布局工作底稿，尚非精细地图交付。']}
        self.ground_coll = collection('01_Terrain_Water')
        self.forest_coll = collection('02_Forest')
        self.slots = collection('03_Asset_Placement')
        self.details = collection('04_Environment_Details')
        self.cameras = collection('05_Cameras_Lighting')

    def flag(self, x, y):
        i = max(0, min(128, round((x + 8192) / 128)))
        j = max(0, min(128, round((y + 8192) / 128)))
        return self.samples['flags'][j][i]

    def point(self, x, y, height=0):
        return (x / self.upm, y / self.upm, self.terrain.z(x, y) + height)

    def ground(self):
        materials = [
            surface('Forest_soil', (0.035, .024, .013), (.19, .12, .055), 0.9),
            surface('Living_grass_moss', (.025, .045, .012), (.14, .22, .045), 1.4, bump=.025),
            surface('Cliff_strata', (.07, .065, .06), (.30, .28, .23), .8, bump=.18),
            surface('Scourge_ash_soil', (.012, .011, .016), (.105, .09, .11), .8),
            surface('Old_stone_paving', (.10, .095, .08), (.28, .27, .23), 1.5),
        ]
        step = 16
        n = int(16384 / step) + 1
        vertices, faces, indices = [], [], []
        for j in range(n):
            y = -8192 + j * step
            for i in range(n):
                x = -8192 + i * step
                vertices.append(self.point(x, y))
        for j in range(n - 1):
            for i in range(n - 1):
                x, y = -8192 + (i + .5) * step, -8192 + (j + .5) * step
                index = j * n + i
                faces.append((index, index + 1, index + n + 1, index + n))
                flag = self.flag(x, y)
                cliff = self.terrain.tile_kind(x, y) == 'cliff'
                tile = flag & 15
                indices.append(2 if cliff else 3 if flag & 32 else 4 if tile == 6 else 1 if tile in (2, 3, 4, 5) else 0)
        obj = mesh_object('Terrain_683d', vertices, faces, materials, indices, self.ground_coll)
        for poly in obj.data.polygons:
            poly.use_smooth = True
        self.report['terrain_vertices'] = len(vertices)
        water_z = (8.3 - self.common['base_layer']) * self.common['level_height_m']
        extent = 8192 / self.upm
        water = surface('River_water', (.015, .05, .052), (.035, .12, .10), 0.5, .13, .035)
        bsdf = water.node_tree.nodes.get('Principled BSDF')
        bsdf.inputs['Transmission Weight'].default_value = .85
        bsdf.inputs['IOR'].default_value = 1.333
        mesh_object('River_surface', [(-extent, -extent, water_z), (extent, -extent, water_z),
                                     (extent, extent, water_z), (-extent, extent, water_z)],
                    [(0, 1, 2, 3)], [water], [], self.ground_coll)
        print('GROUND', len(vertices), flush=True)

    def tree_library(self):
        bark = surface('Tree_bark', (.032, .018, .009), (.17, .10, .045), 3, bump=.065)
        ash = surface('Dead_bark', (.018, .018, .022), (.14, .135, .15), 3, bump=.07)
        leaves = [surface(f'Leaves_{i}', (.012 + i*.005, .025 + i*.012, .006),
                          (.055 + i*.012, .13 + i*.025, .018), 8, .62, .003) for i in range(3)]
        result = []
        for variant in range(8):
            rng = random.Random(287 + variant)
            dead = variant >= 5
            prototype = bpy.data.collections.new(f'LIB_Tree_{variant}')
            geometry = Geometry()
            height = rng.uniform(12, 17)
            trunk = [(0, 0, 0), (.15, -.1, height*.25), (-.3, .15, height*.52), (.35, .3, height*.82), (.1, .2, height)]
            geometry.branch(trunk, [.6, .43, .31, .14, .025], segments=12)
            for j in range(6):
                a = math.tau * j / 6
                geometry.branch([(math.cos(a)*2.1, math.sin(a)*2.1, -.03),
                                 (math.cos(a)*.8, math.sin(a)*.8, .3), (0,0,1.4)], [.05,.19,.25])
            for j in range(28 if not dead else 19):
                angle = j * 2.39996 + rng.uniform(-.3,.3)
                z = height * rng.uniform(.32,.87)
                radius = (1 - (z / height - .5)**2) * rng.uniform(2.8,4.8)
                end = Vector((math.cos(angle)*radius, math.sin(angle)*radius,z+1.2))
                middle = Vector((end.x*.55,end.y*.55,z-.4))
                geometry.branch([(0,0,z), middle,end], [.20 if not dead else .13,.10,.02])
                for twig in range(5):
                    a = angle + rng.uniform(-1.3,1.3)
                    tip = end + Vector((math.cos(a)*rng.uniform(.4,1.4),math.sin(a)*rng.uniform(.4,1.4),rng.uniform(-.4,1.2)))
                    geometry.branch([middle.lerp(end,.7),end,tip], [.045,.025,.004], segments=5)
                    if not dead:
                        for leaf in range(23):
                            center=tip+Vector((rng.gauss(0,.5),rng.gauss(0,.5),rng.gauss(0,.3)))
                            geometry.leaf(center,(rng.uniform(-1,1),rng.uniform(-1,1),rng.uniform(-.4,.6)),
                                          rng.uniform(.20,.40),rng.uniform(.07,.13),1+rng.randrange(3))
            obj=mesh_object(f'Tree_{variant}',geometry.vertices,geometry.faces,[ash if dead else bark,*leaves],geometry.indices,prototype)
            for poly in obj.data.polygons:
                poly.use_smooth = poly.material_index == 0
            result.append(prototype)
        return result

    def forest(self):
        library=self.tree_library()
        trees=read(RESEARCH/'map_regions/navigation/tree_positions.json')
        for i,tree in enumerate(trees):
            if tree['life'] <= 0:
                continue
            x,y=tree['x'],tree['y']
            dead=bool(self.flag(x,y)&32)
            obj=bpy.data.objects.new(f'Tree_{tree["editor_id"]}',None)
            obj.instance_type='COLLECTION'
            obj.instance_collection=library[5+i%3 if dead else i%5]
            obj.location=self.point(x,y)
            obj.rotation_euler.z=tree['angle'] + (i*.618 % math.tau)
            scale=tree['scale']
            obj.scale=scale
            self.forest_coll.objects.link(obj)
        self.report['tree_instances']=len(self.forest_coll.objects)
        print('FOREST',self.report['tree_instances'],flush=True)

    def placement(self):
        rows=[]
        for row in self.base['rows']:
            if row.get('asset_id'):
                rows.append({'id':row['instance_id'],'asset':row['asset_id'],
                             'xy':[row['x'],row['y']],'facing':row['facing'],'source':'base_layout_manifest.rows'})
        for tower in self.features['towers']:
            x,y=tower['spawn']
            if any(math.dist(row['xy'],(x,y))<50 for row in rows):
                continue
            asset='bg16' if tower['side']=='sentinel' else 'bg37' if tower['tier']==4 else 'bg26'
            rows.append({'id':tower['id'],'asset':asset,'xy':[x,y],'facing':270,'source':'map_features.towers'})
        for shop in self.features['shops']:
            asset={'uC74':'m308','u00Z':'bg36','u010':'bg12'}[shop['rawcode']]
            rows.append({'id':shop['id'],'asset':asset,'xy':shop['spawn'],'facing':270,'source':'map_features.shops'})
        roshan=self.features['roshan']
        rows.append({'id':'Roshan','asset':'m7','xy':roshan['spawn'],'facing':135,'source':'map_features.roshan'})
        for row in rows:
            obj=bpy.data.objects.new(row['id'],None)
            obj.empty_display_type='PLAIN_AXES'
            obj.empty_display_size=1.5
            obj.location=self.point(*row['xy'])
            obj.rotation_euler.z=math.radians(row['facing'])
            obj['asset_id']=row['asset']
            obj['source']=row['source']
            obj['status']='awaiting_reviewed_model'
            self.slots.objects.link(obj)
        self.report['placements']=rows
        self.report['missing_models']=sorted(set(row['asset'] for row in rows))

    def lighting(self):
        scene=bpy.context.scene
        scene.unit_settings.system='METRIC'
        scene.unit_settings.scale_length=1
        scene.render.engine='CYCLES'
        scene.cycles.samples=64
        scene.cycles.use_denoising=True
        scene.view_settings.view_transform='AgX'
        scene.world=bpy.data.worlds.new('Daylight')
        scene.world.use_nodes=True
        nt=scene.world.node_tree
        sky=nt.nodes.new('ShaderNodeTexSky')
        sky.sky_type='MULTIPLE_SCATTERING'
        sky.sun_elevation=math.radians(28)
        sky.sun_rotation=math.radians(292.5)
        sky.sun_intensity=.8
        sky.altitude=0
        sky.air_density=1.2
        nt.links.new(sky.outputs[0],nt.nodes.get('Background').inputs['Color'])
        nt.nodes.get('Background').inputs['Strength'].default_value=.35
        for name,pos,target,ortho in [
            ('Map_Overview',(0,-610,800),(0,0,-2),1020),
            ('Sentinel_Base',(-335,-360,52),(-285,-285,3),0),
            ('Scourge_Base',(360,295,65),(270,245,4),0),
            ('Mid_River',(-70,-110,28),(5,0,-3),0),
        ]:
            data=bpy.data.cameras.new(name)
            obj=bpy.data.objects.new(name,data)
            self.cameras.objects.link(obj)
            obj.location=pos
            obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
            data.clip_end=2500
            data.lens=35
            if ortho:
                data.type='ORTHO';data.ortho_scale=ortho
            if name=='Map_Overview':scene.camera=obj
        scene.render.resolution_x=1600
        scene.render.resolution_y=1200
        scene.render.resolution_percentage=100

    def save(self):
        OUT.mkdir(exist_ok=True,parents=True)
        path=OUT/'foundation_v001.blend'
        if path.exists():raise FileExistsError(path)
        bpy.context.scene['production_status']='FOUNDATION: precision terrain + forest; detailed assets pending'
        bpy.context.scene['units_per_game_metre']=self.upm
        bpy.context.scene['followup']=287
        bpy.ops.wm.save_as_mainfile(filepath=str(path))
        (OUT/'foundation_report.json').write_text(json.dumps(self.report,ensure_ascii=False,indent=2),encoding='utf-8')
        print('SAVED',path,flush=True)


if __name__=='__main__':
    for obj in list(bpy.data.objects):bpy.data.objects.remove(obj,do_unlink=True)
    builder=MapBuilder()
    builder.ground()
    builder.forest()
    builder.placement()
    builder.lighting()
    builder.save()
