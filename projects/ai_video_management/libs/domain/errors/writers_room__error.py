class WritersRoomError(Exception):
    def __init__(self, message: str, kind: str = "writers_room_error", status_code: int = 400) -> None:
        super().__init__(message)
        self.kind = kind
        self.status_code = status_code
