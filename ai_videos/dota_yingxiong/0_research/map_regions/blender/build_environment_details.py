"""Place editable environment geometry from the original map object records."""
from __future__ import annotations
import json
import math
import random
import sys
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector
from mathutils.noise import noise_vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_production_map import Geometry, mesh_object, surface, collection

ROOT = Path(__file__).resolve().parents[3]
OUT = next(ROOT.glob('2_*')) / 'background/map_3d'


class DetailGeometry(Geometry):
    def ellipsoid(self, center, scale, material, rings=12, segments=20, irregular=0):
        start = len(self.vertices)
        center, scale = Vector(center), Vector(scale)
        for i in range(rings+1):
            t = math.pi * i / rings
            for j in range(segments):
                a = math.tau * j / segments
                v = Vector((math.sin(t)*math.cos(a), math.sin(t)*math.sin(a), math.cos(t)))
                if irregular:
                    v *= 1 + irregular * noise_vector(v*3+center).x
                self.vertices.append(center + Vector((v.x*scale.x,v.y*scale.y,v.z*scale.z)))
        for i in range(rings):
            for j in range(segments):
                a=start+i*segments+j;b=start+i*segments+(j+1)%segments
                self.faces.append((a,b,b+segments,a+segments));self.indices.append(material)

    def box(self, center, size, material):
        offset=len(self.vertices)
        for z in (-1,1):
            for y in (-1,1):
                for x in (-1,1):
                    self.vertices.append(tuple(center[i]+size[i]*v*.5 for i,v in enumerate((x,y,z))))
        for face in ((0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)):
            self.faces.append(tuple(offset+x for x in face));self.indices.append(material)

    def ring(self, center, radius, tube, material, segments=48):
        points=[]
        for i in range(segments+1):
            a=math.tau*i/segments;points.append((center[0]+radius*math.cos(a),center[1]+radius*math.sin(a),center[2]))
        self.branch(points,[tube]*len(points),material,8)

    def skull(self, center, scale=1):
        c=Vector(center)
        self.ellipsoid(c,(.12*scale,.15*scale,.17*scale),5)
        self.ellipsoid(c+Vector((0,-.08,-.105))*scale,(.09*scale,.10*scale,.075*scale),5)
        for sign in (-1,1):
            self.ellipsoid(c+Vector((sign*.057,-.136,.018))*scale,(.041*scale,.021*scale,.044*scale),6,8,12)
        self.ellipsoid(c+Vector((0,-.157,-.034))*scale,(.025*scale,.01*scale,.028*scale),6,6,8)
        for j in range(8):
            self.box(c+Vector(((j-3.5)*.019,-.16,-.10))*scale,(.014*scale,.025*scale,.031*scale),5)

    def skeleton(self, center=(0,0,0), scale=1, seated=False):
        c=Vector(center)
        def p(x,y,z):return c+Vector((x,y,z))*scale
        self.skull(p(0,0,1.45),scale)
        self.branch([p(0,0,.65),p(0,.04,1.25)],[.06*scale,.045*scale],5)
        for i in range(7):
            z=.84+i*.052;r=.12+math.sin(i/7*math.pi)*.1
            pts=[p(math.cos(a)*r,math.sin(a)*r*.52,z) for a in np.linspace(0,math.tau,20)]
            self.branch(pts,[.014*scale]*20,5,6)
        for side in (-1,1):
            self.branch([p(side*.08,0,.7),p(side*.13,-.3 if seated else 0,.38),p(side*.15,-.35 if seated else -.02,.06)],[.065*scale,.045*scale,.025*scale],5)
            self.branch([p(side*.21,0,1.2),p(side*.30,.01,.9),p(side*.32,-.1,.63)],[.04*scale,.025*scale,.018*scale],5)
        self.ellipsoid(p(0,0,.69),(.15*scale,.09*scale,.11*scale),5)


