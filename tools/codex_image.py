# -*- coding: utf-8 -*-
"""经 Codex CLI 调内置 image_gen 出图（复用本机 ChatGPT 订阅登录，不要 OPENAI_API_KEY）。

Claude 或任何代理都走这里，不直接跑 `codex exec`：先写 request_log 再调用；Codex 在空目录、只读沙箱里
只做一次 image_gen，图片由本脚本从 `$CODEX_HOME/generated_images/<thread_id>/` 拷到目标路径。
内置工具不暴露型号、quality、尺寸与费用：日志记为未知；结果不明不自动重提。规则见 paid_services.md「Codex 内置出图」。

    python tools/codex_image.py --out ai_videos/<剧>/.../xxx.png --prompt-file prompt.txt [--ref a.png --ref b.png]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.service_request import RequestLog

PROVIDER = "codex_imagegen"
OPERATION = "image_gen"
DEFAULT_TIMEOUT = 900

INSTRUCTION = """你是出图执行器。只做一件事：调用一次内置 image_gen 工具生成一张图片。

- 图片描述原样使用下方 <prompt> 里的全文，不增删、不改写、不翻译。
{refs}{transparent}- 不运行任何 shell 命令，不读写文件，不调用其他工具，不搜索网络，不提问。
- 生成后只回复 DONE；工具失败或被拒时只回复 FAILED: 加原因。

