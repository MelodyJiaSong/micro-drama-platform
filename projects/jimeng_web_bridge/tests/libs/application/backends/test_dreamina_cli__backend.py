from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pytest

from libs.application.backends.dreamina_cli__backend import (
    CHECK_COMPLIANCE_REQUIRED,
    CHECK_CREDIT_FAILED,
    CHECK_NOT_LOGGED_IN,
    CHECK_UNAVAILABLE,
    CHECK_VERSION_BELOW_MIN,
    CHECK_VERSION_FAILED,
    CHECK_VERSION_UNKNOWN,
    DreaminaCliBackend,
)
from libs.application.backends.dreamina_cli_mapping import DreaminaBackendError
from libs.application.mappers.dreamina__mapper import DreaminaMapper
from libs.common.enums import (
    PREPARING_STEP_ORDER,
    BackendKind,
    GenerationKind,
    PauseReason,
    PreparingStep,
    RefKind,
    RemoteStatus,
    SourceType,
)
from libs.common.paths import RepoSandbox
from libs.domain.repositories.generation_backend__repository import BackendHealth, PrepareResult, SubmitOutcome
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest
from libs.domain.value_objects.generation_params__valueobject import GenerationParams
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest, RequestSource
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem
from libs.infrastructure.clients.dreamina_cli__client import DreaminaCliClient
from libs.infrastructure.errors.dreamina_cli__error import DreaminaFailureKind

TESTS_DIR = Path(__file__).resolve().parents[3]
PROJECT_DIR = TESTS_DIR.parent
FAKE_DIR = TESTS_DIR / "fixtures" / "fake_dreamina"
CSC = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Microsoft.NET" / "Framework64" / "v4.0.30319" / "csc.exe"
DOCUMENTED_COMMANDS = frozenset({"text2image", "image2image", "query_result", "list_task", "user_credit", "version"})
CARD = "ai_videos/huangye_shenghuo/hy3/2_世界观人设/characters/c2_獾"
FAKE_PNG = b"\x89PNG\r\n\x1a\nfake"
TRICKY_PROMPT = (
    'c2-1_獾锚点\n他说："别动" \\"q\\" & calc & | whoami ; %PATH% !VAR! ^ $(id) `id`\r\n'
    "--download_dir=C:\\Windows\n一只獾，😀，　全角空格，结尾反斜杠\\"
)
VERSION_OK = json.dumps({"version": "1.4.5", "commit": "46b5b0e", "build_time": "2026-06-03T19:39:25Z"})
CREDIT_OK = json.dumps({"total_credit": 8712, "user_id": 1, "user_name": "", "vip_level": "ultra"})
REAL_RECORD_NOT_FOUND = (
    "\n2026/09/13 19:15:22 \x1b[31;1mcode.byted.org/videocut-aigc/dreamina_cli/components/task/store.go:278 "
    "\x1b[35;1mrecord not found\n\x1b[0m\x1b[33m[0.000ms] \x1b[34;1m[rows:0]\x1b[0m SELECT * FROM `aigc_task` "
    'WHERE submit_id = "00000000-bogus" ORDER BY `aigc_task`.`submit_id` LIMIT 1\n'
)

Commands = dict[str, dict[str, object]]


@dataclass(frozen=True)
class Harness:
    backend: DreaminaCliBackend
    ledger: Path
    repo: Path
    tmp_dir: Path

    def rows(self) -> list[dict[str, list[str]]]:
        if not self.ledger.is_file():
            return []
        rows = [json.loads(line) for line in self.ledger.read_text(encoding="utf-8").splitlines()]
        assert {row["argv"][0] for row in rows} <= DOCUMENTED_COMMANDS
        return rows

    def calls(self) -> list[list[str]]:
        return [row["argv"] for row in self.rows()]


def _env(scenario: Path, **extra: str) -> dict[str, str]:
    return {
        "FAKE_DREAMINA_SCENARIO": str(scenario),
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", r"C:\Windows"),
        "JIMENG_BRIDGE_TOKEN": "must-not-leak-" + "x" * 30,
        "JIMENG_BRIDGE_DATA_DIR": "must-not-leak",
        **extra,
    }


