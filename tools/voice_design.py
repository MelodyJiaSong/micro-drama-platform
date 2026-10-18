# -*- coding: utf-8 -*-
"""ElevenLabs 声音设计与台词合成：按文字描述设计一个新声音（不克隆、不上传参考音频），再用它念台词。

三步，每次 HTTP 都经 `RequestLog` 先落请求再调用（paid_services.md）；音频直接写盘，日志只记摘要
（时长、字节数、sha256），不把 base64 / 二进制塞进日志。归属由 `--target` 决定：放在
`ai_videos/{剧}/2_世界观人设/characters/{卡}/voice/` 下，日志落 `characters/request_log.md`。

    python tools/voice_design.py design --target <卡>/voice/design_01 --description "..." --text "..." [--model eleven_ttv_v3] [--seed N]
    python tools/voice_design.py save   --target <卡>/voice --generated-voice-id ID --name NAME --description "..."
    python tools/voice_design.py tts    --target <卡>/voice/lines/xxx.mp3 --voice-id ID --text "..." [--model eleven_v3]

不支持 `reference_audio_base64`：原版语音是第三方版权素材，只供人耳参考，不上传给生成服务（本剧 refs.md）。
2026-10-18：Voice Design 在官方帮助页标为 experimental，商用条款未确认——产出先作试验，进成片由用户决定。
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
import uuid
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from tools import image_fetch as el  # noqa: E402  key 读取与 curl（不把 key 打进日志）
from tools.service_request import RequestLog  # noqa: E402

OUTPUT_FORMAT = "mp3_44100_128"


def _post(path: str, key: str, payload: dict, *, timeout: int = 300) -> tuple[int, bytes]:
    body = el.TMP / f"body_{uuid.uuid4().hex}.json"
    body.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    try:
        return el._curl(["-X", "POST", f"{el.API}{path}", "-H", f"xi-api-key: {key}",
                         "-H", "Content-Type: application/json", "--data-binary", f"@{body}"], timeout=timeout)
    finally:
        body.unlink(missing_ok=True)


def _check(code: int, data: bytes) -> None:
    if not 200 <= code < 300:
        raise SystemExit(f"ElevenLabs HTTP {code}：{data.decode('utf-8', 'replace')[:300]}")


def _digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def design(target: Path, description: str, text: str | None, model: str, seed: int | None) -> dict:
    key = el.api_key()
    target.mkdir(parents=True, exist_ok=True)
    payload = {"voice_description": description, "model_id": model}
    if text:
        payload["text"] = text
    else:
        payload["auto_generate_text"] = True
    if seed is not None:
        payload["seed"] = seed
    path = f"/text-to-voice/design?output_format={OUTPUT_FORMAT}"

    def call() -> dict:
        code, data = _post(path, key, payload)
        _check(code, data)
        d = json.loads(data)
        previews = []
        for i, p in enumerate(d.get("previews", []), 1):
            audio = base64.b64decode(p["audio_base_64"])
            out = target / f"preview_{i}.mp3"
            out.write_bytes(audio)
            previews.append({"file": out.name, "generated_voice_id": p["generated_voice_id"],
                             "duration_secs": p.get("duration_secs"), "bytes": len(audio), "sha256": _digest(audio)})
        return {"http_status": code, "text": d.get("text"), "previews": previews}

    result = RequestLog(target / "previews.json").invoke(
        "elevenlabs", "POST /v1/text-to-voice/design",
        {"method": "POST", "url": el.API + path, "body": payload, "output_dir": str(target)}, call)
    (target / "previews.json").write_text(json.dumps({"request": payload, **result}, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def save(target: Path, generated_voice_id: str, name: str, description: str) -> dict:
    key = el.api_key()
    target.mkdir(parents=True, exist_ok=True)
    payload = {"voice_name": name, "voice_description": description, "generated_voice_id": generated_voice_id}

    def call() -> dict:
        code, data = _post("/text-to-voice", key, payload)
        _check(code, data)
        d = json.loads(data)
        return {"http_status": code, "voice_id": d.get("voice_id"), "name": d.get("name")}

    out = target / "voice.json"
    result = RequestLog(out).invoke("elevenlabs", "POST /v1/text-to-voice",
                                    {"method": "POST", "url": el.API + "/text-to-voice", "body": payload}, call)
    out.write_text(json.dumps({**payload, **result}, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def tts(target: Path, voice_id: str, text: str, model: str, settings: dict | None) -> dict:
    key = el.api_key()
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {"text": text, "model_id": model}
    if settings:
        payload["voice_settings"] = settings
    path = f"/text-to-speech/{voice_id}?output_format={OUTPUT_FORMAT}"

    def call() -> dict:
        code, data = _post(path, key, payload)
        _check(code, data)
        target.write_bytes(data)
        return {"http_status": code, "file": str(target), "bytes": len(data), "sha256": _digest(data)}

    return RequestLog(target).invoke("elevenlabs", "POST /v1/text-to-speech",
                                     {"method": "POST", "url": el.API + path, "voice_id": voice_id, "body": payload}, call)


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="step", required=True)
    a = sub.add_parser("design")
    a.add_argument("--target", required=True)
    a.add_argument("--description", required=True)
    a.add_argument("--text")
    a.add_argument("--model", default="eleven_ttv_v3", choices=("eleven_ttv_v3", "eleven_multilingual_ttv_v2"))
    a.add_argument("--seed", type=int)
    b = sub.add_parser("save")
    b.add_argument("--target", required=True)
    b.add_argument("--generated-voice-id", required=True)
    b.add_argument("--name", required=True)
    b.add_argument("--description", required=True)
    c = sub.add_parser("tts")
    c.add_argument("--target", required=True)
    c.add_argument("--voice-id", required=True)
    c.add_argument("--text", required=True)
    c.add_argument("--model", default="eleven_v3")
    c.add_argument("--settings", help='JSON，如 {"stability":0.5}')
    args = ap.parse_args()
    t = Path(args.target)
    if args.step == "design":
        r = design(t, args.description, args.text, args.model, args.seed)
    elif args.step == "save":
        r = save(t, args.generated_voice_id, args.name, args.description)
    else:
        r = tts(t, args.voice_id, args.text, args.model, json.loads(args.settings) if args.settings else None)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
