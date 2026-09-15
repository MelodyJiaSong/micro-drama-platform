from libs.common.enums import OperationState


class OperationError(Exception):
    error_code: str = "operation_error"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message: str = message


class OperationInvariantError(OperationError):
    error_code = "operation_invariant"


class IllegalOperationTransitionError(OperationError):
    error_code = "illegal_operation_transition"

    def __init__(self, from_state: OperationState, command: str) -> None:
        super().__init__(f"operation 处于 {from_state}，不能执行 {command}")
        self.from_state: OperationState = from_state
        self.command: str = command
