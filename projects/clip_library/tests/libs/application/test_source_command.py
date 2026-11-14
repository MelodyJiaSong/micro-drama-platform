from pathlib import Path

from dependency_injector import providers

from libs.application.containers.library__container import LibraryContainer
from libs.common.options import LicenseKind
from libs.common.types import Auth
from libs.infrastructure.daos.source__dao import SourceInfoDao


class StubYoutube:
    def info(self, url: str, auth: Auth) -> SourceInfoDao:
        return SourceInfoDao("vid00000001", url, "标题", "频道", "", 120.0, "20260101", 9, "", "{}")


class StubWriter:
    def __init__(self) -> None:
        self.saved = []

    def download(self, info, sub_langs, auth, notify):
        return "video.mp4", ("video.en.vtt",)

    def save(self, source):
        self.saved.append(source)


def test_download_records_license_and_reports_failures(tmp_path: Path) -> None:
    container = LibraryContainer()
    container.library.override(providers.Object(tmp_path))
    writer = StubWriter()
    container.youtube.override(providers.Object(StubYoutube()))
    container.source_writer.override(providers.Object(writer))
    ok = container.source_command().download(["u1"], None, "", "en", Auth(), lambda _: None)
    assert ok.items[0].status == "完成"
    assert writer.saved[0].license_kind == "quote"
    failed = container.source_command().download(["u2"], LicenseKind.CC_BY, "", "en", Auth(), lambda _: None)
    assert failed.items[0].status == "失败" and "Creative Commons" in failed.items[0].message
