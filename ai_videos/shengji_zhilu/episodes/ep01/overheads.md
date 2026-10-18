# ep01 镜头平面图（overhead）索引

> 生成物：`python tools/shot_overhead.py --all ai_videos/shengji_zhilu/episodes/ep01`。改走位 ＝ 改各镜 `planning/overhead.toml` 重跑。
> 这一层只定「镜头与人各自在哪、往哪走、几秒到」；动作细节与形状在 shot blend 层。**这里点头之后才做 shot blend。**
> 每镜两张：`_overhead.png` 给人审，`_overhead_ref.png` 给 Seedance。默认所有镜头 **previz 免**，`_ref` 图直接当运动与几何参考上传；只有 `[meta] previz = true` 单独要的镜才渲 previz MP4（复杂镜判据只作提示，见 `previz_triggers`）。

| 镜 | 状态 | 审阅图 | Seedance 图 | previz |
|---|---|---|---|---|
| scenes/s1/shots/st1 | ✅ | [st1_overhead.png](scenes/s1/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s1/shots/st1/planning/st1_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s1/shots/st2 | ✅ | [st2_overhead.png](scenes/s1/shots/st2/planning/st2_overhead.png) | [st2_overhead_ref.png](scenes/s1/shots/st2/planning/st2_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s1/shots/st4 | ✅ | [st4_overhead.png](scenes/s1/shots/st4/planning/st4_overhead.png) | [st4_overhead_ref.png](scenes/s1/shots/st4/planning/st4_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s2/shots/st1 | ✅ | [st1_overhead.png](scenes/s2/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s2/shots/st1/planning/st1_overhead_ref.png) | **要**：简单镜按判据不需要，但第二轮亚伦的站位与朝向两次都被画反（站到墙南、朝镜头走），用 previz 锁住「墙北、背对镜头、不走动」与拉远运镜 |
| scenes/s2/shots/st2 | ✅ | [st2_overhead.png](scenes/s2/shots/st2/planning/st2_overhead.png) | [st2_overhead_ref.png](scenes/s2/shots/st2/planning/st2_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s3/shots/st1 | ✅ | [st1_overhead.png](scenes/s3/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s3/shots/st1/planning/st1_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s3/shots/st2 | ✅ | [st2_overhead.png](scenes/s3/shots/st2/planning/st2_overhead.png) | [st2_overhead_ref.png](scenes/s3/shots/st2/planning/st2_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s3/shots/st3 | ✅ | [st3_overhead.png](scenes/s3/shots/st3/planning/st3_overhead.png) | [st3_overhead_ref.png](scenes/s3/shots/st3/planning/st3_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s4/shots/st1 | ✅ | [st1_overhead.png](scenes/s4/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s4/shots/st1/planning/st1_overhead_ref.png) | 免：默认不做 previz（复杂镜提示：同时走动 3 人 ≥ 3） |
| scenes/s4/shots/st2 | ✅ | [st2_overhead.png](scenes/s4/shots/st2/planning/st2_overhead.png) | [st2_overhead_ref.png](scenes/s4/shots/st2/planning/st2_overhead_ref.png) | 免：默认不做 previz（复杂镜提示：同时走动 3 人 ≥ 3） |
| scenes/s4/shots/st3 | ✅ | [st3_overhead.png](scenes/s4/shots/st3/planning/st3_overhead.png) | [st3_overhead_ref.png](scenes/s4/shots/st3/planning/st3_overhead_ref.png) | 免：默认不做 previz（复杂镜提示：同时走动 3 人 ≥ 3；肢体接触 2 对 ≥ 2） |
| scenes/s5/shots/st1 | ✅ | [st1_overhead.png](scenes/s5/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s5/shots/st1/planning/st1_overhead_ref.png) | 免：默认不做 previz（复杂镜提示：同时走动 3 人 ≥ 3；肢体接触 3 对 ≥ 2） |
| scenes/s5/shots/st2 | ✅ | [st2_overhead.png](scenes/s5/shots/st2/planning/st2_overhead.png) | [st2_overhead_ref.png](scenes/s5/shots/st2/planning/st2_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s5/shots/st3 | ✅ | [st3_overhead.png](scenes/s5/shots/st3/planning/st3_overhead.png) | [st3_overhead_ref.png](scenes/s5/shots/st3/planning/st3_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s5/shots/st4 | ✅ | [st4_overhead.png](scenes/s5/shots/st4/planning/st4_overhead.png) | [st4_overhead_ref.png](scenes/s5/shots/st4/planning/st4_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s5/shots/st6 | ✅ | [st6_overhead.png](scenes/s5/shots/st6/planning/st6_overhead.png) | [st6_overhead_ref.png](scenes/s5/shots/st6/planning/st6_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s5/shots/st5 | ✅ | [st5_overhead.png](scenes/s5/shots/st5/planning/st5_overhead.png) | [st5_overhead_ref.png](scenes/s5/shots/st5/planning/st5_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s5/shots/st7 | ✅ | [st7_overhead.png](scenes/s5/shots/st7/planning/st7_overhead.png) | [st7_overhead_ref.png](scenes/s5/shots/st7/planning/st7_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s5/shots/st8 | ✅ | [st8_overhead.png](scenes/s5/shots/st8/planning/st8_overhead.png) | [st8_overhead_ref.png](scenes/s5/shots/st8/planning/st8_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s5/shots/st9 | ✅ | [st9_overhead.png](scenes/s5/shots/st9/planning/st9_overhead.png) | [st9_overhead_ref.png](scenes/s5/shots/st9/planning/st9_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s5/shots/st10 | ✅ | [st10_overhead.png](scenes/s5/shots/st10/planning/st10_overhead.png) | [st10_overhead_ref.png](scenes/s5/shots/st10/planning/st10_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s5/shots/st11 | ✅ | [st11_overhead.png](scenes/s5/shots/st11/planning/st11_overhead.png) | [st11_overhead_ref.png](scenes/s5/shots/st11/planning/st11_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s5/shots/st12 | ✅ | [st12_overhead.png](scenes/s5/shots/st12/planning/st12_overhead.png) | [st12_overhead_ref.png](scenes/s5/shots/st12/planning/st12_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s5/shots/st13 | ✅ | [st13_overhead.png](scenes/s5/shots/st13/planning/st13_overhead.png) | [st13_overhead_ref.png](scenes/s5/shots/st13/planning/st13_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s5/shots/st14 | ✅ | [st14_overhead.png](scenes/s5/shots/st14/planning/st14_overhead.png) | [st14_overhead_ref.png](scenes/s5/shots/st14/planning/st14_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s5/shots/st15 | ✅ | [st15_overhead.png](scenes/s5/shots/st15/planning/st15_overhead.png) | [st15_overhead_ref.png](scenes/s5/shots/st15/planning/st15_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s5/shots/st16 | ✅ | [st16_overhead.png](scenes/s5/shots/st16/planning/st16_overhead.png) | [st16_overhead_ref.png](scenes/s5/shots/st16/planning/st16_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s5/shots/st17 | ✅ | [st17_overhead.png](scenes/s5/shots/st17/planning/st17_overhead.png) | [st17_overhead_ref.png](scenes/s5/shots/st17/planning/st17_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s6/shots/st1 | ✅ | [st1_overhead.png](scenes/s6/shots/st1/planning/st1_overhead.png) | [st1_overhead_ref.png](scenes/s6/shots/st1/planning/st1_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s6/shots/st2 | ✅ | [st2_overhead.png](scenes/s6/shots/st2/planning/st2_overhead.png) | [st2_overhead_ref.png](scenes/s6/shots/st2/planning/st2_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s6/shots/st3 | ✅ | [st3_overhead.png](scenes/s6/shots/st3/planning/st3_overhead.png) | [st3_overhead_ref.png](scenes/s6/shots/st3/planning/st3_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
| scenes/s6/shots/st4 | ✅ | [st4_overhead.png](scenes/s6/shots/st4/planning/st4_overhead.png) | [st4_overhead_ref.png](scenes/s6/shots/st4/planning/st4_overhead_ref.png) | 免：默认不做 previz，overhead 图足够 |
