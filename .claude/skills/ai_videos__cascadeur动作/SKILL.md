---
name: ai_videos__cascadeur动作
description: 用 Claude 驱动 Cascadeur（2026.2.x）做 AI 短剧的人物动作 previz：官方 MCP/脚本服务器接法、已验证的 csc Python API 事实、分段投递/截图调试/改完重开等工作纪律、AI 工具（AutoPosing/AutoPhysics/Inbetweening/Motion Generation/Video Mocap/Unbaking/Retargeting）能干什么与怎么触发、逐版本 release notes 摘要（2019.5b→2026.2.1）。凡 Cascadeur 相关的建动作、排错、导 FBX 给 Blender 之前先读本文。
---

# ai_videos__cascadeur动作 —— Claude 驾驭 Cascadeur 的完整手册

> 适用版本：Cascadeur **2026.2.1**（2026-09 实测）。本文分四层：① 接法 ② 已验证 API 事实 ③ 工作纪律 ④ 工具与版本知识。
> 前三层来自 xianjian_yi_mv shot12 的实战（`tools/cascadeur/*`、`shots/shot12/cascadeur/*`），第四层来自
> https://cascadeur.com/help/release_notes 全部 42 个子页 + Scripts / Python API / 工具文档（2026-09-06 抓取）。
> 规则出处：`.claude/agent_refs/project/ai_video.md` rule 4h（3D 层工程契约，§H「改完必重开」）。

## 0. 它在流水线里的位置

- Cascadeur 只负责**人物身体动作**（骨骼 + 手指），产出 `.casc`（源）与 **带烘焙动画的 FBX**。
- 剑 / 道具 / 特效 / 机位 / 环境在 **Blender previz** 里做（`shots/shotNN/previz/shotNN_previz.py --body=cascadeur` 导入 FBX，30→24 fps 重定时）。
- 最终给出片模型的是 Blender 渲的 previz mp4；Cascadeur 里的截图只用于调试。
- 单镜产物落点：`shots/shotNN/cascadeur/{脚本, full_*/shotNN_full.casc, shotNN_full.fbx}`，`shots/shotNN/shotNN_previz.{blend,mp4}`（与 cascadeur/ 同级）。

## 1. 接法：官方 MCP / 脚本服务器（2026.2 起内置）

| 事实 | 内容 |
|---|---|
| 官方入口 | 菜单 **Scripts → MCP → Start script server / Stop script server**（2026.2 release notes：“Added support for a simple MCP server”）。输出在 Event Log。官方文档**没有**写端口/传输/工具列表，以下是实测。 |
| 实测 | 服务器代码在 `<Cascadeur>/resources/scripts/python/scripts/mcp/script_server/`，HTTP **127.0.0.1:8765**；MCP 端点 `/mcp`（唯一工具 `run_script`），另有裸 HTTP `POST /run`（JSON `{"code": ...}`），健康检查 `GET /`。 |
| 命令行启动 | `cascadeur.exe --run-script scripts.mcp.start_server`（`--run-script` 自 2023.1 起可用）。 |
| 本仓库封装 | `.mcp.json` 注册了 `cascadeur`（http://127.0.0.1:8765/mcp，需 `/mcp` 重连才热加载）。日常用 **`python tools/cascadeur/casc_run.py -c "<code>"`** 直接 POST /run（打印 ok / value / messages）。 |
| 崩了怎么办 | `bash tools/cascadeur/casc_restart.sh`：健康检查 → taskkill 无响应实例 → 后台拉起 → 循环 `--run-script scripts.mcp.start_server` 直到 MCP up → PowerShell ShowWindow 还原窗口（最小化时截图不落盘）。 |
| 限制 | 单次脚本 **30 s 超时**；播放中 / 弹窗 / 卡死时不应答；长脚本曾把 Cascadeur 跑崩、内存冲到 5 GB → **一切按 STAGE 分段短投递**。 |
| 第三方 | 不需要任何第三方 cascadeur-mcp 包，官方内置的就够。 |

脚本在 Cascadeur 内的命名空间有 `csc`、`scene`（domain scene）、`app`。所有辅助函数集中在 **`tools/cascadeur/casc_lib.py`**（头注即事实表），用法：`exec(open(LIB, encoding="utf-8").read())`。

## 2. 已验证的 csc API 事实（2026.2.1 · Cascy 骨架）

