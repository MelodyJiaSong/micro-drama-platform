import ast
import importlib
import sys
from pathlib import Path

import pytest

PROJECT = Path(__file__).resolve().parents[3]
STDLIB: frozenset[str] = frozenset(sys.stdlib_module_names)


def _modules(package: str) -> list[Path]:
    return sorted(p for p in (PROJECT / "libs" / package).rglob("*.py") if p.name != "__init__.py")


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names |= {alias.name for alias in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


@pytest.mark.parametrize("path", _modules("domain"), ids=lambda p: p.name)
def test_domain_imports_only_stdlib_common_and_domain(path: Path) -> None:
    for name in _imports(path):
        top = name.split(".")[0]
        assert top in STDLIB or name.startswith(("libs.common", "libs.domain")), f"{path.name} imports {name}"


@pytest.mark.parametrize("path", [p for p in _modules("common") if p.name in {"enums.py", "canonical_json.py"}], ids=lambda p: p.name)
def test_common_imports_only_stdlib(path: Path) -> None:
    assert all(name.split(".")[0] in STDLIB for name in _imports(path))


@pytest.mark.parametrize("path", _modules("domain"), ids=lambda p: p.name)
def test_every_domain_module_imports(path: Path) -> None:
    module = ".".join(path.relative_to(PROJECT).with_suffix("").parts)
    importlib.import_module(module)


@pytest.mark.parametrize("path", _modules("domain"), ids=lambda p: p.name)
def test_file_suffix_matches_role_folder(path: Path) -> None:
    role = {"entities": "entity", "value_objects": "valueobject", "errors": "error", "repositories": "repository"}[path.parent.name]
    assert path.stem.endswith(f"__{role}")
