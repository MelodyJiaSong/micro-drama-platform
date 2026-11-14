from libs.common.options import LICENSE_LABELS, LicenseKind


class LicenseError(Exception):
    pass


class LicenseEvidenceMissingError(LicenseError):
    def __init__(self, kind: LicenseKind) -> None:
        super().__init__(f"标为「{LICENSE_LABELS[kind]}」必须用 --note 写明依据（许可链接、邮件、来源说明）")


class LicenseMismatchError(LicenseError):
    def __init__(self) -> None:
        super().__init__("平台没有标 Creative Commons 授权，不能记为 CC；有作者许可用 permission，否则用 quote")