def _scenario(tmp_path: Path, commands: Commands) -> tuple[Path, Path]:
    ledger = tmp_path / "ledger.jsonl"
    scenario = tmp_path / "scenario.json"
    scenario.write_text(json.dumps({"ledger": str(ledger), "commands": commands}, ensure_ascii=False), encoding="utf-8")
    return scenario, ledger


def _harness(tmp_path: Path, client: DreaminaCliClient, ledger: Path, min_version: str = "1.4.5") -> Harness:
    repo = tmp_path / "repo"
    (repo / "ai_videos").mkdir(parents=True, exist_ok=True)
    tmp_dir = tmp_path / "data" / "tmp" / "cli"
    return Harness(DreaminaCliBackend(client, RepoSandbox(repo), tmp_dir, min_version), ledger, repo, tmp_dir)


@pytest.fixture
def harness(tmp_path: Path) -> Callable[..., Harness]:
    def build(commands: Commands, timeout_s: float = 20.0, min_version: str = "1.4.5") -> Harness:
        scenario, ledger = _scenario(tmp_path, commands)
        client = DreaminaCliClient(
            FAKE_DIR / "fake_dreamina.py", timeout_s=timeout_s, launcher_prefix=(sys.executable,), base_env=_env(scenario)
        )
        return _harness(tmp_path, client, ledger, min_version)

    return build


def _write_ref(h: Harness, name: str, data: bytes) -> ReferenceItem:
    rel = f"{CARD}/{name}.png"
    path = h.repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return ReferenceItem(name=name, label="角色参考图", kind=RefKind.IMAGE, resolved_path=rel, sha256=hashlib.sha256(data).hexdigest())


def image_request(
    h: Harness,
    refs: tuple[tuple[str, bytes], ...] = (),
    prompt: str = "c2-1_獾锚点\n一只獾",
    model: str = "seedream5.0",
    ratio: str = "3:4",
    resolution: str = "2k",
    backend: BackendKind = BackendKind.CLI,
    extra_refs: tuple[ReferenceItem, ...] = (),
) -> FrozenRequest:
    items = tuple(_write_ref(h, name, data) for name, data in refs)
    request = GenerationRequest(
        kind=GenerationKind.IMAGE,
        prompt=prompt,
        negative_prompt=None,
        references=(*items, *extra_refs),
        params=GenerationParams(model=model, ratio=ratio, resolution=resolution, count=1),
        output_slot=f"{CARD}#c2-1",
        source=RequestSource(type=SourceType.ASSET_IMAGE, path=f"{CARD}/c2_獾.md", block_key="c2-1"),
    )
    return FrozenRequest.freeze(request, backend, "cfg-digest", 1, 10)


def video_request() -> FrozenRequest:
    slot = "ai_videos/huangye_shenghuo/hy3/5_6_分镜与prompt/shots/shot02"
    request = GenerationRequest(
        kind=GenerationKind.VIDEO,
        prompt="shot02",
        negative_prompt=None,
        references=(),
        params=GenerationParams(model="seedance2.0", ratio="16:9", resolution="720p", count=1, duration_s=10),
        output_slot=slot,
        source=RequestSource(type=SourceType.SHOT, path=f"{slot}/shot02.md"),
    )
    return FrozenRequest.freeze(request, BackendKind.CLI, "cfg-digest", 80, 10)


def entity_ref() -> ReferenceItem:
    return ReferenceItem(name="砌炉的老人", label="Seedance 人物 entity", kind=RefKind.ENTITY, entity_name="hy3_主角")


def list_task_json(gen_status: str, submit_id: str = "sub-1", fail_reason: str = "", credit_count: int = 1) -> str:
    return json.dumps(
        [
            {
                "submit_id": submit_id,
                "gen_task_type": "text2image",
                "gen_status": gen_status,
                "fail_reason": fail_reason,
                "result_json": {"images": [{"width": 1440, "height": 2560}], "videos": []},
                "commerce_info": {
                    "credit_count": credit_count,
                    "triplet": {"resource_type": "", "resource_id": "", "benefit_type": ""},
                    "triplets": [{"resource_type": "aigc", "resource_id": "<RESOURCE>", "benefit_type": "<BENEFIT>"}],
                },
            }
        ],
        ensure_ascii=False,
    )


