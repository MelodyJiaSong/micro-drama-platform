import pytest

from libs.common.options import QUOTE_MAX_SECONDS, LicenseKind
from libs.domain.errors.license__error import LicenseEvidenceMissingError, LicenseMismatchError
from libs.domain.value_objects.license__valueobject import License

CC = "Creative Commons Attribution license (reuse allowed)"


def test_platform_cc_is_detected_automatically() -> None:
    assert License.resolve(None, CC, "").kind == LicenseKind.CC_BY


def test_unlabelled_video_defaults_to_quote_with_cap() -> None:
    license = License.resolve(None, "", "")
    assert license.kind == LicenseKind.QUOTE
    assert license.max_clip_seconds == QUOTE_MAX_SECONDS


def test_cc_claim_without_platform_label_is_rejected() -> None:
    with pytest.raises(LicenseMismatchError):
        License.resolve(LicenseKind.CC_BY, "", "")


@pytest.mark.parametrize("kind", [LicenseKind.PERMISSION, LicenseKind.PUBLIC_DOMAIN])
def test_permission_needs_evidence(kind: LicenseKind) -> None:
    with pytest.raises(LicenseEvidenceMissingError):
        License.resolve(kind, "", " ")
    assert License.resolve(kind, "", "作者邮件 2026-11-14").max_clip_seconds is None


def test_session_requires_login_cookie() -> None:
    from libs.domain.errors.session__error import NotLoggedInError
    from libs.domain.value_objects.session__valueobject import Session, in_scope
    assert Session(frozenset({"SAPISID", "PREF"}))
    with pytest.raises(NotLoggedInError):
        Session(frozenset({"PREF"}))
    assert in_scope(".youtube.com") and not in_scope("example.com")
