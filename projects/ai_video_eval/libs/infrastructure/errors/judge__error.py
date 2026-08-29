class JudgeError(Exception):
    pass


class JudgeRefusedError(JudgeError):
    pass


class JudgeSchemaError(JudgeError):
    pass


class ApiKeyMissingError(JudgeError):
    pass