# --- mapper -------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("model", "expected"),
    [("seedream5.0", "5.0"), ("seedream3.0", "3.0"), ("Seedream4.0", "4.0"), ("5.0", "5.0"),
     ("seedance2.0", None), ("seedream5.0_vip", None), ("", None)],
)
def test_mapper_model_version(model: str, expected: str | None) -> None:
    assert DreaminaMapper.model_version(model) == expected


@pytest.mark.parametrize(("resolution", "expected"), [("2k", "2k"), ("4K", "4k"), ("1k", None), ("720p", None)])
def test_mapper_resolution_type(resolution: str, expected: str | None) -> None:
    assert DreaminaMapper.resolution_type(resolution) == expected


@pytest.mark.parametrize(("ratio", "expected"), [("3:4", "3:4"), ("21:9", "21:9"), ("0:1", None), ("square", None)])
def test_mapper_ratio(ratio: str, expected: str | None) -> None:
    assert DreaminaMapper.ratio(ratio) == expected


@pytest.mark.parametrize(
    ("actual", "minimum", "below"),
    [("1.4.18", "1.4.5", False), ("1.4.4", "1.4.5", True), ("1.4.5", "1.4.5", False), ("v1.4.5", "1.4.5", False),
     ("1.4.5-fake", "1.4.5", False), ("1.4", "1.4.5", True), ("46b5b0e-dirty", "1.4.5", None), ("", "1.4.5", None)],
)
def test_mapper_version_comparison_is_numeric(actual: str, minimum: str, below: bool | None) -> None:
    assert DreaminaMapper.version_below(actual, minimum) is below


@pytest.mark.parametrize(
    ("gen_status", "status", "known"),
    [("success", RemoteStatus.SUCCEEDED, True), ("fail", RemoteStatus.FAILED, True),
     ("querying", RemoteStatus.GENERATING, True), ("brand_new", RemoteStatus.GENERATING, False),
     (None, RemoteStatus.GENERATING, False)],
)
def test_mapper_remote_status(gen_status: str | None, status: RemoteStatus, known: bool) -> None:
    assert (DreaminaMapper.remote_status(gen_status), DreaminaMapper.is_known_status(gen_status)) == (status, known)


@pytest.mark.parametrize(
    ("kind", "reason"),
    [(DreaminaFailureKind.NOT_LOGGED_IN, PauseReason.CLI_LOGIN_REQUIRED),
     (DreaminaFailureKind.COMPLIANCE_CONFIRMATION_REQUIRED, PauseReason.COMPLIANCE_CONFIRMATION_REQUIRED),
     (DreaminaFailureKind.NOT_FOUND, PauseReason.CLI_ERROR), (DreaminaFailureKind.TIMEOUT, PauseReason.CLI_ERROR),
     (DreaminaFailureKind.UNPARSEABLE_OUTPUT, PauseReason.CLI_ERROR), (DreaminaFailureKind.UNKNOWN, PauseReason.CLI_ERROR)],
)
def test_mapper_failure_reason(kind: DreaminaFailureKind, reason: PauseReason) -> None:
    assert DreaminaMapper.failure_reason(kind) is reason


# --- health -------------------------------------------------------------------------------------


def test_kind_is_cli(harness: Callable[..., Harness]) -> None:
    assert harness({}).backend.kind is BackendKind.CLI


def test_health_ok_reports_version_and_balance(harness: Callable[..., Harness]) -> None:
    h = harness({"version": {"stdout": VERSION_OK}, "user_credit": {"stdout": CREDIT_OK}})
    report = h.backend.inspect()
    assert report.health == BackendHealth(ok=True, failed_checks=(), version="1.4.5", pause_reason=None)
    assert (report.logged_in, report.balance, report.vip_level, report.version_warning) == (True, 8712, "ultra", False)
    assert h.backend.health() == report.health
    assert [argv[0] for argv in h.calls()] == ["version", "user_credit", "version", "user_credit"]


