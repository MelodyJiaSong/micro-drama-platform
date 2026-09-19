"""UT-R-SHOT-01 / UT-R-SHOT-18: pinned prompt bytes per real fixture, and provenance against `SOURCES.md`.

Golden values were produced by the reader and cross-checked against an independent line-based
extractor (first ```text fence under `## 视频 prompt`, marked negative fence) before being pinned.
"""
from __future__ import annotations

import hashlib
import re
import warnings

import pytest

from libs.common.paths import RepoSandbox
from libs.infrastructure.readers.shot_prompt__reader import ShotPromptReader
from tests.libs.infrastructure.support import FIXTURES_DIR, REAL_CARDS_DIR, REAL_SHOTS_DIR, require_repo_root

READER = ShotPromptReader(RepoSandbox(REAL_SHOTS_DIR))
_SOURCE_ROW_RE = re.compile(r"^\| `(real_(?:shots|cards)/[^`]+)` \| `(ai_videos/[^`]+)` \|$", re.MULTILINE)

# name -> (prompt sha256, prompt code points, negative prompt sha256 | None)
GOLDEN: dict[str, tuple[str, int, str | None]] = {
    "duikang__shot01.md": ("975b6761af94d86e153385c46ac0c6058ea5a9b14f984964a9fa97babf2f292a", 1196, "232a7f52215d9c4e54d0e56f747b201847c7e2e5980e29806c050719ffeac977"),
    "duikang__shot09.md": ("88420d5813b0c77873417c2b4832bdd16fc07085af321cb49ca75cf3472ab74e", 1046, "44b41b9a2a937c35e02b24d8e0064590d7e5f2d750f22904836d3514fda46dff"),
    "duikang__shot20.md": ("46b6540b171631a9ff4b1a958dcb94a7c11ff2485d6e3795914b5f10c6abf4a2", 1258, "5e79eb7e680e652c0f712bf3611fb8924ee3840db64cfc01d0ccc93eeb07d59e"),
    "hy2__shot01.md": ("9243eee27f50ae7948b08ea3deb1f86353cc6fdca858095fcdaefdafae28d8a5", 2155, "1a77256f471db06b25f6d39d7a0ab8d86cae2c84c9af584738505fa451e6f683"),
    "hy2__shot02.md": ("0eb4b7b693214c1e388be2012450391fa550ac28c7c7efdc1478e239f36b461d", 2218, "1a77256f471db06b25f6d39d7a0ab8d86cae2c84c9af584738505fa451e6f683"),
    "hy3__shot02.crlf.md": ("631e682e28ad089eacaf9e4118f0a05eb6a51824709991e9d7d1d76fa66a94de", 2314, "69bc6313cc14ef2753c8761bc3424d3119770644057247281126d61a2496d8e3"),
    "hy3__shot02.md": ("631e682e28ad089eacaf9e4118f0a05eb6a51824709991e9d7d1d76fa66a94de", 2314, "69bc6313cc14ef2753c8761bc3424d3119770644057247281126d61a2496d8e3"),
    "rexue__shot01.md": ("4b6991b93a321b83d00daf8e0bf759125b954a7f3fa1610d27a99461cfd56256", 508, None),
    "rexue__shot21.md": ("585c708b4366fcb44926e223b0daed72971c8cc7262580b7d5395ad7b39c8ecb", 569, None),
    "wushen__ep01_shot03.md": ("eeafec6682febf73fd5bd54d800001dd5ab379e5656074f89bacc2e4c9fa4629", 2208, None),
    "wushen__ep03_shot05.md": ("31425e26607cc890dd4ce74c08d5c9f0e2470dbbb936fbdcd4bdee71929f9e63", 1558, None),
    "wushen__ep06_shot01.md": ("ae8332ccd7c84974825c62dfd1930408963ca4364e687e1fe135a8e8f20ac26a", 1997, None),
    "xianjian__shot01.md": ("73c7e7ef2274db9c82093d1fee9c931aac0b187d72677a4445b87adf75ea5dc9", 1255, "429ba7641a40ed6ccc0609faef1c9bb4fcc871504a34de1d807601432331dc33"),
    "xianjian__shot02.md": ("a9753378b29592961e25080cb53ce25fc7e15b29bd6d5a955eb642e15247ed02", 1633, "becfb87590eb67a6dc0955b460596026053bf6c00088a6673b27418a921abdcb"),
    "xianjian__shot03.md": ("849acec7350174c6ae21b240ccf27d7d82b57b2ec9fe3bdc3ed2be5fa2059d01", 1863, "9c1d0dba9e4d24d45a8b0f400243b1021e6bbe332287980a6b3f5596e7dd8c52"),
    "xianjian__shot14.md": ("75325c60763a94a9ca10fea70b51255c38c7dfa243cf66d11bbd1a63ea83563a", 1496, "07c7d21db4347be3942e10fcc46992451f25f2d26ad27b5d7de386b5c82c74e0"),
    "xianjian__shot17.md": ("487490d3471213a497931c12fd09810a80ba1e835f8e1145c54ec27ca814c76c", 880, "b5f7172c8ab80ce788fce4346db59eee0925ec35e294ee13800465392e5cf04b"),
    "xianjian__shot23.md": ("2aad41f913a81551bfc15a5555a76cc509ff2f9551d519433987bbdb3cf17d76", 1019, None),
    "xingji__shot02.md": ("5f610ae5361e41c2178ce45e752f56ca2411e78da0f7e3d20ec993d44c6d983b", 1096, "731f231cd417c2da845c2a6fe88aa9a4c67be49181d3a2fe02d9e4d09865c42c"),
    "xingji__shot10.md": ("b3d67257c8d22ee14d049bc26c3372319f82d7c7f435c34a9355ddb21737c3ea", 1385, "95d9dedecd853a9e3d8a11cbf1efa1b9dcef738a6b4dc66ea9100966ee0f7775"),
}


