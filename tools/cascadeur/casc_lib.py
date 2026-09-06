# Helper library exec'd INSIDE Cascadeur via the in-app MCP script server (namespace has csc, scene, app).
# Usage at top of a script:  exec(open(LIB, encoding="utf-8").read())
#
# Driving Cascadeur 2026.2.1 from Claude — verified facts (2026-09-05, Cascy_sword rig):
#   * server: Cascadeur menu "MCP.Start script server" (or `cascadeur.exe --run-script scripts.mcp.start_server`),
#     HTTP on 127.0.0.1:8765; project .mcp.json registers it as MCP server `cascadeur`; tools/cascadeur/casc_run.py
#     posts code to /run without an MCP client; casc_restart.sh recovers after a crash.
#   * pose = write "Local Rotation" of the *_Box_* controllers (fingers: local Z = curl, +Z bends more; Y = twist)
#     and "Position" of the *_MainPoint_* / *_DirectionPoint_* / *_AdditionalPoint_* IK points (global cm).
#   * keys: layers_editor.set_fixed_interpolation_or_key_if_need(track, frame, True); sections default to STEP-like
#     hold -> call set_interpolation(..., "BEZIER") on every key. Animation length = key the last frame + fit_animation_size_by_layers.
#   * to_euler_angles_x_y_z() inverts as Rz*Ry*Rx (rot_from_xyz); store rotations as quaternions (rot_to_q / q_to_rot).
#   * RenderToFile.take_image is deferred and renders the CURRENT scene state: ONE snapshot per script call (goto+snap),
#     wait for the file, then the next. play_to_video_file / play_to_images_sequence CRASH Cascadeur when called from
#     the script server -> render frames one by one and encode with ffmpeg (scene fps is 30, see render info.txt).
#   * FbxSceneLoader.get_fbx_loader needs the VIEW scene (app.current_scene()); export_model bakes joints+mesh+anim.
#   * 调试节奏（用户 2026-09-05）：改姿态只重跑对应 STAGE（~5s）+ 单帧截图（~4s）核对；不出 mp4、不导 FBX、不碰 Blender，全部关键帧确认后才全渲。
#   * 无响应就直接杀（用户 2026-09-05）：播放中 / 弹窗 / 卡死时脚本服务器不应答，不要等用户暂停，taskkill 后 casc_restart.sh 重开、从 .casc 或脚本重建。
#   * 一只手的 MainPoint / DirectionPoint / AdditionalPoint 共用一条 Animation Track（2026-09-06 实测，layer_id_by_obj_id 相同）：
#     给其中任一点打键 = 整条轨道在该帧的当前值都存成键 → 逐帧 pass 要连 MainPoint 一起显式写回，并把网格键区间设 LINEAR。
#   * 求值是异步 + 只算可视范围（2026-09-06 实测，耗掉半天）：set_anim_size 扩出来的帧在 set_visible_range 之前不求值，gpos 读到的全是
#     最后一个可视帧的姿态（整段 act2 曾僵成第一幕末姿势）；扩长后立刻 set_visible_range(0, last)，读非键帧前先 goto 扫几帧 + sleep 5 s，
#     再读两遍确认稳定。另外扩展区间里 BEZIER 段曾整段平直（615→690），先设 LINEAR 让求值可靠，finish 再换 BEZIER。
#   * 窗口最小化时 take_image 永远不落盘（2026-09-05 实测）：截图前确认窗口未最小化（casc_restart.sh 末尾用 PowerShell ShowWindow 还原）。
#   * 改完必重开（用户 2026-09-06）：任何 Cascadeur / Blender 相关的改动交付，最后一步固定是 taskkill 现有实例、重新打开最新文件（.casc / .blend），
#     保证用户看到的就是最新改动；GUI 里留着的是打开时的旧内存副本，不会自己刷新。
#   * AutoPosing / AutoPhysics 等菜单工具没有直接的 API 函数，但官方给了 action id 表（2026-09-06 查 help/category/301）：
#     app.get_action_manager().call_action("AutoPosingTool.AutoPosing" | "AutoPosingTool.Update" | "AutoPhysicsTool.Snap to Auto Physics"
#     | "View.MotionGeneration_Run" | "View.Animation unbaking" | "View.Retargeting_Copy" | "Timeline.Bezier.Bezier on current frame" …)。
#     需要先有正确的选区/时间轴区间（与 GUI 一致）；本仓库尚未实测；官方说明 call_action 以后会逐步换成正式 API。全表见 .claude/skills/ai_videos__cascadeur动作/SKILL.md。
import csc, json, math, os, time
import numpy as np

_MV = scene.model_viewer()
_BV = _MV.behaviour_viewer()
_DV = _MV.data_viewer()
IDS = {_MV.get_object_name(i): i for i in _MV.get_objects()}


