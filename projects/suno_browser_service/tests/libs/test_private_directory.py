import json
import os
import subprocess
from pathlib import Path
from unittest.mock import Mock

import pytest

from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.infrastructure.writers.audio__writer import AudioWriter
from projects.suno_browser_service.libs.infrastructure.writers.private_directory__writer import PrivateDirectoryWriter


pytestmark = pytest.mark.skipif(os.name != "nt", reason="Windows NTFS ACL / junction verification")
SONG_ID = "12345678-1234-1234-1234-123456789abc"


def powershell(script: str, **paths: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
        env={**os.environ, **{key: str(value) for key, value in paths.items()}},
        capture_output=True, text=True, timeout=30,
    )


def acl(path: Path) -> dict:
    result = powershell(
        "$a = Get-Acl -LiteralPath $env:SUNO_TEST_ACL_PATH; "
        "$u = [System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value; "
        "@{protected=$a.AreAccessRulesProtected; user=$u; "
        "rules=@($a.Access | ForEach-Object { "
        "@{sid=$_.IdentityReference.Translate([System.Security.Principal.SecurityIdentifier]).Value; "
        "allow=($_.AccessControlType -eq 'Allow')} })} | ConvertTo-Json -Depth 4 -Compress",
        SUNO_TEST_ACL_PATH=path,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_private_directory_removes_broad_access_and_propagates_to_existing_file(tmp_path: Path):
    root = tmp_path / "private"
    root.mkdir()
    state = root / "fake-storage-state.json"
    state.write_text("{}", encoding="utf-8")
    granted = subprocess.run(
        ["icacls", str(root), "/grant", "*S-1-5-11:(OI)(CI)M"],
        capture_output=True, text=True, timeout=15,
    )
    assert granted.returncode == 0, granted.stderr
    assert "S-1-5-11" in {rule["sid"] for rule in acl(state)["rules"]}

    PrivateDirectoryWriter.ensure(root)

    root_acl = acl(root)
    assert root_acl["protected"] is True
    for current in (root_acl, acl(state)):
        allowed = {current["user"], "S-1-5-18", "S-1-5-32-544"}
        assert {rule["sid"] for rule in current["rules"] if rule["allow"]} <= allowed
        assert current["user"] in {rule["sid"] for rule in current["rules"] if rule["allow"]}


def test_download_rejects_parent_junction_before_creating_external_job_directory(tmp_path: Path):
    service = tmp_path / "service"
    outside = tmp_path / "outside-output-root"
    service.mkdir()
    outside.mkdir()
    junction = service / "outputs"
    created = powershell(
        "New-Item -ItemType Junction -Path $env:SUNO_TEST_LINK "
        "-Target $env:SUNO_TEST_TARGET -ErrorAction Stop | Out-Null",
        SUNO_TEST_LINK=junction, SUNO_TEST_TARGET=outside,
    )
    if created.returncode:
        pytest.skip("Windows junction creation unavailable: " + created.stderr.strip())
    try:
        job_id = "a" * 32
        ui = Mock()
        writer = AudioWriter(ui, junction / job_id)
        with pytest.raises(ServiceError) as raised:
            writer.download("https://suno.com/song/" + SONG_ID, "mp3")
        assert raised.value.code == "unsafe_output"
        ui.navigate.assert_not_called()
        assert not (outside / job_id).exists(), "Rejected output must not create a directory outside its root"
        assert list(outside.iterdir()) == []
    finally:
        assert junction.parent.resolve().is_relative_to(tmp_path.resolve())
        assert outside.resolve().is_relative_to(tmp_path.resolve())
        junction.rmdir()
