# -*- coding: utf-8 -*-
"""Hyper3D / Rodin 适配器：prompt（+参考图）→ 原始网格 GLB。**无头、可脚本化。**

为什么不走 BlenderMCP 的那条路
------------------------------
`mcp__blender__generate_hyper3d_model_via_text` 要一个开着的 Blender GUI + addon，
而且开关 `blendermcp_use_hyper3d` 是 **per-scene** 的（换 .blend 就得重开，这是误判
「没装好」的头号来源，`ai_video.md` rule 4h §G）。那条路适合人坐在电脑前试一个东西，
**不适合进 pipeline**：pipeline 要能在 CI 里、在批处理里、对着一张资产清单跑。
本文件直接打 Rodin 的 HTTP API，请求体逐字照 `addon.py` 的 `create_rodin_job_main_site`
（那是已验证能跑通的形状），所以两条路生成的东西是同一个东西。

产物是**原始网格**，不是可用白模 —— 朝向随机、尺度随机、自带烤死的材质。
下一步必须过同一道闸门（vendor 无关，见 `tools/whitemodel_normalize.py` 抬头）：

    blender -b --factory-startup --python tools/whitemodel_normalize.py -- \
        --src <raw.glb> --spec <object.toml> --out <{name}.blend>

用法（仓库根目录）：
    python tools/hyper3d_fetch.py --prompt "a Song dynasty wooden handcart" --out raw.glb
    python tools/hyper3d_fetch.py --prompt "..." --image ref/a.png --image ref/b.png --out raw.glb
    python tools/hyper3d_fetch.py --prompt "..." --bbox 2.4 1.1 1.0 --out raw.glb --tier Regular

key 只从环境 / 仓库根 gitignored `.env` 里读（`HYPER3D_API_KEY`），**不进任何被 git 跟踪的文件**。
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid as _uuid
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
API = "https://hyperhuman.deemos.com/api/v2"
CTX = ssl.create_default_context()


def api_key() -> str:
    key = os.environ.get("HYPER3D_API_KEY")
    if not key:
        env = REPO / ".env"
        if env.is_file():
            for line in env.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("HYPER3D_API_KEY="):
                    key = line.split("=", 1)[1].strip()
                    break
    if not key:
        raise SystemExit("缺 HYPER3D_API_KEY：写进仓库根的 .env（已 gitignore），或设进环境变量")
    return key


def _multipart(fields: list[tuple[str, str | None, bytes | None, str | None]]) -> tuple[bytes, str]:
    """fields: (name, text_value | None, file_bytes | None, filename | None)。"""
    boundary = "----hyper3d" + _uuid.uuid4().hex
    out = bytearray()
    for name, text, blob, filename in fields:
        out += f"--{boundary}\r\n".encode()
        if blob is None:
            out += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
            out += (text or "").encode("utf-8") + b"\r\n"
        else:
            ctype = mimetypes.guess_type(filename or "")[0] or "application/octet-stream"
            out += (f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'
                    f"Content-Type: {ctype}\r\n\r\n").encode()
            out += blob + b"\r\n"
    out += f"--{boundary}--\r\n".encode()
    return bytes(out), f"multipart/form-data; boundary={boundary}"


def _retry(what: str, fn, tries: int = 4):
    """网络抖动不是失败。2026-09-17 实测：p19 的 /rodin 调用撞上一次 read timeout，
    整个物件就被判成 rodin-failed —— 而重跑一次就过了。HTTP 4xx/5xx 仍然直接判死
    （那是真的出错了，重试只会多花一次钱）。"""
    for i in range(tries):
        try:
            return fn()
        except urllib.error.HTTPError:
            raise
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if i == tries - 1:
                raise SystemExit(f"Rodin {what} 连续 {tries} 次网络失败：{e}")
            print(f"  ! {what} 网络抖动（{type(e).__name__}），{2 ** i * 5}s 后重试 {i + 1}/{tries - 1}")
            time.sleep(2 ** i * 5)


def _post(path: str, key: str, *, body: bytes, ctype: str) -> dict:
    def once() -> dict:
        req = urllib.request.Request(f"{API}/{path}", data=body, method="POST",
                                     headers={"Authorization": f"Bearer {key}", "Content-Type": ctype})
        with urllib.request.urlopen(req, timeout=180, context=CTX) as r:
            return json.loads(r.read().decode("utf-8"))
    try:
        return _retry(path, once)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Rodin {path} HTTP {e.code}：{e.read().decode('utf-8', 'replace')[:400]}")


def post_json(path: str, key: str, payload: dict) -> dict:
    """JSON 调用走 curl，不走 urllib。

    2026-09-17 实测：`/status` 轮询在 urllib 下反复抛
    `SSL: UNEXPECTED_EOF_WHILE_READING`，连退避重试也救不回来（p42 连挂两轮）；
    curl 的 `--retry-all-errors` 在同一条网络上一次就过。这与 `image_fetch.py`
    当初从 urllib 换到 curl 是同一个坑、同一个解法。
    multipart 的建任务调用仍走 urllib —— 它只发一次、且 body 是二进制拼好的。
    """
    body = json.dumps(payload).encode()
    cmd = ["curl", "-sS", "--retry", "6", "--retry-all-errors", "--retry-delay", "4",
           "--retry-connrefused", "-m", "180", "-X", "POST", f"{API}/{path}",
           "-H", f"Authorization: Bearer {key}", "-H", "Content-Type: application/json",
           "--data-binary", "@-"]
    r = subprocess.run(cmd, input=body, capture_output=True)
    if r.returncode != 0 or not r.stdout:
        raise SystemExit(f"Rodin {path} curl 失败（exit {r.returncode}）：{r.stderr.decode('utf-8', 'replace')[:300]}")
    try:
        return json.loads(r.stdout.decode("utf-8"))
    except json.JSONDecodeError:
        raise SystemExit(f"Rodin {path} 返回的不是 JSON：{r.stdout.decode('utf-8', 'replace')[:300]}")


def create_job(key: str, prompt: str | None, images: list[Path], bbox: list[float] | None,
               tier: str, mesh_mode: str) -> dict:
    fields: list[tuple[str, str | None, bytes | None, str | None]] = []
    for i, p in enumerate(images):
        fields.append(("images", None, p.read_bytes(), f"{i:04d}{p.suffix}"))
    fields += [("tier", tier, None, None), ("mesh_mode", mesh_mode, None, None)]
    # 白模只承载几何，材质在闸门里会被无条件剥掉 —— 贴图给最低档就行（API 不接受 "None"，
    # 合法值只有 legacy/minimum/extreme-low/low/medium/high/extreme-high）
    fields.append(("texture_mode", "minimum" if mesh_mode == "Raw" else "high", None, None))
    if prompt:
        fields.append(("prompt", prompt, None, None))
    if bbox:
        # API 只吃整数比例（不是米）——按最大边归一到 100 再取整，比例不变
        m = max(bbox)
        fields.append(("bbox_condition", json.dumps([max(1, round(v / m * 100)) for v in bbox]), None, None))
    body, ctype = _multipart(fields)
    data = _post("rodin", key, body=body, ctype=ctype)
    if "uuid" not in data:
        raise SystemExit(f"Rodin 没给 uuid：{json.dumps(data, ensure_ascii=False)[:400]}")
    return data


def wait(key: str, sub_key: str, timeout_s: int) -> None:
    t0 = time.time()
    last = ""
    while True:
        data = post_json("status", key, {"subscription_key": sub_key})
        states = [j["status"] for j in data.get("jobs", [])]
        cur = "/".join(sorted(set(states))) or "?"
        if cur != last:
            print(f"  [{int(time.time() - t0):4d}s] {cur}")
            last = cur
        if states and all(s == "Done" for s in states):
            return
        if any(s in ("Failed", "Canceled") for s in states):
            raise SystemExit(f"Rodin 任务失败：{states}")
        if time.time() - t0 > timeout_s:
            raise SystemExit(f"Rodin 超时（{timeout_s}s），最后状态 {states}")
        time.sleep(5)


def download(key: str, task_uuid: str, out: Path) -> Path:
    data = post_json("download", key, {"task_uuid": task_uuid})
    items = data.get("list", [])
    glb = next((i for i in items if i["name"].lower().endswith(".glb")), None)
    if glb is None:
        raise SystemExit(f"下载列表里没有 .glb：{[i.get('name') for i in items]}")
    out.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["curl", "-sS", "-L", "--retry", "6", "--retry-all-errors", "--retry-delay", "4",
           "-m", "600", "-o", str(out), "-w", "%{http_code}", glb["url"]]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip().startswith("2") or not out.is_file() or out.stat().st_size == 0:
        raise SystemExit(f"Rodin 下载失败（exit {r.returncode}, http {r.stdout.strip()}）：{r.stderr[:300]}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", default=None, help="英文描述（Rodin 只吃英文）")
    ap.add_argument("--image", action="append", default=[], type=Path, help="参考图，可重复；多视角比单图稳得多")
    ap.add_argument("--bbox", nargs=3, type=float, default=None, metavar=("L", "W", "H"),
                    help="长宽高比例（不是米；Rodin 只用它定比例，内部会归一成整数）")
    ap.add_argument("--tier", default="Sketch", choices=("Sketch", "Regular"),
                    help="Sketch 快而糙、适合试；Regular 慢而细")
    ap.add_argument("--mesh-mode", default="Raw", choices=("Raw", "Quad"))
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    if not args.prompt and not args.image:
        raise SystemExit("--prompt 与 --image 至少给一个")

    key = api_key()
    print(f"→ 建任务：tier={args.tier} mesh={args.mesh_mode} images={len(args.image)} bbox={args.bbox}")
    job = create_job(key, args.prompt, args.image, args.bbox, args.tier, args.mesh_mode)
    task_uuid, sub = job["uuid"], job["jobs"]["subscription_key"]
    print(f"  uuid={task_uuid}")
    wait(key, sub, args.timeout)
    out = download(key, task_uuid, args.out)
    print(f"✓ {out}  {out.stat().st_size / 1024:.0f} KB")
    print(f"  下一步（闸门，vendor 无关）：blender -b --factory-startup "
          f"--python tools/whitemodel_normalize.py -- --src {out} --spec <object.toml> --out <{out.stem}.blend>")


if __name__ == "__main__":
    main()
