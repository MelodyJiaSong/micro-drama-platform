import re
from collections.abc import Mapping
from dataclasses import dataclass

from libs.common.enums import BackendKind
from libs.domain.errors.config__error import ConfigError
from libs.domain.value_objects.config_table__valueobject import ConfigTable
from libs.domain.value_objects.global_config_sections__valueobject import (
    ApiSection, ArtifactsSection, BrowserSection, CanarySection, CliSection, ConcurrencySection, ConfirmSection,
    DownloadSection, EntitiesSection, IdempotencySection, McpSection, NotificationsSection, PacingSection,
    RetriesSection, RoutingSection, ServerSection, StatusSection, TimeSection, UiSection, WaitSection,
)
from libs.domain.value_objects.model_limits__valueobject import ModelLimits
from libs.domain.value_objects.price_estimate__valueobject import PriceTable

GLOBAL_SECTIONS: tuple[str, ...] = (
    "server", "routing", "concurrency", "pacing", "wait", "retries", "confirm", "idempotency", "status",
    "entities", "download", "api", "mcp", "ui", "artifacts", "time", "browser", "canary", "cli",
    "notifications", "model_limits", "price_table",
)

_TIMEZONE = re.compile(r"^(UTC|[A-Za-z]+(/[A-Za-z0-9_+\-]+)+)$")
_VERSION = re.compile(r"^\d+\.\d+\.\d+$")
_REAL_START_URL = "https://jimeng.jianying.com/"
_TEST_START_URL = re.compile(r"^http://(127\.0\.0\.1|localhost)(:\d+)?/")


@dataclass(frozen=True)
class GlobalConfig:
    server: ServerSection
    routing: RoutingSection
    concurrency: ConcurrencySection
    pacing: PacingSection
    wait: WaitSection
    retries: RetriesSection
    confirm: ConfirmSection
    idempotency: IdempotencySection
    status: StatusSection
    entities: EntitiesSection
    download: DownloadSection
    api: ApiSection
    mcp: McpSection
    ui: UiSection
    artifacts: ArtifactsSection
    time: TimeSection
    browser: BrowserSection
    canary: CanarySection
    cli: CliSection
    notifications: NotificationsSection
    model_limits: ModelLimits
    price_table: PriceTable

    @classmethod
    def from_dict(cls, data: Mapping[str, object], test_mode: bool = False) -> "GlobalConfig":
        root: ConfigTable = ConfigTable.of(data)
        root.only_keys(GLOBAL_SECTIONS)
        limits: ModelLimits = ModelLimits.from_table(root.table("model_limits"))
        return cls(
            server=ServerSection(port=_section(root, "server", ("port",)).integer("port", 1, 65535)),
            routing=_routing(root),
            concurrency=ConcurrencySection(
                _section(root, "concurrency", ("max_remote_rendering",)).integer("max_remote_rendering", 1, 5)
            ),
            pacing=PacingSection(_section(root, "pacing", ("min_submit_interval_s",)).number("min_submit_interval_s", 5)),
            wait=WaitSection(_section(root, "wait", ("timeout_h",)).integer("timeout_h", 1, 48)),
            retries=_retries(root),
            confirm=ConfirmSection(_section(root, "confirm", ("token_ttl_min",)).integer("token_ttl_min", 5, 240)),
            idempotency=IdempotencySection(_section(root, "idempotency", ("retention_h",)).integer("retention_h", 1, 168)),
            status=StatusSection(
                _section(root, "status", ("parse_failure_threshold",)).integer("parse_failure_threshold", 1, 50)
            ),
            entities=EntitiesSection(_section(root, "entities", ("snapshot_stale_h",)).integer("snapshot_stale_h", 1, 168)),
            download=DownloadSection(
                _section(root, "download", ("duration_tolerance_s",)).number("duration_tolerance_s", 0.1, 2)
            ),
            api=_api(root),
            mcp=McpSection(_section(root, "mcp", ("thumbnail_max_px",)).integer("thumbnail_max_px", 1)),
            ui=UiSection(_section(root, "ui", ("reference_thumb_max_px",)).integer("reference_thumb_max_px", 1)),
            artifacts=_artifacts(root),
            time=TimeSection(_section(root, "time", ("timezone",)).string("timezone", pattern=_TIMEZONE)),
            browser=_browser(root, test_mode),
            canary=CanarySection(_section(root, "canary", ("interval_min",)).integer("interval_min", 1)),
            cli=_cli(root),
            notifications=NotificationsSection(_section(root, "notifications", ("toast",)).boolean("toast")),
            model_limits=limits,
            price_table=PriceTable.from_table(root.table("price_table"), limits),
        )


