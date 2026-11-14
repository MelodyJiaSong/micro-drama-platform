"""英雄 demo 定版标记（follow-up 315）：全部剧里 demo 已定版的人物。只读。"""
from __future__ import annotations

from libs.application.dtos.demo_status__dto import DemoStatusListQdto
from libs.infrastructure.readers.demo_status__reader import DemoStatusReader


class DemoStatusQuery:
    def __init__(self, reader: DemoStatusReader) -> None:
        self.reader = reader

    def read(self) -> DemoStatusListQdto:
        return DemoStatusListQdto(self.reader.read())
