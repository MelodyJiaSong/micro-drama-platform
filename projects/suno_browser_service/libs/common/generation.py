from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class GenerationOptions(BaseModel):
    """网页可选设置；省略或 null 遵循页面当前值。显式值在 Create 前逐项读回，不支持时停止。"""
    model_config = ConfigDict(extra="forbid")
    model: str | None = Field(default=None, min_length=1, max_length=80, description="页面显示的精确模型名；如 v6。只选择已有模型，不训练模型；Sounds 不适用。", examples=["v6"])
    exclude_styles: str | None = Field(default=None, max_length=1000, description="排除的风格或乐器；不是正向风格 prompt。仅歌曲模式。", examples=["heavy drums, distorted guitar"])
    vocal_gender: Literal["male", "female"] | None = Field(default=None, description="人声性别选项，要求 instrumental=false；不保证生成结果一定符合。")
    weirdness: float | None = Field(default=None, ge=0, le=100, description="Weirdness 滑杆百分比；数值越高越偏探索。页面步长和可用性优先。")
    style_influence: float | None = Field(default=None, ge=0, le=100, description="Style Influence 滑杆百分比，控制风格提示的影响强度。")
    audio_influence: float | None = Field(default=None, ge=0, le=100, description="Audio Influence 滑杆百分比；须同时提供 references 或已有 voice_name。")
    variety: float | None = Field(default=None, ge=0, le=100, description="Variety 滑杆百分比；仅当当前模式/模型存在该控件时可用。")
    duration_seconds: int | None = Field(default=None, ge=1, le=480, description="请求时长，单位秒。网页限制可能更严；控件单位不明确会停止，成品实际时长需另检查。", examples=[30])
    max_mode: bool | None = Field(default=None, description="显式开关 Max Mode；true 可能增加积分消耗，金额以 Suno 为准。省略使用页面当前值。")
    my_taste: bool | None = Field(default=None, description="显式开关 My Taste 个性化选项；省略使用页面当前值。")
    voice_name: str | None = Field(default=None, min_length=1, max_length=120, description="已有 Voice/Style Persona 的精确名称；要求 instrumental=false，不注册或克隆声音。")
    inspiration_name: str | None = Field(default=None, min_length=1, max_length=120, description="已有灵感歌单的精确名称；不创建歌单。")
    sound_type: Literal["one_shot", "loop"] | None = Field(default=None, description="Sounds 专用：one_shot 单次音效，loop 循环声音。")
    bpm: int | None = Field(default=None, ge=20, le=300, description="Sounds 专用速度，单位 beats per minute；歌曲的速度写入 prompt。")


class ReferenceInput(BaseModel):
    """一条参考，asset_id 与 url 必须且只能提供一个；不抓取任意外网文件。"""
    model_config = ConfigDict(extra="forbid")
    asset_id: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$", description="先上传本机媒体，将返回对象的 id 原样放在这里；即文件 SHA256。")
    url: str | None = Field(default=None, pattern=r"^https://suno\.com/(song|playlist)/[0-9a-fA-F-]{36}$", description="已有 Suno song/playlist 的完整 HTTPS URL；不能同时传 asset_id。")

    @model_validator(mode="after")
    def one_source(self) -> "ReferenceInput":
        if bool(self.asset_id) == bool(self.url):
            raise ValueError("Reference requires exactly one of asset_id or Suno song/playlist url")
        return self


