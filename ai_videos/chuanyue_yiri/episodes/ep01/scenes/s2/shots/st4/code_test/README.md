# 代码出片测试：ep1_s2_st4 街景背影 + 路人（2026-11-08）

目的：测「有人物、但不是特写（背影 / 远景路人）」的镜头能否用 3D 人物 + 动捕替代 Seedance。

| 文件 | 内容 |
|---|---|
| `ep1_s2_st4_code_v1.mp4` | 代码版：8 秒、1280×720、24fps，无声 |
| `compare_seedance_vs_code.mp4` | 左 Seedance 2.5 正片（160 积分）/ 右代码版 |
| `plate_empty_v1.png` | Codex：以首帧为参考、去掉所有人的空街底图（固定机位，背景就是这张图的像素） |

做法：
- 人物：MPFB 生成 6 人（Riley、顶篮女孩、扛双罐搬运工、老人、孩子、女人）+ 6 个远处复制路人；Riley 用 MPFB 女装与长发改色，路人是贴身上衣 + 喇叭下摆（`scripts/make_cast.py`，`work/cast.json`）。
- 动作：CMU 动捕（08_01、35_01、07_06、08_04、07_05、05_01），按骨骼迁移，顶篮 / 扛罐 / 牵手的手臂单独指定方向；孩子按老人速度加快步频（`scripts/retarget_cast.py`，`work/jobs.json`）。
- 尺度：用首帧里 Riley、老人、搬运工的像素高度拟合深度→米（第四人验证误差 < 12%），场景以米为单位。
- 渲染：Cycles，深度网格做阴影接收 + 遮挡，人物和影子渲 RGBA 后叠回底图；喷泉、溢流与积水反光在后期做流动（`scripts/render_street.py`，`scripts/composite_anim.py`）。约 13.5 秒 / 帧。

结论（代理自评）：人物位置、大小、步态与 Seedance 的调度一致，但一眼是 CG——人物发白、发平、像假人模特，近处的 Riley 尤其明显；远处 20–40 像素高的路人才勉强能混进去。这一镜不能替代 Seedance。
