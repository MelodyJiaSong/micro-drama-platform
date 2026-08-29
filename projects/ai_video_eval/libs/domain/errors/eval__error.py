class EvalError(Exception):
    pass


class RubricError(EvalError):
    pass


class ArtifactError(EvalError):
    pass


class AggregationError(EvalError):
    pass
