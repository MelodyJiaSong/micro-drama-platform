from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from libs.infrastructure.clients.dreamina_cli__client import DreaminaCliClient
from libs.infrastructure.errors.dreamina_cli__error import DreaminaCliError, DreaminaFailureKind

FAKE = Path(__file__).resolve().parents[3] / "fixtures" / "fake_dreamina" / "fake_dreamina.py"
REAL_RECORD_NOT_FOUND = (
    "\n2026/09/13 19:15:22 \x1b[31;1mcode.byted.org/videocut-aigc/dreamina_cli/components/task/store.go:278 "
    "\x1b[35;1mrecord not found\n\x1b[0m\x1b[33m[0.000ms] \x1b[34;1m[rows:0]\x1b[0m SELECT * FROM `aigc_task` "
    'WHERE submit_id = "00000000-bogus" ORDER BY `aigc_task`.`submit_id` LIMIT 1\n'
)
REAL_LIST_TASK = json.dumps(
    [
        {
            "submit_id": "3f6eb41f-0000-0000-0000-000000000000",
            "gen_task_type": "text2image",
            "gen_status": "success",
            "fail_reason": "",
            "result_json": {"images": [{"width": 1440, "height": 2560}], "videos": []},
            "commerce_info": {
                "credit_count": 1,
                "triplet": {"resource_type": "", "resource_id": "", "benefit_type": ""},
                "triplets": [{"resource_type": "aigc", "resource_id": "<RESOURCE>", "benefit_type": "<BENEFIT>"}],
            },
        }
    ]
)


def _client(tmp_path: Path, commands: dict[str, dict[str, object]], timeout_s: float = 20.0) -> tuple[DreaminaCliClient, Path]:
    ledger = tmp_path / "ledger.jsonl"
    scenario = tmp_path / "scenario.json"
    scenario.write_text(json.dumps({"ledger": str(ledger), "commands": commands}, ensure_ascii=False), encoding="utf-8")
    env = {
        "FAKE_DREAMINA_SCENARIO": str(scenario),
        "SYSTEMROOT": "C:\\Windows",
        "PATH": "",
        "JIMENG_BRIDGE_TOKEN": "must-not-leak-" + "x" * 30,
    }
    client = DreaminaCliClient(FAKE, timeout_s=timeout_s, launcher_prefix=(sys.executable,), base_env=env)
    return client, ledger


def _ledger(ledger: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]


def test_version_parses_real_shape(tmp_path: Path) -> None:
    client, _ = _client(tmp_path, {"version": {"stdout": '{\n  "version": "46b5b0e-dirty",\n  "commit": "46b5b0e",\n  "build_time": "2026-06-03T19:39:25Z"\n}'}})
    version = client.version()
    assert (version.version, version.commit) == ("46b5b0e-dirty", "46b5b0e")


def test_user_credit_parses_real_shape(tmp_path: Path) -> None:
    client, _ = _client(tmp_path, {"user_credit": {"stdout": '{"total_credit": 8712, "user_id": 1, "user_name": "", "vip_level": "ultra"}'}})
    credit = client.user_credit()
    assert (credit.total_credit, credit.vip_level) == (8712, "ultra")


def test_prompt_with_quotes_newlines_and_chinese_arrives_as_one_exact_argument(tmp_path: Path) -> None:
    prompt = 'c1-1_立绘\n一位"老人" & 50% | echo %PATH% ; `rm`'
    client, ledger = _client(tmp_path, {"text2image": {"stdout": '{"submit_id": "abc-123", "gen_status": "querying"}'}})
    submitted = client.text2image(prompt, model_version="5.0", ratio="3:4", resolution_type="2k")
    assert submitted.submit_id == "abc-123"
    argv = _ledger(ledger)[0]["argv"]
    assert argv == ["text2image", f"--prompt={prompt}", "--model_version=5.0", "--ratio=3:4", "--resolution_type=2k"]


