"""Cloudflare R2 access (S3-compatible) via boto3.

Credentials come from the environment, optionally seeded from a gitignored
`.env` at the repo root. Nothing here is ever written to the manifest.

    R2_ENDPOINT=https://<account-id>.r2.cloudflarestorage.com   # as shown in the R2 dashboard
    R2_ACCESS_KEY_ID=...
    R2_SECRET_ACCESS_KEY=...
    R2_BUCKET=...

`R2_ACCOUNT_ID` is accepted instead of `R2_ENDPOINT` and the endpoint derived
from it; the dashboard hands you the full endpoint, so that is the primary form.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

_REQUIRED: tuple[str, ...] = ("R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET")


def load_env_file(path: Path) -> None:
    """Seed os.environ from KEY=VALUE lines. An already-set shell value wins."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        os.environ.setdefault(key.strip(), value)


@dataclass(frozen=True)
class R2Store:
    bucket: str
    client: object

    @classmethod
    def from_env(cls, repo_root: Path) -> R2Store:
        load_env_file(repo_root / ".env")
        missing = [name for name in _REQUIRED if not os.environ.get(name)]
        if not os.environ.get("R2_ENDPOINT") and not os.environ.get("R2_ACCOUNT_ID"):
            missing.append("R2_ENDPOINT")
        if missing:
            raise RuntimeError(
                f"missing R2 credentials: {', '.join(missing)} — "
                f"copy tools/assets/.env.example to {repo_root / '.env'} and fill it in"
            )
        endpoint = os.environ.get("R2_ENDPOINT") or (
            f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com"
        )
        client = boto3.session.Session().client(
            "s3",
            endpoint_url=endpoint.rstrip("/"),
            aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
            region_name="auto",
            config=Config(signature_version="s3v4", retries={"max_attempts": 5, "mode": "standard"}),
        )
        return cls(bucket=os.environ["R2_BUCKET"], client=client)

    def exists(self, key: str) -> bool:
        try:
            self.client.head_object(Bucket=self.bucket, Key=key)  # type: ignore[attr-defined]
            return True
        except ClientError as err:
            if err.response["Error"]["Code"] in ("404", "NoSuchKey", "NotFound"):
                return False
            raise

    def upload(self, key: str, path: Path) -> None:
        self.client.upload_file(str(path), self.bucket, key)  # type: ignore[attr-defined]

    def download(self, key: str, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.client.download_file(self.bucket, key, str(path))  # type: ignore[attr-defined]

    def list_keys(self, prefix: str = "") -> Iterator[str]:
        for key, _ in self.list_objects(prefix):
            yield key

    def list_objects(self, prefix: str = "") -> Iterator[tuple[str, int]]:
        """Key and size for every object — one listing answers "what is already
        up there", which is how an interrupted push resumes without re-sending."""
        paginator = self.client.get_paginator("list_objects_v2")  # type: ignore[attr-defined]
        for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
            for item in page.get("Contents", []):
                yield str(item["Key"]), int(item["Size"])

    def copy(self, src_key: str, dst_key: str) -> None:
        """Server-side move — the bytes never round-trip through this machine."""
        self.client.copy_object(  # type: ignore[attr-defined]
            Bucket=self.bucket, Key=dst_key, CopySource={"Bucket": self.bucket, "Key": src_key}
        )

    def delete(self, keys: list[str]) -> None:
        for start in range(0, len(keys), 1000):
            batch = [{"Key": k} for k in keys[start : start + 1000]]
            self.client.delete_objects(Bucket=self.bucket, Delete={"Objects": batch})  # type: ignore[attr-defined]
