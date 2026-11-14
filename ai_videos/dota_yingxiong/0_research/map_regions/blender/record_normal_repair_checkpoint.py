"""Record verified export diagnosis and current continuation state."""
from pathlib import Path
import json,datetime
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
now=datetime.datetime.now().astimezone().isoformat()
path=OUT/'pipeline_comparison.json';p=json.loads(path.read_text(encoding='utf-8'))
p.update(at=now,status='comparisons_complete_quality_still_fails')
p['comparison']['outcome']='bg12 r02 多视图、r03 单视图 wrapper、r04 单视图 official 均未通过；单视图保留较完整结构，但不解决草叶熔化与苍白配色。'
p['official_sampling_profile']={'ss_guidance':7.5,'ss_rescale':.7,'shape_guidance':7.5,'shape_rescale':.5,'texture_guidance':1,'texture_rescale':0,'new_batch_only':True}
p['normal_export_defect']={'cause':'导出节点改变顶点坐标后使 trimesh 法线缓存失效，又将已经重新计算的法线再旋转一次。','verified_assets':{'m300_r14':{'before_median_dot':.3230,'after_median_dot':.99681},'bg12_r04':{'before_median_dot':.20791,'after_median_dot':.99233},'m300_r08_authored':{'before_median_dot':.35441,'after_median_dot':.99158}},'repair':'保留原件，在副本上对识别出的错误法线绕 X 轴旋转 +90°；数值验证后才保存。','scope':'修正表面明暗，不修正原有几何、闭眼、布料破洞、草叶熔化或配色。','new_inspections':'inspect_model.py 自动检测与修正导出副本；未修改共享 ComfyUI 安装。'}
if 'scheduler_stopped_pid' in p:p['scheduler_stopped_pid_historical']=p.pop('scheduler_stopped_pid')
runtime_path=sorted((ROOT.parents[1]/'.audit/adhoc_agents/2026-10-27/dota-local-3d-287').glob('runtime_r*.json'))[-1]
runtime=json.loads(runtime_path.read_text(encoding='utf-8-sig')) if runtime_path.exists() else {}
p['scheduler_resumed_pid']=runtime.get('scheduler_pid',17008)
p['runtime_timeout_repair']={'task_launcher_only':True,'node_timeout_seconds':3600,'failed_request':'bg21:r01','retry':'bg21:r02','bg22_receipt_saved_before_restart':True}
p['mesh_preservation_trial']={'asset':'m1','revision':'r08','status':'independent_review_fail_5_blockers','finding':'Installed nodes_unwrap.py ProcessMesh remesh-on hardcodes resolution=512 after 1024 generation.','trial':'Same reference, seed, 1024 cascade and official sampler; disable remesh, disable fill-holes and retain 3M faces.','raw_glb_sha256_identical_in_r01_r08':'092df0ed7aa96143faab86e8d57affcc9ba8fcd9ac0d5bd7715ecbc0d7a4d2dc','processed_faces':2794043,'conclusion':'Author verified sharper bark and lichen. Independent review still fails: foliage colour and fused shape, floating fragments, torso texture distortion and fused roots. Raw clay retains more detail but contains voxel noise and fragments. No acceptance implied.','new_batch_requests':'Scheduler resumed with preserve mesh profile; m15 existing baseline receipt retained. Prior models unchanged.','reference':'https://github.com/microsoft/TRELLIS.2/issues/92'}
p['ground_fragment_diagnosis']={'verified':{'m5_r03':{'removed_faces':94,'corrected_height_m':.0542565},'m8_r02':{'removed_faces':288,'corrected_height_m':.038521}},'method':'Weld coincident UV-split vertices in analysis; remove disconnected components wholly below a principal body with >95% area and each below-body component <0.5% area. Re-ground from remaining geometry.','new_imports':'inspect_model.py applies this to NPC exports except Wisp; raw GLB retained.','rejected_trial':'m5 r02 analysed UV-split vertices as physical components; rejected and superseded by seam-aware r03.'}
p['high_resolution_remesh_trial']={'asset':'m1','revisions':['r11 preserve','r16 remesh1024'],'raw_sha256_identical':'b751eeaf433fe818c349244430d0ec354c30fe92936de4dec9668a46a5d80dfa','worker_log_verified':'ProcessMesh Remeshing quad DC resolution=1024','result':'r16 independent visual review fail, 8 blockers','topology_report':'characters/近卫_sentinel/m1_Treant/model_3d/remesh_topology_comparison.json','boundary_edges_at_5_decimal_quantization':{'r11':1246583,'r16':0},'nonmanifold_edges_at_5_decimal_quantization':{'r11':1262,'r16':17430},'caution':'Quantized topology statistics are not manifold acceptance. Blender distance-based weld found 2751 boundary edges in r16. No final batch profile change.'}
path.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
path=OUT/'authoring_checkpoint.json';p=json.loads(path.read_text(encoding='utf-8'));current=json.loads((OUT/'current_status.json').read_text(encoding='utf-8'))
p.update(at=now,followup=292,status='in_progress_not_deliverable',acceptance=f"{current['families_with_candidates']}/59 类已有完整候选，{current['accepted_families']}/59 类通过；以 current_status.json 实时扫描为准。")
p['runtime'].update(batch=f"full_models_v1 已恢复，PID {runtime.get('scheduler_pid',17008)}；新请求使用 official 参数、单正视图；活跃资产 {current['active_batch_asset']}。",collectors=[],quality_diagnosis='单视图参数对照均未通过；已验证并修正导出法线多转 90° 的错误。',legacy_repairs='旧候选九项修正与重新检查已结束；均未通过精细外观检查，具体以 legacy_normal_repairs.json 为准。',timeout_repair='仅本任务 launcher 将 TRELLIS2 节点等待上限改为 3600 秒；bg21:r01 的 600 秒超时记录保留，r02 已成功生成。')
p['assets']['m300'].update(authoring='r16：从 r08 精修版修正已验证的法线错误',candidate='r16 fail',remaining='披风错色、闭眼、胡须形状、手部熔化；法线修正不能替代几何修复。')
p['assets']['bg12'].update(candidate='r08 fail：有真实草纤维、独立招牌与石板，但草顶像假发、布幔错色、竹结构熔化。',authoring='r09 作者预览拒绝：重建分层草顶试验过于规整，删除旧布面造成缺口；禁止作为新地图候选。',comparison='r02/r03/r04 单/多视图参数对照均 fail。')
p['assets']['bg23'].update(authoring='r27 增加门环、铆钉、石块边缘变化和雕刻，但探测确认八块布尔石带均为空网格，作者拒绝。r28 直接重建封闭石带与凹刻，透视已查看，黑缝消失；完整检查正在进行。',candidate='r26 独立检查 fail，5 个阻断项；r28 待完整检查',remaining='石带接触、根部自然度、门扇与石材细节须独立检查。r28 八块石带均通过每条边恰好两个邻面的封闭检查；不代表全模型拓扑或外观通过。')
p['assets']['m306'].update(authoring='r22 关闭降噪、提高至 96 采样与 64 透明反弹；全视角检查完成。',candidate='r22 独立审查 pass，阻断项 0；r22 平移实例检查 pass',remaining='非阻断改进包括光丝弯曲、尘粒尺寸与光斑柔化；成片镜头须提高采样或可控降噪。v007 实际地图日光近景已由作者检查，位置、可见性和悬浮接地正常；整图独立检查仍待完成。')
p['assets']['m4'].update(authoring='r17 按当前网格修正牙齿颜色、扩宽下颌；r18 填补 20 个局部肩部边界环。',candidate='r15 fail',remaining='r16 平涂试验拒绝；r18 最大肩部薄片仍存在，尚未转为完整候选；布料融化和毛发轮廓仍需修复。')
p['assets']['bg17'].update(candidate='r02 fail',review='法线修正后仍有叶片与树干熔化。')
p['assets']['bg18'].update(candidate='r02 fail')
p['assets']['bg19']={'candidate':'r02 fail','normal_repair':'已完成，几何仍需重建'}
p['assets']['bg20']={'candidate':'r01 complete','normal_repair':'新检查已自动处理'}
p['assets']['bg21']={'candidate':'r02 complete','prior_failure':'r01 failed at node 21 after 600 seconds','retry':'r02 succeeded using task-only 3600 second timeout'}
p['assets']['bg22']={'candidate':'r01 complete'}
p['assets']['bg25']={'candidate':'r01 fail','remaining':'泉水背部呈切平薄壳，需闭合岩石与水体重建。'}
p['assets']['bg26']={'candidate':'r12 fail，8 个阻断项','authoring':'r08 修正 closure 警告；r09–r12 贯通骨肋、骨爪和横向板缝的补建均未达到外观标准。','remaining':'晶体照明和内部结构不足、铜绿楼梯缺失、骨肋塑料感、塔顶熔化、凸出钢丝状板缝、针状骨爪和截平弯牙。','component_source':'environment_sources/blender_human_base_meshes/skull_provenance.json，官方 LFS SHA256 已核对。'}
p['assets']['m1']={'candidate':'r24 独立检查 fail，5 个阻断项','authoring':'r25 重建深褐树皮着色、缩小地衣斑块、恢复局部湿苔、统一暗绿叶色并拉高枝冠；作者预览正在渲染。','remaining':'树冠伞盖形状、枝条连接、自然叶片、地衣苔藓分布和树皮颜色。','diagnosis':'r11/r16 原始 GLB 相同；1024 重建减少开口但非流形未清零。r22 已有曲线逐点半径渐变，检查导出已补充半径范围；这不证明外观合格。'}
p['assets']['m5']={'candidate':'r03 fail；接地已修复，材质与几何仍不合格','authoring':'r05 眼光移入眼部、皮肤遮罩软化、金色限定腰饰；脸部已查看，胡须仍像笔刷，眼光覆盖闭合眼皮，未转完整候选。','remaining':'眼部几何、自然胡须、金边准确覆盖、骨链与斗篷、手部。'}
p['assets']['m7']={'candidate':'r01 fail','authoring':'r02 作者预览拒绝：紫岩改善，但晶刺过规整且有悬浮碎片，脸光像贴上去的波浪线。'}
p['assets']['m8']={'candidate':'r01 fail','authoring':'r02 作者检查接地修复有效；仍未完整检查，毛发、配色、蜡烛与五官未修。'}
p['assets']['m16']={'candidate':'r05 fail，8 个阻断项；r01 fail 3 项','authoring':'r02 材质硬边、r03 切开面颊、r04 牙变成楔形均作者拒绝。r05 保留原拓扑局部转向缩短长牙，暖化皮肤和磨损三角纹；独立审稿未通过。','remaining':'其他獠牙仍褐色、侧牙朝向、角上皮肤斑点、熔化兽皮、右脸封闭、旧纹样残迹、白毛状伤疤、蜡感皮肤。'}
p['assets']['m21']={'candidate':'r03 独立检查 fail，12 个阻断项','authoring':'r04–r06 的分离皮篷仍有孔洞与材质接缝；r07–r08 连续缝合皮篷消除了孔洞，但衣身贴合与头部比例不合格；r09 抬头试验拉伸了颈部，作者拒绝。已回看 r01 与 r03，下一步回到原始头部基准处理旧皮篷交界，不采用 r09。','remaining':'驼背体型、头部过小、额头错误皮革遮罩、融化毛发、披篷与木杆、悬浮残片。'}
p['runtime']['manual_revision_files']={}
manifest=json.loads((OUT/'asset_manifest.json').read_text(encoding='utf-8'))
for asset_id,revision in [('m1','r25'),('bg23','r30'),('m21','r11')]:
 a=next(a for a in manifest['assets'] if a['id']==asset_id);folder=ROOT/a['model_directory']/revision;review=folder/'inspection/independent_review.json'
 p['runtime']['manual_revision_files'][asset_id+':'+revision]={'authoring_saved':(folder/'authoring.blend').exists(),'author_preview_saved':(folder/'author_preview.png').exists() or (folder/'perspective_preview.png').exists(),'inspection_complete':(folder/'inspection/inspection.json').exists(),'review':json.loads(review.read_text(encoding='utf-8')).get('verdict') if review.exists() else 'pending'}
