from libs.application.dtos.request_log__dto import RequestLogQdto
from libs.infrastructure.readers.request_log__reader import RequestLogReader


class RequestLogQuery:
    def __init__(self, reader: RequestLogReader) -> None:
        self._reader = reader

    def list(self) -> RequestLogQdto:
        result = self._reader.list()
        return RequestLogQdto(result.logs, result.entries, result.total)

    def read(self, path: str, offset: int, limit: int) -> RequestLogQdto:
        result = self._reader.read(path, offset, limit)
        return RequestLogQdto(result.logs, result.entries, result.total)
