# ep01 镜头平面图（overhead）索引

> 生成物：`python tools/shot_overhead.py --all ai_videos/shengji_zhilu/episodes/ep01`。改走位 ＝ 改各镜 `planning/overhead.toml` 重跑。
> 这一层只定「镜头与人各自在哪、往哪走、几秒到」；动作细节与形状在 shot blend 层。**这里点头之后才做 shot blend。**
> 每镜两张：`_overhead.png` 给人审，`_overhead_ref.png` 给 Seedance。**previz 免** 的镜不做 shot blend，`_ref` 图直接当运动与几何参考上传；**要** 的镜照旧渲 previz MP4（判据见 `tools/shot_overhead.py` `previz_triggers`）。

| 镜 | 状态 | 审阅图 | Seedance 图 | previz |
|---|---|---|---|---|
| scenes/s1/shots/st1 | ✅ | [st1_overhead.png](scenes/s1/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s1/shots/st1/planning/st1_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s11/shots/st1 | ✅ | [st1_overhead.png](scenes/s11/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s11/shots/st1/planning/st1_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s2/shots/st1 | ✅ | [st1_overhead.png](scenes/s2/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s2/shots/st1/planning/st1_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s2/shots/st14 | ✅ | [st14_overhead.png](scenes/s2/shots/st14/planning/st14_overhead.png) | [st14_overhead_ref.png](scenes/s2/shots/st14/planning/st14_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s2/shots/st2 | ✅ | [st2_overhead.png](scenes/s2/shots/st2/planning/st2_overhead.png) | [st2_overhead_ref.png](scenes/s2/shots/st2/planning/st2_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s2/shots/st3 | ✅ | [st3_overhead.png](scenes/s2/shots/st3/planning/st3_overhead.png) | [st3_overhead_ref.png](scenes/s2/shots/st3/planning/st3_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s2/shots/st4 | ✅ | [st4_overhead.png](scenes/s2/shots/st4/planning/st4_overhead.png) | [st4_overhead_ref.png](scenes/s2/shots/st4/planning/st4_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s2/shots/st5 | ✅ | [st5_overhead.png](scenes/s2/shots/st5/planning/st5_overhead.png) | [st5_overhead_ref.png](scenes/s2/shots/st5/planning/st5_overhead_ref.png) | **要**：同时走动 4 人 ≥ 3 |
| scenes/s2/shots/st6 | ✅ | [st6_overhead.png](scenes/s2/shots/st6/planning/st6_overhead.png) | [st6_overhead_ref.png](scenes/s2/shots/st6/planning/st6_overhead_ref.png) | **要**：同时走动 5 人 ≥ 3；护人格挡 1 段 |
| scenes/s2/shots/st15 | ✅ | [st15_overhead.png](scenes/s2/shots/st15/planning/st15_overhead.png) | [st15_overhead_ref.png](scenes/s2/shots/st15/planning/st15_overhead_ref.png) | **要**：人与怪攻防接触 c1_Aaron×m7_Wolf；护人格挡 1 段 |
| scenes/s2/shots/st16 | ✅ | [st16_overhead.png](scenes/s2/shots/st16/planning/st16_overhead.png) | [st16_overhead_ref.png](scenes/s2/shots/st16/planning/st16_overhead_ref.png) | **要**：同时走动 3 人 ≥ 3；人与怪攻防接触 c1_Aaron×m7_Wolf |
| scenes/s2/shots/st7 | ✅ | [st7_overhead.png](scenes/s2/shots/st7/planning/st7_overhead.png) | [st7_overhead_ref.png](scenes/s2/shots/st7/planning/st7_overhead_ref.png) | **要**：同时走动 3 人 ≥ 3；人与怪攻防接触 c1_Aaron×m7_Wolf |
| scenes/s2/shots/st17 | ✅ | [st17_overhead.png](scenes/s2/shots/st17/planning/st17_overhead.png) | [st17_overhead_ref.png](scenes/s2/shots/st17/planning/st17_overhead_ref.png) | **要**：同时走动 3 人 ≥ 3；人与怪攻防接触 c1_Aaron×m7_Wolf |
| scenes/s2/shots/st8 | ✅ | [st8_overhead.png](scenes/s2/shots/st8/planning/st8_overhead.png) | [st8_overhead_ref.png](scenes/s2/shots/st8/planning/st8_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s2/shots/st9 | ✅ | [st9_overhead.png](scenes/s2/shots/st9/planning/st9_overhead.png) | [st9_overhead_ref.png](scenes/s2/shots/st9/planning/st9_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s2/shots/st18 | ✅ | [st18_overhead.png](scenes/s2/shots/st18/planning/st18_overhead.png) | [st18_overhead_ref.png](scenes/s2/shots/st18/planning/st18_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s2/shots/st10 | ✅ | [st10_overhead.png](scenes/s2/shots/st10/planning/st10_overhead.png) | [st10_overhead_ref.png](scenes/s2/shots/st10/planning/st10_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s2/shots/st11 | ✅ | [st11_overhead.png](scenes/s2/shots/st11/planning/st11_overhead.png) | [st11_overhead_ref.png](scenes/s2/shots/st11/planning/st11_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s2/shots/st12 | ✅ | [st12_overhead.png](scenes/s2/shots/st12/planning/st12_overhead.png) | [st12_overhead_ref.png](scenes/s2/shots/st12/planning/st12_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s2/shots/st19 | ✅ | [st19_overhead.png](scenes/s2/shots/st19/planning/st19_overhead.png) | [st19_overhead_ref.png](scenes/s2/shots/st19/planning/st19_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s2/shots/st13 | ✅ | [st13_overhead.png](scenes/s2/shots/st13/planning/st13_overhead.png) | [st13_overhead_ref.png](scenes/s2/shots/st13/planning/st13_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s3/shots/st5 | ✅ | [st5_overhead.png](scenes/s3/shots/st5/planning/st5_overhead.png) | [st5_overhead_ref.png](scenes/s3/shots/st5/planning/st5_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s3/shots/st1 | ✅ | [st1_overhead.png](scenes/s3/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s3/shots/st1/planning/st1_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s3/shots/st2 | ✅ | [st2_overhead.png](scenes/s3/shots/st2/planning/st2_overhead.png) | [st2_overhead_ref.png](scenes/s3/shots/st2/planning/st2_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s3/shots/st3 | ✅ | [st3_overhead.png](scenes/s3/shots/st3/planning/st3_overhead.png) | [st3_overhead_ref.png](scenes/s3/shots/st3/planning/st3_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s3/shots/st4 | ✅ | [st4_overhead.png](scenes/s3/shots/st4/planning/st4_overhead.png) | [st4_overhead_ref.png](scenes/s3/shots/st4/planning/st4_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st1 | ✅ | [st1_overhead.png](scenes/s4/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s4/shots/st1/planning/st1_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st2 | ✅ | [st2_overhead.png](scenes/s4/shots/st2/planning/st2_overhead.png) | [st2_overhead_ref.png](scenes/s4/shots/st2/planning/st2_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st3 | ✅ | [st3_overhead.png](scenes/s4/shots/st3/planning/st3_overhead.png) | [st3_overhead_ref.png](scenes/s4/shots/st3/planning/st3_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st4 | ✅ | [st4_overhead.png](scenes/s4/shots/st4/planning/st4_overhead.png) | [st4_overhead_ref.png](scenes/s4/shots/st4/planning/st4_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st5 | ✅ | [st5_overhead.png](scenes/s4/shots/st5/planning/st5_overhead.png) | [st5_overhead_ref.png](scenes/s4/shots/st5/planning/st5_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st6 | ✅ | [st6_overhead.png](scenes/s4/shots/st6/planning/st6_overhead.png) | [st6_overhead_ref.png](scenes/s4/shots/st6/planning/st6_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st7 | ✅ | [st7_overhead.png](scenes/s4/shots/st7/planning/st7_overhead.png) | [st7_overhead_ref.png](scenes/s4/shots/st7/planning/st7_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st8 | ✅ | [st8_overhead.png](scenes/s4/shots/st8/planning/st8_overhead.png) | [st8_overhead_ref.png](scenes/s4/shots/st8/planning/st8_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st9 | ✅ | [st9_overhead.png](scenes/s4/shots/st9/planning/st9_overhead.png) | [st9_overhead_ref.png](scenes/s4/shots/st9/planning/st9_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st10 | ✅ | [st10_overhead.png](scenes/s4/shots/st10/planning/st10_overhead.png) | [st10_overhead_ref.png](scenes/s4/shots/st10/planning/st10_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st11 | ✅ | [st11_overhead.png](scenes/s4/shots/st11/planning/st11_overhead.png) | [st11_overhead_ref.png](scenes/s4/shots/st11/planning/st11_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st12 | ✅ | [st12_overhead.png](scenes/s4/shots/st12/planning/st12_overhead.png) | [st12_overhead_ref.png](scenes/s4/shots/st12/planning/st12_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st13 | ✅ | [st13_overhead.png](scenes/s4/shots/st13/planning/st13_overhead.png) | [st13_overhead_ref.png](scenes/s4/shots/st13/planning/st13_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st14 | ✅ | [st14_overhead.png](scenes/s4/shots/st14/planning/st14_overhead.png) | [st14_overhead_ref.png](scenes/s4/shots/st14/planning/st14_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st15 | ✅ | [st15_overhead.png](scenes/s4/shots/st15/planning/st15_overhead.png) | [st15_overhead_ref.png](scenes/s4/shots/st15/planning/st15_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st16 | ✅ | [st16_overhead.png](scenes/s4/shots/st16/planning/st16_overhead.png) | [st16_overhead_ref.png](scenes/s4/shots/st16/planning/st16_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s4/shots/st17 | ✅ | [st17_overhead.png](scenes/s4/shots/st17/planning/st17_overhead.png) | [st17_overhead_ref.png](scenes/s4/shots/st17/planning/st17_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s5/shots/st1 | ✅ | [st1_overhead.png](scenes/s5/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s5/shots/st1/planning/st1_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s5/shots/st2 | ✅ | [st2_overhead.png](scenes/s5/shots/st2/planning/st2_overhead.png) | [st2_overhead_ref.png](scenes/s5/shots/st2/planning/st2_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s5/shots/st3 | ✅ | [st3_overhead.png](scenes/s5/shots/st3/planning/st3_overhead.png) | [st3_overhead_ref.png](scenes/s5/shots/st3/planning/st3_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s5/shots/st4 | ✅ | [st4_overhead.png](scenes/s5/shots/st4/planning/st4_overhead.png) | [st4_overhead_ref.png](scenes/s5/shots/st4/planning/st4_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s5/shots/st5 | ✅ | [st5_overhead.png](scenes/s5/shots/st5/planning/st5_overhead.png) | [st5_overhead_ref.png](scenes/s5/shots/st5/planning/st5_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s5/shots/st6 | ✅ | [st6_overhead.png](scenes/s5/shots/st6/planning/st6_overhead.png) | [st6_overhead_ref.png](scenes/s5/shots/st6/planning/st6_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s5/shots/st7 | ✅ | [st7_overhead.png](scenes/s5/shots/st7/planning/st7_overhead.png) | [st7_overhead_ref.png](scenes/s5/shots/st7/planning/st7_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s5/shots/st8 | ✅ | [st8_overhead.png](scenes/s5/shots/st8/planning/st8_overhead.png) | [st8_overhead_ref.png](scenes/s5/shots/st8/planning/st8_overhead_ref.png) | **要**：同时走动 3 人 ≥ 3 |
| scenes/s5/shots/st9 | ✅ | [st9_overhead.png](scenes/s5/shots/st9/planning/st9_overhead.png) | [st9_overhead_ref.png](scenes/s5/shots/st9/planning/st9_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s5/shots/st10 | ✅ | [st10_overhead.png](scenes/s5/shots/st10/planning/st10_overhead.png) | [st10_overhead_ref.png](scenes/s5/shots/st10/planning/st10_overhead_ref.png) | **要**：同时走动 3 人 ≥ 3 |
| scenes/s6/shots/st1 | ✅ | [st1_overhead.png](scenes/s6/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s6/shots/st1/planning/st1_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s6/shots/st2 | ✅ | [st2_overhead.png](scenes/s6/shots/st2/planning/st2_overhead.png) | [st2_overhead_ref.png](scenes/s6/shots/st2/planning/st2_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s6/shots/st3 | ✅ | [st3_overhead.png](scenes/s6/shots/st3/planning/st3_overhead.png) | [st3_overhead_ref.png](scenes/s6/shots/st3/planning/st3_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s6/shots/st4 | ✅ | [st4_overhead.png](scenes/s6/shots/st4/planning/st4_overhead.png) | [st4_overhead_ref.png](scenes/s6/shots/st4/planning/st4_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s6/shots/st5 | ✅ | [st5_overhead.png](scenes/s6/shots/st5/planning/st5_overhead.png) | [st5_overhead_ref.png](scenes/s6/shots/st5/planning/st5_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s6/shots/st6 | ✅ | [st6_overhead.png](scenes/s6/shots/st6/planning/st6_overhead.png) | [st6_overhead_ref.png](scenes/s6/shots/st6/planning/st6_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s7/shots/st1 | ✅ | [st1_overhead.png](scenes/s7/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s7/shots/st1/planning/st1_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s13/shots/st1 | ✅ | [st1_overhead.png](scenes/s13/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s13/shots/st1/planning/st1_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st1 | ✅ | [st1_overhead.png](scenes/s8/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s8/shots/st1/planning/st1_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st2 | ✅ | [st2_overhead.png](scenes/s8/shots/st2/planning/st2_overhead.png) | [st2_overhead_ref.png](scenes/s8/shots/st2/planning/st2_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st3 | ✅ | [st3_overhead.png](scenes/s8/shots/st3/planning/st3_overhead.png) | [st3_overhead_ref.png](scenes/s8/shots/st3/planning/st3_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st4 | ✅ | [st4_overhead.png](scenes/s8/shots/st4/planning/st4_overhead.png) | [st4_overhead_ref.png](scenes/s8/shots/st4/planning/st4_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st5 | ✅ | [st5_overhead.png](scenes/s8/shots/st5/planning/st5_overhead.png) | [st5_overhead_ref.png](scenes/s8/shots/st5/planning/st5_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st6 | ✅ | [st6_overhead.png](scenes/s8/shots/st6/planning/st6_overhead.png) | [st6_overhead_ref.png](scenes/s8/shots/st6/planning/st6_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st7 | ✅ | [st7_overhead.png](scenes/s8/shots/st7/planning/st7_overhead.png) | [st7_overhead_ref.png](scenes/s8/shots/st7/planning/st7_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st8 | ✅ | [st8_overhead.png](scenes/s8/shots/st8/planning/st8_overhead.png) | [st8_overhead_ref.png](scenes/s8/shots/st8/planning/st8_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st9 | ✅ | [st9_overhead.png](scenes/s8/shots/st9/planning/st9_overhead.png) | [st9_overhead_ref.png](scenes/s8/shots/st9/planning/st9_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st10 | ✅ | [st10_overhead.png](scenes/s8/shots/st10/planning/st10_overhead.png) | [st10_overhead_ref.png](scenes/s8/shots/st10/planning/st10_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st11 | ✅ | [st11_overhead.png](scenes/s8/shots/st11/planning/st11_overhead.png) | [st11_overhead_ref.png](scenes/s8/shots/st11/planning/st11_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st12 | ✅ | [st12_overhead.png](scenes/s8/shots/st12/planning/st12_overhead.png) | [st12_overhead_ref.png](scenes/s8/shots/st12/planning/st12_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st13 | ✅ | [st13_overhead.png](scenes/s8/shots/st13/planning/st13_overhead.png) | [st13_overhead_ref.png](scenes/s8/shots/st13/planning/st13_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st14 | ✅ | [st14_overhead.png](scenes/s8/shots/st14/planning/st14_overhead.png) | [st14_overhead_ref.png](scenes/s8/shots/st14/planning/st14_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st15 | ✅ | [st15_overhead.png](scenes/s8/shots/st15/planning/st15_overhead.png) | [st15_overhead_ref.png](scenes/s8/shots/st15/planning/st15_overhead_ref.png) | **要**：护人格挡 1 段 |
| scenes/s8/shots/st16 | ✅ | [st16_overhead.png](scenes/s8/shots/st16/planning/st16_overhead.png) | [st16_overhead_ref.png](scenes/s8/shots/st16/planning/st16_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st17 | ✅ | [st17_overhead.png](scenes/s8/shots/st17/planning/st17_overhead.png) | [st17_overhead_ref.png](scenes/s8/shots/st17/planning/st17_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st18 | ✅ | [st18_overhead.png](scenes/s8/shots/st18/planning/st18_overhead.png) | [st18_overhead_ref.png](scenes/s8/shots/st18/planning/st18_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st19 | ✅ | [st19_overhead.png](scenes/s8/shots/st19/planning/st19_overhead.png) | [st19_overhead_ref.png](scenes/s8/shots/st19/planning/st19_overhead_ref.png) | **要**：同时走动 3 人 ≥ 3 |
| scenes/s8/shots/st20 | ✅ | [st20_overhead.png](scenes/s8/shots/st20/planning/st20_overhead.png) | [st20_overhead_ref.png](scenes/s8/shots/st20/planning/st20_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s8/shots/st21 | ✅ | [st21_overhead.png](scenes/s8/shots/st21/planning/st21_overhead.png) | [st21_overhead_ref.png](scenes/s8/shots/st21/planning/st21_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s9/shots/st1 | ✅ | [st1_overhead.png](scenes/s9/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s9/shots/st1/planning/st1_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s9/shots/st2 | ✅ | [st2_overhead.png](scenes/s9/shots/st2/planning/st2_overhead.png) | [st2_overhead_ref.png](scenes/s9/shots/st2/planning/st2_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s9/shots/st3 | ✅ | [st3_overhead.png](scenes/s9/shots/st3/planning/st3_overhead.png) | [st3_overhead_ref.png](scenes/s9/shots/st3/planning/st3_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s9/shots/st4 | ✅ | [st4_overhead.png](scenes/s9/shots/st4/planning/st4_overhead.png) | [st4_overhead_ref.png](scenes/s9/shots/st4/planning/st4_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s9/shots/st5 | ✅ | [st5_overhead.png](scenes/s9/shots/st5/planning/st5_overhead.png) | [st5_overhead_ref.png](scenes/s9/shots/st5/planning/st5_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s9/shots/st6 | ✅ | [st6_overhead.png](scenes/s9/shots/st6/planning/st6_overhead.png) | [st6_overhead_ref.png](scenes/s9/shots/st6/planning/st6_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s10/shots/st1 | ✅ | [st1_overhead.png](scenes/s10/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s10/shots/st1/planning/st1_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s10/shots/st2 | ✅ | [st2_overhead.png](scenes/s10/shots/st2/planning/st2_overhead.png) | [st2_overhead_ref.png](scenes/s10/shots/st2/planning/st2_overhead_ref.png) | 免：简单镜，overhead 图足够 |
| scenes/s10/shots/st3 | ✅ | [st3_overhead.png](scenes/s10/shots/st3/planning/st3_overhead.png) | [st3_overhead_ref.png](scenes/s10/shots/st3/planning/st3_overhead_ref.png) | 免：简单镜，overhead 图足够 |
