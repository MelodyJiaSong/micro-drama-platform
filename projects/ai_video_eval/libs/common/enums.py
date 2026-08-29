from enum import Enum


class SubType(str, Enum):
    NOVEL = "novel"
    SHORT = "short"


class EvaluatorKind(str, Enum):
    LLM = "llm"
    RULE = "rule"


class FieldStatus(str, Enum):
    GRADED = "graded"
    INCONCLUSIVE = "inconclusive"
    INAPPLICABLE = "inapplicable"
    JUDGE_ERROR = "judge_error"


class VerdictTier(str, Enum):
    PASS = "pass"
    CONDITIONAL_PASS = "conditional_pass"
    FAIL = "fail"
    NEEDS_CANON_FIX = "needs_canon_fix"


class Severity(str, Enum):
    BLOCKER = "blocker"
    MAJOR = "major"
    MINOR = "minor"


TIER_ORDER: dict[VerdictTier, int] = {
    VerdictTier.PASS: 0,
    VerdictTier.CONDITIONAL_PASS: 1,
    VerdictTier.NEEDS_CANON_FIX: 2,
    VerdictTier.FAIL: 3,
}

SEVERITY_ORDER: dict[Severity, int] = {
    Severity.BLOCKER: 0,
    Severity.MAJOR: 1,
    Severity.MINOR: 2,
}
