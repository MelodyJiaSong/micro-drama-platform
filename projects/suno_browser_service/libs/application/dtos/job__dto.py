from dataclasses import dataclass, field


@dataclass(frozen=True)
class JobQdto:
    id: str
    status: str
    prompt: str
    format: str
    instrumental: bool
    song_urls: list[str]
    files: list[dict]
    error: dict | None
    created_at: str
    updated_at: str
    request: dict = field(default_factory=dict)
    next_action: str = ""
    applied_options: dict = field(default_factory=dict)


@dataclass(frozen=True)
class JobCdto:
    prompt: str
    format: str = "mp3"
    instrumental: bool = True
    target: str | None = None
    lyrics: str | None = None
    mode: str = "advanced"
    title: str | None = None
    options: dict = field(default_factory=dict)
    references: list[dict] = field(default_factory=list)