# xianjian_yi_mv was deleted 2026-09-19 when the drama was restarted as the xianjian_yi
# series. The fixtures are still valid parser inputs — only their upstream is gone, so a
# missing source is expected here rather than a warning worth reading.
DELETED_UPSTREAM: frozenset[str] = frozenset({
    "real_shots/xianjian__shot01.md", "real_shots/xianjian__shot02.md",
    "real_shots/xianjian__shot03.md", "real_shots/xianjian__shot14.md",
    "real_shots/xianjian__shot17.md", "real_shots/xianjian__shot23.md",
    "real_cards/xianjian__p1_木剑.md",
})


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _source_rows() -> list[tuple[str, str]]:
    return _SOURCE_ROW_RE.findall((FIXTURES_DIR / "SOURCES.md").read_text(encoding="utf-8"))


def test_every_shot_fixture_has_a_golden() -> None:
    assert sorted(path.name for path in REAL_SHOTS_DIR.glob("*.md")) == sorted(GOLDEN)


@pytest.mark.parametrize("name", sorted(GOLDEN))
def test_prompt_bytes_match_golden(name: str) -> None:
    dao = READER.parse_bytes((REAL_SHOTS_DIR / name).read_bytes(), name)
    negative = None if dao.negative_prompt is None else _sha(dao.negative_prompt)
    assert (_sha(dao.prompt), len(dao.prompt), negative) == GOLDEN[name]


def test_crlf_fixture_is_derived_from_the_lf_copy() -> None:
    lf = (REAL_SHOTS_DIR / "hy3__shot02.md").read_bytes()
    assert b"\r\n" not in lf
    assert (REAL_SHOTS_DIR / "hy3__shot02.crlf.md").read_bytes() == lf.replace(b"\n", b"\r\n")


def test_sources_md_lists_every_copied_fixture() -> None:
    listed = {fixture for fixture, _ in _source_rows()}
    copied = {f"real_shots/{path.name}" for path in REAL_SHOTS_DIR.glob("*.md") if ".crlf." not in path.name}
    copied |= {f"real_cards/{path.name}" for path in REAL_CARDS_DIR.glob("*.md")}
    assert listed == copied


@pytest.mark.requires_real_repo
def test_fixture_provenance_against_real_sources() -> None:
    root = require_repo_root()
    rows = _source_rows()
    assert rows
    for fixture, source in rows:
        origin = root / source
        if fixture in DELETED_UPSTREAM:
            assert not origin.is_file(), f"{source} is back — drop {fixture} from DELETED_UPSTREAM"
            continue
        if not origin.is_file():
            warnings.warn(f"fixture source no longer exists: {source}", stacklevel=1)
        elif origin.read_bytes() != (FIXTURES_DIR / fixture).read_bytes():
            # Upstream shots keep evolving; drift is reported, and a fixture is refreshed deliberately.
            warnings.warn(f"fixture drifted from its source: {fixture} <- {source}", stacklevel=1)
