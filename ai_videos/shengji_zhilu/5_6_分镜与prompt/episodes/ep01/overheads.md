# ep01 镜头平面图（overhead）索引

> 生成物：`python tools/shot_overhead.py --all ai_videos/shengji_zhilu/5_6_分镜与prompt/episodes/ep01`。改走位 ＝ 改各镜 `planning/overhead.toml` 重跑。
> 这一层只定「镜头与人各自在哪、往哪走、几秒到」；动作细节与形状在 shot blend 层。**这里点头之后才做 shot blend。**
> 每镜两张：`_overhead.png` 给人审，`_overhead_ref.png` 给 Seedance。**previz 免** 的镜不做 shot blend，`_ref` 图直接当运动与几何参考上传；**要** 的镜照旧渲 previz MP4（判据见 `tools/shot_overhead.py` `previz_triggers`）。

| 镜 | 状态 | 审阅图 | Seedance 图 | previz |
|---|---|---|---|---|
| shot01 | ✅ | [shot01_overhead.png](shots/shot01/planning/shot01_overhead.png) | [shot01_overhead_ref.png](shots/shot01/planning/shot01_overhead_ref.png) | **要**：机位连续移动 14m > 12m |
| shot02 | ✅ | [shot02_overhead.png](shots/shot02/planning/shot02_overhead.png) | [shot02_overhead_ref.png](shots/shot02/planning/shot02_overhead_ref.png) | **要**：同时走动 4 人 ≥ 3；肢体接触 3 对 ≥ 2；人与怪攻防接触 c1_Aaron×m7_Wolf、c2_Duke×m7_Wolf；护人格挡 1 段；反应窗 3 段 |
| shot03 | ✅ | [shot03_overhead.png](shots/shot03/planning/shot03_overhead.png) | [shot03_overhead_ref.png](shots/shot03/planning/shot03_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot04 | ✅ | [shot04_overhead.png](shots/shot04/planning/shot04_overhead.png) | [shot04_overhead_ref.png](shots/shot04/planning/shot04_overhead_ref.png) | **要**：镜内硬切 5 段 ≥ 4 |
| shot05 | ✅ | [shot05_overhead.png](shots/shot05/planning/shot05_overhead.png) | [shot05_overhead_ref.png](shots/shot05/planning/shot05_overhead_ref.png) | **要**：同时走动 5 人 ≥ 3；肢体接触 2 对 ≥ 2；人与怪攻防接触 c1_Aaron×m7_Wolf、c2_Duke×m7_Wolf；护人格挡 1 段 |
| shot06 | ✅ | [shot06_overhead.png](shots/shot06/planning/shot06_overhead.png) | [shot06_overhead_ref.png](shots/shot06/planning/shot06_overhead_ref.png) | **要**：机位连续移动 14m > 12m；同时走动 3 人 ≥ 3 |
| shot07 | ✅ | [shot07_overhead.png](shots/shot07/planning/shot07_overhead.png) | [shot07_overhead_ref.png](shots/shot07/planning/shot07_overhead_ref.png) | **要**：镜内硬切 7 段 ≥ 4 |
| shot08 | ⚠ 1 | [shot08_overhead.png](shots/shot08/planning/shot08_overhead.png) | [shot08_overhead_ref.png](shots/shot08/planning/shot08_overhead_ref.png) | **要**：镜内硬切 7 段 ≥ 4；肢体接触 2 对 ≥ 2 |
| shot09 | ✅ | [shot09_overhead.png](shots/shot09/planning/shot09_overhead.png) | [shot09_overhead_ref.png](shots/shot09/planning/shot09_overhead_ref.png) | **要**：同时走动 3 人 ≥ 3；肢体接触 2 对 ≥ 2；人与怪攻防接触 c2_Duke×m1_Kobold |
| shot10 | ✅ | [shot10_overhead.png](shots/shot10/planning/shot10_overhead.png) | [shot10_overhead_ref.png](shots/shot10/planning/shot10_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot11 | ✅ | [shot11_overhead.png](shots/shot11/planning/shot11_overhead.png) | [shot11_overhead_ref.png](shots/shot11/planning/shot11_overhead_ref.png) | **要**：盾墙挡一群、盾后施法、侧面鼠洞偷袭、锤被拖走、镜内四次硬切——判据只数到机位与走动，漏了多人肢体接触与物件交接；手动要 previz |
| shot12 | ✅ | [shot12_overhead.png](shots/shot12/planning/shot12_overhead.png) | [shot12_overhead_ref.png](shots/shot12/planning/shot12_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot13 | ✅ | [shot13_overhead.png](shots/shot13/planning/shot13_overhead.png) | [shot13_overhead_ref.png](shots/shot13/planning/shot13_overhead_ref.png) | **要**：镜内硬切 6 段 ≥ 4 |
| shot14 | ✅ | [shot14_overhead.png](shots/shot14/planning/shot14_overhead.png) | [shot14_overhead_ref.png](shots/shot14/planning/shot14_overhead_ref.png) | **要**：机位连续移动 13m > 12m |
| shot15 | ✅ | [shot15_overhead.png](shots/shot15/planning/shot15_overhead.png) | [shot15_overhead_ref.png](shots/shot15/planning/shot15_overhead_ref.png) | **要**：同时走动 4 人 ≥ 3 |
| shot16 | ✅ | [shot16_overhead.png](shots/shot16/planning/shot16_overhead.png) | [shot16_overhead_ref.png](shots/shot16/planning/shot16_overhead_ref.png) | **要**：同时走动 3 人 ≥ 3；人与怪攻防接触 c1_Aaron×m1_Kobold |
| shot17 | ✅ | [shot17_overhead.png](shots/shot17/planning/shot17_overhead.png) | [shot17_overhead_ref.png](shots/shot17/planning/shot17_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot18 | ✅ | [shot18_overhead.png](shots/shot18/planning/shot18_overhead.png) | [shot18_overhead_ref.png](shots/shot18/planning/shot18_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot19 | ✅ | [shot19_overhead.png](shots/shot19/planning/shot19_overhead.png) | [shot19_overhead_ref.png](shots/shot19/planning/shot19_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot20 | ✅ | [shot20_overhead.png](shots/shot20/planning/shot20_overhead.png) | [shot20_overhead_ref.png](shots/shot20/planning/shot20_overhead_ref.png) | **要**：同时走动 3 人 ≥ 3 |
| shot21 | ✅ | [shot21_overhead.png](shots/shot21/planning/shot21_overhead.png) | [shot21_overhead_ref.png](shots/shot21/planning/shot21_overhead_ref.png) | **要**：反应窗 2 段 |
| shot22 | ✅ | [shot22_overhead.png](shots/shot22/planning/shot22_overhead.png) | [shot22_overhead_ref.png](shots/shot22/planning/shot22_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot23 | ✅ | [shot23_overhead.png](shots/shot23/planning/shot23_overhead.png) | [shot23_overhead_ref.png](shots/shot23/planning/shot23_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot24 | ✅ | [shot24_overhead.png](shots/shot24/planning/shot24_overhead.png) | [shot24_overhead_ref.png](shots/shot24/planning/shot24_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot25 | ✅ | [shot25_overhead.png](shots/shot25/planning/shot25_overhead.png) | [shot25_overhead_ref.png](shots/shot25/planning/shot25_overhead_ref.png) | **要**：机位连续移动 13m > 12m |
