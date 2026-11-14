from dataclasses import dataclass


@dataclass(frozen=True)
class JobDao:
    id: str
    key: str
    fingerprint: str
    status: str
    payload: dict
    version: int