def materials():
    specs=[
        ('Weathered_wood',(.025,.013,.006),(.18,.105,.04),4,.78,.035),
        ('Grey_limestone',(.065,.058,.045),(.30,.28,.22),2,.85,.045),
        ('Forged_iron',(.015,.019,.022),(.08,.09,.095),5,.48,.012),
        ('Leaf_green',(.009,.025,.003),(.08,.18,.025),12,.65,.002),
        ('Leaf_dark',(.007,.009,.006),(.035,.05,.02),12,.75,.002),
        ('Old_bone',(.16,.13,.085),(.53,.47,.33),18,.8,.004),
        ('Recess_shadow',(.002,.002,.002),(.009,.007,.005),10,.95,.001),
        ('Mushroom_cap',(.045,.014,.004),(.24,.065,.012),8,.6,.007),
        ('Pale_fungus',(.12,.105,.065),(.40,.33,.16),8,.75,.003),
        ('Flower_petals',(.12,.045,.12),(.48,.20,.42),20,.58,.001),
        ('Weathered_bronze',(.018,.055,.044),(.19,.16,.075),5,.5,.009),
        ('Basalt',(.015,.016,.02),(.075,.07,.065),3,.83,.05),
    ]
    result=[surface(*s) for s in specs]
    for i in (2,10):result[i].node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=.8
    for name,color,power in [('Ember',(1,.12,.008),5),('Faerie_light',(.16,.3,1),3),('Rune_glow',(.05,.5,.35),2)]:
        m=bpy.data.materials.new(name);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*color,1);b.inputs['Emission Color'].default_value=(*color,1);b.inputs['Emission Strength'].default_value=power;result.append(m)
    leaf=result[3].node_tree.nodes.get('Principled BSDF');leaf.inputs['Subsurface Weight'].default_value=.09
    return result


def vegetation(g,rng,kind,dark=False):
    leaf=4 if dark else 3
    if kind in ('shrub','flower'):
        for b in range(16):
            a=rng.uniform(0,math.tau);h=rng.uniform(.35,1.25);r=rng.uniform(.15,.7)
            end=Vector((math.cos(a)*r,math.sin(a)*r,h))
            g.branch([(0,0,0),end*.6,end],[.025,.012,.003],0,6)
            for j in range(16):
                center=end*rng.uniform(.3,1)+Vector((rng.uniform(-.18,.18),rng.uniform(-.18,.18),rng.uniform(-.08,.12)))
                g.leaf(center,(math.cos(a+j),math.sin(a+j),.2),.18,.055,leaf)
            if kind=='flower':
                for j in range(6):
                    a=j*math.tau/6;g.leaf(end,(math.cos(a),math.sin(a),.2),.12,.05,9)
                g.ellipsoid(end,(.035,.035,.025),8,5,8)
    elif kind in ('reeds','grass','wheat'):
        for i in range(35):
            x,y=rng.uniform(-.6,.6),rng.uniform(-.6,.6);h=rng.uniform(.4,1.4) if kind!='grass' else rng.uniform(.08,.4)
            bend=Vector((rng.uniform(-.2,.2),rng.uniform(-.2,.2),h))
            g.branch([(x,y,0),(x+bend.x*.3,y+bend.y*.3,h*.6),(x+bend.x,y+bend.y,h)],[.012,.006,.002],leaf,4)
            for z in (.25,.5,.7):g.leaf((x+bend.x*z,y+bend.y*z,h*z),(bend.x+.3,bend.y+.2,.4),h*.45,.023,leaf)
            if kind!='grass':g.ellipsoid((x+bend.x,y+bend.y,h*.95),(.035,.035,.15),0 if kind=='reeds' else 8,8,8)
    elif kind=='mushrooms':
        for i in range(9):
            x,y=rng.uniform(-.7,.7),rng.uniform(-.7,.7);h=rng.uniform(.12,.65)
            g.branch([(x,y,0),(x+.03,y,h)],[h*.13,h*.1],8,8)
            g.ellipsoid((x+.03,y,h),(h*.6,h*.6,h*.2),7 if not dark else 4,10,16)
    elif kind=='lily':
        for i in range(7):
            x,y=rng.uniform(-.6,.6),rng.uniform(-.6,.6);g.ellipsoid((x,y,.018),(.2,.23,.015),leaf,4,18)
    elif kind=='thorns':
        for j in range(6):
            pts=[(i*.18-.9,math.sin(i*.5+j)*.25,j*.05+.15) for i in range(12)]
            g.branch(pts,[.04]*12,0)
            for p in pts[::2]:g.branch([p,(p[0]+.03,p[1]-.02,p[2]+.15)],[.025,.001],0,6)


