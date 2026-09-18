# -*- coding: utf-8 -*-
"""即梦（Jimeng / Dreamina）OpenAPI 适配器：签名 + 提交 + 轮询。

能干什么、不能干什么（2026-09-17 读文档 + 实测）
----------------------------------------------
这个 API 只有**两个能力**，都是「Agent 级」的，不是「模型级」的：

    pippit_novel_agent            短剧：script_analysis → narration_design → character_generate
                                  → scene_generate → storyboard_design → shot_video_generate
                                  → shot_video_compose   （分镜短片走 Seedance 2.0）
    pippit_avatar_marketing_agent 营销视频：generate_video

**它没有任意文生图接口。** `character_generate` / `scene_generate` 看着像出图，但它们绑在一条
由 `script_analysis`（上传剧本文件）建起的 thread 上，产出什么由 Agent 自己决定——
给不了「p19 独轮串车的正视图」这种任意 prompt。所以 sk1 的物件三视图**不能**走这条路，
它的用处在别处：**整集短剧的自动生成**（上传剧本 → 直出分镜短片 → 合成成片）。

鉴权（文档 §2，已实测通过）
    StringToSign = METHOD \n PATH \n CANONICAL_QUERY \n CONTENT_TYPE \n
                   SHA256(body) \n TIMESTAMP \n NONCE \n ACCESS_KEY
    Signature    = Base64URL( HMAC-SHA256(SK, StringToSign) )   # 去掉 = padding
常见失败：时钟偏差 > 300 s → 10006；body SHA 必须小写十六进制；nonce 300 s 内不可重复；
Content-Type 参与签名，必须与实际发送的完全一致。

实测证据：用一个不存在的 run_id 打 `/novel/query` → `code 20001 task not found`
（不是 10002 AK 不存在、不是 10006 签名失败、不是 10007 权限不足）＝ 签名与账号都对。

用法（仓库根目录）：
    python tools/jimeng_fetch.py query --run-id biz-xxx
    python tools/jimeng_fetch.py query --task-id 7660...
    python tools/jimeng_fetch.py submit --path /agent_openapi/v1/novel/submit --body body.json
    python tools/jimeng_fetch.py probe          # 只验签，不花 token

key 只从环境 / 仓库根 gitignored `.env` 读（`SEEDANCE_ACCESS_KEY` / `SEEDANCE_SECRET_KEY`）。
注意计费：提交即预扣 token，失败全额返还；token 包与网页端积分不通用。
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from urllib.parse import quote

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
HOST = "https://jimeng.jianying.com"
CONTENT_TYPE = "application/json"
CTX = ssl.create_default_context()


def keys() -> tuple[str, str]:
    ak, sk = os.environ.get("SEEDANCE_ACCESS_KEY"), os.environ.get("SEEDANCE_SECRET_KEY")
    if not (ak and sk):
        env = REPO / ".env"
        if env.is_file():
            for line in env.read_text(encoding="utf-8").splitlines():
                if line.startswith("SEEDANCE_ACCESS_KEY="):
                    ak = line.split("=", 1)[1].strip()
                elif line.startswith("SEEDANCE_SECRET_KEY="):
                    sk = line.split("=", 1)[1].strip()
    if not (ak and sk):
        raise SystemExit("缺 SEEDANCE_ACCESS_KEY / SEEDANCE_SECRET_KEY（写进仓库根 .env，已 gitignore）")
    return ak, sk


def canonical_query(params: dict | None) -> str:
    if not params:
        return ""
    parts = []
    for k in sorted(params):
        raw = params[k]
        for v in sorted("" if x is None else str(x) for x in (raw if isinstance(raw, list) else [raw])):
            parts.append(f"{quote(str(k), safe='~')}={quote(v, safe='~')}")
    return "&".join(parts)


def call(path: str, body: dict, *, query: dict | None = None, method: str = "POST") -> dict:
    ak, sk = keys()
    raw = json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    body_sha = hashlib.sha256(raw).hexdigest()          # 必须小写十六进制
    cq = canonical_query(query)
    ts, nonce = str(int(time.time())), uuid.uuid4().hex
    sts = "\n".join([method, path, cq, CONTENT_TYPE, body_sha, ts, nonce, ak])
    sig = base64.urlsafe_b64encode(
        hmac.new(sk.encode("utf-8"), sts.encode("utf-8"), hashlib.sha256).digest()).rstrip(b"=").decode()
    url = HOST + path + (("?" + cq) if cq else "")
    req = urllib.request.Request(url, data=raw, method=method, headers={
        "Content-Type": CONTENT_TYPE, "X-Agent-Access-Key": ak, "X-Agent-Timestamp": ts,
        "X-Agent-Nonce": nonce, "X-Agent-Body-SHA256": body_sha,
        "X-Agent-Signature-Method": "HMAC-SHA256", "X-Agent-Version": "v1", "X-Agent-Signature": sig})
    try:
        with urllib.request.urlopen(req, timeout=120, context=CTX) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"即梦 {method} {path} HTTP {e.code}：{e.read().decode('utf-8', 'replace')[:400]}")


ERRS = {"10002": "AK 不存在", "10003": "AK 被禁用 / 冻结", "10004": "未授权 / UserID 缺失",
        "10005": "未知能力 / 动作", "10006": "签名校验失败（查时钟 / body SHA / padding）",
        "10007": "身份权限不满足（如需即梦 Ultra 会员）", "10008": "请求频率超限",
        "20001": "任务不存在", "20002": "Token 余额不足 / 预扣失败"}


def explain(d: dict) -> str:
    code = str(d.get("code", "?"))
    return f"code={code} {d.get('message', '')}" + (f"　（{ERRS[code]}）" if code in ERRS else "")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("query"); q.add_argument("--run-id"); q.add_argument("--task-id")
    q.add_argument("--path", default="/agent_openapi/v1/novel/query")
    s = sub.add_parser("submit"); s.add_argument("--path", required=True); s.add_argument("--body", required=True, type=Path)
    sub.add_parser("probe")
    a = ap.parse_args()

    if a.cmd == "probe":
        # 只验签：用一个必然不存在的 run_id。20001 ＝ 签名与账号都对
        d = call("/agent_openapi/v1/novel/query", {"run_id": "probe-" + uuid.uuid4().hex[:12]})
        print("验签：", explain(d))
        print("结论：" + ("签名与账号 OK（20001 只是任务不存在）" if str(d.get("code")) == "20001" else "见上面的 code"))
        return
    if a.cmd == "query":
        if not (a.run_id or a.task_id):
            raise SystemExit("--run-id 与 --task-id 给一个")
        body = {"run_id": a.run_id} if a.run_id else {"task_id": a.task_id}
        d = call(a.path, body)
    else:
        d = call(a.path, json.loads(a.body.read_text(encoding="utf-8")))
    print(explain(d))
    print(json.dumps(d.get("data", {}), ensure_ascii=False, indent=1)[:3000])


if __name__ == "__main__":
    main()
