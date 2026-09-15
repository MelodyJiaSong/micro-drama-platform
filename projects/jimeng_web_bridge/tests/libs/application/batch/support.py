from __future__ import annotations

import shutil
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import tomlkit

from libs.application.commands.batch__command import BatchCommand
from libs.application.mappers.batch__mapper import BatchMapper
from libs.application.mappers.job__mapper import JobMapper
from libs.application.mappers.request__mapper import RequestMapper
from libs.application.mappers.request_asset__mapper import AssetRequestMapper
from libs.application.mappers.request_context__mapper import RequestContextMapper
from libs.application.mappers.request_drama__mapper import DramaSettingsMapper
from libs.application.mappers.request_entity__mapper import EntityCreateRequestMapper
from libs.application.mappers.request_input__mapper import RequestInputMapper
from libs.application.mappers.request_json__mapper import RequestJsonMapper
from libs.application.mappers.request_raw__mapper import RawRequestMapper
from libs.application.mappers.request_reference__mapper import ReferenceRequestMapper
from libs.application.mappers.request_shot__mapper import ShotRequestMapper
from libs.application.queries.batch__query import BatchQuery
from libs.application.repositories.batch__repository import SqliteBatchRepository
from libs.application.repositories.job__repository import SqliteJobRepository
from libs.common.clock import FrozenClock, iso
from libs.common.paths import RepoSandbox
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.daos.store_record__dao import EntitySnapshotDao
from libs.infrastructure.readers.asset_card__reader import AssetCardReader
from libs.infrastructure.readers.batch__reader import BatchReader
from libs.infrastructure.readers.drama_config__reader import DramaConfigReader
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from libs.infrastructure.readers.file_index__reader import FileIndexReader
from libs.infrastructure.readers.global_config__reader import GlobalConfigReader
from libs.infrastructure.readers.job__reader import JobReader
from libs.infrastructure.readers.markdown__reader import MarkdownReader
from libs.infrastructure.readers.shot_prompt__reader import ShotPromptReader
from libs.infrastructure.readers.store_record__reader import EntitySnapshotReader, IdempotencyReader
from libs.infrastructure.writers.batch__writer import BatchWriter
from libs.infrastructure.writers.batch_confirmation__writer import BatchConfirmationWriter
from libs.infrastructure.writers.job__writer import JobWriter
from libs.infrastructure.writers.secret_key__writer import SecretKeyWriter
from libs.infrastructure.writers.store_record__writer import EntitySnapshotWriter, IdempotencyWriter
from tests.libs.infrastructure.support import write_file

PROJECT_ROOT: Path = Path(__file__).resolve().parents[4]
T0: datetime = datetime(2026, 9, 13, 10, 0, 0, tzinfo=timezone.utc)

SERIES: str = "ai_videos/huangye_shenghuo"
HY3: str = f"{SERIES}/hy3"
SHOT02_DIR: str = f"{HY3}/5_6_分镜与prompt/shots/shot02"
SHOT02: str = f"{SHOT02_DIR}/shot02.md"
C1_DIR_NAME: str = "c1_砌炉的老人"
C1_DIR: str = f"{HY3}/2_世界观人设/characters/{C1_DIR_NAME}"
C1_CARD: str = f"{C1_DIR}/{C1_DIR_NAME}.md"
C1_1: str = f"{C1_DIR}/c1-1.png"
BG11: str = f"{HY3}/2_世界观人设/scenes/caoya/bg11_崖脚洼地/bg11-1.png"
P2: str = f"{HY3}/2_世界观人设/props/p2_随身装备/p2-1.png"
P3: str = f"{HY3}/2_世界观人设/props/p3_抹泥板与黏土壁炉/p3-1.png"
REXUE: str = "ai_videos/rexue_gaoxiao"
REXUE_SHOT01: str = f"{REXUE}/5_6_分镜与prompt/shots/shot01/shot01.md"
REXUE_SHOT21: str = f"{REXUE}/5_6_分镜与prompt/shots/shot21/shot21.md"
DUIKANG_SHOT01: str = "ai_videos/duikang_shangzeng/5_6_分镜与prompt/shots/shot01/shot01.md"

COPIED_FROM_REAL_REPO: tuple[str, ...] = (
    f"{SERIES}/series.json",
    f"{SERIES}/_series/series_bible.md",
    SHOT02,
    C1_CARD,
    C1_1,
    BG11,
    P2,
    P3,
    REXUE_SHOT01,
    REXUE_SHOT21,
    DUIKANG_SHOT01,
)
SAME_STEM_TRAPS: tuple[str, ...] = (
    f"{SERIES}/hy1/2_世界观人设/scenes/yulin/bg11_溪谷/bg11-1.png",
    f"{SERIES}/hy2/2_世界观人设/scenes/hongshan/bg11_地窝风暴夜/bg11-1.png",
    f"{SERIES}/hy2/2_世界观人设/props/p3_树皮门与顶/p3-1_树皮门板锚点.png",
    f"{SERIES}/hy4/2_世界观人设/scenes/shenxue/bg11_雪井风雪夜/bg11-1.png",
    f"{SERIES}/hy4/2_世界观人设/props/p2_冰镩/p2-1.png",
    f"{SERIES}/hy4/2_世界观人设/props/p3_随身装备与食材/p3-1.png",
)