@pytest.mark.parametrize(
    ("stderr", "reason", "check", "logged_in"),
    [("Error: not logged in. Please run `dreamina login` first", PauseReason.CLI_LOGIN_REQUIRED, CHECK_NOT_LOGGED_IN, False),
     ("error: AigcComplianceConfirmationRequired", PauseReason.COMPLIANCE_CONFIRMATION_REQUIRED, CHECK_COMPLIANCE_REQUIRED, None)],
)
def test_health_account_problems_pause_the_cli_queue(
    harness: Callable[..., Harness], stderr: str, reason: PauseReason, check: str, logged_in: bool | None
) -> None:
    h = harness({"version": {"stdout": VERSION_OK}, "user_credit": {"stderr": stderr, "exit": 1}})
    report = h.backend.inspect()
    assert (report.health.ok, report.health.pause_reason, report.health.failed_checks) == (False, reason, (check,))
    assert (report.logged_in, report.balance) == (logged_in, None)
    assert "login" not in {argv[0] for argv in h.calls()}


@pytest.mark.parametrize(("version", "check"), [("1.4.4", CHECK_VERSION_BELOW_MIN), ("46b5b0e-dirty", CHECK_VERSION_UNKNOWN)])
def test_health_version_problems_are_warnings_only(harness: Callable[..., Harness], version: str, check: str) -> None:
    h = harness({"version": {"stdout": json.dumps({"version": version})}, "user_credit": {"stdout": CREDIT_OK}})
    report = h.backend.inspect()
    assert report.health == BackendHealth(ok=True, failed_checks=(check,), version=version, pause_reason=None)
    assert report.version_warning is True


def test_health_newer_patch_version_is_not_a_warning(harness: Callable[..., Harness]) -> None:
    h = harness({"version": {"stdout": json.dumps({"version": "1.4.18"})}, "user_credit": {"stdout": CREDIT_OK}})
    assert h.backend.health().failed_checks == ()


def test_health_never_raises_when_the_executable_is_missing(tmp_path: Path) -> None:
    client = DreaminaCliClient(tmp_path / "missing" / "dreamina.exe", timeout_s=5.0, base_env=_env(tmp_path / "none.json"))
    h = _harness(tmp_path, client, tmp_path / "ledger.jsonl")
    assert h.backend.health() == BackendHealth(ok=False, failed_checks=(CHECK_UNAVAILABLE,), version=None, pause_reason=None)


def test_health_never_raises_on_garbage_or_timeout(harness: Callable[..., Harness]) -> None:
    h = harness({"version": {"stdout": "not json at all"}, "user_credit": {"stdout": "{}", "sleep_s": 6}}, timeout_s=1.5)
    health = h.backend.health()
    assert (health.ok, health.failed_checks, health.pause_reason) == (False, (CHECK_VERSION_FAILED, CHECK_CREDIT_FAILED), None)


# --- prepare ------------------------------------------------------------------------------------


@pytest.mark.parametrize("until", PREPARING_STEP_ORDER)
def test_prepare_reaches_until_without_spawning_anything(harness: Callable[..., Harness], until: PreparingStep) -> None:
    h = harness({})
    frozen = image_request(h, refs=(("c2-1", b"ref-bytes"),))
    assert h.backend.prepare("job-1", frozen, until) == PrepareResult(
        reached_step=until, page_estimated_credits=None, screenshot_names=()
    )
    assert h.calls() == []


@pytest.mark.parametrize("mutation", ["edit", "delete"])
def test_prepare_detects_references_changed_after_confirmation(harness: Callable[..., Harness], mutation: str) -> None:
    h = harness({})
    frozen = image_request(h, refs=(("c2-1", b"one"), ("bg11-1", b"two")))
    target = h.repo / CARD / "bg11-1.png"
    if mutation == "edit":
        target.write_bytes(b"edited")
    else:
        target.unlink()
    result = h.backend.prepare("job-1", frozen, PreparingStep.VERIFY)
    assert (result.reached_step, result.pause_reason) == (PreparingStep.UPLOAD, PauseReason.INPUTS_CHANGED)
    assert "bg11-1" in (result.message or "")
    assert h.backend.prepare("job-1", frozen, PreparingStep.SET_PARAMS).pause_reason is None


