"""Refine cliff transitions, vegetation and atmosphere without moving map anchors."""
from pathlib import Path
import sys,json,math,random
import bpy
import numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_environment_details import DetailGeometry, prototype, OUT
from build_production_map import mesh_object, collection, surface

dest=OUT/'environment_v004.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v003.blend'))
terrain=bpy.data.objects['Terrain_683d'].data
flat=np.empty(len(terrain.vertices)*3,np.float32);terrain.vertices.foreach_get('co',flat)
coords=flat.reshape(1025,1025,3);z=coords[:,:,2].copy();original=z.copy()
gy,gx=np.gradient(z,.8);steep=np.sqrt(gx*gx+gy*gy)
# Small-radius smoothing softens voxel-shaped corners; preserve flat levels.
blur=z.copy()
for _ in range(4):
    p=np.pad(blur,1,mode='edge');blur=(p[1:-1,1:-1]*4+p[:-2,1:-1]+p[2:,1:-1]+p[1:-1,:-2]+p[1:-1,2:])/8
blend=np.clip(steep*.9,0,1)
z=z*(1-blend)+blur*blend
noise=(np.sin(coords[:,:,0]*2.7+np.sin(coords[:,:,1]*.8))*np.cos(coords[:,:,1]*2.3)+np.sin(coords[:,:,0]*.73+coords[:,:,1]*1.2))*.055
z+=noise*np.clip(steep,0,1)
coords[:,:,2]=z;terrain.vertices.foreach_set('co',coords.ravel());terrain.update()
gy,gx=np.gradient(z,.8);steep=np.sqrt(gx*gx+gy*gy)
terrain.attributes['Rock'].data.foreach_set('value',np.clip((steep-.3)*1.3,0,1).astype(np.float32).ravel())
def height(x,y):
    u,v=np.clip((x+409.6)/.8,0,1023.999),np.clip((y+409.6)/.8,0,1023.999);i,j=int(u),int(v);a,b=u-i,v-j
    return float((z[j,i]*(1-a)+z[j,i+1]*a)*(1-b)+(z[j+1,i]*(1-a)+z[j+1,i+1]*a)*b)
def delta(x,y):
    i,j=int(np.clip((x+409.6)/.8,0,1024)),int(np.clip((y+409.6)/.8,0,1024));return float(z[j,i]-original[j,i])
for name in ('02_Forest','03_Asset_Placement','04_Environment_Details','06_Undergrowth'):
    for obj in bpy.data.collections[name].objects:
        if obj.get('source_rawcode') not in ('AWfs','ZWfs','ZWsf','CPlp'):
            obj.location.z+=delta(obj.location.x,obj.location.y)
mats=[bpy.data.materials[n] for n in ['Weathered_wood','Grey_limestone','Forged_iron','Leaf_green','Leaf_dark','Old_bone','Recess_shadow','Mushroom_cap','Pale_fungus','Flower_petals','Weathered_bronze','Basalt','Ember','Faerie_light','Rune_glow']]
rocks=[prototype('CLIFF',i+10,mats,{}) for i in range(7)]
coll=bpy.data.collections['07_Cliff_Relief'];rng=random.Random(290)
locations=np.argwhere(steep>1.0)
for j,i in locations[::7]:
    x,y,ground=coords[j,i]
    obj=bpy.data.objects.new('Layered_cliff_rock',None);coll.objects.link(obj);obj.instance_type='COLLECTION';obj.instance_collection=rocks[(int(i)+int(j))%7]
    obj.location=(float(x),float(y),float(ground)-.55)
    obj.scale=(rng.uniform(.9,1.8),rng.uniform(.6,1.3),rng.uniform(.7,1.6));obj.rotation_euler.z=math.atan2(float(gy[j,i]),float(gx[j,i]))+rng.uniform(-.4,.4)