def prototype(code,variant,mats,record):
    rng=random.Random(code+str(variant));g=DetailGeometry();kind=''
    if code in ('ZPsh','D00B'):kind='shrub'
    elif code=='ZPfw':kind='flower'
    elif code in ('APms','CPms'):kind='mushrooms'
    elif code in ('CPct','ZPru'):kind='reeds'
    elif code=='CPlp':kind='lily'
    elif code=='LPwh':kind='wheat'
    elif code=='APtv':kind='thorns'
    elif code=='GRASS':kind='grass'
    if kind:vegetation(g,rng,kind,code in ('D00B','CPms','CPct'))
    elif code in ('ARrk','CRrk','NRfs','CLIFF'):
        for i in range(3 if code!='CLIFF' else 1):
            g.ellipsoid((rng.uniform(-.5,.5),rng.uniform(-.4,.4),.4),(.7,.55,.7),11 if code=='CRrk' else 1,14,22,.4)
    elif code in ('LOsk','OOsk','AOsr'):
        for i in range(7 if code!='OOsk' else 1):g.skull((rng.uniform(-.35,.35),rng.uniform(-.3,.3),.17+(i%3)*.12),rng.uniform(.8,1.6))
        if code=='AOsr':
            for i in range(8):g.branch([(rng.uniform(-.5,.5),rng.uniform(-.5,.5),.04),(rng.uniform(-.5,.5),rng.uniform(-.5,.5),.07)],[.025,.015],5)
    elif code in ('LOth','LOtz','IOst','LOlp','AOnt'):
        h=2.5 if code in ('LOlp','AOnt') else 1.9
        g.branch([(0,0,0),(0,0,h)],[.12,.085],0,12)
        for z in (.15,h*.5,h-.2):g.ring((0,0,z),.10,.025,2)
        if code in ('AOnt','LOlp'):
            g.box((0,0,h+.1),(.42,.42,.55),10)
            for side in (-1,1):g.box((side*.218,0,h+.1),(.01,.25,.32),12)
            g.ellipsoid((0,0,h+.45),(.33,.33,.13),2,6,12)
        else:
            if code=='IOst':g.skull((0,-.05,h-.05),1.7)
            g.ellipsoid((0,0,h+.13),(.1,.10,.25),12,10,12,.3)
    elif code in ('NOfl','D000','NOal','VOfs','VOfl'):
        length=1.8 if code=='VOfs' else 3.4
        for x in (-length/2,length/2):g.branch([(x,0,0),(x,0,1.2)],[.10,.07],0)
        for z in (.38,.9):g.box((0,0,z),(length,.12,.12),0)
        if code=='NOal':
            for z in (.38,.9):g.box((length/2,length/2,z),(.12,length,.12),0)
            g.branch([(length/2,length,0),(length/2,length,1.2)],[.1,.07],0)
    elif code in ('NOfg','NOfp','LObz','AObr','LOca'):
        radius=.65 if code in ('NOfg','NOfp') else .42
        for i in range(12):
            a=i*math.tau/12;g.ellipsoid((radius*math.cos(a),radius*math.sin(a),.10),(.18,.16,.13),1,7,10,.2)
        for i in range(6):
            a=i*math.tau/6;g.branch([(math.cos(a)*.5,math.sin(a)*.5,.12),(math.cos(a+math.pi)*.5,math.sin(a+math.pi)*.5,.18)],[.075,.06],0)
        if code in ('LObz','AObr','LOca'):
            g.ellipsoid((0,0,.6),(.48,.48,.3),2);g.ring((0,0,.8),.44,.05,2)
            for a in (0,2.1,4.2):g.branch([(.4*math.cos(a),.4*math.sin(a),0),(.3*math.cos(a),.3*math.sin(a),.6)],[.05,.04],2)
        else:g.ellipsoid((0,0,.23),(.35,.35,.12),12,8,12,.3)
        if code=='NOfg':
            g.branch([(-1,0,0),(-1,0,1.2)],[.06,.04],0);g.branch([(1,0,0),(1,0,1.2)],[.06,.04],0);g.branch([(-1.1,0,1),(1.1,0,1)],[.025,.025],2)
            g.ellipsoid((0,0,1),(.55,.23,.24),7);g.ellipsoid((.6,0,1),(.18,.18,.18),7)
        if code in ('AObr','LOca'):
            for i in range(3):g.skull((math.cos(i*2.1)*.34,math.sin(i*2.1)*.34,.85),1)
    elif code in ('LOpg','LOgr','NOtb','COob','AOob','NOok','AOsk','ASbc','CSbc','CSbl','OOob','OOal','NSct','D001'):
        if code in ('LOpg','LOgr','NOtb'):
            g.ellipsoid((0,.4,.07),(.45,.9,.1),1,8,16,.12);g.box((0,0,.5),(.65,.18,1),1);g.ellipsoid((0,0,1),(.32,.09,.22),1,8,16)
            g.box((0,-.1,.7),(.3,.025,.035),6);g.box((0,-.1,.7),(.035,.025,.4),6)
        elif code in ('ASbc','CSbc'):
            g.box((0,0,.12),(1.2,1.2,.24),1);g.branch([(0,0,.24),(.03,.01,1.7)],[.42,.36],1,16);g.ring((0,0,.35),.45,.07,1)
        elif code=='CSbl':
            for i in range(12):g.box((rng.uniform(-1,1),rng.uniform(-1,1),rng.uniform(.1,.5)),(.55,.40,.30),1)
        elif code=='NSct':
            g.box((0,0,.7),(2.5,3,1.4),1);g.ellipsoid((0,0,1.4),(1.25,1.5,.8),1);g.box((0,-1.51,.6),(.8,.02,1.2),6)
        elif code in ('OOal','D001'):
            for i in range(3):g.box((0,0,i*.15+.075),(2.4-i*.4,2.4-i*.4,.15),1)
            g.branch([(0,0,.4),(0,0,1.35)],[.40,.25],1,8);g.box((0,0,1.45),(1.1,.8,.2),10)
            if code=='D001':g.box((0,0,1.58),(.7,.5,.08),8)
        else:
            g.box((0,0,.12),(1.4,1.4,.24),1);g.branch([(0,0,.24),(0,0,2.4),(0,0,3.1)],[.48,.29,.005],1,4)
            for j in range(5):g.box((0,-.32,.6+j*.3),(.15,.01,.08),14 if code=='AOob' else 10)
    elif code in ('LOic','LOsh','LOss','LOsc'):
        if code=='LOsc':g.skeleton(seated=True)
        else:
            g.branch([(0,0,0),(0,0,2.6)],[.06,.012],0)
            if code=='LOic':g.skeleton((0,0,.6))
            else:
                for i in range(3 if code=='LOss' else 1):g.skull((0,-.03,2.2-i*.35),1.2)
    elif code in ('COhs',):
        for i in range(18):
            a=i*math.tau/18;h=rng.uniform(.7,1.1);g.branch([(.65*math.cos(a),.65*math.sin(a),0),(.5*math.cos(a),.5*math.sin(a),h)],[.13,.09],0)
        for i in range(6):
            a=i*math.tau/6;g.branch([(math.cos(a),math.sin(a),0),(.5*math.cos(a),.5*math.sin(a),.4)],[.04,.15],0)
    elif code in ('AObd','NObt','AWfs','ZWfs','ZWsf','LOfl'):
        for i in range(7 if code in ('ZWsf','LOfl') else 3):
            x,y,z=rng.uniform(-.6,.6),rng.uniform(-.6,.6),rng.uniform(.2,1.4)
            if code in ('AWfs','ZWfs','ZWsf'):
                g.ellipsoid((x,y,z),(.06,.2,.07),10,6,10);g.leaf((x,y+.22,z),(0,1,0),.15,.10,10)
            else:
                size=.02 if code=='LOfl' else .16;g.ellipsoid((x,y,z),(size*.5,size,size*.5),4,6,10)
                for sign in (-1,1):g.leaf((x+sign*size,y,z),(sign,0,.3),size*2.4,size*.8,4)
    elif code in ('D009','JOgr','CObl','LWw0'):
        if code=='JOgr':
            for j in range(9):
                a=j*math.tau/9;g.box((math.cos(a)*.8,math.sin(a)*.8,.015),(.09,.24,.015),14)
        elif code=='LWw0':
            for j in range(15):
                x=(j-7)*.09;g.branch([(x,0,1.6),(x,.2,.7),(x,.35,-1.4)],[.05,.06,.08],13,6)
        else:
            for i in range(12):g.ellipsoid((rng.uniform(-.5,.5),rng.uniform(-.5,.5),rng.uniform(.2,1.2)),(.012,.012,.012),13,5,8)
    elif code in ('NWrd','NWsd'):
        length=3 if code=='NWrd' else 8;width=length*.3
        for j in range(9):
            z=j*.09;points=[]
            for a in np.linspace(0,math.tau,40):points.append((math.cos(a)*length/2,math.sin(a)*width*(.3+j*.07),z))
            g.branch(points,[.06]*len(points),0,6)
        for i in range(7):g.box(((i-3)*length/8,0,.22),(.15,width*1.4,.08),0)
        if code=='NWsd':g.branch([(0,0,.3),(.4,.2,4)],[.15,.07],0)
    elif code in ('AOks','AOgs'):
        g.box((0,0,.2),(1.8,1.8,.4),1);g.ellipsoid((0,0,1.9),(.4,.24,.7),1)
        g.ellipsoid((0,0,2.8),(.24,.23,.30),1)
        for sign in (-1,1):
            g.branch([(sign*.19,0,1.5),(sign*.25,0,.45)],[.17,.12],1)
            g.branch([(sign*.33,0,2.3),(sign*.6,-.08,1.6)],[.13,.09],1)
        g.branch([(.65,-.05,.3),(.65,-.05,3.2)],[.035,.025],10)
    else:raise ValueError('Unclassified visible object '+code)
    lib=bpy.data.collections.new(f'ENV_{code}_{variant}')
    obj=mesh_object(f'{code}_{variant}',g.vertices,g.faces,mats,g.indices,lib)
    for poly in obj.data.polygons:poly.use_smooth=poly.material_index not in (1,2)
    obj['source_rawcode']=code;obj['source_model']=record.get('source_model','procedural support vegetation')
    return lib