- **姿态写入**：手指 = `*_Box_*` 控制器的 `Local Rotation`（局部 **Z = 蜷曲**，+Z 更弯；Y = 扭转）；四肢 = `*_MainPoint_* / *_DirectionPoint_* / *_AdditionalPoint_*` IK 点的 `Position`（全局 cm，**Y 向上，人面朝 +Z**）。写法：`scene.modify_update(title, mod)`，`mod(model, update, sc)` 里 `update.get_object_by_id(id).root_group().node_deep("Local Rotation"|"Position").set_value(v, frame)`，然后 `sc.run_update(ids, frame)`。
- **打键**：`model.layers_editor().set_fixed_interpolation_or_key_if_need(track, frame, True)`（`track = layers_viewer().layer_id_by_obj_id(obj)`）。默认区间是 STEP 样保持 → 每个键后要 `le.change_section(frame, track, f)` 把 `section.interval.interpolation` 设成 `csc.layers.layer.Interpolation.BEZIER / LINEAR`。
- **动画长度**：先给最后一帧打键，再 `model.fit_animation_size_by_layers()`（2024.1.2 新增），否则 “last frame in animation is 0”。载入后还要 `set_visible_range(first, last)`，否则时间轴只显示旧范围。
- **旋转**：`Rotation.to_euler_angles_x_y_z()` 的逆是 **Rz·Ry·Rx**；存盘/传递一律用四元数（`to_quaternion()` / `from_quaternion(w,x,y,z)`）。
- **读位置**：`behaviour_viewer().get_behaviour_by_name(id, "Transform")` → `get_behaviour_data(tr, "global_position")` → `data_viewer().get_data_value(d, frame)`。
- **截图**：`RenderToFile.take_image(view_scene, RenderParameters, path)` 是**延迟执行、渲染当前状态**——一次脚本只能一张（goto + snap），窗口不能最小化。`play_to_video_file / play_to_images_sequence` 从脚本服务器调会**崩**。
- **相机**：`app.current_scene().active_viewport().domain_viewport().camera_struct()` 改 position/target 后 `set_camera_struct`；逐帧改相机曾崩过一次。
- **FBX**：`app.get_tools_manager().get_tool("FbxSceneLoader").get_fbx_loader(app.current_scene())`，`FbxSettings(mode=Binary, bake_animation=True)`；**`export_all_objects` 带动画，`export_model` 不带**。
- **场景**：`ProjectLoader.load_from(path, view_scene.domain_scene())`；**读不了中文路径**（2026.2.1 修了 FBX 贴图的非 ASCII 路径，但 .casc 读取仍失败）→ 先拷到 ASCII 临时目录；存盘用时间戳文件名（同名文件在别的 tab 打开会拒存）。
- **网格道具**：`common.mesh.add_object_with_mesh`；球原生半径 ≈ 51.5 cm，立方体按 100 cm 边长；驱动 `Local Position / Local Rotation / Local Scale`（`Position` 对它无效）。
- **Bezier 保持段会鼓起**：相邻两键姿态相同的区间若用 Bezier，Cascadeur 会把下一段的大位移拉进来（人曾凭空浮起 46 cm）→ **每一段保持一律 LINEAR**（手指 Box 轨道同理）。
- **手腕不弯**：两骨 IK 预测肘位 + 极向点，让手沿前臂延伸（`hand_straight`）；Cascy 基础姿态掌心朝前 → 垂手/平张要绕前臂轴 roll ±90°。
- **一只手的三个点共用一条轨道**：MainPoint / DirectionPoint / AdditionalPoint 的 `layer_id_by_obj_id` 相同，给任一点打键会把整条轨道当前值存成键 → 逐帧 pass 要连 MainPoint 一起显式写回，网格键区间设 LINEAR。
- **求值异步、只算可视范围**（2026-09-06，耗掉半天的坑）：`set_anim_size` 扩出来的帧在 `set_visible_range` 之前**不求值**，`gpos` 读到的全是最后一个可视帧的姿态（整段第二幕曾僵成第一幕末姿势，只有键帧本身对）。扩长后立刻 `set_visible_range(0, last)`；读非键帧前先 `goto` 扫几帧 + sleep 5 s，再读两遍确认稳定。扩展区间里 BEZIER 段曾整段平直，先设 LINEAR 让求值可靠、finish 再换 BEZIER。
- **菜单工具的脚本入口**：AutoPosing / AutoPhysics / Motion Generation / Unbaking / Retargeting 没有直接 API 函数，但有 **action id**（见 §4.2），`app.get_action_manager().call_action(id)`；需要与 GUI 相同的选区/区间前置状态；**本仓库尚未实测**。

## 3. 工作纪律（用户裁定，违反会空转一轮反馈）

