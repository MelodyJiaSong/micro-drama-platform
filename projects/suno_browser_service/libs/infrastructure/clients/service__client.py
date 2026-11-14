import hashlib
import os
import re
import time
import uuid
from pathlib import Path
from urllib.parse import urlsplit

import httpx

from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.generation import TERMINAL_STATUSES
from projects.suno_browser_service.libs.common.settings import Settings


class ServiceClient:
    def __init__(self) -> None:
        settings = Settings.from_env()
        self.url = os.getenv("SUNO_SERVICE_URL", f"http://127.0.0.1:{settings.port}").rstrip("/")
        parsed = urlsplit(self.url)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost"} or parsed.path or parsed.query or parsed.username:
            raise ServiceError("invalid_service_url", "代理入口仅连接本机 HTTP Suno 服务")
        token = os.getenv("SUNO_SERVICE_TOKEN")
        path = settings.data_dir / "service-token.txt"
        if not token and path.is_file():
            token = path.read_text(encoding="utf-8").strip()
        if not token or len(token) < 24:
            raise ServiceError("service_not_configured", "先运行 Suno start.ps1；令牌由客户端从私有文件读取，无需粘贴到对话")
        self.headers = {"Authorization": "Bearer " + token}

    def request(self, method: str, path: str, *, body: dict | None = None, key: str | None = None, files: dict | None = None, data: dict | None = None) -> dict | list:
        headers = {**self.headers, **({"Idempotency-Key": key} if key else {})}
        try:
            response = httpx.request(method, self.url + path, headers=headers, json=body, files=files, data=data, timeout=30, trust_env=False, follow_redirects=False)
        except httpx.HTTPError:
            raise ServiceError("service_unavailable", "本机 Suno API 不可达；检查 start.ps1。提交请求超时请保持相同幂等键") from None
        if response.is_error or response.is_redirect:
            try:
                payload = response.json()
            except ValueError:
                payload = {}
            error = payload.get("error", {})
            raise ServiceError(error.get("code", "http_" + str(response.status_code)), error.get("message", str(payload.get("detail", "本机服务请求失败"))), response.status_code)
        return response.json()

    @staticmethod
    def job_path(job_id: str) -> str:
        if not re.fullmatch(r"[a-f0-9]{32}", job_id):
            raise ServiceError("invalid_job_id", "job_id 须为服务返回的 32 位 ID", 422)
        return "/v1/jobs/" + job_id

    def wait(self, job_id: str, seconds: int = 45) -> dict:
        if not 0 <= seconds <= 45:
            raise ServiceError("invalid_wait", "一次等待 0–45 秒；未完成时继续等待同一 job", 422)
        deadline = time.monotonic() + seconds
        while True:
            job = self.request("GET", self.job_path(job_id))
            if job["status"] in TERMINAL_STATUSES or time.monotonic() >= deadline:
                return {"job": job, "timed_out": job["status"] not in TERMINAL_STATUSES}
            health = self.request("GET", "/health")
            if health["automation_paused"]:
                return {"job": job, "automation_paused": True, "timed_out": False, "next_action": "manual_verification_required_do_not_resubmit"}
            time.sleep(min(2, max(0, deadline - time.monotonic())))

    def download(self, job_id: str, directory: str) -> dict:
        job_path = self.job_path(job_id)
        job = self.request("GET", job_path)
        output = Path(directory).expanduser().resolve()
        output.mkdir(parents=True, exist_ok=True)
        files = []
        for item in job["files"]:
            name = item["name"]
            if not re.fullmatch(r"[a-fA-F0-9-]{36}\.(mp3|wav)", name):
                raise ServiceError("unsafe_filename", "服务返回的文件名不符合音频命名契约")
            path = output / name
            if path.is_symlink() or path.resolve().parent != output:
                raise ServiceError("unsafe_output", "输出文件指向目录外，停止写入")
            if path.exists():
                if hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
                    raise ServiceError("output_exists", "目标同名文件内容不同，保留原文件；请选新目录")
            else:
                temporary = output / (name + "." + uuid.uuid4().hex + ".part")
                try:
                    with httpx.stream("GET", self.url + job_path + "/files/" + name, headers=self.headers, timeout=60, trust_env=False) as response:
                        response.raise_for_status()
                        digest, size = hashlib.sha256(), 0
                        with temporary.open("xb") as file:
                            for chunk in response.iter_bytes():
                                digest.update(chunk)
                                size += len(chunk)
                                file.write(chunk)
                    if digest.hexdigest() != item["sha256"] or size != item["bytes"]:
                        raise ServiceError("download_checksum", "下载校验不通过，未发布本地文件")
                    # Exclusive destination creation never overwrites a concurrently written file.
                    os.link(temporary, path)
                except httpx.HTTPError:
                    raise ServiceError("download_failed", "本机成品下载失败，可对同一 job 重试") from None
                finally:
                    temporary.unlink(missing_ok=True)
            files.append({**item, "path": str(path)})
        return {"job_id": job_id, "status": job["status"], "files": files, "next_action": job.get("next_action")}
