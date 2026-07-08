# Copyright 2021-2025 ONDEWO GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Guardrails for the `examples/` tree.

`compile()` proves every example is valid Python (it parses/compiles the source but does
not execute it, so no config file is read and no network call is made). A second check
enforces the D18 auth migration: no NLU example may reconstruct the removed legacy
`http_token=` auth argument on its `ClientConfig` — authentication is Keycloak bearer only.
"""

from pathlib import Path
from typing import List

import pytest

_EXAMPLES_DIR: Path = Path(__file__).parents[3] / "examples"
_EXAMPLE_FILES: List[Path] = sorted(_EXAMPLES_DIR.rglob("*.py"))

# The `ondewo.qa` example client has its own (host/port only) config and is out of scope
# for the NLU Keycloak-auth guard below.
_NLU_EXAMPLE_FILES: List[Path] = [p for p in _EXAMPLE_FILES if "qa" not in p.parts]


def test_examples_present() -> None:
    """The examples tree is non-empty (guards against a broken path/glob)."""
    assert _EXAMPLE_FILES, f"No example files found under {_EXAMPLES_DIR}"


@pytest.mark.parametrize("example_path", _EXAMPLE_FILES, ids=lambda p: str(p.relative_to(_EXAMPLES_DIR)))
def test_example_compiles(example_path: Path) -> None:
    """Every example file is syntactically valid Python."""
    source: str = example_path.read_text()
    # Raises SyntaxError (failing the test) if the file cannot be compiled.
    compile(source, str(example_path), "exec")


@pytest.mark.parametrize("example_path", _NLU_EXAMPLE_FILES, ids=lambda p: str(p.relative_to(_EXAMPLES_DIR)))
def test_example_does_not_use_legacy_http_token_auth(example_path: Path) -> None:
    """No NLU example reintroduces the removed legacy `http_token=` auth argument (D18)."""
    source: str = example_path.read_text()
    assert "http_token=" not in source, (
        f"{example_path} uses the removed legacy `http_token=` auth; "
        "use the Keycloak fields (keycloak_url / realm / client_id) instead."
    )
