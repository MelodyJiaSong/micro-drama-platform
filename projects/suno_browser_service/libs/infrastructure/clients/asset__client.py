import hashlib
import json
import os
import re
import subprocess
import uuid
from pathlib import Path
from typing import BinaryIO

from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.generation import ASSET_EXTENSIONS, ASSET_MAX_BYTES
from projects.suno_browser_service.libs.common.settings import Settings


class AssetClient:
    def __init__(self, settings: Settings) -> None:
        self.root = (settings.data_dir / "assets").absolute()
        if self.root.resolve() != self.root:
            raise ServiceError("unsafe_assets", "参考素材目录含重定向链接")

    def put(self, filename: str, source: BinaryIO, rights_confirmed: bool) -> dict:
        if Path(filename).name != filename or any(c in filename for c in "\\/\r\n\x00") or len(filename) > 180:
            raise ServiceError("invalid_filename", "只接受短文件名，不接受路径", 422)
        suffix = Path(filename).suffix.lower()
        if suffix not in ASSET_EXTENSIONS:
            raise ServiceError("invalid_media", "不支持此参考媒体扩展名", 422)
        self.root.mkdir(parents=True, exist_ok=True)
        temporary = self.root / (uuid.uuid4().hex + suffix)
        try:
            size, digest = 0, hashlib.sha256()
            with temporary.open("xb") as output:
                while chunk := source.read(1024 * 1024):
                    size += len(chunk)
                    if size > ASSET_MAX_BYTES:
                        raise ServiceError("asset_too_large", "参考媒体最大 64 MiB", 413)
                    digest.update(chunk)
                    output.write(chunk)
            if not size:
                raise ServiceError("invalid_media", "空文件不可作为参考", 422)
            try:
                probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name:format=duration,format_name",
                                        "-of", "json", str(temporary)], capture_output=True, text=True, timeout=30, check=True)
                info = json.loads(probe.stdout)
                kinds = {s["codec_type"] for s in info.get("streams", [])}
                if not kinds.intersection({"audio", "video"}):
                    raise ValueError("no audio/video stream")
                codecs = {s.get("codec_name") for s in info.get("streams", [])}
                if suffix in {".png", ".jpg", ".jpeg", ".webp"} and not codecs.intersection({"png", "mjpeg", "webp"}):
                    raise ValueError("not an image")
                if suffix in {".wav", ".mp3", ".flac", ".m4a", ".ogg"} and "audio" not in kinds:
                    raise ValueError("not audio")
            except (OSError, ValueError, subprocess.SubprocessError):
                raise ServiceError("invalid_media", "ffprobe 无法识别参考文件；需本机 ffmpeg/ffprobe", 422) from None
            asset_id = digest.hexdigest()
            manifest = self.root / (asset_id + ".json")
            if manifest.exists():
                existing = self.get(asset_id)
                if rights_confirmed and not existing["rights_confirmed"]:
                    existing["rights_confirmed"] = True
                    staging = manifest.with_suffix("." + uuid.uuid4().hex + ".tmp")
                    staging.write_text(json.dumps(existing, ensure_ascii=False), encoding="utf-8")
                    os.replace(staging, manifest)
                return existing
            kind = "image" if suffix in {".png", ".jpg", ".jpeg", ".webp"} else ("video" if "video" in kinds and suffix in {".mp4", ".mov", ".webm"} else "audio")
            metadata = {"id": asset_id, "name": filename, "stored_name": asset_id + suffix,
                        "bytes": size, "sha256": asset_id, "kind": kind,
                        "duration_seconds": float(info.get("format", {}).get("duration", 0)),
                        "rights_confirmed": rights_confirmed, "storage_scope": "local"}
            os.replace(temporary, self.root / metadata["stored_name"])
            staging = manifest.with_suffix("." + uuid.uuid4().hex + ".tmp")
            staging.write_text(json.dumps(metadata, ensure_ascii=False), encoding="utf-8")
            os.replace(staging, manifest)
            return metadata
        finally:
            temporary.unlink(missing_ok=True)

    def get(self, asset_id: str) -> dict:
        if not re.fullmatch(r"[a-f0-9]{64}", asset_id):
            raise ServiceError("invalid_asset", "asset_id 必须是上传接口返回的 SHA256", 422)
        path = self.root / (asset_id + ".json")
        if not path.exists():
            raise ServiceError("asset_not_found", "参考文件不存在；先上传至 /v1/assets", 404)
        value = json.loads(path.read_text(encoding="utf-8"))
        stored = (self.root / value["stored_name"]).resolve()
        if not stored.is_relative_to(self.root.resolve()) or not stored.is_file() or hashlib.sha256(stored.read_bytes()).hexdigest() != asset_id:
            raise ServiceError("asset_changed", "参考文件内容不匹配原始哈希，停止使用", 409)
        return value

    def path(self, metadata: dict) -> Path:
        return self.root / metadata["stored_name"]
