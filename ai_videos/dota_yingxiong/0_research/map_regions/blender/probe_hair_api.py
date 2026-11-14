import bpy,json
print('CURVE_COLLECTIONS',[x for x in dir(bpy.data) if 'curve' in x],flush=True)
data=bpy.data.hair_curves.new('Task_hair_api_probe')
print('CURVE_FUNCTIONS',list(data.bl_rna.functions.keys()),flush=True)
print('CURVE_PROPERTIES',list(data.bl_rna.properties.keys()),flush=True)
for name in ['add_curves','set_types','resize_curves']:
 function=getattr(data,name,None)
 if function:print(name,function.__doc__,flush=True)
data.add_curves([4,4]);print('ATTRIBUTES',[(a.name,a.data_type,a.domain) for a in data.attributes],flush=True)
print('CURVES',len(data.curves),'POINTS',len(data.points),flush=True)