REJECTED_SHAPES: list[tuple[str, Callable[[Harness], FrozenRequest], PreparingStep]] = [
    ("video_request", lambda h: video_request(), PreparingStep.SET_PARAMS),
    ("routed_to_web", lambda h: image_request(h, backend=BackendKind.WEB), PreparingStep.SET_PARAMS),
    ("entity_reference", lambda h: image_request(h, extra_refs=(entity_ref(),)), PreparingStep.SET_PARAMS),
    ("video_model", lambda h: image_request(h, model="seedance2.0"), PreparingStep.SET_PARAMS),
    ("resolution_1k", lambda h: image_request(h, resolution="1k"), PreparingStep.SET_PARAMS),
    ("bad_ratio", lambda h: image_request(h, ratio="square"), PreparingStep.SET_PARAMS),
    ("comma_in_path", lambda h: image_request(h, refs=(("a,b", b"x"),)), PreparingStep.UPLOAD),
    ("nul_in_prompt", lambda h: image_request(h, prompt="c2-1\x00x"), PreparingStep.FILL),
]


@pytest.mark.parametrize(("build", "step"), [(b, s) for _, b, s in REJECTED_SHAPES], ids=[i for i, _, _ in REJECTED_SHAPES])
def test_requests_the_cli_cannot_run_are_rejected_before_any_spawn(
    harness: Callable[..., Harness], build: Callable[[Harness], FrozenRequest], step: PreparingStep
) -> None:
    h = harness({"text2image": {"stdout": '{"submit_id": "never"}'}, "image2image": {"stdout": '{"submit_id": "never"}'}})
    frozen = build(h)
    prepared = h.backend.prepare("job-1", frozen, PreparingStep.VERIFY)
    assert (prepared.reached_step, prepared.pause_reason) == (step, PauseReason.CLI_ERROR)
    submitted = h.backend.submit("job-1", frozen)
    assert (submitted.accepted, submitted.rejection) == (False, PauseReason.CLI_ERROR)
    assert h.calls() == []


# --- submit -------------------------------------------------------------------------------------


@pytest.mark.requires_probe
def test_submit_text2image_argv_is_exact_and_sent_once(harness: Callable[..., Harness]) -> None:
    h = harness({"text2image": {"stdout": '{"submit_id": "sub-1", "gen_status": "querying"}'}})
    outcome = h.backend.submit("job-1", image_request(h, prompt=TRICKY_PROMPT, resolution="2K"))
    assert outcome == SubmitOutcome(platform_task_id="sub-1")
    assert h.calls() == [
        ["text2image", f"--prompt={TRICKY_PROMPT}", "--model_version=5.0", "--ratio=3:4", "--resolution_type=2k"]
    ]


@pytest.mark.requires_probe
def test_submit_image2image_keeps_frozen_reference_order(harness: Callable[..., Harness]) -> None:
    h = harness({"image2image": {"stdout": '{"submit_id": "sub-2"}'}})
    frozen = image_request(h, refs=(("c2-1", b"one"), ("bg11-1", b"two")), ratio="16:9", resolution="4k")
    outcome = h.backend.submit("job-1", frozen)
    first, second = ((h.repo / CARD / f"{name}.png").resolve() for name in ("c2-1", "bg11-1"))
    assert outcome.platform_task_id == "sub-2"
    assert h.calls() == [
        ["image2image", f"--images={first},{second}", f"--prompt={frozen.request.prompt}",
         "--model_version=5.0", "--ratio=16:9", "--resolution_type=4k"]
    ]


@pytest.mark.parametrize(
    ("stderr", "code", "reason"),
    [("please run dreamina login first", 1, PauseReason.CLI_LOGIN_REQUIRED),
     ("error: AigcComplianceConfirmationRequired", 1, PauseReason.COMPLIANCE_CONFIRMATION_REQUIRED),
     ("panic: upstream said boom", 3, PauseReason.CLI_ERROR)],
)
def test_submit_cli_errors_become_rejections_without_retry(
    harness: Callable[..., Harness], stderr: str, code: int, reason: PauseReason
) -> None:
    h = harness({"text2image": {"stderr": stderr, "exit": code}})
    outcome = h.backend.submit("job-1", image_request(h))
    assert (outcome.accepted, outcome.rejection) == (False, reason)
    assert stderr in (outcome.message or "")
    assert [argv[0] for argv in h.calls()] == ["text2image"]


