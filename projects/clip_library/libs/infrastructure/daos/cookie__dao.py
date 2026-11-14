from dataclasses import dataclass


@dataclass(frozen=True)
class CookieDao:
    domain: str
    path: str
    secure: bool
    expires: int
    name: str
    value: str
