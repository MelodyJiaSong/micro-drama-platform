from __future__ import annotations

import hashlib
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from libs.application.commands.drama_config__command import DramaConfigCommand
from libs.application.mappers.drama_config__mapper import DramaConfigMapper
from libs.application.mappers.entity__mapper import EntityMapper
from libs.application.queries.drama_config__query import DramaConfigQuery
from libs.application.queries.entity__query import EntityQuery
from libs.common.clock import FrozenClock, iso
from libs.common.paths import RepoSandbox
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.daos.store_record__dao import EntitySnapshotDao
from libs.infrastructure.readers.drama_config__reader import DramaConfigReader
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from libs.infrastructure.readers.global_config__reader import GlobalConfigReader
from libs.infrastructure.readers.shot_prompt__reader import ShotPromptReader
from libs.infrastructure.readers.store_record__reader import EntitySnapshotReader
from libs.infrastructure.readers.toml_file__reader import TomlFileReader
from libs.infrastructure.writers.drama_config__writer import DramaConfigWriter
from libs.infrastructure.writers.store_record__writer import EntitySnapshotWriter
from tests.libs.infrastructure.support import find_repo_root, skip_or_fail, write_file

PROJECT_ROOT: Path = Path(__file__).resolve().parents[4]
GLOBAL_TOML: Path = PROJECT_ROOT / "config" / "global.toml"
SERIES: str = "ai_videos/huangye_shenghuo"
HY1: str = f"{SERIES}/hy1"
HY2: str = f"{SERIES}/hy2"
HY3: str = f"{SERIES}/hy3"
FLAT: str = "ai_videos/solo_drama"
T0: datetime = datetime(2026, 9, 13, 10, 0, 0, tzinfo=timezone.utc)
CONFIG_NAME: str = "jimeng_config.toml"

_COPY_SUFFIXES: frozenset[str] = frozenset({".md", ".json"})
_PLACEHOLDER_SUFFIXES: frozenset[str] = frozenset({".png", ".jpg", ".jpeg", ".webp", ".mp4", ".mov"})
_SENTINEL_MEDIA: str = f"{HY3}/2_世界观人设/characters/c1_砌炉的老人/c1-1.png"

FLAT_SHOT01: str = """# shot01

## 视频 prompt

```text
参考: `缺失图(场景参考图)=>@`，`双胞胎(道具参考图)=>@`，`某物(神秘标签)=>@`，`独行者(人物主体)=>@`
情节: 测试镜。
比例: 9:16
时长: 5秒
```
"""

FLAT_SHOT02: str = """# shot02

## 视频 prompt

```text
参考: `旧图(场景参考图)=>@1`
情节: 旧写法。
比例: 9:16
时长: 5秒
```
"""


def build_repo_template(root: Path) -> None:
    """hy1–hy3 markdown/json copied byte-for-byte; media become empty placeholders (resolvers only need names)."""
    real = find_repo_root()
    if real is None or not (real / _SENTINEL_MEDIA).is_file():
        skip_or_fail("real ai_videos tree or its media is absent (python tools/assets_sync.py pull)")
        return
    source = real / SERIES
    shutil.copyfile(source / "series.json", root / _mkparent(root / SERIES / "series.json"))
    for episode in ("hy1", "hy2", "hy3", "_series"):
        for path in sorted((source / episode).rglob("*")):
            relative = path.relative_to(source)
            if not path.is_file() or "_deleted" in relative.parts or path.name == CONFIG_NAME:
                continue
            target = _mkparent(root / SERIES / relative)
            suffix = path.suffix.lower()
            if suffix in _COPY_SUFFIXES:
                shutil.copyfile(path, target)
            elif suffix in _PLACEHOLDER_SUFFIXES:
                target.write_bytes(b"")
    write_file(root, f"{FLAT}/characters/c1_独行者/c1_独行者.md", "# c1_独行者\n")
    write_file(root, f"{FLAT}/characters/c1_独行者/c1-1.png", b"")
    write_file(root, f"{FLAT}/props/p1_甲/双胞胎.png", b"")
    write_file(root, f"{FLAT}/props/p2_乙/双胞胎.png", b"")
    write_file(root, f"{FLAT}/shots/shot01/shot01.md", FLAT_SHOT01)
    write_file(root, f"{FLAT}/shots/shot02/shot02.md", FLAT_SHOT02)
    write_file(root, "ai_videos/notes/note.txt", "not a drama")
    write_file(root, "ai_videos/empty_series/series.json", "{}")
    write_file(root, "ai_videos/_deleted/old_drama/shots/shot01/shot01.md", "x")


def _mkparent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def config_text(mapper: DramaConfigMapper, abbrev: str = "hy3", overrides: dict[str, str] | None = None) -> str:
    data = DramaConfig.defaults(abbrev)
    if overrides:
        data["entities"] = {**_as_dict(data["entities"]), "overrides": overrides}
    text = mapper.toml_text(data)
    return text.replace("[video]\n", "[video]\n# 视频默认档位，按剧调整\n", 1)


def _as_dict(value: object) -> dict[str, object]:
    assert isinstance(value, dict)
    return value


@dataclass
class Harness:
    repo: Path
    data_dir: Path
    global_path: Path
    sandbox: RepoSandbox
    db: SqliteClient
    snapshot_writer: EntitySnapshotWriter
    snapshot_reader: EntitySnapshotReader
    clock: FrozenClock
    mapper: DramaConfigMapper
    entity_mapper: EntityMapper
    configs: DramaConfigQuery
    config_command: DramaConfigCommand
    entities: EntityQuery

    def sync(self, *names: str, at: datetime | None = None) -> None:
        synced_at = iso(at or self.clock.now())
        self.snapshot_writer.replace_all([EntitySnapshotDao(name, None, None, synced_at) for name in names])

    def write_config(self, drama_rel: str, text: str) -> Path:
        return write_file(self.repo, f"{drama_rel}/{CONFIG_NAME}", text)

    def config_path(self, drama_rel: str) -> Path:
        return self.repo / drama_rel / CONFIG_NAME


def build_harness(repo: Path, work: Path) -> Harness:
    data_dir = work / "data"
    global_path = _mkparent(work / "config" / "global.toml")
    shutil.copyfile(GLOBAL_TOML, global_path)
    sandbox = RepoSandbox(repo, (data_dir,))
    db = SqliteClient(data_dir / "bridge.db")
    snapshot_reader = EntitySnapshotReader(db)
    clock = FrozenClock(T0)
    mapper = DramaConfigMapper()
    entity_mapper = EntityMapper()
    global_reader = GlobalConfigReader(global_path)
    config_reader = DramaConfigReader(sandbox)
    configs = DramaConfigQuery(
        sandbox, DramaTreeReader(sandbox), config_reader, global_reader, ShotPromptReader(sandbox), snapshot_reader, mapper
    )
    return Harness(
        repo=repo,
        data_dir=data_dir,
        global_path=global_path,
        sandbox=sandbox,
        db=db,
        snapshot_writer=EntitySnapshotWriter(db),
        snapshot_reader=snapshot_reader,
        clock=clock,
        mapper=mapper,
        entity_mapper=entity_mapper,
        configs=configs,
        config_command=DramaConfigCommand(configs, config_reader, DramaConfigWriter(sandbox), TomlFileReader(), mapper),
        entities=EntityQuery(configs, snapshot_reader, global_reader, clock, entity_mapper, test_mode=False),
    )