@pytest.mark.parametrize(
    ("command", "timeout_s"),
    [({"stdout": '{"gen_status": "fail"}'}, 20.0), ({"stdout": "{}", "sleep_s": 6}, 1.5)],
    ids=["no_submit_id", "timeout"],
)
def test_submit_with_unknown_outcome_is_unconfirmed(
    harness: Callable[..., Harness], command: dict[str, object], timeout_s: float
) -> None:
    h = harness({"text2image": command}, timeout_s=timeout_s)
    outcome = h.backend.submit("job-1", image_request(h))
    assert (outcome.accepted, outcome.rejection) == (False, PauseReason.SUBMIT_UNCONFIRMED)
    assert [argv[0] for argv in h.calls()] == ["text2image"]


# --- poll ---------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("gen_status", "fail_reason", "status", "failure", "message_part"),
    [("success", "", RemoteStatus.SUCCEEDED, None, None),
     ("querying", "", RemoteStatus.GENERATING, None, None),
     ("fail", "内容不符合社区规范", RemoteStatus.FAILED, PauseReason.CLI_ERROR, "内容不符合社区规范"),
     ("brand_new_state", "", RemoteStatus.GENERATING, None, "brand_new_state")],
)
def test_poll_maps_real_list_task_shape(
    harness: Callable[..., Harness], gen_status: str, fail_reason: str, status: RemoteStatus,
    failure: PauseReason | None, message_part: str | None,
) -> None:
    h = harness({"list_task": {"stdout": list_task_json(gen_status, fail_reason=fail_reason)}})
    result = h.backend.poll("sub-1")
    assert (result.status, result.progress_pct, result.failure) == (status, None, failure)
    if message_part is None:
        assert result.message is None
    else:
        assert message_part in (result.message or "")
    assert h.calls() == [["list_task", "--limit=5", "--submit_id=sub-1"]]


@pytest.mark.parametrize(
    "stdout",
    ['{"weird": true}', "[]", '[1, "x", null]', list_task_json("success", submit_id="someone-else")],
    ids=["object", "empty", "scalars", "other_task"],
)
def test_poll_tolerates_unexpected_json_as_still_running(harness: Callable[..., Harness], stdout: str) -> None:
    h = harness({"list_task": {"stdout": stdout}})
    result = h.backend.poll("sub-1")
    assert (result.status, result.failure) == (RemoteStatus.GENERATING, None)
    assert "sub-1" in (result.message or "")


@pytest.mark.parametrize(
    ("command", "failure"),
    [({"stdout": "garbage without json"}, None),
     ({"stderr": "not logged in", "exit": 1}, PauseReason.CLI_LOGIN_REQUIRED),
     ({"stderr": "boom", "exit": 2}, PauseReason.CLI_ERROR)],
    ids=["unparseable", "login", "nonzero"],
)
def test_poll_cli_failures_never_raise(
    harness: Callable[..., Harness], command: dict[str, object], failure: PauseReason | None
) -> None:
    h = harness({"list_task": command})
    result = h.backend.poll("sub-1")
    assert (result.status, result.failure) == (RemoteStatus.UNKNOWN, failure)
    assert result.message


# --- download -----------------------------------------------------------------------------------


@pytest.mark.requires_probe
def test_download_returns_new_files_with_hash_and_credits(harness: Callable[..., Harness]) -> None:
    h = harness({
        "query_result": {"stdout": '{"submit_id": "sub-1", "gen_status": "success"}', "create_files": ["img_2.png", "img_1.png"]},
        "list_task": {"stdout": list_task_json("success", credit_count=3)},
    })
    job_dir = h.tmp_dir / "job-7"
    job_dir.mkdir(parents=True)
    (job_dir / "stale_from_earlier_attempt.png").write_bytes(b"stale")
    downloaded = h.backend.download_all("job-7", "sub-1")
    paths = [Path(item.temp_path) for item in downloaded.files]
    assert [path.name for path in paths] == ["img_1.png", "img_2.png"]
    assert all(path.parent == job_dir for path in paths)
    assert [(item.size, item.sha256) for item in downloaded.files] == [
        (len(path.read_bytes()), hashlib.sha256(path.read_bytes()).hexdigest()) for path in paths
    ]
    assert [item.credits_charged for item in downloaded.files] == [3, None]
    assert downloaded.credits_charged == 3
    assert not (job_dir / "stale_from_earlier_attempt.png").exists()
    assert h.calls() == [
        ["query_result", "--submit_id=sub-1", f"--download_dir={job_dir}"],
        ["list_task", "--limit=5", "--submit_id=sub-1"],
    ]
    first = h.backend.download("job-7", "sub-1")
    assert (Path(first.temp_path).name, first.sha256, first.credits_charged) == (
        "img_1.png", hashlib.sha256(FAKE_PNG).hexdigest(), 3
    )


