"""Independent static-asset review through the shared qc_review process launcher."""
import argparse,datetime,json,sys,tempfile,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
REPO=ROOT.parents[1]
sys.path.insert(0,str(REPO/'tools'))
import qc_review

def main(args):
    manifest=json.loads((next(ROOT.glob('2_*'))/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'))
    asset=next(a for a in manifest['assets'] if a['id']==args.asset)
    inspection=ROOT/asset['model_directory']/args.revision/'inspection'
    refs=[ROOT/v['path'] for v in asset['views'].values()] or [ROOT/asset['anchor']['path']]
    renders=[inspection/(v+'.png') for v in ['south','east','north','west','perspective']]
    report=json.loads((inspection/'inspection.json').read_text(encoding='utf-8'))
    supplemental=[inspection/name for name in report.get('supplemental_views',[])]
    renders.extend(supplemental)
    blend=inspection/f'{args.asset}_{args.revision}.blend'
    blend_hash=hashlib.sha256(blend.read_bytes()).hexdigest()
    card=(ROOT/asset['card']['path']).read_text(encoding='utf-8')
    prompt=f'''你是独立的三维资产质检员。任务：从已有人物/建筑设计图制作精细、真实、可从任意方向拍摄的静态 Blender 模型，用于完整 DotA 6.83d 电影地图。英雄、绑定、动画不在范围内。
先逐张看图。前 {len(refs)} 张是已确定的设计参考；后五张依次为候选模型南、东、北、西和透视渲染。不要把参考图误当模型。
检查 1) 轮廓、物种、服装/建筑识别特征是否一致；2) 真实三维厚度、背面合理性、无严重熔化、断裂、悬浮零件、复制正脸或正门；3) 材质真实且没有明显投影错误；4) 静态姿态、脚/地基接地；5) 当前可用于地图中远景、场景中景还是需要返工，具体哪些距离不适用。以用户“精细、越逼真越好”为目标，不用“只是占位”放宽标准。有限渲染无法证明的拓扑质量应明确未验证。
只输出一个 JSON 对象，包含 verdict (pass/fail), suitable_use, blockers (具体可见缺陷列表), refinements (非阻断改进列表), evidence (逐图依据)。不要修改文件或写代码。材质名不是着色器行为的证据（例如名字含 unlit 不代表实际使用自发光），基础网格面数也不包含修改器和实例；不能据此断言“没有真实几何”或“不会受光照”。核对提供的实际节点和修改器数据，并把图像无法证明的结构问题记为未验证。仍须明确报告可见缺陷，不因程序声明而放宽外观标准。
模型机器数据：{json.dumps(report,ensure_ascii=False)}
资产卡：\n{card[:18000]}'''
    if supplemental:prompt+='\nAfter the five standard candidate views, additional close-up evidence is supplied: '+', '.join(p.name for p in supplemental)+'. Inspect these as supplemental candidate renders, not design references.'
    if any(p.name=='hook_matte_clearance_control.png' for p in supplemental):prompt+='\nhook_matte_clearance_control.png 是同一几何和机位的材质诊断对照，仅把最高银球临时换成中性漫反射；正式模型仍用镜面银材质。结合机器数据中的三角面到球体的实际最小距离，区分真实穿插、二维投影重叠与邻近金属的反射。对照不代表正式材质验收；任何实际可见接头、外形和材质问题仍须照常报告。'
    audit=REPO/'.audit/adhoc_agents'/datetime.date.today().isoformat()/'model_3d_review'/f'{args.asset}_{args.revision}'
    audit.mkdir(parents=True,exist_ok=True)
    evidence=[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in refs+renders]
    (audit/'request.json').write_text(json.dumps({'prompt':prompt,'images':evidence,'source_artifact_sha256':report['sha256'],'blend_sha256':blend_hash},ensure_ascii=False,indent=2),encoding='utf-8')
    errors=[]
    for who in qc_review.pick('auto'):
        try:
            with tempfile.TemporaryDirectory(prefix='dota_static_review_') as temp:
                raw=qc_review.run_reviewer(who,prompt,refs+renders,Path(temp),600)
            (audit/(who+'_response.txt')).write_text(raw,encoding='utf-8')
            start,end=raw.find('{'),raw.rfind('}')
            result=json.loads(raw[start:end+1])
            if result.get('verdict') not in ('pass','fail'):raise ValueError('No valid verdict')
            result.update(reviewer=who,source_artifact_sha256=report['sha256'],blend_sha256=blend_hash,evidence_files=evidence,prior_errors=errors)
            (inspection/'independent_review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
            print(json.dumps(result,ensure_ascii=False),flush=True);return
        except Exception as exc:errors.append({'reviewer':who,'error':str(exc)})
    (inspection/'independent_review.json').write_text(json.dumps({'verdict':'not_reviewed','errors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
    print('NOT_REVIEWED',errors,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('asset');p.add_argument('--revision',required=True);main(p.parse_args())
