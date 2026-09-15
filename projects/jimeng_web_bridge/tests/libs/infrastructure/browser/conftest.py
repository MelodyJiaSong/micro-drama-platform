from __future__ import annotations

from collections.abc import Iterator

import pytest

from libs.infrastructure.clients.jimeng_browser__client import JimengBrowserClient
from tests.fixtures.fake_jimeng_site.server import FakeJimengSite, fake_jimeng_site  # noqa: F401
from tests.libs.infrastructure.browser.support import start_client


@pytest.fixture(scope="session")
def browser_client(fake_jimeng_site: FakeJimengSite, tmp_path_factory: pytest.TempPathFactory) -> Iterator[JimengBrowserClient]:  # noqa: F811
    client = start_client(fake_jimeng_site, tmp_path_factory.mktemp("browser_profile"))
    yield client
    client.close()
