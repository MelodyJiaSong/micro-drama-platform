from typing import BinaryIO

from projects.suno_browser_service.libs.common.settings import Settings
from projects.suno_browser_service.libs.infrastructure.clients.asset__client import AssetClient


class AssetCommand:
    def __init__(self, settings: Settings) -> None:
        self.assets = AssetClient(settings)

    def upload(self, filename: str, stream: BinaryIO, rights_confirmed: bool) -> dict:
        return self.assets.put(filename, stream, rights_confirmed)

    def get(self, asset_id: str) -> dict:
        return self.assets.get(asset_id)