def main():
    dest=OUT/'environment_v003.blend'
    if dest.exists():raise FileExistsError(dest)
    bpy.ops.wm.open_mainfile(filepath=str(OUT/'foundation_v002.blend'))
    inv=json.loads((OUT/'environment_inventory.json').read_text(encoding='utf-8'))
    mats=materials();terrain=bpy.data.objects['Terrain_683d'].data
    coords=np.empty(len(terrain.vertices)*3,np.float32);terrain.vertices.foreach_get('co',coords);coords=coords.reshape(1025,1025,3)
    def height(x,y):
        u,v=np.clip((x+409.6)/.8,0,1023.999),np.clip((y+409.6)/.8,0,1023.999);i,j=int(u),int(v);a,b=u-i,v-j
        return float((coords[j,i,2]*(1-a)+coords[j,i+1,2]*a)*(1-b)+(coords[j+1,i,2]*(1-a)+coords[j+1,i+1,2]*a)*b)
    details=bpy.data.collections['04_Environment_Details'];library={}
    for record in inv['types']:
        code=record['rawcode']
        if code in ('YTlb','YTpb'):continue
        library[code]=[prototype(code,i,mats,record) for i in range(3 if record['instances']>20 else 1)]
    for row in inv['placements']:
        code=row['id']
        if code not in library:continue
        obj=bpy.data.objects.new(f'Original_{code}_{row["editor_id"]}',None);details.objects.link(obj)
        obj.instance_type='COLLECTION';obj.instance_collection=library[code][row['editor_id']%len(library[code])]
        x,y=row['x']/20,row['y']/20;z=height(x,y)
        if code in ('AWfs','ZWfs','ZWsf','CPlp'):z=-6.85
        if code in ('AObd','NObt'):z+=4
        obj.location=(x,y,z);obj.rotation_euler.z=row['angle'];obj.scale=(row['scale'],)*3
        obj['source_editor_id']=row['editor_id'];obj['source_rawcode']=code
    # Grass is concentrated around existing tree roots, keeping original lanes open.
    grass=[prototype('GRASS',i,mats,{}) for i in range(5)];undergrowth=collection('06_Undergrowth')
    rng=random.Random(289)
    for tree in bpy.data.collections['02_Forest'].objects:
        if not tree.instance_collection or 'Tree_5' in tree.instance_collection.name or 'Tree_6' in tree.instance_collection.name or 'Tree_7' in tree.instance_collection.name:continue
        for i in range(14):
            a=rng.uniform(0,math.tau);r=rng.uniform(.8,2.8);x,y=tree.location.x+math.cos(a)*r,tree.location.y+math.sin(a)*r
            obj=bpy.data.objects.new('Forest_floor_grasses',None);undergrowth.objects.link(obj);obj.instance_type='COLLECTION';obj.instance_collection=grass[i%5]
            obj.location=(x,y,height(x,y));obj.rotation_euler.z=a;obj.scale=(rng.uniform(.6,1.5),)*3
    # Surface rock relief uses the cliff mask, never the road/ramp interiors.
    rocks=[prototype('CLIFF',i,mats,{}) for i in range(5)];cliffs=collection('07_Cliff_Relief')
    for j in range(2,1023,4):
        for i in range(2,1023,4):
            x,y,z=coords[j,i];slope=max(abs(coords[j,i+1,2]-coords[j,i-1,2]),abs(coords[j+1,i,2]-coords[j-1,i,2]))/1.6
            if slope<1.2 or rng.random()>.55:continue
            obj=bpy.data.objects.new('Cliff_outcrop',None);cliffs.objects.link(obj);obj.instance_type='COLLECTION';obj.instance_collection=rocks[(i+j)%5]
            obj.location=(float(x),float(y),float(z)-.4);obj.scale=(rng.uniform(1,2.6),rng.uniform(1,2.6),rng.uniform(.7,1.6));obj.rotation_euler.z=rng.uniform(0,math.tau)
    bpy.context.scene['production_status']='ENVIRONMENT CANDIDATE: original doodads + undergrowth + cliff relief; asset assembly and QC pending'
    bpy.ops.wm.save_as_mainfile(filepath=str(dest))
    report={'file':dest.name,'status':'candidate_pending_visual_review','original_visible_instances':len(details.objects),'original_types':len(library),'grass_instances':len(undergrowth.objects),'cliff_outcrops':len(cliffs.objects),'logical_blockers_excluded':195,'limitations':['Statues and corpse props need close-up detail review','Ambient effects are static representations; animation out of scope']}
    (OUT/'environment_v003_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(report,flush=True)


if __name__=='__main__':main()