p['map']=f"{current['latest_assembly']} 仍是未验收工作文件。v016 的五视角环境独立检查 fail，10 个阻断项；河岸形状、水体、道路、地表重复、天灾绿色树林、稀疏林地、外边界及基地疑似穿插须继续修正。v017 已保存全部 59 类候选，仍在渲染。v024 草地距离切换改成渐疏，基地和河道预览均已查看。v025 移除天灾树种叶面、恢复扫描枯枝，并按与外围一致的地理规则补齐天灾侧枯树林；候选待查看，尚未换入整图。"
if current['batch_status']=='candidates_generated_pending_review':
 p['runtime']['batch']='59/59 类候选生成完成，队列为空；本任务 Comfy 服务与模型 worker 已停止释放内存，仍须单体修复与整图验收。'
 p['runtime']['task_comfy_server']='stopped_after_empty_queue_and_all_candidates_saved'
p['assets']['bg23'].update(authoring='r28 独立 fail 4；r29 补上吊钩到球架的金属连接、隐藏硬边土圈并降低根须，但根截面被压扁，未转完整候选。r30 恢复原始根截面，沿中心线转向，浅化树皮；作者已查看根部和透视，完整检查已完成，独立审稿待结果。',candidate='r30 待独立结果；r28 fail 4',remaining='根须管状感、入口与水晶龛接触、吊钩支撑，须以当前完整检查为准。')
p['assets']['m1'].update(candidate='r25 独立 fail 8，较 r24 fail 5 回退；工作图已按哈希固定 r24。',authoring='r25 作者已查看正面与冠部；整体归一化使体躯变细，冠形和叶面高光仍不合格。',remaining='体躯深度、粗壮比例、枝系连接与自然树冠、灰褐树皮和地衣苔藓分布。')
p['assets']['m21'].update(authoring='r10 从 r03 修正额头皮革遮罩，白毛头部恢复。r11 烘焙原材质颜色并以 4 mm 体素封闭表面：开口边与非流形边均为 0，作者已查看全身与脸部；嘴部被磨钝、披篷发蜡，尚未转完整候选。',remaining='头部比例、嘴与牙、颈部薄片、披篷材质和木杆、体态；拓扑封闭不代表外观通过。')
p['map']=f"{current['latest_assembly']} 为未验收工作文件。v018 已装入 59 类候选，95 个建筑/营地等布置、30 个线兵实例，抽样导航失败 0；五视角环境独立 fail 9。v026 已查看水面与全景，限制水面到原始水域单元并增加真实波纹；抽样多余湿点从 90 减至 41，仍缺 37 个源湿点。v027 为河岸曲线和碎石修整试验，正在渲染，尚未换入整图。"
p['runtime']['latest_water_audit']='environment_v026_water_footprint_audit.json'
p['runtime']['rock_diagnosis']='射线定位到三个缩小的直立岩壁实例；连通片最低点均入土约 6–8 cm，并非悬空。v027 改用低矮碎石，待作者看图。'
p['runtime']['generation_inspection_overlap']={'enabled':runtime.get('prefetch_next_gpu_during_cpu_inspection',False),'evidence':runtime.get('prefetch_overlap_evidence',[]),'scope':'One next GPU request overlaps current CPU inspection. Existing receipts are reused; current m301 prompt ID remained unchanged through restart.'}
p['assets']['bg23'].update(authoring='r33 作者已查看弯钩和根部：弯钩合为连续铸件并后移，最小球体间隙 0.07255 m；根须提亮并加局部土包。完整检查对土包中心重合点做局部焊接，原 authoring.blend 保留。',candidate='r32 独立 fail 3；r33 完整渲染/独立检查以实时文件为准。',remaining='根部自然度、金属连接与正式镜面外观；几何间隙不代表外观通过。')
p['assets']['m26']={'candidate':'r01 独立 fail 3；r02–r05 为作者修订试验，未验收。','authoring':'纠正 X 轴 5 m 体长，保留 +X 朝向校准。r03/r04 局部封孔后仍有 76182 条边界边；r05 按实际背部渲染射线和连通色块清理四处白线，候选图待查看。','remaining':'其他线状残片、头部贴图与眼睛、大裂口、不同方向检查；小型变体缩放已写入装配脚本，尚待新整图核对。'}
p['map']=f"{current['latest_assembly']} 为未验收工作文件，当前装配环境以 draft_refresh_state.json 为准。v018 使用 v025，59 类候选、95 个布置、30 个线兵实例，抽样导航失败 0，环境独立 fail 9。v030 三张作者预览均已查看；恢复全部 885 个源湿点（缺失 0，额外 38），调整源地块泥土层次并纠正 498 棵树的生境类型。仍有方折岸线和过平地表，尚未整图独立通过。"
p['runtime']['latest_water_audit']='environment_v030_water_footprint_audit.json'
p['runtime']['rejected_environment_trial']='v028 缺失源湿点 161 个，禁止合入；v029 恢复源湿点约束，v030 继承其几何并已核对实际水面覆盖。'
p['runtime']['rock_diagnosis']='原低机位薄片来自缩小的直立岩壁，最低点入土 6–8 cm；v027 起替换为低矮碎石，作者确认外观改善。'
p['assets']['bg23'].update(candidate='r33 独立 fail 4；r34 完整检查进行中。',authoring='r34 按钩管真实末端放置端珠，对接头做 3 mm 体素融合；恢复被旧高度变形压入地下的主根和交织细根，隐藏四角爪状补根。三张作者预览已查看。',remaining='根网自然度、接头和端珠外观；其他石带、材质与植被改进仍未完成。')
p['assets']['m26'].update(candidate='r06 独立 fail 7；5 m 尺寸已修正并用于工作图资产库。',authoring='r07 非金属材质对照已查看，灰白反射减轻但几何与纹理仍失败；r08 的 2 mm 壳层/3 mm 重建出现筛孔状表面，作者拒绝，尽管边界和非流形边为 0。r09 改为 12 mm 向内壳层、保留 3 mm 网格和无整体平滑，等待看图。',remaining='孔洞和细丝、眼睛及嘴部结构、口腔暗红色、象牙骨板分色、皮肤贴图清晰度。')
p['assets']['m303']={'candidate':'r01 独立 fail 4；仍是整图所用工作候选。','authoring':'r02 通用眼睑环重建出现 UV 条纹和外露眼白，作者拒绝。r03 为非金属材质对照，已查看；r04 改用本地 MPFB 真实眼眶拓扑，烘焙皮肤颜色转移，正在制作。','remaining':'自然眼球眼睑、皮肤边界、黑短发胡茬、友善表情及原网格孔洞。'}
p['map']=f"{current['latest_assembly']} 为未验收工作文件。v019 已使用环境 v031，59 类资产库、95 个布置、30 个线兵实例，抽样导航失败 0；全景和近卫林地机位作者已查看，另外三机位与独立检查进行中。实际摆放 51 类，7 类未选野怪组合另行切换，m309 尚无清单对应摆放。v031 水域缺失源湿点 0、额外 38；同机位关闭镜面反射对照证实原大范围泛白来自反射，现已分开干土、湿岸与铺装反射。仍有方折岸线、硬地图边界和过平地形。"
p['runtime']['latest_water_audit']='environment_v031_water_footprint_audit.json'
p['runtime']['asset_coverage']='assembly_working_v019_asset_coverage.json：59 类载入不等于全部可见，当前 51 类实际实例化。'
p['runtime']['camp_diagnostic']='camp_K8_RAO_v001.blend：通过同一 assemble_map.py 路径加载 m26 r06，一大两小、+X 朝向和小型 .9/1.15 缩放；抽样导航失败 0，小型灰色材质仅作者试验，待查看画面。'
p['runtime']['organic_pbr_diagnosis']='m303/m26 贴图金属通道中位数分别约 0.263/0.149；仅做两个资产的非金属材质对照，未批量改写其他模型。'
p['assets']['bg23'].update(candidate='r34 独立 fail 3，工作图 v020 使用该候选。',authoring='r35 三张作者预览已查看：石材真实分缝加深、屋顶同青铜材质浮雕改善；粗根起点暴露截头，未验收。r36 将粗根起点后退入墙基并连接支根，作者渲染进行中。',remaining='根须自然度、石材近景和青铜浮雕仍需独立复查；其余细化项保留。')
p['assets']['m26'].update(candidate='r06 独立 fail 7；r09/r10 尚未形成新的完整检查候选。',authoring='r09 12 mm 壳层/3 mm 重建的头部、背部、全身已查看，比 r08 筛孔面改善，但仍有凹坑和模糊纹理。r10 已按侧面实测眼位加金色竖瞳、眼睑及口腔；两张作者图已查看，口腔过亮像光滑红团，需要内收并降低反光。',remaining='眼睑融合、口腔形状、凹坑与角质分色；新几何不得以零边界边代替视觉验收。')
p['assets']['m303'].update(candidate='r01 独立 fail 4；r07 完整多角度检查与独立审查运行中。',authoring='r04 MPFB 眼眶与皮肤颜色转移、r05 头发局部反射和视线修正已查看。r06 未焊接 UV 重合点就补了 156764 个环，产生多余补面，作者拒绝。r07 从 r05 重新焊接 1 微米内重合点，顶点 2210507→1410576，边界边 1433098→27578，再只补 189 个真实小环；三张作者图已查看。',remaining='额头和下巴少数黑点、皮肤眼眶真实度、自然表情、独立全角度复查。')
p['map']='assembly_working_v020.blend 已保存，环境 v031，59 类资产库、52 类实际实例化，增加两处 m309 地精商人，97 个布置、30 个线兵实例、抽样导航失败 0。第一次整图渲染 OOM；正在保留原装配文件、88 GiB 空闲门槛、每机位独立进程重跑。v019 的五图作者检查与环境独立审查已完成：fail 6，主要为地图矩形边界、缺乏崖壁体积、方折河岸和水池、地表材质及不成形道路。v020 尚无新的独立通过结论。'
p['runtime']['asset_coverage']='v020 装配报告确认 52 类实际实例化；剩余 7 类为不同原始野怪组合的替代项。m309 依据资产卡属于 bg12 右侧木平台，已实测局部落点并查看整体、正面、脚部三视图。'
p['runtime']['camp_diagnostic']='K8 RAO 一大两小，导航抽样 0 失败；原斜视图被树木挡住，补俯视后确认无互相重叠、大小与灰色变体可区分。模型和完整足部碰撞仍未验收。'
p['runtime']['metric_terrain_trial']='v032 数组已准备，等待整图内存锁后另存并渲染。统一为 20 游戏单位/米：悬崖层 6.4 m，主水位 -10.88 m；885 源湿点缺失 0。保留原图 (117,17) 唯一高水位凹点 -4.48 m；其周围为干地，原文件附近存储水位也一致。添加 488 个与原水域相连的水面细格，未替换工作环境 v031。'
p['assets']['bg23'].update(candidate='r36 独立 fail 4；石材分缝与青铜浮雕改善。',authoring='r37 正在渲染：主根起点从 .525 降为 .105 父空间米，根截面缩小，直接恢复扫描树皮贴图；土堆移到外侧可见根段，钩端上抬并重测间隙。',remaining='自然根形、树皮与土壤接地、钩端投影与托座连接；其他细化项保留。')
p['assets']['m26'].update(authoring='r11 头部、背部、全身三图已查看。眼位与口腔内收改善，皮肤分色和轻微平滑已完成；背棘和表面凹孔仍不真实，尚未转完整候选。')
p['assets']['m303'].update(candidate='r07 独立 fail 4。',authoring='r07 射线证实额头、下巴、鼻旁和领口黑点为真实孔洞；几何有 49812 条三面共边、6249 条四面共边。r08 MeshFix 小孔试验补 10999 环，但作者图出现大量重叠补面，明确拒绝。r09 正在主连通分量上做填孔与自交清理，尚未验证。',remaining='干净无重叠的面部表面、头发帽状轮廓、眼睛皮肤真实度、服装颜色。')
p['map']='assembly_working_v020.blend 使用环境 v031，59 类载入、52 类实际实例化，97 个布置、30 个线兵实例、抽样导航失败 0。分机位新进程与 88 GiB 空闲门槛已成功恢复全景和近卫林地图，作者已查看；覆盖审计已落盘。v019 环境独立 fail 6 的问题仍未关闭，v020 不是成品。'
p['runtime']['metric_terrain_trial']='v032 已保存并查看全景，源 885 湿点缺失 0、额外 41、3 个水下粗格没有水面。v033 已软化岸线并修正三条沿用旧水位的湿岸着色分支，全景和河岸近景均已查看；崖壁过平、石块串列和边界仍未合格。新版本尚未并入整图。'
p['runtime']['manual_revision_files']={}
for asset_id,revision in [('m1','r25'),('bg23','r37'),('m21','r11'),('m26','r11'),('m303','r09')]:
 a=next(a for a in manifest['assets'] if a['id']==asset_id);folder=ROOT/a['model_directory']/revision;review=folder/'inspection/independent_review.json'
 p['runtime']['manual_revision_files'][asset_id+':'+revision]={'authoring_saved':(folder/'authoring.blend').exists(),'author_preview_saved':(folder/'author_preview.png').exists() or (folder/'perspective_preview.png').exists(),'inspection_complete':(folder/'inspection/inspection.json').exists(),'review':json.loads(review.read_text(encoding='utf-8')).get('verdict') if review.exists() else 'pending'}
path.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
print('Recorded verified normal defect and continuation checkpoint')
