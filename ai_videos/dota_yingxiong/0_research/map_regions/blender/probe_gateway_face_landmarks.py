"""Map visible eye and mouth landmarks to the actual merchant surface."""
from pathlib import Path
import bpy,json,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m303_Gateway_Relics/model_3d'));bpy.ops.wm.open_mainfile(filepath=str(folder/'r01/inspection/m303_r01.blend'));ob=bpy.data.objects['geometry_0'];inv=ob.matrix_world.inverted();rows=[]
for label,px,py in [('left_eye',370,429),('right_eye',563,425),('left_outer',325,426),('left_inner',410,426),('right_inner',527,425),('right_outer',607,425),('mouth_left',370,610),('mouth_right',591,610),('mouth_center',481,610),('front_hairline',480,190),('left_temple',270,320),('right_temple',698,320)]:
 origin=Vector(((px-500)*.38/1000,-2,1.70+(500-py)*.38/1000));hit,p,n,face=ob.ray_cast(inv@origin,(inv.to_3x3()@Vector((0,1,0))).normalized());rows.append({'label':label,'pixel':[px,py],'hit':hit,'point':list(ob.matrix_world@p) if hit else None,'normal':list((inv.transposed().to_3x3()@n).normalized()) if hit else None,'face':face})
(folder/'face_diagnosis_r01/landmarks.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows),flush=True)
