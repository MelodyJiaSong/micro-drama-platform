from __future__ import annotations

import argparse
import json

from apps.story_run.container import Container
from libs.common.repo_root import RepoRoot


def main() -> None:
    parser = argparse.ArgumentParser(description="创建独立故事run，不调用生成服务")
    commands = parser.add_subparsers(dest="operation", required=True)
    begin = commands.add_parser("begin")
    begin.add_argument("--episode-path", required=True)
    begin.add_argument("--input", required=True)
    promote = commands.add_parser("promote")
    promote.add_argument("--episode-path", required=True)
    promote.add_argument("--run-id", required=True)
    args = parser.parse_args()
    container = Container()
    container.repo_root_path.override(RepoRoot.find().path)
    if args.operation == "begin":
        result = container.command().begin_from_file(args.episode_path, args.input)
        result = {"run_id": result["run_id"], "audit_path": result["audit_path"]}
    else:
        result = container.command().promote(args.episode_path, args.run_id)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
