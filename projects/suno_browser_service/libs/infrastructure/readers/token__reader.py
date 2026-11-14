import os
import secrets
from pathlib import Path
from projects.suno_browser_service.libs.infrastructure.writers.private_directory__writer import PrivateDirectoryWriter


class TokenReader:
    def __init__(self, data_dir: Path) -> None:
        self.path = data_dir / "service-token.txt"

    def load(self) -> str:
        PrivateDirectoryWriter.ensure(self.path.parent)
        supplied = os.getenv("SUNO_SERVICE_TOKEN")
        if supplied:
            if len(supplied) < 24:
                raise ValueError("SUNO_SERVICE_TOKEN 至少 24 个字符")
            return supplied
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with self.path.open("x", encoding="utf-8") as file:
                file.write(secrets.token_urlsafe(32))
            self.path.chmod(0o600)
        except FileExistsError:
            pass
        token = self.path.read_text(encoding="utf-8").strip()
        if len(token) < 24:
            raise ValueError("service-token.txt 损坏或过短；停止启动，请修复本机服务令牌")
        return token
