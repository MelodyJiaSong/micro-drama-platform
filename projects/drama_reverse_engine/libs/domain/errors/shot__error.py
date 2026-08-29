from __future__ import annotations


class ShotError(Exception):
    pass


class InvalidTimeRangeError(ShotError):
    pass


class PromptBudgetExceededError(ShotError):
    pass


class DescriptorDriftError(ShotError):
    pass


class SubtitleContaminationError(ShotError):
    pass


class CorruptExtractOutputError(ShotError):
    pass