def _section(root: ConfigTable, name: str, keys: tuple[str, ...], hints: Mapping[str, str] | None = None) -> ConfigTable:
    table: ConfigTable = root.table(name)
    table.only_keys(keys, hints)
    return table


def _routing(root: ConfigTable) -> RoutingSection:
    table = _section(root, "routing", ("video",), {"image": "routing.image 固定为 cli，不可配置"})
    return RoutingSection(video=table.enum("video", BackendKind))


def _retries(root: ConfigTable) -> RetriesSection:
    table = _section(root, "retries", ("set_params", "upload", "download", "fill"))
    return RetriesSection(
        set_params=table.integer("set_params", 0, 5),
        upload=table.integer("upload", 0, 5),
        download=table.integer("download", 0, 5),
        fill=table.integer("fill", 0, 2),
    )


def _api(root: ConfigTable) -> ApiSection:
    keys = ("max_call_s", "progress_interval_s", "page_size_default", "page_size_max", "max_body_bytes", "max_batch_items")
    table = _section(root, "api", keys)
    max_call_s: int = table.integer("max_call_s", 1, 85)
    page_size_max: int = table.integer("page_size_max", 1)
    return ApiSection(
        max_call_s=max_call_s,
        progress_interval_s=table.integer("progress_interval_s", 1, max_call_s),
        page_size_default=table.integer("page_size_default", 1, page_size_max),
        page_size_max=page_size_max,
        max_body_bytes=table.integer("max_body_bytes", 1),
        max_batch_items=table.integer("max_batch_items", 1),
    )


def _artifacts(root: ConfigTable) -> ArtifactsSection:
    table = _section(root, "artifacts", ("preview_max_bytes", "preview_retention_days"))
    return ArtifactsSection(
        preview_max_bytes=table.integer("preview_max_bytes", 1),
        preview_retention_days=table.integer("preview_retention_days", 1),
    )


def _browser(root: ConfigTable, test_mode: bool) -> BrowserSection:
    table = _section(root, "browser", ("channel", "profile_dir", "start_url"))
    profile_dir: str = table.string("profile_dir")
    parts: list[str] = re.split(r"[\\/]", profile_dir)
    if re.match(r"^([A-Za-z]:|[\\/])", profile_dir) or ".." in parts or ":" in profile_dir or parts[0] == "ai_videos":
        raise ConfigError(table.at("profile_dir"), "必须是项目内相对路径，不能含 ..、盘符、绝对路径或指向 ai_videos")
    start_url: str = table.string("start_url")
    if test_mode and not _TEST_START_URL.match(start_url):
        raise ConfigError(table.at("start_url"), "测试模式下必须指向 localhost")
    if not test_mode and not start_url.startswith(_REAL_START_URL):
        raise ConfigError(table.at("start_url"), f"必须以 {_REAL_START_URL} 开头")
    return BrowserSection(channel=table.one_of("channel", ("chrome", "chromium")), profile_dir=profile_dir, start_url=start_url)


def _cli(root: ConfigTable) -> CliSection:
    table = _section(root, "cli", ("path", "min_version"))
    path: str = table.string("path")
    if not path.lower().endswith(".exe"):
        raise ConfigError(table.at("path"), "必须指向 .exe 文件（拒绝 .cmd / .bat / .ps1 等）")
    return CliSection(path=path, min_version=table.string("min_version", pattern=_VERSION))