class GenerationRequest(BaseModel):
    """HTTP、CLI、MCP 共用生成请求。先 plan，再以稳定幂等键 create；参数可接受不等于真实 Suno 已验收。"""
    model_config = ConfigDict(extra="forbid")
    prompt: str = Field(min_length=1, max_length=2000, description="Advanced 写音乐风格；Simple 写自然语言需求（可要求写词）；Sounds 描述音效。网页字符上限可能更小。", examples=["Warm cinematic piano, gentle strings, reflective, no vocals"])
    format: Literal["mp3", "wav"] = Field(default="mp3", description="通过官方菜单下载的目标格式；受账号权限和下载额度限制。")
    instrumental: bool = Field(default=True, description="true 纯音乐，不能同时提供歌词、Voice 或人声性别；Sounds 必须为 true。")
    target: str | None = Field(default=None, description="请求日志归属：仓库 ai_videos 下已有剧/集/资产目录，或 edu_videos 下已有系列/知识点目录；独立任务省略。不是输出目录；不能传尚未创建的占位路径。")
    lyrics: str | None = Field(default=None, max_length=5000, description="Advanced 人声必填的明确歌词；其他模式不接受。Simple 的写词要求写在 prompt。")
    mode: Literal["advanced", "simple", "sounds"] = Field(default="advanced", description="advanced 分开风格与歌词；simple 自然语言及多媒体参考；sounds 单次/循环音效。模式控件仍需真实账号校准。")
    title: str | None = Field(default=None, min_length=1, max_length=80, description="显示标题前缀，服务追加唯一 job 标记关联结果；不能设置精确标题时停止。")
    options: GenerationOptions = Field(default_factory=GenerationOptions, description="可选网页控件；未传字段使用页面当前值，不静默忽略显式值。")
    references: list[ReferenceInput] = Field(default_factory=list, max_length=8, description="最多 8 个不同参考。Advanced 上传仅音频；图片/视频用 Simple；Sounds 不接受参考。素材仅在正式任务执行时上传 Suno。")

    @model_validator(mode="after")
    def compatible(self) -> "GenerationRequest":
        if not self.prompt.strip():
            raise ValueError("prompt must not be blank")
        if self.mode == "advanced" and not self.instrumental and not (self.lyrics or "").strip():
            raise ValueError("Advanced vocal mode requires lyrics; Simple may write lyrics from the prompt")
        if self.instrumental and (self.lyrics or "").strip():
            raise ValueError("instrumental=true conflicts with non-empty lyrics")
        if self.mode != "advanced" and self.lyrics:
            raise ValueError("Explicit lyrics require advanced mode")
        if self.mode != "sounds" and (self.options.sound_type is not None or self.options.bpm is not None):
            raise ValueError("sound_type and bpm require sounds mode; put song tempo in prompt")
        if self.mode == "sounds":
            if not self.instrumental or self.references:
                raise ValueError("Sounds requires instrumental=true and no references")
            # v6 Sounds page (2026-10-24) has Type/BPM/Key but no duration control, and a 500-character prompt box.
            invalid = set(self.options.model_dump(exclude_none=True)) - {"sound_type", "bpm"}
            if invalid:
                raise ValueError("Options unavailable in Sounds: " + ", ".join(sorted(invalid)))
            if len(self.prompt) > 500:
                raise ValueError("Sounds prompt is limited to 500 characters on the page")
        if self.instrumental and (self.options.voice_name or self.options.vocal_gender):
            raise ValueError("Voice/gender options require instrumental=false")
        if self.options.audio_influence is not None and not (self.references or self.options.voice_name):
            raise ValueError("audio_influence requires a reference or existing voice")
        sources = [(r.asset_id, r.url) for r in self.references]
        if len(sources) != len(set(sources)):
            raise ValueError("Duplicate references are not allowed")
        return self


ASSET_MAX_BYTES = 64 * 1024 * 1024
ASSET_MIME_TYPES = {".wav": "audio/wav", ".mp3": "audio/mpeg", ".flac": "audio/flac", ".m4a": "audio/mp4", ".ogg": "audio/ogg",
                    ".mp4": "video/mp4", ".mov": "video/quicktime", ".webm": "video/webm", ".png": "image/png",
                    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
ASSET_EXTENSIONS = set(ASSET_MIME_TYPES)
TERMINAL_STATUSES = {"completed", "needs_login", "needs_attention", "uncertain", "cancelled"}
