import sys

from projects.suno_browser_service.apps.login.container import Container
from projects.suno_browser_service.libs.common.errors import ServiceError

if __name__ == "__main__":
    try:
        print(Container().session().window())
    except ServiceError as exc:
        print(f"{exc.code}: {exc}", file=sys.stderr)
        sys.exit(1)
