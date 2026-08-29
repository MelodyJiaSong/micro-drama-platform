from dataclasses import dataclass, field


@dataclass(frozen=True)
class SelectorCdto:
    project: str
    eps: tuple[str, ...] = ()
    shots: tuple[str, ...] = ()
    dimensions: tuple[str, ...] = ()
    dry_run: bool = False
    budget_usd: float | None = None
    samples_override: int | None = None
    assume_yes: bool = False


@dataclass(frozen=True)
class EstimateQdto:
    project: str
    unit_count: int
    llm_call_count: int
    est_input_tokens: int
    est_output_tokens: int
    est_cost_usd: float
    est_cost_cached_usd: float
    budget_usd: float


@dataclass(frozen=True)
class UsageCdto:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    cost_usd: float = 0.0
    api_calls: int = 0


@dataclass(frozen=True)
class RunResultCdto:
    run_id: str
    run_dir: str
    report_path: str
    project: str
    project_tier: str
    project_composite: float | None
    unit_count: int
    findings_total: int
    findings_blocker: int
    usage: UsageCdto
    halted_reason: str | None = None


@dataclass(frozen=True)
class TrendsQdto:
    project: str
    runs: tuple[dict, ...] = field(default_factory=tuple)
    recurring_fields: tuple[dict, ...] = field(default_factory=tuple)
