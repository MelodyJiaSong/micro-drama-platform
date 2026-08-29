from __future__ import annotations

import argparse

import uvicorn

from apps.api.app_factory import create_app
from apps.api.container import Container


def main() -> None:
    parser = argparse.ArgumentParser(description="drama_reverse_engine API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8620)
    parser.add_argument("--serve-static", action="store_true")
    args = parser.parse_args()

    app = create_app(serve_static=args.serve_static)
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
