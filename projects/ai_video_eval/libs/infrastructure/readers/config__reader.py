import os

import yaml

from libs.infrastructure.daos.config__dao import (
    EvalConfigDao,
    GroundingConfigDao,
    JudgeModelConfigDao,
)


class ConfigReader:
    def __init__(self, project_root: str) -> None:
        self._project_root = os.path.abspath(project_root)

    def read(self) -> EvalConfigDao:
        path = os.path.join(self._project_root, "config", "eval_config.yaml")
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)

        paths = data.get("paths", {})
        judge = data.get("judge", {})
        default = self._model(judge.get("default", {}))
        per_dim = {
            dim: self._model(cfg, default) for dim, cfg in (judge.get("per_dimension") or {}).items()
        }
        grounding_raw = data.get("grounding", {})
        grounding = GroundingConfigDao(
            world_slice_max_chars=int(grounding_raw.get("world_slice_max_chars", 6000)),
            card_max_chars=int(grounding_raw.get("card_max_chars", 4000)),
            script_max_chars=int(grounding_raw.get("script_max_chars", 20000)),
            dialogue_max_chars=int(grounding_raw.get("dialogue_max_chars", 20000)),
            adjacent_prompt_max_chars=int(grounding_raw.get("adjacent_prompt_max_chars", 5000)),
            prior_ep_ending_max_chars=int(grounding_raw.get("prior_ep_ending_max_chars", 3000)),
        )
        return EvalConfigDao(
            project_root=self._project_root,
            videos_root=os.path.abspath(
                os.path.join(self._project_root, paths.get("videos_root", "../../ai_videos"))
            ),
            runs_dir=os.path.join(self._project_root, paths.get("runs_dir", "runs")),
            disputes_dir=os.path.join(self._project_root, paths.get("disputes_dir", "disputes")),
            golden_dir=os.path.join(self._project_root, paths.get("golden_dir", "golden")),
            api_key_envs=tuple(data.get("api_key_env", ["AI_VIDEO_EVAL_ANTHROPIC_KEY"])),
            judge_engine=str(judge.get("engine", "api")),
            judge_default=default,
            judge_per_dimension=per_dim,
            concurrency=int(judge.get("concurrency", 8)),
            timeout_s=float(judge.get("timeout_s", 600)),
            budget_default_usd=float(data.get("budget", {}).get("default_usd", 20.0)),
            pricing={
                model: {k: float(v) for k, v in cfg.items()}
                for model, cfg in (data.get("pricing") or {}).items()
            },
            grounding=grounding,
            project_overrides=data.get("project_overrides") or {},
        )

    @staticmethod
    def _model(raw: dict, fallback: JudgeModelConfigDao | None = None) -> JudgeModelConfigDao:
        return JudgeModelConfigDao(
            model=str(raw.get("model", fallback.model if fallback else "claude-opus-5")),
            effort=str(raw.get("effort", fallback.effort if fallback else "high")),
            samples=int(raw.get("samples", fallback.samples if fallback else 3)),
            max_tokens=int(raw.get("max_tokens", fallback.max_tokens if fallback else 16000)),
        )
