from __future__ import annotations

import os
from pathlib import Path

from libs.application.commands.setup__command import SetupCommand
from libs.infrastructure.readers.env_file__reader import EnvFileReader
from libs.infrastructure.writers.env_file__writer import EnvFileWriter
from libs.infrastructure.writers.secret_key__writer import SecretKeyWriter

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    repo_root = Path(os.environ.get("JIMENG_BRIDGE_REPO_ROOT", PROJECT_ROOT.parents[1]))
    data_dir = Path(os.environ.get("JIMENG_BRIDGE_DATA_DIR", PROJECT_ROOT / ".data"))
    result = SetupCommand(EnvFileReader(), EnvFileWriter(), SecretKeyWriter()).init(repo_root, data_dir)
    token_state = "已生成并写入" if result.token_created else "已存在，未改动"
    print(f"JIMENG_BRIDGE_TOKEN：{token_state}（{result.env_path}，值不打印）")
    print(f".data 目录：{result.data_dir}；新建子目录：{', '.join(result.created_data_dirs) or '无'}")
    print(f"HMAC 密钥：{'已生成' if result.secret_key_created else '已存在'}")


if __name__ == "__main__":
    main()