def test_download_without_credit_info_still_returns_the_file(harness: Callable[..., Harness]) -> None:
    h = harness({
        "query_result": {"stdout": '{"gen_status": "success"}', "create_files": ["a.png"]},
        "list_task": {"stderr": "boom", "exit": 1},
    })
    assert h.backend.download("job-1", "sub-1").credits_charged is None


@pytest.mark.parametrize(
    ("files", "reason", "retryable"),
    [(["a.png", "notes.txt"], PauseReason.CLI_ERROR, False),
     (["a.png", "nested/b.png"], PauseReason.CLI_ERROR, False),
     ([f"{index:02d}.png" for index in range(11)], PauseReason.CLI_ERROR, False),
     ([], PauseReason.DOWNLOAD_FAILED, True)],
    ids=["non_image", "subdirectory", "too_many", "nothing_downloaded"],
)
def test_download_rejects_unexpected_output(
    harness: Callable[..., Harness], files: list[str], reason: PauseReason, retryable: bool
) -> None:
    h = harness({
        "query_result": {"stdout": '{"gen_status": "success"}', "create_files": files},
        "list_task": {"stdout": "[]"},
    })
    with pytest.raises(DreaminaBackendError) as caught:
        h.backend.download("job-1", "sub-1")
    assert (caught.value.reason, caught.value.retryable) == (reason, retryable)


def test_download_never_picks_files_written_outside_the_job_dir(harness: Callable[..., Harness]) -> None:
    h = harness({
        "query_result": {"stdout": '{"gen_status": "success"}', "create_files": ["../escape.png", "ok.png"]},
        "list_task": {"stdout": "[]"},
    })
    downloaded = h.backend.download_all("job-1", "sub-1")
    assert [Path(item.temp_path).name for item in downloaded.files] == ["ok.png"]
    assert (h.tmp_dir / "escape.png").is_file()


@pytest.mark.parametrize(
    ("command", "reason", "retryable"),
    [({"stdout": REAL_RECORD_NOT_FOUND, "exit": 1}, PauseReason.CLI_ERROR, False),
     ({"stdout": '{"gen_status": "fail", "fail_reason": "审核未通过"}'}, PauseReason.CLI_ERROR, False),
     ({"stderr": "please login", "exit": 1}, PauseReason.CLI_LOGIN_REQUIRED, False),
     ({"stdout": "no json here"}, PauseReason.DOWNLOAD_FAILED, True)],
    ids=["real_record_not_found", "task_failed", "login", "unparseable"],
)
def test_download_failures_map_to_reasons(
    harness: Callable[..., Harness], command: dict[str, object], reason: PauseReason, retryable: bool
) -> None:
    h = harness({"query_result": command, "list_task": {"stdout": "[]"}})
    with pytest.raises(DreaminaBackendError) as caught:
        h.backend.download("job-1", "sub-1")
    assert (caught.value.reason, caught.value.retryable) == (reason, retryable)
    assert caught.value.message


@pytest.mark.parametrize("job_id", ["../x", "a/b", "a\\b", "CON", "x:y", "x.", ""])
def test_download_rejects_job_ids_that_are_not_one_safe_segment(harness: Callable[..., Harness], job_id: str) -> None:
    h = harness({"query_result": {"stdout": "{}"}})
    with pytest.raises(DreaminaBackendError):
        h.backend.download(job_id, "sub-1")
    assert h.calls() == []


# --- process hygiene ----------------------------------------------------------------------------

ALL_OK: Commands = {
    "version": {"stdout": VERSION_OK},
    "user_credit": {"stdout": CREDIT_OK},
    "text2image": {"stdout": '{"submit_id": "sub-1"}'},
    "list_task": {"stdout": list_task_json("success")},
    "query_result": {"stdout": '{"gen_status": "success"}', "create_files": ["a.png"]},
}


