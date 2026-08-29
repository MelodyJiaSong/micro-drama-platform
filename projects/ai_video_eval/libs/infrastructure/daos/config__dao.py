from dataclasses import dataclass, field


@dataclass(frozen=True)
class JudgeModelConfigDao:
    model: str
    effort: str
    samples: int
    max_tokens: int


@dataclass(frozen=True)
class GroundingConfigDao:
    world_slice_max_chars: int
    card_max_chars: int
    script_max_chars: int
    dialogue_max_chars: int
    adjacent_prompt_max_chars: int
    prior_ep_ending_max_chars: int


@dataclass(frozen=True)
class EvalConfigDao:
    project_root: str
    videos_root: str
    runs_dir: str
    disputes_dir: str
    golden_dir: str
    api_key_envs: tuple[str, ...]
    judge_engine: str
    judge_default: JudgeModelConfigDao
    judge_per_dimension: dict[str, JudgeModelConfigDao] = field(compare=False)
    concurrency: int = 8
    timeout_s: float = 600.0
    budget_default_usd: float = 20.0
    pricing: dict[str, dict[str, float]] = field(default_factory=dict, compare=False)
    grounding: GroundingConfigDao | None = None
    project_overrides: dict[str, dict[str, object]] = field(default_factory=dict, compare=False)

    def judge_for(self, dim_id: str) -> JudgeModelConfigDao:
        return self.judge_per_dimension.get(dim_id, self.judge_default)
