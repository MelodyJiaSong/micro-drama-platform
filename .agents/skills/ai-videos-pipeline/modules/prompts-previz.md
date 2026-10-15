# Previz

绿幕前纯色小人偶的走位预演视频。它比 overhead 精确：逐秒给出每个人的站位、朝向、走位和姿势，以及机位的移动与取景。复杂镜用它代替 overhead 图当运动参考。

## 哪些镜要

由 `tools/shot_overhead.py` 从 overhead.toml 量化判定，任一成立就要（写进 `planning/previz.json`）：

| 判据 | 阈值 |
|---|---|
| 机位长距离移动 | 连续水平移动 > 12 m |
| 镜内多段硬切 | ≥ 4 段 |
| 多人同时走动 | 同一时刻 ≥ 3 人在走 |
| 肢体接触 | ≥ 2 对人贴近（< 0.8 m 且有人在动） |
| 攻防 | 人与怪攻防接触 ≥ 1 对；有护人格挡 |

`[meta] previz = true / false` 可以推翻判定，但与判据相反时必须写 `previz_why`。简单镜不渲视频，只出静帧核对取景。

## 怎么做

```
python tools/overhead_previz.py <镜头目录> --stills    # 先出关键时刻静帧拼图（十几秒），看过再渲
python tools/overhead_previz.py <镜头目录> --render    # 渲整条 MP4（几分钟）→ previz/stN_previz.mp4
python tools/overhead_previz.py --all <集目录> --render # 本集所有要 previz 的镜
```

配置 `previz/previz_config.toml` 由工具从 overhead.toml 生成，不手改；改走位改 overhead 重跑。引擎是共享的 `tools/previz/build_previz.py`（Blender）。

| 画面里有 | 规则 |
|---|---|
| 绿幕地面与背景 | 不建场景：空间关系已在 overhead 里定，场景长相交给场景图 |
| 纯色关节小人偶 | 颜色按剧 `figure_colors`，与 overhead 圆点同色；人偶有四肢，姿势来自 `[[pose]]`，走动时自动换行走姿态 |
| 灰色方块 | overhead 的 `[[object]]`，按 `h` 定高 |
| 机位 | overhead 的 `[[camera]]` 路点、焦距与离地高 |

规格：1280×720、24 fps（Seedance 参考视频下限 409600 像素、24–60 fps；单条 2–15 秒，2.5 输出上限 30 秒，见 `tools/previz/seedance_ref.py`）。

## 交给 Seedance

previz 视频排在参考第一位，「参考用法」固定写：只参考机位、运镜、站位、朝向、走位路线和动作时刻；不参考人偶外形与颜色；画面里不出现绿幕和人偶；人偶颜色只是身份标记。「人物」行把每个颜色绑到人物图，「要求」行加自然表演句。

| 应该 | 不应该 |
|---|---|
| 先看静帧再渲整条 | 渲完整条才发现机位错 |
| 人偶颜色低调、每人固定 | 绿色人偶（与绿幕同色） |
| 动作细节、表情、光线写在 prompt 与分镜里 | 指望小人偶表演情绪 |
| 不出现轨迹线、坐标轴、相机框 | 把辅助线渲进视频——会被画进成片 |

**已知风险**：旧流程实测白模人偶的僵硬会被照搬进成片，所以有自然表演句；白模能减少抽卡，不能消除抽卡。2.5 官方支持白模参考，绿幕小人偶的效果仍要在出片时核对。
