import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from libs.application.mappers.shot__mapper import ShotMapper
from libs.common.enums import SubType
from libs.infrastructure.readers.shot__reader import ShotReader

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")
MINI = os.path.join(FIXTURES, "mini_drama")


def _shot_path(shot_id: str) -> str:
    return os.path.join(
        MINI, "5_6_分镜与prompt", "episodes", "ep01", "shots", shot_id, f"{shot_id}.md"
    )


@pytest.fixture(scope="session")
def shot01():
    dao = ShotReader().read(_shot_path("shot01"))
    return ShotMapper().map(dao, "mini_drama", SubType.NOVEL, "ep01", "shot01", 0, 2)


@pytest.fixture(scope="session")
def shot02():
    dao = ShotReader().read(_shot_path("shot02"))
    return ShotMapper().map(dao, "mini_drama", SubType.NOVEL, "ep01", "shot02", 1, 2)