def test_bridge_secrets_are_not_passed_to_the_child(tmp_path: Path) -> None:
    client, ledger = _client(tmp_path, {"user_credit": {"stdout": '{"total_credit": 1}'}})
    client.user_credit()
    assert not any(key.startswith("JIMENG_BRIDGE_") for key in _ledger(ledger)[0]["env_keys"])


def test_real_record_not_found_output_is_classified_without_json(tmp_path: Path) -> None:
    client, _ = _client(tmp_path, {"query_result": {"stdout": REAL_RECORD_NOT_FOUND, "exit": 1}})
    with pytest.raises(DreaminaCliError) as caught:
        client.query_result("00000000-bogus", tmp_path / "dl")
    assert caught.value.kind is DreaminaFailureKind.NOT_FOUND
    assert caught.value.exit_code == 1
    assert "\x1b[" not in caught.value.output_tail


@pytest.mark.parametrize(
    ("output", "kind"),
    [
        ("error: AigcComplianceConfirmationRequired", DreaminaFailureKind.COMPLIANCE_CONFIRMATION_REQUIRED),
        ("please run dreamina login first", DreaminaFailureKind.NOT_LOGGED_IN),
        ("boom", DreaminaFailureKind.UNKNOWN),
    ],
)
def test_nonzero_exit_is_classified(tmp_path: Path, output: str, kind: DreaminaFailureKind) -> None:
    client, _ = _client(tmp_path, {"text2image": {"stderr": output, "exit": 3}})
    with pytest.raises(DreaminaCliError) as caught:
        client.text2image("p", "5.0", "1:1", "2k")
    assert caught.value.kind is kind


def test_timeout_is_reported(tmp_path: Path) -> None:
    client, _ = _client(tmp_path, {"user_credit": {"stdout": "{}", "sleep_s": 5}}, timeout_s=1.0)
    with pytest.raises(DreaminaCliError) as caught:
        client.user_credit()
    assert caught.value.kind is DreaminaFailureKind.TIMEOUT


def test_submit_without_submit_id_is_unparseable(tmp_path: Path) -> None:
    client, _ = _client(tmp_path, {"text2image": {"stdout": '{"gen_status": "fail"}'}})
    with pytest.raises(DreaminaCliError) as caught:
        client.text2image("p", "5.0", "1:1", "2k")
    assert caught.value.kind is DreaminaFailureKind.UNPARSEABLE_OUTPUT


def test_query_result_reports_only_newly_downloaded_files(tmp_path: Path) -> None:
    download_dir = tmp_path / "dl"
    download_dir.mkdir()
    (download_dir / "old.png").write_bytes(b"old")
    client, ledger = _client(
        tmp_path,
        {"query_result": {"stdout": '{"submit_id": "abc", "gen_status": "success"}', "create_files": ["a.png", "b.png"]}},
    )
    result = client.query_result("abc", download_dir)
    assert [path.name for path in result.downloaded_files] == ["a.png", "b.png"]
    assert _ledger(ledger)[0]["argv"] == ["query_result", "--submit_id=abc", f"--download_dir={download_dir}"]


def test_list_task_parses_real_shape(tmp_path: Path) -> None:
    client, _ = _client(tmp_path, {"list_task": {"stdout": REAL_LIST_TASK}})
    tasks = client.list_task(limit=2)
    assert tasks[0].gen_status == "success" and tasks[0].credit_count == 1 and tasks[0].image_count == 1


def test_non_exe_path_is_rejected_without_a_test_launcher(tmp_path: Path) -> None:
    for name in ("dreamina.cmd", "dreamina.bat", "dreamina.ps1", "dreamina"):
        with pytest.raises(DreaminaCliError) as caught:
            DreaminaCliClient(tmp_path / name, timeout_s=5.0)
        assert caught.value.kind is DreaminaFailureKind.EXECUTABLE_REJECTED
