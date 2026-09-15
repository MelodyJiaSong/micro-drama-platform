from __future__ import annotations

import os
import sys
from pathlib import Path

import uvicorn

from apps.api.app_factory import create_app
from apps.api.container import Container
from libs.application.queries.app_settings__query import AppSettingsQuery
from libs.common.app_settings import HOST, StartupConfigError
from libs.infrastructure.readers.env_file__reader import EnvFileReader

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    try:
        settings = AppSettingsQuery(EnvFileReader()).load(PROJECT_ROOT, os.environ)
    except StartupConfigError as error:
        print(f"启动失败：{error}", file=sys.stderr)
        sys.exit(2)
    container = Container(settings=settings)
    container.wire()
    app = create_app(settings, container)
    uvicorn.run(
        app,
        host=HOST,
        port=settings.port,
        proxy_headers=False,
        forwarded_allow_ips="",
        server_header=False,
        log_level="info",
        timeout_graceful_shutdown=5,
    )


if __name__ == "__main__":
    main()