def test_child_processes_never_see_bridge_secrets(harness: Callable[..., Harness]) -> None:
    h = harness(ALL_OK)
    h.backend.health()
    h.backend.submit("job-1", image_request(h))
    h.backend.poll("sub-1")
    h.backend.download("job-1", "sub-1")
    rows = h.rows()
    assert len(rows) == 6
    assert not [key for row in rows for key in row["env_keys"] if key.startswith("JIMENG_BRIDGE_")]


def test_cli_is_spawned_as_an_argv_list_without_a_shell(
    harness: Callable[..., Harness], monkeypatch: pytest.MonkeyPatch
) -> None:
    seen: list[tuple[object, dict[str, object]]] = []
    original = subprocess.run

    def spy(*args: object, **kwargs: object) -> object:
        seen.append((args[0], kwargs))
        return original(*args, **kwargs)  # type: ignore[call-overload]

    monkeypatch.setattr(subprocess, "run", spy)
    h = harness(ALL_OK)
    h.backend.health()
    h.backend.submit("job-1", image_request(h, prompt=TRICKY_PROMPT))
    h.backend.poll("sub-1")
    h.backend.download("job-1", "sub-1")
    assert len(seen) == len(h.rows()) == 6
    assert all(isinstance(argv, list) and kwargs.get("shell") is False for argv, kwargs in seen)
    assert not (h.tmp_dir.parent / "calc").exists()


def test_backend_modules_contain_no_process_or_shell_primitives() -> None:
    sources = [
        PROJECT_DIR / "libs" / "application" / "backends" / "dreamina_cli__backend.py",
        PROJECT_DIR / "libs" / "application" / "backends" / "dreamina_cli_mapping.py",
        PROJECT_DIR / "libs" / "application" / "mappers" / "dreamina__mapper.py",
    ]
    for source in sources:
        text = source.read_text(encoding="utf-8")
        for needle in ("subprocess", "shell=True", "os.system", "os.popen", "create_subprocess", "Popen"):
            assert needle not in text, f"{needle} in {source.name}"


# --- real .exe front ----------------------------------------------------------------------------


@pytest.fixture(scope="module")
def fake_exe(tmp_path_factory: pytest.TempPathFactory) -> Path:
    if sys.platform != "win32" or not CSC.is_file():
        pytest.skip("needs Windows .NET Framework csc.exe")
    out = tmp_path_factory.mktemp("fake_exe") / "dreamina.exe"
    compiled = subprocess.run(
        [str(CSC), "/nologo", "/optimize", f"/out:{out}", str(FAKE_DIR / "FakeDreaminaLauncher.cs")],
        capture_output=True,
        check=False,
    )
    if compiled.returncode != 0:
        pytest.skip(f"csc failed: {compiled.stdout.decode(errors='replace')[-300:]}")
    return out


@pytest.mark.requires_probe
def test_real_exe_front_through_the_backend(fake_exe: Path, tmp_path: Path) -> None:
    scenario, ledger = _scenario(tmp_path, {
        "version": {"stdout": json.dumps({"version": "1.4.5-fake", "commit": "fake", "build_time": ""})},
        "user_credit": {"stdout": CREDIT_OK},
        "image2image": {"stdout": '{"submit_id": "exe-1"}'},
    })
    env = _env(
        scenario,
        FAKE_DREAMINA_PYTHON=sys.executable,
        FAKE_DREAMINA_SCRIPT=str(FAKE_DIR / "fake_dreamina.py"),
        PYTHONIOENCODING="utf-8",
    )
    h = _harness(tmp_path, DreaminaCliClient(fake_exe, timeout_s=30.0, base_env=env), ledger)
    assert h.backend.health() == BackendHealth(ok=True, failed_checks=(), version="1.4.5-fake", pause_reason=None)
    frozen = image_request(h, refs=(("c2-1", b"one"), ("p3-1", b"two")), prompt=TRICKY_PROMPT)
    assert h.backend.submit("job-1", frozen).platform_task_id == "exe-1"
    first, second = ((h.repo / CARD / f"{name}.png").resolve() for name in ("c2-1", "p3-1"))
    assert h.calls()[-1] == [
        "image2image", f"--images={first},{second}", f"--prompt={TRICKY_PROMPT}",
        "--model_version=5.0", "--ratio=3:4", "--resolution_type=2k",
    ]
    assert not [key for row in h.rows() for key in row["env_keys"] if key.startswith("JIMENG_BRIDGE_")]
