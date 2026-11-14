"""Assemble asset collections at original coordinates; draft/final gates explicit."""
from pathlib import Path
import argparse,json,math,sys,hashlib,base64
import bpy,numpy as np
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_production_map import collection,mesh_object,surface
from build_environment_details import DetailGeometry

ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'


def main(args):
    dest=OUT/args.output
    if dest.exists():raise FileExistsError(dest)
    manifest=json.loads((OUT/'asset_manifest.json').read_text(encoding='utf-8'))
    only=set(args.only_assets or [])
    if only-set(a['id'] for a in manifest['assets']):raise ValueError('Unknown asset selection')
    if only and not args.draft:raise ValueError('Partial asset selection is a draft diagnostic only')
    forward_axes=json.loads((OUT/'model_calibration.json').read_text(encoding='utf-8')).get('verified_forward_axes',{})
    def facing_offset(key):return {'+X':0,'+Y':-math.pi/2,'-X':math.pi,'-Y':math.pi/2}[forward_axes.get(key,'-Y')]
    sources={};missing=[];unreviewed=[];draft_pins={};pin_path=OUT/'draft_asset_selection.json'
    if args.draft and pin_path.exists():draft_pins=json.loads(pin_path.read_text(encoding='utf-8')).get('assets',{})
    for a in manifest['assets']:
        if only and a['id'] not in only:continue
        folder=ROOT/a['model_directory'];options=sorted(folder.glob('r*/inspection/'+a['id']+'_*.blend'))
        reviewed=[]
        for p in options:
            review=p.parent/'independent_review.json'
            if review.exists():
                record=json.loads(review.read_text(encoding='utf-8'))
                if record.get('verdict')=='pass' and record.get('blend_sha256')==hashlib.sha256(p.read_bytes()).hexdigest():
                    evidence=record.get('evidence_files',[])
                    if evidence and all((ROOT/e['path']).exists() and hashlib.sha256((ROOT/e['path']).read_bytes()).hexdigest()==e['sha256'] for e in evidence):reviewed.append(p)
        if reviewed:sources[a['id']]=reviewed[-1]
        elif options and args.draft:
            selected=options[-1];pin=draft_pins.get(a['id'])
            if pin:
                selected=folder/pin['revision']/'inspection'/f"{a['id']}_{pin['revision']}.blend"
                if selected not in options or hashlib.sha256(selected.read_bytes()).hexdigest()!=pin['blend_sha256']:raise ValueError({'invalid_draft_selection':a['id']})
            sources[a['id']]=selected;unreviewed.append(a['id'])
        elif options:unreviewed.append(a['id'])
        else:missing.append(a['id'])
    if not args.draft and (missing or unreviewed):raise RuntimeError({'missing':missing,'unreviewed':unreviewed})
    bpy.ops.wm.open_mainfile(filepath=str(OUT/args.environment))
    library={}
    for key,path in sources.items():
        with bpy.data.libraries.load(str(path),link=True) as (src,dst):
            name='ASSET_'+key
            if name not in src.collections:raise ValueError(f'Missing asset collection: {path}')
            dst.collections=[name]
        library[key]=dst.collections[0]
    terrain=bpy.data.objects['Terrain_683d'].data
    coord=np.empty(len(terrain.vertices)*3,np.float32);terrain.vertices.foreach_get('co',coord);coord=coord.reshape(1025,1025,3)
    def height(x,y):
        u,v=np.clip((x+409.6)/.8,0,1023.999),np.clip((y+409.6)/.8,0,1023.999);i,j=int(u),int(v);a,b=u-i,v-j
        z=coord[:,:,2];return float((z[j,i]*(1-a)+z[j,i+1]*a)*(1-b)+(z[j+1,i]*(1-a)+z[j+1,i+1]*a)*b)
    grid=json.loads((ROOT/'0_research/map_regions/navigation/grid.json').read_text())
    cells=np.frombuffer(base64.b64decode(grid['cells_base64']),np.uint8).reshape(512,512)
    occupied=[];navigation_failures=[]
    def walkable(x,y,radius):
        samples=[(x,y)]+[(x+radius*math.cos(i*math.pi/4),y+radius*math.sin(i*math.pi/4)) for i in range(8)]
        heights=[]
        for px,py in samples:
            if not -409.6<px<409.6 or not -409.6<py<409.6:return False
            code=int(cells[int((409.6-py)/1.6),int((px+409.6)/1.6)])
            if not code&1 or code&(2|4):return False
            heights.append(height(px,py))
        return max(heights)-min(heights)<max(.25,radius*.6)
    def find_ground(x,y,radius,identifier,max_shift=16):
        for distance in np.arange(0,max_shift+.1,.8):
            for i in range(1 if distance==0 else 24):
                angle=i*math.tau/24;px=x+distance*math.cos(angle);py=y+distance*math.sin(angle)
                if walkable(px,py,radius) and all(math.hypot(px-ox,py-oy)>=radius+rr+.2 for ox,oy,rr in occupied):
                    occupied.append((px,py,radius));return px,py,float(distance)
        navigation_failures.append(identifier);return x,y,None
    placed=[]
    for slot in bpy.data.collections['03_Asset_Placement'].objects:
        key=slot.get('asset_id')
        if key not in library:continue
        slot.instance_type='COLLECTION';slot.instance_collection=library[key]
        # Warcraft facing 0=east. Use inspected axes where known; retain the
        # prior -Y assumption for other unverified families.
        slot.rotation_euler.z+=facing_offset(key)
        slot['status']='candidate' if key in unreviewed else 'independently_reviewed'
        placed.append({'instance':slot.name,'asset':key,'location':list(slot.location),'source':slot.get('source')})
    # The original Goblin Merchant is embedded in the side-shop building model.
    # Our separate actor inherits each shop transform and its measured platform.
    if 'm309' in library and 'bg12' in library:
        anchor=json.loads((OUT/'side_shop_merchant_anchor_v001.json').read_text(encoding='utf-8'))
        if anchor.get('status')!='local_anchor_author_checked_pending_whole_map_review' or sources['bg12'].name!='bg12_r08.blend':raise ValueError('Side-shop platform anchor needs revalidation for this host revision')
        merchants=collection('14_Side_Shop_Merchants')
        for host in bpy.data.collections['03_Asset_Placement'].objects:
            if host.get('asset_id')!='bg12':continue
            ob=bpy.data.objects.new(host.name+'_m309',None);merchants.objects.link(ob);ob.instance_type='COLLECTION';ob.instance_collection=library['m309'];ob.matrix_world=host.matrix_world@Matrix.Translation(Vector(anchor['local_position']));ob['asset_id']='m309';ob['host_instance']=host.name;ob['status']='candidate_platform_anchor_author_checked';ob['source']='m309 asset card: actor on right raised platform of bg12; original game embeds actor in building'
            placed.append({'instance':ob.name,'asset':'m309','location':list(ob.location),'source':ob['source'],'host_instance':host.name,'local_anchor':anchor['local_position'],'contact_evidence':'side_shop_merchant_contact_probe.json'})
    features=json.loads((ROOT/'0_research/map_regions/map_features.json').read_text(encoding='utf-8'))
    camps=collection('10_Neutral_Camps')
    defaults={'J3':'R8O','J4':'RVO','J5':'RFO','J6':'RJO','J7':'RBO','J8':'RHO','K3':'RKO','K4':'R5O','K5':'RGO','K6':'REO','K7':'RCO','K8':'R9O'}
    overrides={}
    for item in args.camp_overrides or []:
        camp_id,combination=item.split('=',1)
        camp=next((c for c in features['camps'] if c['id']==camp_id),None)
        if not camp or combination not in [c['function'] for c in camp['combos']]:raise ValueError({'invalid_original_camp_combination':item})
        overrides[camp_id]=combination
    defaults.update(overrides)
    variant_scale={'nbdk':.65,'ncnk':1.3,'n00S':1.18,'nowe':1.25,'nomg':1.12,'nkol':1.18,'nkot':1.08,'ndtw':1.25,'n0HX':1.12,'nfpu':1.15,'nggr':1.25,'n0LD':.9/1.15}
    camp_report=[]
    for camp in features['camps']:
        combo=next(c for c in camp['combos'] if c['function']==defaults[camp['id']])
        x,y=[v/20 for v in camp['spawn']];units=[]
        for i,unit in enumerate(combo['units']):
            key=unit['card'].split('_')[0]
            if key not in library:continue
            radius=5.5 if key=='m24' else 1.8 if len(combo['units'])>2 else 1.3
            a=math.tau*i/len(combo['units']);px,py=x+radius*math.cos(a),y+radius*math.sin(a)
            footprint=2.5 if key=='m24' else 2.5*variant_scale.get(unit['rawcode'],1) if key=='m26' else 1.2 if key in ['m22','m23','m25'] else .7
            px,py,shift=find_ground(px,py,footprint,f'{camp["id"]}_{i}')
            obj=bpy.data.objects.new(f'{camp["id"]}_{unit["rawcode"]}_{i+1}',None);camps.objects.link(obj);obj.instance_type='COLLECTION';obj.instance_collection=library[key]
            obj.location=(px,py,height(px,py));obj.rotation_euler.z=math.atan2(y-py,x-px)+facing_offset(key);obj.scale=(variant_scale.get(unit['rawcode'],1),)*3
            obj['asset_id']=key;obj['rawcode']=unit['rawcode'];obj['camp']=camp['id'];obj['variant_status']='size_only_colour_equipment_variants_need_review'
            units.append({'object':obj.name,'asset':key,'rawcode':unit['rawcode'],'location':list(obj.location),'navigation_shift_m':shift,'forward_axis':forward_axes.get(key,'-Y_assumed'),'footprint_radius_m':footprint,'variant_scale':variant_scale.get(unit['rawcode'],1)})
        camp_report.append({'camp':camp['id'],'combo':combo['function'],'units':units})
    # Static lane formations near their original first towers, not an invented battle.
    lanes=collection('11_Lane_Creeps')
    lane_report=[]
    for tower in features['towers']:
        if tower['tier']!=1:continue
        sentinel=tower['side']=='sentinel';x,y=[v/20 for v in tower['spawn']]
        inner=next(t for t in features['towers'] if t['side']==tower['side'] and t['lane']==tower['lane'] and t['tier']==2)
        direction=Vector((x-inner['spawn'][0]/20,y-inner['spawn'][1]/20)).normalized()
        occupied.append((x,y,5))
        for i,key in enumerate(['m1','m1','m1','m2','m3'] if sentinel else ['m4','m4','m4','m5','m6']):
            if key not in library:continue
            back=8+i*2.1;side=(i%3-1)*1.2;px=x-direction.x*back-direction.y*side;py=y-direction.y*back+direction.x*side
            px,py,shift=find_ground(px,py,.65,f'{tower["id"]}_lane_{i}')
            obj=bpy.data.objects.new(f'{tower["id"]}_lane_{i}',None);lanes.objects.link(obj);obj.instance_type='COLLECTION';obj.instance_collection=library[key];obj.location=(px,py,height(px,py));obj.rotation_euler.z=math.atan2(direction.y,direction.x)+math.pi/2;obj['asset_id']=key;obj['placement_status']='static_formation_navigation_review_pending'
            lane_report.append({'object':obj.name,'asset':key,'location':list(obj.location),'navigation_shift_m':shift})
    # Ten original hero arrival circles are permanent architectural fixtures.
    circles=collection('12_Arrival_Circles');g=DetailGeometry();g.ring((0,0,.015),1.4,.025,0)
    for j in range(12):
        a=j*math.tau/12;g.box((math.cos(a)*1.2,math.sin(a)*1.2,.012),(.08,.17,.02),0)
    mat=surface('Arrival_runes',(.01,.025,.018),(.08,.22,.12),4,.55,.001);bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Emission Color'].default_value=(.05,.22,.1,1);bs.inputs['Emission Strength'].default_value=.6
    lib=bpy.data.collections.new('LIB_Arrival_Circle');mesh_object('Arrival_circle',g.vertices,g.faces,[mat],g.indices,lib)
    base=json.loads((ROOT/'0_research/base_layout_refs/base_layout_manifest.json').read_text(encoding='utf-8'))
    for row in base['rows']:
        if row['category']!='spawn':continue
        obj=bpy.data.objects.new(row['faction']+'_'+row['instance_id'],None);circles.objects.link(obj);obj.instance_type='COLLECTION';obj.instance_collection=lib;x,y=row['x']/20,row['y']/20;obj.location=(x,y,height(x,y))
    report={'file':dest.name,'status':'DRAFT_NOT_RELEASED' if args.draft else 'assembled_pending_map_review','asset_library_count':len(library),'missing_assets':missing,'unreviewed_assets':unreviewed,'placements':placed,'camps':camp_report,'lane_units':lane_report,'arrival_circles':len(circles.objects),'source_libraries':{k:str(p.relative_to(ROOT)) for k,p in sources.items()},'remaining':['Camps need colour/equipment variant review','Lane formations need navigation check','Whole scene independent QC']}
    bpy.context.scene['production_status']=report['status'];bpy.context.scene['asset_count']=len(library)
    report['navigation_failures']=navigation_failures
    instanced={p['asset'] for p in placed+lane_report}|{u['asset'] for c in camp_report for u in c['units']}
    report['currently_instanced_asset_families']=sorted(instanced)
    report['loaded_but_not_currently_instanced']=sorted(set(library)-instanced)
    report['camp_overrides']=overrides
    report['partial_diagnostic_asset_filter']=sorted(only)
    report['draft_selection_notes']=draft_pins
    report['navigation_method']='Original 1.6 m WPM-derived walk/tree grid, 9-point footprint, height slope and inter-unit clearance; full collision mesh review still required'
    if navigation_failures and not args.draft:raise RuntimeError({'navigation_failures':navigation_failures})
    # Asset collection linking does not carry its studio compositor. Keep a
    # consistent, restrained optical response for emissive objects in the map.
    scene=bpy.context.scene
    if scene.compositing_node_group is None and 'm306' in library:
        nt=bpy.data.node_groups.new('Map_optical_bloom','CompositorNodeTree');scene.compositing_node_group=nt
        nt.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
        layers=nt.nodes.new('CompositorNodeRLayers');glare=nt.nodes.new('CompositorNodeGlare');glare.inputs['Type'].default_value='Fog Glow';glare.inputs['Quality'].default_value='High';glare.inputs['Threshold'].default_value=1.0;glare.inputs['Size'].default_value=.25;glare.inputs['Strength'].default_value=.35
        output=nt.nodes.new('NodeGroupOutput');nt.links.new(layers.outputs['Image'],glare.inputs['Image']);nt.links.new(glare.outputs['Image'],output.inputs['Image'])
        report['optical_bloom']={'threshold':1.0,'strength':.35,'size':.25,'status':'whole_scene_appearance_review_pending'}
    bpy.ops.wm.save_as_mainfile(filepath=str(dest),relative_remap=True)
    (OUT/(dest.stem+'_report.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('placements','camps','lane_units','source_libraries')},ensure_ascii=False),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--environment',default='environment_v005.blend');p.add_argument('--output',required=True);p.add_argument('--draft',action='store_true');p.add_argument('--only-assets',nargs='+');p.add_argument('--camp-overrides',nargs='+',help='Original camp combinations, e.g. K8=RAO');main(p.parse_args(sys.argv[sys.argv.index('--')+1:]))
