# ep02 镜头平面图（overhead）索引

> 生成物：`python tools/shot_overhead.py --all ai_videos/shengji_zhilu/5_6_分镜与prompt/episodes/ep02`。改走位 ＝ 改各镜 `planning/overhead.toml` 重跑。
> 这一层只定「镜头与人各自在哪、往哪走、几秒到」；动作细节与形状在 shot blend 层。**这里点头之后才做 shot blend。**
> 每镜两张：`_overhead.png` 给人审，`_overhead_ref.png` 给 Seedance。**previz 免** 的镜不做 shot blend，`_ref` 图直接当运动与几何参考上传；**要** 的镜照旧渲 previz MP4（判据见 `tools/shot_overhead.py` `previz_triggers`）。

| 镜 | 状态 | 审阅图 | Seedance 图 | previz |
|---|---|---|---|---|
| shot01 | ✅ | [shot01_overhead.png](shots/shot01/planning/shot01_overhead.png) | [shot01_overhead_ref.png](shots/shot01/planning/shot01_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot02 | ✅ | [shot02_overhead.png](shots/shot02/planning/shot02_overhead.png) | [shot02_overhead_ref.png](shots/shot02/planning/shot02_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot03 | ✅ | [shot03_overhead.png](shots/shot03/planning/shot03_overhead.png) | [shot03_overhead_ref.png](shots/shot03/planning/shot03_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot04 | ✅ | [shot04_overhead.png](shots/shot04/planning/shot04_overhead.png) | [shot04_overhead_ref.png](shots/shot04/planning/shot04_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot05 | ✅ | [shot05_overhead.png](shots/shot05/planning/shot05_overhead.png) | [shot05_overhead_ref.png](shots/shot05/planning/shot05_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot06 | ✅ | [shot06_overhead.png](shots/shot06/planning/shot06_overhead.png) | [shot06_overhead_ref.png](shots/shot06/planning/shot06_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot07 | ✅ | [shot07_overhead.png](shots/shot07/planning/shot07_overhead.png) | [shot07_overhead_ref.png](shots/shot07/planning/shot07_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot08 | ✅ | [shot08_overhead.png](shots/shot08/planning/shot08_overhead.png) | [shot08_overhead_ref.png](shots/shot08/planning/shot08_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot09 | ✅ | [shot09_overhead.png](shots/shot09/planning/shot09_overhead.png) | [shot09_overhead_ref.png](shots/shot09/planning/shot09_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot10 | ✅ | [shot10_overhead.png](shots/shot10/planning/shot10_overhead.png) | [shot10_overhead_ref.png](shots/shot10/planning/shot10_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot11 | ✅ | [shot11_overhead.png](shots/shot11/planning/shot11_overhead.png) | [shot11_overhead_ref.png](shots/shot11/planning/shot11_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot12 | ✅ | [shot12_overhead.png](shots/shot12/planning/shot12_overhead.png) | [shot12_overhead_ref.png](shots/shot12/planning/shot12_overhead_ref.png) | 免：自动判定的「同时走动 3 人」是 14.2s 切点三人一齐换位（跳过跑上坡那段时间）算出来的，不是同时在走：切点两侧同时走的最多 2 人（0–6.3s 两人沿岸走来、汤米·乔站着刷靴子；14.2–14.7s 汤米·乔冲进门、两人刚上坡站住，14.75s 起两人才走）；三段、机位连续移动 11.3 m、无接触，平面图交代得清 |
| shot13 | ✅ | [shot13_overhead.png](shots/shot13/planning/shot13_overhead.png) | [shot13_overhead_ref.png](shots/shot13/planning/shot13_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot14 | ✅ | [shot14_overhead.png](shots/shot14/planning/shot14_overhead.png) | [shot14_overhead_ref.png](shots/shot14/planning/shot14_overhead_ref.png) | **要**：同时走动 3 人 ≥ 3；护人格挡 1 段 |
| shot15 | ✅ | [shot15_overhead.png](shots/shot15/planning/shot15_overhead.png) | [shot15_overhead_ref.png](shots/shot15/planning/shot15_overhead_ref.png) | **要**：同时走动 3 人 ≥ 3 |
| shot16 | ✅ | [shot16_overhead.png](shots/shot16/planning/shot16_overhead.png) | [shot16_overhead_ref.png](shots/shot16/planning/shot16_overhead_ref.png) | **要**：人与怪攻防接触 c2_Duke×m1_Kobold |
| shot17 | ✅ | [shot17_overhead.png](shots/shot17/planning/shot17_overhead.png) | [shot17_overhead_ref.png](shots/shot17/planning/shot17_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot18 | ✅ | [shot18_overhead.png](shots/shot18/planning/shot18_overhead.png) | [shot18_overhead_ref.png](shots/shot18/planning/shot18_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot19 | ✅ | [shot19_overhead.png](shots/shot19/planning/shot19_overhead.png) | [shot19_overhead_ref.png](shots/shot19/planning/shot19_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot20 | ✅ | [shot20_overhead.png](shots/shot20/planning/shot20_overhead.png) | [shot20_overhead_ref.png](shots/shot20/planning/shot20_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot21 | ✅ | [shot21_overhead.png](shots/shot21/planning/shot21_overhead.png) | [shot21_overhead_ref.png](shots/shot21/planning/shot21_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot22 | ✅ | [shot22_overhead.png](shots/shot22/planning/shot22_overhead.png) | [shot22_overhead_ref.png](shots/shot22/planning/shot22_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot23 | ✅ | [shot23_overhead.png](shots/shot23/planning/shot23_overhead.png) | [shot23_overhead_ref.png](shots/shot23/planning/shot23_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot24 | ✅ | [shot24_overhead.png](shots/shot24/planning/shot24_overhead.png) | [shot24_overhead_ref.png](shots/shot24/planning/shot24_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot25 | ✅ | [shot25_overhead.png](shots/shot25/planning/shot25_overhead.png) | [shot25_overhead_ref.png](shots/shot25/planning/shot25_overhead_ref.png) | **要**：同时走动 6 人 ≥ 3 |
| shot26 | ✅ | [shot26_overhead.png](shots/shot26/planning/shot26_overhead.png) | [shot26_overhead_ref.png](shots/shot26/planning/shot26_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot27 | ✅ | [shot27_overhead.png](shots/shot27/planning/shot27_overhead.png) | [shot27_overhead_ref.png](shots/shot27/planning/shot27_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot28 | ✅ | [shot28_overhead.png](shots/shot28/planning/shot28_overhead.png) | [shot28_overhead_ref.png](shots/shot28/planning/shot28_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot29 | ✅ | [shot29_overhead.png](shots/shot29/planning/shot29_overhead.png) | [shot29_overhead_ref.png](shots/shot29/planning/shot29_overhead_ref.png) | 免：只有镜尾 15.7–17s 三人同时起步往东走一两步（触发「同时走动 3 人」）；定机位对话镜，俯视图把站位与起步方向交代得清 |
| shot30 | ✅ | [shot30_overhead.png](shots/shot30/planning/shot30_overhead.png) | [shot30_overhead_ref.png](shots/shot30/planning/shot30_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot31 | ✅ | [shot31_overhead.png](shots/shot31/planning/shot31_overhead.png) | [shot31_overhead_ref.png](shots/shot31/planning/shot31_overhead_ref.png) | **要**：人与怪攻防接触 c2_Duke×m9_Princess |
| shot32 | ✅ | [shot32_overhead.png](shots/shot32/planning/shot32_overhead.png) | [shot32_overhead_ref.png](shots/shot32/planning/shot32_overhead_ref.png) | **要**：护人格挡 2 段 |
| shot33 | ✅ | [shot33_overhead.png](shots/shot33/planning/shot33_overhead.png) | [shot33_overhead_ref.png](shots/shot33/planning/shot33_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot34 | ✅ | [shot34_overhead.png](shots/shot34/planning/shot34_overhead.png) | [shot34_overhead_ref.png](shots/shot34/planning/shot34_overhead_ref.png) | **要**：同时走动 3 人 ≥ 3；护人格挡 1 段 |
| shot35 | ✅ | [shot35_overhead.png](shots/shot35/planning/shot35_overhead.png) | [shot35_overhead_ref.png](shots/shot35/planning/shot35_overhead_ref.png) | **要**：同时走动 3 人 ≥ 3；反应窗 2 段 |
| shot36 | ✅ | [shot36_overhead.png](shots/shot36/planning/shot36_overhead.png) | [shot36_overhead_ref.png](shots/shot36/planning/shot36_overhead_ref.png) | **要**：同时走动 4 人 ≥ 3；肢体接触 2 对 ≥ 2；护人格挡 1 段 |
| shot37 | ✅ | [shot37_overhead.png](shots/shot37/planning/shot37_overhead.png) | [shot37_overhead_ref.png](shots/shot37/planning/shot37_overhead_ref.png) | **要**：同时走动 3 人 ≥ 3；肢体接触 2 对 ≥ 2；人与怪攻防接触 c33_Surena_Caledon×m4_Defias_Bandit；护人格挡 2 段；反应窗 1 段 |
| shot38 | ✅ | [shot38_overhead.png](shots/shot38/planning/shot38_overhead.png) | [shot38_overhead_ref.png](shots/shot38/planning/shot38_overhead_ref.png) | **要**：同时走动 3 人 ≥ 3；肢体接触 5 对 ≥ 2；人与怪攻防接触 c32_Erlan_Drudgemoor×m4_Defias_Bandit；护人格挡 1 段；反应窗 1 段 |
| shot39 | ✅ | [shot39_overhead.png](shots/shot39/planning/shot39_overhead.png) | [shot39_overhead_ref.png](shots/shot39/planning/shot39_overhead_ref.png) | **要**：护人格挡 2 段 |
| shot40 | ✅ | [shot40_overhead.png](shots/shot40/planning/shot40_overhead.png) | [shot40_overhead_ref.png](shots/shot40/planning/shot40_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot41 | ✅ | [shot41_overhead.png](shots/shot41/planning/shot41_overhead.png) | [shot41_overhead_ref.png](shots/shot41/planning/shot41_overhead_ref.png) | 免：三个人沿农舍南边往西跑成一列（瘦子在前、沃尔特、杜克在后），路线单一、同一个方向，俯视图交代得清谁先谁后；插入段是长焦定机位 |
| shot42 | ✅ | [shot42_overhead.png](shots/shot42/planning/shot42_overhead.png) | [shot42_overhead_ref.png](shots/shot42/planning/shot42_overhead_ref.png) | 免：「同时走动 3 人」只出在 3s 镜内硬切（过了一会儿）换位置的那一跳；两段各自最多两人在动：林缘外一绊一压一推、谷仓门口拨猪闩门，都是一两个人的动作，俯视图交代得清 |
| shot43 | ✅ | [shot43_overhead.png](shots/shot43/planning/shot43_overhead.png) | [shot43_overhead_ref.png](shots/shot43/planning/shot43_overhead_ref.png) | 免：只有 0–3s 四人一起沿主街走上来站住（触发「同时走动 ≥ 3」）；此后是站着说话的三段定机位对话镜，俯视图把站位、朝向与递东西的先后交代得清 |
| shot44 | ✅ | [shot44_overhead.png](shots/shot44/planning/shot44_overhead.png) | [shot44_overhead_ref.png](shots/shot44/planning/shot44_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot45 | ✅ | [shot45_overhead.png](shots/shot45/planning/shot45_overhead.png) | [shot45_overhead_ref.png](shots/shot45/planning/shot45_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot46 | ✅ | [shot46_overhead.png](shots/shot46/planning/shot46_overhead.png) | [shot46_overhead_ref.png](shots/shot46/planning/shot46_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot47 | ✅ | [shot47_overhead.png](shots/shot47/planning/shot47_overhead.png) | [shot47_overhead_ref.png](shots/shot47/planning/shot47_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot48 | ✅ | [shot48_overhead.png](shots/shot48/planning/shot48_overhead.png) | [shot48_overhead_ref.png](shots/shot48/planning/shot48_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| shot49 | ✅ | [shot49_overhead.png](shots/shot49/planning/shot49_overhead.png) | [shot49_overhead_ref.png](shots/shot49/planning/shot49_overhead_ref.png) | 免：简单镜，overhead 图足够 |
