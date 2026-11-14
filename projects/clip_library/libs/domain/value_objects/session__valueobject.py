from dataclasses import dataclass

from libs.common.options import COOKIE_DOMAINS, LOGIN_COOKIES
from libs.domain.errors.session__error import NotLoggedInError


def in_scope(domain: str) -> bool:
    return any(domain.lstrip(".").endswith(scope) for scope in COOKIE_DOMAINS)


@dataclass(frozen=True)
class Session:
    cookie_names: frozenset[str]

    def __post_init__(self) -> None:
        if not self.cookie_names & LOGIN_COOKIES:
            raise NotLoggedInError()
