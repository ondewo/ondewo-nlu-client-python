"""Every third-party module this package imports at runtime is a declared RUNTIME dependency.

ondewo-t2s-client 6.7.1 shipped `utils/keycloak.py` with `from loguru import logger` while `loguru` was declared only
in the `dev` extra, so `from ondewo.t2s.client.client import Client` raised `ModuleNotFoundError: No module named
'loguru'` in any environment that installed the wheel alone (ondewo-t2s-release PR-221 #4, its client-SDK test
image), while every developer venv - which installs `dev` - stayed green. s2t, sip, vtsi and survey had the same
defect. A transitive dependency is not a dependency either: a requirement that drops one breaks the import silently.

A hermetic scan: `ast` over the package and the `[project]` table read as text (`tomllib` is 3.11+, and these
SDKs support 3.10). Deliberately not `importlib.metadata`, which would read the installed closure and so re-confirm
exactly what hid the defect. Shared verbatim by every ondewo python SDK.
"""

import ast
import re
import sys
from pathlib import Path
from typing import Dict, FrozenSet, List, Set

#: The repository root: the nearest directory above this file that holds pyproject.toml (the SDKs keep their
#: tests at different depths).
ROOT: Path = next(parent for parent in Path(__file__).resolve().parents if (parent / "pyproject.toml").is_file())

#: The distribution that provides a top-level import name, where the two differ.
DISTRIBUTION_OF_MODULE: Dict[str, str] = {
    "grpc": "grpcio",
    "google.protobuf": "protobuf",
    "google.api": "googleapis-common-protos",
    "google.rpc": "googleapis-common-protos",
    "google.type": "googleapis-common-protos",
    "google.longrunning": "googleapis-common-protos",
    "dataclasses_json": "dataclasses-json",
    "ondewo.utils": "ondewo-client-utils",
    "ondewo.nlu": "ondewo-nlu-client",
    "ondewo.qa": "ondewo-nlu-client",
    "ondewo.s2t": "ondewo-s2t-client",
    "ondewo.t2s": "ondewo-t2s-client",
    "ondewo.sip": "ondewo-sip-client",
    "ondewo.csi": "ondewo-csi-client",
    "ondewo.vtsi": "ondewo-vtsi-client",
    "ondewo.survey": "ondewo-survey-client",
    "yaml": "pyyaml",
}

#: Imported directly but guaranteed by a declared dependency's OWN hard requirement, which is the only kind of
#: transitive dependency accepted here: `requests` requires `urllib3`, and `google-api-core` requires
#: `googleapis-common-protos` (the google.api / google.rpc / google.type stubs).
GUARANTEED_BY: Dict[str, str] = {
    "urllib3": "requests",
    "google.api": "google-api-core",
    "google.rpc": "google-api-core",
    "google.type": "google-api-core",
}


def _runtime_requirements() -> FrozenSet[str]:
    """The distribution names of `[project].dependencies` (never an extra)."""
    text: str = "\n" + (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    project: str = text[text.index("\n[project]\n") :]
    next_table = re.search(r"\n\[(?!project\])[^\n]*\]\n", project[1:])
    project = project[: next_table.start() + 1] if next_table else project
    block = re.search(r"\ndependencies = \[\n(.*?)\n\]", project, re.S)
    assert block, "pyproject.toml has no [project].dependencies array"
    requirements: List[str] = re.findall(r'^\s*"([^"]+)"', block.group(1), re.M)
    assert requirements, "the dependencies array parsed empty"
    names: Set[str] = set()
    for requirement in requirements:
        match = re.match(r"\s*([A-Za-z0-9][A-Za-z0-9._-]*)", requirement)
        assert match, f"unparseable requirement {requirement!r}"
        names.add(match.group(1).lower().replace("_", "-"))
    return frozenset(names)


def _imported_modules() -> Dict[str, str]:
    """Map each imported third-party module key to the first file importing it."""
    vendored: Set[str] = {f"ondewo.{p.name}" for p in (ROOT / "ondewo").iterdir() if p.is_dir()}
    found: Dict[str, str] = {}
    for path in sorted((ROOT / "ondewo").rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names: List[str] = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names = [node.module]
            for name in names:
                parts: List[str] = name.split(".")
                if parts[0] in sys.stdlib_module_names or parts[0] == "__future__":
                    continue
                key: str = ".".join(parts[:2]) if parts[0] in ("ondewo", "google") and len(parts) > 1 else parts[0]
                if key in vendored or key == "ondewo":
                    continue
                found.setdefault(key, path.relative_to(ROOT).as_posix())
    return found


def test_the_scan_sees_the_package() -> None:
    """Guard the guard: a scan that finds nothing would pass the next test vacuously."""
    assert "grpc" in _imported_modules()


def test_every_runtime_import_is_a_declared_runtime_dependency() -> None:
    declared: FrozenSet[str] = _runtime_requirements()
    missing: List[str] = []
    for module, first_file in sorted(_imported_modules().items()):
        distribution: str = DISTRIBUTION_OF_MODULE.get(module, module).lower().replace("_", "-")
        if distribution in declared or GUARANTEED_BY.get(module) in declared:
            continue
        missing.append(f"{module} (distribution {distribution!r}, first imported by {first_file})")
    assert not missing, (
        "imported at runtime but not in [project].dependencies - a `dev` extra does not count, a plain "
        f"`pip install` of the wheel will raise ModuleNotFoundError: {missing}"
    )