<prompt>
{prompt}
</prompt>
"""


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")


def generated_root() -> Path:
    return codex_home() / "generated_images"


def codex_executable() -> str:
    found = shutil.which("codex")
    if not found:
        raise FileNotFoundError("找不到 codex CLI；先安装并 `codex login`（ChatGPT 账户）")
    return found


def instruction(prompt: str, refs: list[Path], transparent: bool) -> str:
    ref_text = ""
    if refs:
        names = "；".join(f"第 {i} 张 {p.name}" for i, p in enumerate(refs, 1))
        ref_text = f"- 附带的 {len(refs)} 张图是参考图，按附带顺序：{names}。prompt 里按这个顺序指认它们。\n"
    alpha = "- 要透明背景：调用时请求 transparent background，保留 alpha。\n" if transparent else ""
    return INSTRUCTION.format(refs=ref_text, transparent=alpha, prompt=prompt.strip())


def command(refs: list[Path], model: str | None) -> list[str]:
    argv = [codex_executable(), "exec", "--json", "--skip-git-repo-check", "--sandbox", "read-only"]
    if model:
        argv += ["--model", model]
    for ref in refs:
        argv += ["--image", str(ref)]
    return argv  # 指令走 stdin：不受 Windows 命令行长度与引号影响


def snapshot(root: Path) -> set[Path]:
    return {p.resolve() for p in root.rglob("*.png")} if root.is_dir() else set()


def parse_events(stdout: str) -> dict[str, Any]:
    """codex exec --json 的 JSONL：取 thread_id、出图条目（revised prompt）、用量与最后回复；不保留 base64。"""
    info: dict[str, Any] = {"thread_id": None, "images": [], "usage": None, "last_message": None, "event_types": {}, "errors": []}

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if isinstance(node.get("thread_id"), str) and not info["thread_id"]:
                info["thread_id"] = node["thread_id"]
            kind = str(node.get("kind") or node.get("type") or "")
            if "image_gen" in kind or "image_generation" in kind:
                info["images"].append({k: node.get(k) for k in ("id", "status", "revisedPrompt", "revised_prompt") if node.get(k) is not None})
            for key, value in node.items():
                if key not in {"result", "image_url", "b64_json"}:
                    walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        kind = str(event.get("type"))
        info["event_types"][kind] = info["event_types"].get(kind, 0) + 1
        if kind == "error" or kind.endswith(".failed"):
            info["errors"].append({k: v for k, v in event.items() if k != "type"})
        if event.get("usage"):
            info["usage"] = event["usage"]
        item = event.get("item")
        if isinstance(item, dict) and item.get("type") in {"agent_message", "AgentMessage"}:
            info["last_message"] = item.get("text") or item.get("content")
        walk(event)
    return info


def rollout_images(thread_id: str | None) -> list[dict[str, Any]]:
    """exec 的 JSONL 不含出图条目；会话记录 sessions/**/rollout-*-<thread_id>.jsonl 有 savedPath、revisedPrompt、failure。"""
    if not thread_id:
        return []
    items: dict[str, dict[str, Any]] = {}
    for path in (codex_home() / "sessions").rglob(f"*{thread_id}.jsonl"):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                item = json.loads(line).get("payload", {}).get("item", {})
            except (ValueError, AttributeError):
                continue
            if isinstance(item, dict) and str(item.get("kind", "")).startswith("image_gen"):
                items[item.get("id")] = {k: item.get(k) for k in ("id", "status", "revisedPrompt", "transparentBackground", "failure", "savedPath")}
    return list(items.values())


def pick_new(before: set[Path], after: set[Path], thread_id: str | None) -> list[Path]:
    new = sorted(after - before, key=lambda p: p.stat().st_mtime)
    return [p for p in new if thread_id and p.parent.name == thread_id]


def generate(out: Path, prompt: str, refs: list[Path], *, transparent: bool = False, model: str | None = None,
             timeout: int = DEFAULT_TIMEOUT, overwrite: bool = False) -> dict[str, Any]:
    out = out.resolve()
    if out.suffix.lower() != ".png":
        raise ValueError("内置 image_gen 产出 PNG；--out 用 .png")
    if out.exists() and not overwrite:
        raise FileExistsError(f"{out} 已存在；换带版本号的文件名，确需替换加 --overwrite")
    missing = [str(p) for p in refs if not p.is_file()]
    if missing:
        raise FileNotFoundError("参考图不存在：" + "，".join(missing))
    if not prompt.strip():
        raise ValueError("prompt 为空")
    refs = [p.resolve() for p in refs]
    log = RequestLog(out)
    text = instruction(prompt, refs, transparent)
    argv = command(refs, model)
    root = generated_root()
    request = {
        "service": "Codex CLI 内置 image_gen（ChatGPT 订阅额度）",
        "prompt": prompt, "instruction": text, "argv": argv, "files": refs, "output": str(out),
        "transparent_background": transparent, "codex_model": model or "用户 config 默认",
        "image_model": "未知（内置工具不暴露）", "quality": "未知", "size": "未知", "cost": "未知",
        "sandbox": "read-only", "timeout_s": timeout, "generated_root": str(root),
    }

    def call() -> dict[str, Any]:
        before = snapshot(root)
        with tempfile.TemporaryDirectory(prefix="codex_image_") as work:  # 空目录：不加载仓库 AGENTS.md
            try:
                done = subprocess.run(argv, input=text, cwd=work, capture_output=True, text=True,
                                      encoding="utf-8", errors="replace", timeout=timeout)
                stdout, stderr, code, timed_out = done.stdout, done.stderr, done.returncode, False
            except subprocess.TimeoutExpired as e:
                stdout = e.stdout.decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
                stderr = e.stderr.decode("utf-8", "replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
                code, timed_out = None, True
        info = parse_events(stdout)
        info["images"] += rollout_images(info["thread_id"])
        saved_paths = [Path(i["savedPath"]) for i in info["images"] if i.get("savedPath") and Path(i["savedPath"]).is_file()]
        found = saved_paths or pick_new(before, snapshot(root), info["thread_id"])
        summary = {"returncode": code, "timed_out": timed_out, "stderr_tail": stderr[-2000:], **info,
                   "generated": [RequestLog.file(p) for p in found]}
        if not found:
            raise RuntimeError("没有拿到新图（结果未知，不自动重提；先查 generated_images 与 Codex 会话）："
                               + json.dumps({k: summary[k] for k in ("returncode", "timed_out", "last_message", "errors", "images")},
                                            ensure_ascii=False) + " " + stderr[-500:])
        out.parent.mkdir(parents=True, exist_ok=True)
        saved = []
        for i, src in enumerate(found):
            dest = out if i == 0 else out.with_name(f"{out.stem}_alt{i}{out.suffix}")
            if dest.exists() and dest != out:
                continue
            part = dest.with_name(dest.stem + ".codex-part" + dest.suffix)  # 先落临时名再改名：别的进程可能在等这张图作参考
            shutil.copy2(src, part)
            part.replace(dest)
            saved.append(RequestLog.file(dest))
        summary["saved"] = saved
        return summary

    return log.invoke(PROVIDER, OPERATION, request, call)


def render(prompt: str, refs: list[Path], out: Path, aspect: str | None = None, *, timeout: int = DEFAULT_TIMEOUT) -> str:
    """出图器（gen_*）用：画幅写进 prompt，覆盖 out（调用方已决定要出这张），返回 thread_id 作日志标签。"""
    text = prompt.strip() + (f"\n画幅比例 {aspect}。" if aspect else "")
    result = generate(out, text, refs, timeout=timeout, overwrite=True)
    return f"codex_thread={result['thread_id']}"


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="经 Codex CLI 内置 image_gen 出图，先记请求日志")
    ap.add_argument("--out", required=True, type=Path, help="ai_videos 下的目标 .png（决定日志归属）")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompt")
    group.add_argument("--prompt-file", type=Path)
    ap.add_argument("--ref", action="append", default=[], type=Path, help="参考图，可重复，按顺序附带")
    ap.add_argument("--transparent", action="store_true")
    ap.add_argument("--model", help="Codex 代理模型（不是图像模型）；缺省用 ~/.codex/config.toml")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()
    prompt = args.prompt if args.prompt is not None else args.prompt_file.read_text(encoding="utf-8")
    result = generate(args.out, prompt, args.ref, transparent=args.transparent, model=args.model,
                      timeout=args.timeout, overwrite=args.overwrite)
    for item in result["saved"]:
        print(item["path"])
    revised = [i.get("revisedPrompt") or i.get("revised_prompt") for i in result["images"]]
    if any(r and r.strip() != prompt.strip() for r in revised):
        print("注意：image_gen 改写了 prompt，见 request_log 的 images[].revisedPrompt", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
