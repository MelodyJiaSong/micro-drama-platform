class ClipError(Exception):
    pass


class InvalidTimeError(ClipError):
    def __init__(self, text: str) -> None:
        super().__init__(f"时间格式不对：{text}（用 秒、mm:ss 或 hh:mm:ss[.ms]）")


class EmptyRangeError(ClipError):
    def __init__(self) -> None:
        super().__init__("结束时间必须晚于开始时间")


class ClipOutOfRangeError(ClipError):
    def __init__(self, end: float, duration: float) -> None:
        super().__init__(f"结束时间 {end:.1f}s 超过视频时长 {duration:.1f}s")


class ClipTooLongError(ClipError):
    def __init__(self, seconds: float, limit: float) -> None:
        super().__init__(f"未授权素材只能短引用：本段 {seconds:.1f}s，上限 {limit:.0f}s")