def E(rot):
    """csc.math.Rotation -> [x, y, z] degrees (x-y-z euler)."""
    return [round(math.degrees(a), 1) for a in rot.to_euler_angles_x_y_z()]


def R(x, y, z):
    """degrees -> csc.math.Rotation"""
    return csc.math.Rotation.from_euler(math.radians(x), math.radians(y), math.radians(z))


def M(rot):
    return np.array(rot.to_rotation_matrix(), dtype="float32")


def rot_mul(a, b):
    """a * b (apply b in a's local frame)."""
    return csc.math.Rotation.from_rotation_matrix(M(a) @ M(b))


def rot_axis(deg, axis):
    ax = {"x": [1, 0, 0], "y": [0, 1, 0], "z": [0, 0, 1]}[axis]
    return csc.math.Rotation.from_angle_axis(math.radians(deg), np.array(ax, dtype="float32"))


def gpos(name, frame=None):
    frame = scene.get_current_frame() if frame is None else frame
    tr = _BV.get_behaviour_by_name(IDS[name], "Transform")
    d = _BV.get_behaviour_data(tr, "global_position")
    return [float(v) for v in _DV.get_data_value(d, frame)]


def read_box_rot(names, frame=0):
    out = {}
    def mod(model, update, sc):
        for n in names:
            g = update.get_object_by_id(IDS[n]).root_group()
            out[n] = g.node_deep("Local Rotation").value(frame)
    scene.modify_update("read only", mod)
    return out


def _key(model, obj_id, frame):
    lv = scene.layers_viewer()
    track = lv.layer_id_by_obj_id(obj_id)
    model.layers_editor().set_fixed_interpolation_or_key_if_need(track, frame, True)


def set_box_rots(rots, frame, title="Claude pose", key=True):
    """rots: {box_name: csc.math.Rotation (absolute Local Rotation)}"""
    def mod(model, update, sc):
        ids = set()
        for n, r in rots.items():
            g = update.get_object_by_id(IDS[n]).root_group()
            node = g.node_deep("Local Rotation")
            node.set_value(r, frame)
            ids.add(node.data_id())
            if key:
                _key(model, IDS[n], frame)
        sc.run_update(ids, frame)
    return scene.modify_update(title, mod)


def add_box_rots(deltas, frame, title="Claude pose delta", key=True):
    """deltas: {box_name: csc.math.Rotation} applied in the box's local frame (R = R0 * d)."""
    base = read_box_rot(list(deltas), frame)
    return set_box_rots({n: rot_mul(base[n], d) for n, d in deltas.items()}, frame, title, key)


def set_point_pos(positions, frame, title="Claude move point", key=True):
    """positions: {point_name: [x, y, z]} global position of IK point controllers."""
    def mod(model, update, sc):
        ids = set()
        for n, p in positions.items():
            g = update.get_object_by_id(IDS[n]).root_group()
            node = g.node_deep("Position")
            node.set_value(np.array(p, dtype="float32"), frame)
            ids.add(node.data_id())
            if key:
                _key(model, IDS[n], frame)
        sc.run_update(ids, frame)
    return scene.modify_update(title, mod)


def goto(frame):
    scene.set_current_frame(int(frame))


def cam(position, target):
    vs = app.current_scene()
    dvp = vs.active_viewport().domain_viewport()
    s = dvp.camera_struct()
    s.position = np.array(position, dtype="float32")
    s.target = np.array(target, dtype="float32")
    dvp.set_camera_struct(s)


def snap(path, w=1280, h=720, samples=2):
    rtf = app.get_tools_manager().get_tool("RenderToFile")
    rp = csc.tools.RenderParameters()
    rp.width, rp.height, rp.samples = int(w), int(h), int(samples)
    if os.path.exists(path):
        os.remove(path)
    rtf.take_image(app.current_scene(), rp, path)
    return path


def render_video(path, w=1080, h=1920, samples=2):
    rtf = app.get_tools_manager().get_tool("RenderToFile")
    rp = csc.tools.RenderParameters()
    rp.width, rp.height, rp.samples = int(w), int(h), int(samples)
    rtf.play_to_video_file(app.current_scene(), rp, path)
    return path


def export_fbx(path, method="export_all_objects"):
    loader = app.get_tools_manager().get_tool("FbxSceneLoader").get_fbx_loader(app.current_scene())
    s = csc.fbx.FbxSettings()
    s.mode = csc.fbx.FbxSettingsMode.Binary
    s.bake_animation = True
    loader.set_settings(s)
    getattr(loader, method)(path)
    return path


