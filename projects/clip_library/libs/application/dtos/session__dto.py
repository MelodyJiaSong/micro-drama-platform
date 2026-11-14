from dataclasses import dataclass


@dataclass(frozen=True)
class SessionCdto:
    cookies_file: str
    cookie_count: int