1. **调试只看截图**：改姿态只重跑对应 STAGE（~5 s）+ 单帧截图核对；不出 mp4、不导 FBX、不碰 Blender，全部关键帧确认后才全渲。
2. **无响应直接杀**：不等用户暂停，`taskkill` → `casc_restart.sh` → 从 `.casc` 或脚本重建。
3. **改完必重开**（rule 4h §H）：任何 Cascadeur / Blender 改动的最后一步 = 关掉现有实例、重开最新 `.casc` / `.blend`；GUI 里是打开时的内存副本，不会自己刷新。杀 Blender 前确认后台渲染已结束。
4. **一切可重建**：动作全部由脚本生成（`shot12_cascadeur_{fall,act1,act2}.py` + `rebuild.sh`），改动作 = 改脚本重跑，不手 K。时刻与 `previz_config.toml` 时长链逐拍对齐。
5. **手型默认自然**：只在需要手势（结印/剑指）的时段打手指键，其余时段用放松手型；Cascy 默认手是五指张开的展示姿，不是「自然」。
6. **保持段 LINEAR、过渡段 BEZIER**；每个 STAGE 结束就数值自查（骨盆/脚底高度、手位、剑位），不靠肉眼。

## 4. 工具与版本知识（release notes 2019.5b → 2026.2.1）

### 4.1 AI / 自动化工具一览（做武打 previz 时怎么用）

| 工具 | 干什么 | 怎么触发 | 版本 / 授权 | 对本流水线的意义 |
|---|---|---|---|---|
| **AutoPosing** | 拖几个主控制点，AI 补全全身自然姿态；有 Main / Additional / Direction 三类控制器；Shift+Z 锁定、R 固定 | 工具栏 AutoPosing；`call_action("AutoPosingTool.AutoPosing")` | 2021.1EA 起；2022.1EA 改 IK 新系统；2024.1 加 Additional 与武器/道具；2025.3 四足（Pro+）；2026.2 手脚贴合环境 | 快速摆大姿态；注意它**会覆盖已有姿态**，适合起稿不适合精修 |
| **AutoPosing: Fingers** | 掌上生成手指控制器，食指/小指控制器带整掌 | 工具栏 AutoPosing: Fingers | 2023.1（Pro） | 需要真五指角色（Cascy 可以）；我们目前用 Box 旋转直接写手型 |
| **AutoPhysics** | 分析动作给出物理正确版（重心/弹道/支点） | 工具栏；`call_action("AutoPhysicsTool.Snap to Auto Physics")` | 2021.1EA 起；2024.1 环境交互；2025.2 弹道中角色交互 | 跳旋/翻跟斗段可用来校正弹道；先备份 |
| **Inbetweening（AI 插值）** | 两关键帧之间 AI 生成中间动作，相邻键 ≤120 帧；有 Style；Update Inbetweening 自动刷新 | Timeline 插值菜单里的 **AI** 按钮 | 2025.1 新增；2025.2 Style；2025.3 归入插值类型；2026.2 更大数据集 | 替代手写逐帧过渡的候选；只作用于 Base Layer |
| **Motion Generation（原 Root Motion）** | 按轨迹生成整段动作（Walk/Run/Acrobatic 风格、Keyframes force、Trajectory force、Reference Mode） | 工具栏 Run Motion Generation；`call_action("View.MotionGeneration_Run")` | 2026.1 新增；2026.2 改名并可在键间传递风格 | 输出是逐帧 Fixed 插值；适合走位/跑动，不适合精确武打 |
| **Video Mocap** | 从视频/图片识别姿态套到角色 | Commands 菜单 | 2023.1 alpha（需 ~700 MB 包，~20 s/帧）；2023.2 提速 5×；2025.2 自动清脚滑 | 有参考视频时的另一条路 |
| **Animation Unbaking** | 把逐帧烘焙动画反推成少键 + 插值 | `call_action("View.Animation unbaking")` | 2024.1；2025.1 支持部分烘焙 | 导入 mocap/FBX 后清理 |
| **Retargeting** | 不同骨架间迁移动画 | `call_action("View.Retargeting_Copy/Paste")` | 2024.1；2025.3.1 四足 | 把 Cascy 动作迁到 MPFB/真人比例角色 |
| **Collision Penetration Cleaning** | 去除穿插 | 工具（旧场景需重建 rig） | 2026.1；2026.1.1 支持 AutoPosing 控制器 | 剑/葫芦与身体穿插时 |
| **Ragdoll** | 角色被撞的物理反应，含角度限制 | Physics Settings → Ragdoll | 2024.3；2025.3 角度限制 | 一般不用 |
| **Easing** | 不改轨迹只改帧分布（快慢） | Timeline 的 Easing 按钮 | 2026.2 | 调「起收分明、半拍定格」的节奏 |
| **Additive Layers（alpha）** | 非破坏性叠加层（delta），权重 0–100% | Window → Animation Layers | 2026.2 | AI Inbetweening 只在 Base Layer；进 Rig Mode 前须合并 |
| **Fulcrum Motion Cleaning** | 清支点滑动/膝盖弹跳 | Inbetweening / Motion Generation 选项 | 2022–2025 持续 | 落地/踩剑段可开 |