def reload_scene(path=r"C:\Program Files\Cascadeur\samples\Cascy_sword.casc", remove_old=False):
    """Fresh scene from a .casc. remove_old=True closes the other scenes, but that can pop a modal
    save dialog that freezes the script server (seen 2026-09-05) -> default False. Re-exec LIB afterwards."""
    sm = app.get_scene_manager()
    old = list(sm.scenes())
    vs = sm.create_application_scene()
    sm.set_current_scene(vs)
    csc.app.ProjectLoader.load_from(path, vs.domain_scene())
    globals()["scene"] = vs.domain_scene()
    for s in (old if remove_old else []):
        try:
            sm.remove_application_scene(s)
        except Exception:
            pass
    return vs


def bend_deg(side, finger, seg, frame=0):
    """angle between segment before/after joint seg (1=MCP,2=PIP,3=DIP) in degrees."""
    chain = [f"hand_{side}"] + [f"f_{finger}{k}_{side}" for k in (1, 2, 3, 4)]
    a, b, c = (np.array(gpos(n, frame)) for n in (chain[seg - 1], chain[seg], chain[seg + 1]))
    v1 = (b - a) / (np.linalg.norm(b - a) + 1e-9); v2 = (c - b) / (np.linalg.norm(c - b) + 1e-9)
    return float(math.degrees(math.acos(np.clip(np.dot(v1, v2), -1, 1))))


def spread_deg(side, fa, fb, frame=0):
    va = np.array(gpos(f"f_{fa}2_{side}", frame)) - np.array(gpos(f"f_{fa}1_{side}", frame))
    vb = np.array(gpos(f"f_{fb}2_{side}", frame)) - np.array(gpos(f"f_{fb}1_{side}", frame))
    va /= np.linalg.norm(va) + 1e-9; vb /= np.linalg.norm(vb) + 1e-9
    return float(math.degrees(math.acos(np.clip(np.dot(va, vb), -1, 1))))


def rot_from_xyz(e):
    """inverse of Rotation.to_euler_angles_x_y_z (radians): R = Rz * Ry * Rx"""
    return rot_mul(rot_mul(rot_axis(math.degrees(e[2]), "z"), rot_axis(math.degrees(e[1]), "y")), rot_axis(math.degrees(e[0]), "x"))


def rot_to_q(r):
    q = r.to_quaternion(); return [float(q.w()), float(q.x()), float(q.y()), float(q.z())]


def q_to_rot(q):
    return csc.math.Rotation.from_quaternion(*q)


def set_anim_size(n, title="set animation size"):
    """Animation length = fit to keys: key the last frame on the pelvis track, then fit."""
    lv = scene.layers_viewer()
    def mod(model, update, sc):
        le = model.layers_editor()
        le.set_fixed_interpolation_or_key_if_need(lv.layer_id_by_obj_id(IDS["pelvis_MainPoint"]), int(n) - 1, True)
        model.fit_animation_size_by_layers()
    ok = scene.modify_update(title, mod)
    return ok, scene.layers_viewer().frames_count()


def set_interpolation(obj_names, keys, interp="BEZIER", title="set interpolation"):
    """Set the interval interpolation of the section starting at each key frame on every track of obj_names."""
    lv = scene.layers_viewer()
    tracks = {lv.layer_id_by_obj_id(IDS[n]) for n in obj_names}
    mode = getattr(csc.layers.layer.Interpolation, interp)
    done = []
    def mod(model, update, sc):
        le = model.layers_editor()
        for t in tracks:
            lay = lv.layer(t)
            for k in keys:
                if not lay.is_key(k):
                    continue
                def f(section):
                    section.interval.interpolation = mode
                le.change_section(int(k), t, f)
                done.append(k)
    ok = scene.modify_update(title, mod)
    return ok, len(tracks), len(done)


def hide_controllers(mode="View"):
    dvp = app.current_scene().active_viewport().domain_viewport()
    dvp.set_mode_visualizers(getattr(csc.view.ViewportMode, mode))
    return str(dvp.mode_visualizers())


def cam_pin(position, target, tol=2.0):
    """Re-set the viewport camera only if it drifted (set_camera_struct on every call crashed Cascadeur once)."""
    dvp = app.current_scene().active_viewport().domain_viewport()
    s = dvp.camera_struct()
    if np.linalg.norm(np.array(s.position, float) - np.array(position, float)) > tol or \
       np.linalg.norm(np.array(s.target, float) - np.array(target, float)) > tol:
        cam(position, target)
        return "reset"
    return "ok"


def set_visible_range(first, last):
    """Timeline visible/work range (what Play loops over). Extending the animation does NOT widen it;
    a scene grown from 91 to 451 frames still played 0-90 (user report 2026-09-05)."""
    ab = app.current_scene().animation_boundary()
    try:
        ab.first_visible_frame = int(first); ab.last_visible_frame = int(last)
        ab2 = app.current_scene().animation_boundary()
        return (ab2.first_visible_frame, ab2.last_visible_frame)
    except Exception as e:
        return "not settable: " + str(e)[:100]