# Dense broadleaf crowns: shared geometry per tree variant, not billboards.
for variant in range(5):
    tree=bpy.data.collections[f'LIB_Tree_{variant}'];g=DetailGeometry();rng2=random.Random(490+variant)
    body=next(o for o in tree.objects if o.type=='MESH')
    h=max(v.co.z for v in body.data.vertices)
    for cluster in range(65):
        a=cluster*2.39996;r=rng2.uniform(.5,4.4);zz=h*(.58+rng2.uniform(0,.32))-.075*r*r
        centre=Vector((math.cos(a)*r,math.sin(a)*r,zz))
        for leaf in range(100):
            offset=Vector((rng2.gauss(0,.65),rng2.gauss(0,.65),rng2.gauss(0,.35)))
            point=centre+offset;direction=(rng2.uniform(-1,1),rng2.uniform(-1,1),rng2.uniform(-.3,.6))
            g.leaf(point,direction,rng2.uniform(.15,.29),rng2.uniform(.045,.09),leaf%3)
    obj=mesh_object(f'Leaf_crown_{variant}',g.vertices,g.faces,[bpy.data.materials[f'Leaves_{i}'] for i in range(3)],g.indices,tree)
# Add sparse ground growth on grass tiles, excluding paved areas and steep walls.
def attribute(n):
    data=np.empty(len(terrain.vertices),np.float32);terrain.attributes[n].data.foreach_get('value',data);return data.reshape(1025,1025)
grassmask,blight,paving=attribute('Grass'),attribute('Blight'),attribute('Paving')
grass=[bpy.data.collections[f'ENV_GRASS_{i}'] for i in range(5)]
growth=collection('08_Meadow_Growth');stones=collection('09_Ground_Stones')
for j in range(2,1023,4):
    for i in range(2,1023,4):
        if steep[j,i]>.35 or paving[j,i]>.2 or z[j,i]<-6.5:continue
        x,y,_=coords[j,i]
        if grassmask[j,i]>.5 and blight[j,i]<.4 and rng.random()<.5:
            obj=bpy.data.objects.new('Meadow_grass',None);growth.objects.link(obj);obj.instance_type='COLLECTION';obj.instance_collection=grass[(i+j)%5]
            obj.location=(float(x),float(y),height(x,y));obj.rotation_euler.z=rng.uniform(0,math.tau);obj.scale=(rng.uniform(.5,1.3),)*3
        elif rng.random()<.025:
            obj=bpy.data.objects.new('Ground_stone',None);stones.objects.link(obj);obj.instance_type='COLLECTION';obj.instance_collection=rocks[(i+j)%7]
            obj.location=(float(x),float(y),float(z[j,i])-.05);obj.scale=(rng.uniform(.1,.3),rng.uniform(.1,.3),rng.uniform(.07,.2));obj.rotation_euler.z=rng.uniform(0,math.tau)
# Physical atmosphere provides distance separation without hiding geometry.
atmos=bpy.data.materials.new('Low_density_day_haze');atmos.use_nodes=True;nt=atmos.node_tree;nt.nodes.clear()
out=nt.nodes.new('ShaderNodeOutputMaterial');volume=nt.nodes.new('ShaderNodeVolumeScatter');volume.inputs['Density'].default_value=.00045;volume.inputs['Color'].default_value=(.65,.72,.8,1);volume.inputs['Anisotropy'].default_value=.25;nt.links.new(volume.outputs[0],out.inputs['Volume'])
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,90));fog=bpy.context.object;fog.name='Atmosphere_volume';fog.scale=(1200,1200,220);fog.data.materials.append(atmos);fog.display_type='WIRE'
# A distant ground apron avoids an empty black horizon outside the playable map.
apron=surface('Distant_earth',(.018,.025,.014),(.07,.08,.045),.02,bump=.08)
bpy.ops.mesh.primitive_plane_add(size=6000,location=(0,0,-19));bpy.context.object.name='Distant_land_apron';bpy.context.object.data.materials.append(apron)
bpy.context.scene.view_settings.exposure=-1.0
bpy.context.scene['production_status']='ENVIRONMENT V004 CANDIDATE; detailed buildings/NPC assembly pending'
bpy.ops.wm.save_as_mainfile(filepath=str(dest))
report={'file':dest.name,'cliff_outcrops':len(coll.objects),'meadow_instances':len(growth.objects),'ground_stones':len(stones.objects),'max_height_adjustment_m':float(np.max(np.abs(z-original))),'original_anchor_xy_unchanged':True,'status':'pending_visual_and_route_review'}
(OUT/'environment_v004_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report,flush=True)