### 4.2 Python / 脚本相关的版本线

- **2022.1EA**：内置 Python API 首次出现（自动化、Node Editor 自定义 rig）。
- **2023.1**：`-run-script` 命令行标志（我们用它拉起 MCP 服务器）。**2023.2**：Python 3.11、可从设置加载模块、可用 API 生成 rig 原型。
- **2024.1.2**：`ModelEditor.fit_animation_size_by_layers()`（动画长度的正确写法）。**2025.1.1**：修 `create_object()` 崩溃。
- **2025.2**：behaviour viewer 可取属性类型、可取全部工具对象 id、data editor 删除方法改进。**2026.1**：设置函数 InIntervalInclusive / FindFirstInt / FindFirstBool / At。
- **2026.2**：**内置 MCP 服务器**（Scripts → MCP）；**Python stub 文件**（IDE 智能提示）；**PySide 自定义 UI**；BVH 导入（Commands 菜单）。**2026.2.1**：无脚本改动，修 FBX 非 ASCII 路径贴图、blendshape 导入崩溃、UE LiveLink。
- **action id 表**（help/category/301，官方注明将逐步被正式 API 取代）：`Scene.Undo`、`AutoPosingTool.AutoPosing | SwitchLock | Update`、`AutoPhysicsTool.Switch Auto Physics | Snap to Auto Physics | Show all fucrum points`、`Timeline.Add|Remove key`、`Timeline.Bezier.Bezier on current frame`、`Timeline.Linear.Linear on current frame`、`Timeline.Play`、`File.Import.Animation.Fbx...`、`File.Export.Scene.Fbx...`、`File.Export.Animation.Fbx...`、`View.MotionGeneration_Run`、`View.Animation unbaking`、`View.Retargeting_Copy/Paste`。用法 `csc.app.get_application().get_action_manager().call_action(id)`。
- Python API 结构（help/category/215）：应用层 `csc.app.Application / ToolsManager / get_application()`；数据层 `csc.domain.Scene`；编辑走 `scene.modify / modify_update / modify_with_session`；viewers 只读（`model_viewer / data_viewer / behaviour_viewer / layers_viewer`）、editors 可写（`model_editor / data_editor / behaviour_editor / layers_editor`）；拓扑改动要 `scene_updater.generate_update()`；API 里 Animation Tracks 仍叫 **Layers**；官方承认覆盖不均（约 2 万行，多为 rig 生成）。

### 4.3 导入导出 / 渲染 / 集成的版本线（与 Blender 对接相关）

- FBX：2022.2EA 可选版本；2024.1 设置跨会话保留；2025.1 多 take、模型姿态导入导出（改善 Blender/Daz 兼容）；2025.2 非整数帧率；2025.2.1 默认导入模式 Deep→**Root**；2025.2.3 修非标准旋转顺序；2025.3 相机随 FBX 进出；2025.3.3 修 NaN；2026.2 一网格多材质、贴图弃用改材质。
- 其它格式：USD（2023.2 alpha）、GLTF/GLB（2025.1；2025.3 VRM）、BVH 导入（2026.2）、DAE。
- 渲染：2025.3 起 **Filament** 引擎（环境光/阴影/AO，Windows 优先）；2026.2 相机 ISO/快门/光圈；2026.1.3 修视口阴影抖动。脚本侧仍只能单帧 `take_image`。
- 引擎集成：UE LiveLink（2024.3；2026.1 重写；2026.1.1 Indie 可用；2026.2 支持 UE 5.8）；Roblox 导出脚本。
- 界面：2026.2 全多语言 UI（右上角切换）。

### 4.4 更早的里程碑（只作背景）

2019.5b/2020.x：QML 界面、Quick Rigging Tool、Bezier Clamped、AutoKey、旋转轨迹。2021.x：AutoPhysics 首发、AutoPosing 支持任意人形、Graph Editor、Tween Machine、Animation Cycles、Secondary Motion、Spline IK。2022.x：Python API、Node Editor、GR 运动学、UI 可拆分、暗色主题。

## 5. 触发本 skill 后的动作清单

1. `bash tools/cascadeur/casc_restart.sh`（或确认 `curl 127.0.0.1:8765/` 正常）。
2. 读 `tools/cascadeur/casc_lib.py` 头注 + 目标 shot 的 `cascadeur/*.py` 头注，按 STAGE 短投递。
3. 每改一处：重跑 STAGE → 数值自查 → 单帧截图。
4. 定稿：`bash shots/shotNN/cascadeur/rebuild.sh` → 拷回 `.casc` / 导 FBX → Blender previz 重建重渲 → **关掉重开 Cascadeur 与 Blender** → 交 mp4。
5. 记 follow-up + changelog（`specs/ai_video/{name}/`）。