def build_template(real_root: Path, template: Path, on_missing: Callable[[str], None]) -> None:
    for rel in COPIED_FROM_REAL_REPO:
        source = real_root / rel
        if not source.is_file():
            on_missing(rel)
        target = template / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    for rel in SAME_STEM_TRAPS:
        write_file(template, rel, b"trap: same stem in another episode")


def hy3_config(**reference_overrides: str) -> Callable[[dict[str, Any]], None]:
    def mutate(data: dict[str, Any]) -> None:
        data["entities"]["overrides"][C1_DIR_NAME] = "hy3_主角"
        data["references"]["overrides"].update(reference_overrides)

    return mutate


@dataclass
class BatchEnv:
    repo: Path
    data_dir: Path
    global_path: Path
    clock: FrozenClock
    client: SqliteClient
    command: BatchCommand
    query: BatchQuery
    jobs: SqliteJobRepository
    batches: SqliteBatchRepository
    job_reader: JobReader
    job_writer: JobWriter

    def write_drama_config(self, drama_rel: str, mutate: Callable[[dict[str, Any]], None] | None = None) -> None:
        data: dict[str, Any] = DramaConfig.defaults(drama_rel.rsplit("/", 1)[-1])
        if mutate is not None:
            mutate(data)
        write_file(self.repo, f"{drama_rel}/jimeng_config.toml", tomlkit.dumps(data))

    def set_global(self, section: str, key: str, value: object) -> None:
        document = tomlkit.parse(self.global_path.read_text(encoding="utf-8"))
        document[section][key] = value  # type: ignore[index]
        self.global_path.write_text(tomlkit.dumps(document), encoding="utf-8")

    def seed_snapshot(self, *names: str) -> None:
        records = [EntitySnapshotDao(name, None, None, iso(self.clock.now())) for name in names]
        EntitySnapshotWriter(self.client).replace_all(records)

    def job_count(self) -> int:
        return int(self.client.query("SELECT COUNT(*) FROM jobs")[0][0])

    def batch_count(self) -> int:
        return int(self.client.query("SELECT COUNT(*) FROM batches")[0][0])


def build_env(repo: Path, data_dir: Path, global_path: Path, clock: FrozenClock) -> BatchEnv:
    sandbox = RepoSandbox(repo, (data_dir,))
    client = SqliteClient(data_dir / "bridge.db")
    key_path = data_dir / "secret.key"
    SecretKeyWriter().ensure(key_path)
    tree = DramaTreeReader(sandbox)
    references = ReferenceRequestMapper(sandbox, tree, FileIndexReader(sandbox))
    requests = RequestMapper(
        sandbox,
        RequestInputMapper(),
        DramaSettingsMapper(DramaConfigReader(sandbox)),
        ShotRequestMapper(ShotPromptReader(sandbox), tree, references),
        AssetRequestMapper(AssetCardReader(sandbox), tree, references),
        RawRequestMapper(tree, references),
        EntityCreateRequestMapper(sandbox, tree, MarkdownReader(), references),
    )
    json_mapper = RequestJsonMapper()
    batch_mapper = BatchMapper(json_mapper)
    job_mapper = JobMapper(json_mapper)
    batch_repository = SqliteBatchRepository(BatchReader(client), BatchWriter(client), batch_mapper, clock)
    job_reader = JobReader(client)
    job_writer = JobWriter(client)
    global_reader = GlobalConfigReader(global_path)
    command = BatchCommand(
        global_reader,
        requests,
        RequestInputMapper(),
        RequestContextMapper(sandbox, EntitySnapshotReader(client), job_reader),
        batch_mapper,
        job_mapper,
        batch_repository,
        job_reader,
        BatchConfirmationWriter(client),
        IdempotencyReader(client),
        IdempotencyWriter(client),
        SecretKeyWriter(),
        key_path,
        clock,
    )
    query = BatchQuery(
        global_reader, batch_repository, batch_mapper, BatchReader(client), job_reader, SecretKeyWriter(), key_path, clock
    )
    jobs = SqliteJobRepository(job_reader, job_writer, job_mapper, tree, clock)
    return BatchEnv(repo, data_dir, global_path, clock, client, command, query, jobs, batch_repository, job_reader, job_writer)
