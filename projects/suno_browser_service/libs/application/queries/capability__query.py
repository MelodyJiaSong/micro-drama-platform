from projects.suno_browser_service.libs.common.generation import ASSET_EXTENSIONS, ASSET_MAX_BYTES, GenerationRequest
from projects.suno_browser_service.libs.common.settings import Settings
from projects.suno_browser_service.libs.infrastructure.clients.asset__client import AssetClient
from projects.suno_browser_service.libs.infrastructure.readers.runtime__reader import RuntimeReader


class CapabilityQuery:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get(self) -> dict:
        return {"schema_version": "0.2", "automation_paused": RuntimeReader(self.settings.data_dir).automation_paused(),
                "workflow_default": {"scope": "all_new_audio_generation", "automatic_engine_fallback": False,
                                     "ambience_effects": "sounds", "background_music": "advanced instrumental",
                                     "theme_songs": "advanced vocals with lyrics, or simple",
                                     "unsupported_request_action": "report_capability_gap; no silent engine switch",
                                     "editing_mixing": "existing local post-production tools"},
                "modes": {name: {"implemented": True, "live_verified": False,
                                  "requires": "Unique visible controls, read-back and a writable task title before Create"}
                          for name in ("advanced", "simple", "sounds")},
                "options": list(GenerationRequest.model_fields["options"].annotation.model_fields),
                "uploads": {"max_bytes": ASSET_MAX_BYTES, "extensions": sorted(ASSET_EXTENSIONS),
                            "local_only_until_job_runs": True},
                "request_schema": GenerationRequest.model_json_schema(),
                "unsupported": ["exact text-to-speech", "voice cloning", "audio source separation", "voice enrollment/verification", "custom model training", "publish", "studio timeline editing", "captcha solving"],
                "evidence": {"advanced_basic_form": "v6 live form filled; Create outcome uncertain",
                             "extended_controls": "offline browser fixtures; live calibration pending",
                             "download": "offline browser fixture only; live DOM calibration pending",
                             "browserless": "implemented; no live instance tested"}}

    def plan(self, request: GenerationRequest) -> dict:
        assets = AssetClient(self.settings)
        references = [assets.get(ref.asset_id) if ref.asset_id else {"url": ref.url} for ref in request.references]
        warnings = ["UI availability and applied values are checked again before Create; schema validation is not live verification."]
        if request.options.max_mode:
            warnings.append("Max Mode may cost more credits; exact cost comes from Suno UI.")
        if request.references:
            warnings.append("UI rights confirmation requires rights_confirmed=true on each uploaded asset.")
        return {"schema_valid": True, "browser_called": False, "creates_job": False,
                "automation_paused": RuntimeReader(self.settings.data_dir).automation_paused(),
                "request": request.model_dump(exclude_none=True), "references": references,
                "warnings": warnings, "next_action": "submit_with_stable_idempotency_key_when_ready"}
