import secrets

from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.settings import Settings
from projects.suno_browser_service.libs.infrastructure.readers.token__reader import TokenReader


class AuthQuery:
    def __init__(self, settings: Settings) -> None:
        self.token = TokenReader(settings.data_dir).load()

    def verify(self, authorization: str | None) -> None:
        supplied = authorization.removeprefix("Bearer ") if authorization and authorization.startswith("Bearer ") else ""
        if not secrets.compare_digest(supplied.encode(), self.token.encode()):
            raise ServiceError("unauthorized", "需要正确的 Bearer token", 401)
