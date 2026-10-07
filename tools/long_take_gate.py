"""连续长镜输入指纹闸门；视频差异候选不能代替独立视觉审片。"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_inputs(shot: Path, prompt: str, references: list[Path]) -> list[str]:
    contract_path = shot.parent / "planning/continuous_take.json"
    if not contract_path.is_file():
        return ["连续长镜缺planning/continuous_take.json输入审查契约"]
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    errors = []
    if contract.get("prompt_sha256") != hashlib.sha256(prompt.encode()).hexdigest():
        errors.append("连续长镜prompt改后未重审输入")
    expected = {str(Path(r["path"]).resolve()): r["sha256"] for r in contract.get("references", [])}
    if expected != {str(p.resolve()): sha(p) for p in references}:
        errors.append("连续长镜参考集合或文件SHA与输入审查不一致")
    if contract.get("input_review", {}).get("status") != "passed":
        errors.append("连续长镜输入冲突仍未解决")
    for token in ("一镜到底", "叠化", "溶解", "连续", *contract.get("required_prompt_tokens", [])):
        if token not in prompt:
            errors.append(f"连续长镜缺明确约束：{token}")
    for record in contract.get("evidence", []):
        p = Path(record["path"])
        if not p.is_file() or sha(p) != record["sha256"]:
            errors.append(f"连续长镜证据缺失或过期：{p.name}")
    if not contract.get("evidence"):
        errors.append("连续长镜没有输入/航线独立审查证据")
    ownership = contract.get("item_owners", {})
    if not ownership or any(not isinstance(owner, str) or not owner for owner in ownership.values()):
        errors.append("连续长镜持物没有逐件唯一归属")
    if contract.get("endpoint_drift_count", 0) >= 2:
        terminal = contract.get("terminal_framing", {})
        path = terminal.get("path")
        if (not path or terminal.get("status") != "passed"
                or expected.get(str(Path(path).resolve())) != terminal.get("sha256")):
            errors.append("连续长镜终点重复漂移，缺少已审且实际上传的终点构图帧")
        actors = terminal.get("actors", {})
        required_actors = contract.get("final_framing_constraints", {}).get("actors", [])
        if (not actors or not set(required_actors).issubset(actors)
                or any(not r.get("all_in_frame") or r.get("fraction", 1) > .4 or r.get("foot_margin", 0) < .15 for r in actors.values())):
            errors.append("连续长镜终点构图帧的人物框/脚下留白未验收")
    if contract.get("endpoint_drift_count", 0) >= 3 and contract.get("generation_mode") != "first_last_frame":
        errors.append("连续长镜普通终点参考再次失效，必须切换明确首尾帧模式并审查实际端点")
    if contract.get("generation_mode") == "first_last_frame":
        errors.extend(check_endpoints(contract, references))
    route_path = contract.get("route_readback")
    if not route_path or not Path(route_path).is_file():
        errors.append("连续长镜缺最终blend航线回读")
    else:
        route = json.loads(Path(route_path).read_text(encoding="utf-8"))
        if not route.get("fixed_lens") or not route.get("no_camera_cuts") or route.get("min_clearance_m", 0) < 0.6:
            errors.append("连续长镜航线固定焦距/无切机位/净空未通过")
        framing = contract.get("final_framing_constraints")
        if framing:
            projected = route.get("final_framing", {})
            for actor in framing["actors"]:
                row = projected.get(actor, {})
                if (not row.get("all_in_frame") or row.get("fraction", 1) > framing["max_fraction"]
                        or row.get("foot_margin", 0) < framing["min_foot_margin"]):
                    errors.append(f"连续长镜终点全身/留白未通过：{actor}")
            if route.get("final_hold_s", 0) < framing["min_hold_s"]:
                errors.append("连续长镜终点停稳不足")
    return errors


def check_endpoints(contract: dict, references: list[Path]) -> list[str]:
    """首尾帧实际只有两个上传图；身份由独立验收的端点与上游来源共同证明。"""
    errors = []
    endpoints = contract.get("endpoint_control", {})
    actual = {str(p.resolve()): sha(p) for p in references}
    if len(references) != 2:
        errors.append("首尾帧模式必须明确实际上传的两个端点，不能把其他参考冒充上传")
    for role in ("first", "last"):
        row = endpoints.get(role, {})
        path = row.get("path")
        if (not path or row.get("status") != "passed"
                or actual.get(str(Path(path).resolve())) != row.get("sha256")):
            errors.append(f"首尾帧{role}缺已独立验收且实际上传的图像")
    if endpoints.get("last", {}).get("sha256") != contract.get("terminal_framing", {}).get("sha256"):
        errors.append("首尾帧last与已审终点构图不一致")
    sources = endpoints.get("identity_sources", [])
    for row in sources:
        path = Path(row["path"])
        if not path.is_file() or sha(path) != row["sha256"]:
            errors.append(f"首尾帧上游人物身份来源已变：{path.name}")
        if row.get("character") not in path.parts:
            errors.append(f"首尾帧身份来源不属于登记角色：{path.name}")
    if set(endpoints.get("characters", [])) != {row.get("character") for row in sources}:
        errors.append("首尾帧人物与上游身份来源集合不一致")
    return errors


def freeze_inputs(shot: Path, output: Path) -> dict:
    """冻结已审输入的真实字节，后续审稿修订不覆盖收费提交的证据版本。"""
    contract_path = shot.parent / "planning/continuous_take.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    text = shot.read_text(encoding="utf-8")
    prompt = re.search(r"## Seedance prompt[^\n]*\n+```text\n(.*?)\n```", text, re.S)[1]
    references = [Path(row["path"]) for row in contract["references"]]
    errors = check_inputs(shot, prompt, references)
    if errors:
        raise ValueError("不能冻结未通过输入：" + "；".join(errors))
    records = [*contract["references"], *contract["evidence"],
               *contract.get("endpoint_control", {}).get("identity_sources", []),
               {"path":str(shot),"sha256":sha(shot)}, {"path":str(contract_path),"sha256":sha(contract_path)}]
    output.mkdir(parents=True, exist_ok=False)
    frozen = []
    unique = {str(Path(row["path"]).resolve()):row["sha256"] for row in records}
    for n, (original, expected) in enumerate(unique.items(), 1):
        source = Path(original)
        target = output / f"{n:02d}_{source.name}"
        shutil.copy2(source, target)
        if sha(target) != expected:
            raise ValueError(f"冻结时证据发生变化：{source.name}")
        frozen.append({"original":original,"snapshot":str(target),"sha256":expected})
    result = {"prompt_sha256":contract["prompt_sha256"],"files":frozen}
    (output / "index.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def scan(video: Path, out: Path) -> dict:
    import numpy as np
    from PIL import Image, ImageDraw

    out.mkdir(parents=True, exist_ok=True)
    probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_frames", "-show_entries", "stream=avg_frame_rate:format=duration:frame=best_effort_timestamp_time", "-of", "json", str(video)], capture_output=True, text=True, check=True).stdout)
    a, b = map(int, probe["streams"][0]["avg_frame_rate"].split("/"))
    fps = a / b
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-vf", "scale=192:108", "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, 108, 192)
    timestamps = [float(f["best_effort_timestamp_time"]) for f in probe.get("frames", [])]
    if len(timestamps) != len(frames) or any(t2 < t1 for t1, t2 in zip(timestamps, timestamps[1:])):
        raise ValueError("解码帧与实际PTS不一致，不能生成连续性时间证据")
    timestamps = [t - timestamps[0] for t in timestamps]
    differences = np.mean(np.abs(np.diff(frames.astype(np.int16), axis=0)), axis=(1, 2))
    candidates = sorted(range(len(differences)), key=lambda i: float(differences[i]), reverse=True)[:12]
    report = {"take_sha256": sha(video), "decoded_frames": len(frames), "fps": fps, "duration_s": float(probe["format"]["duration"]), "time_basis": "原始解码帧best_effort_timestamp_time；不补帧、不按名义fps推时刻", "purpose": "全部帧差异排名只提供疑点，不证明无叠化/变形", "candidates": [{"t": timestamps[i+1], "difference": float(differences[i])} for i in candidates]}
    (out / "continuity_scan.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    regular = [i * 0.25 for i in range(int(report["duration_s"] * 4))]
    selected = sorted(set(regular + [max(0, min(report["duration_s"]-0.04, timestamps[i+1]+delta)) for i in candidates for delta in (-0.125, 0, 0.125)]))
    for page in range((len(selected)+23)//24):
        sheet = Image.new("RGB", (1920, 1740), (25, 25, 25))
        draw = ImageDraw.Draw(sheet)
        for cell, t in enumerate(selected[page*24:(page+1)*24]):
            data = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(video), "-frames:v", "1", "-vf", "scale=480:270", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
            if len(data) != 480*270*3:
                continue
            x, y = cell%4*480, cell//4*290
            sheet.paste(Image.frombytes("RGB", (480, 270), data), (x, y+20))
            draw.text((x+5, y+3), f"{t:.3f}s", fill="white")
        sheet.save(out / f"continuity_{page+1:02d}.jpg", quality=92)
    return {k:v for k,v in report.items() if k != "candidates"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(scan(args.video, args.output), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
