from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from libs.infrastructure.clients.dreamina_cli__client import DreaminaCliClient

FIXTURES = Path(__file__).resolve().parents[3] / "fixtures" / "fake_dreamina"
CSC = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Microsoft.NET" / "Framework64" / "v4.0.30319" / "csc.exe"

pytestmark = pytest.mark.skipif(sys.platform != "win32" or not CSC.is_file(), reason="needs Windows .NET Framework csc.exe")


@pytest.fixture(scope="module")
def fake_exe(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("fake_exe") / "dreamina.exe"
    compiled = subprocess.run(
        [str(CSC), "/nologo", "/optimize", f"/out:{out}", str(FIXTURES / "FakeDreaminaLauncher.cs")],
        capture_output=True,
        check=False,
    )
    if compiled.returncode != 0:
        pytest.skip(f"csc failed: {compiled.stdout.decode(errors='replace')[-300:]}")
    return out


def test_real_exe_receives_tricky_prompt_as_one_exact_argument(fake_exe: Path, tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.jsonl"
    scenario = tmp_path / "scenario.json"
    scenario.write_text(
        json.dumps({"ledger": str(ledger), "commands": {"text2image": {"stdout": '{"submit_id": "s-1"}'}}}),
        encoding="utf-8",
    )
    env = {
        "FAKE_DREAMINA_SCENARIO": str(scenario),
        "FAKE_DREAMINA_PYTHON": sys.executable,
        "FAKE_DREAMINA_SCRIPT": str(FIXTURES / "fake_dreamina.py"),
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", r"C:\Windows"),
        "PYTHONIOENCODING": "utf-8",
    }
    prompt = 'c1-1_立绘\n他说："别动" \\"quoted\\" C:\\path\\ & | %PATH% ; 结尾反斜杠\\'
    client = DreaminaCliClient(fake_exe, timeout_s=30.0, base_env=env)
    assert client.text2image(prompt, "5.0", "3:4", "2k").submit_id == "s-1"
    argv = json.loads(ledger.read_text(encoding="utf-8").splitlines()[0])["argv"]
    assert argv == ["text2image", f"--prompt={prompt}", "--model_version=5.0", "--ratio=3:4", "--resolution_type=2k"]
