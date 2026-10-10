# Copyright 2021-2026 ONDEWO GmbH
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
Release credentials reach twine, gh and docker through the environment, never through an argv.

``/proc/<pid>/cmdline`` is world-readable, so a password on twine's, docker's or make's command line is
visible to every user on the release host for the life of the process. make expands ``$(NAME)`` and
``${NAME}`` in a recipe line BEFORE it runs ``/bin/sh -c '<line>'``, so a secret make expands into a
recipe lands on the shell's argv even when it is only piped into another program. A recipe reads a
secret as ``$${NAME}`` (expanded by the shell from the exported environment), and docker forwards it
by name only (``-e NAME``). Same contract as ondewo-client-utils-python's hygiene test.
"""

import re
from pathlib import Path
from typing import List

REPO_ROOT: Path = Path(__file__).resolve().parents[2]
MAKEFILE: str = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
RECIPE_LINES: List[str] = [line for line in MAKEFILE.splitlines() if line.startswith("\t")]
DOCKERFILES: List[Path] = sorted(REPO_ROOT.glob("Dockerfile*"))
WORKFLOWS: List[Path] = sorted((REPO_ROOT / ".github" / "workflows").glob("*.y*ml"))

SECRET: str = r"[A-Z0-9_]*(?:TOKEN|PASSWORD|USERNAME|SECRET|API_KEY)[A-Z0-9_]*"


def test_make_never_expands_a_secret_into_a_recipe_line() -> None:
    """Verify no recipe line carries ``$(NAME)`` / ``${NAME}`` of a credential (``$(if $(NAME),...)`` is fine)."""
    leaks: List[str] = []
    for line in RECIPE_LINES:
        # `$(if $(NAME),<set>,<unset>)` is evaluated by make; only `<set>` / `<unset>` reaches the shell.
        line_without_if: str = re.sub(rf"\$\(if\s+\$[({{]{SECRET}[)}}],", "", line)
        if re.search(rf"(?<!\$)\$[({{]{SECRET}[)}}]", line_without_if):
            leaks.append(line)
    assert leaks == []


def test_no_recipe_echoes_a_secret() -> None:
    """Verify no recipe prints a credential to the console (piping it into a program on stdin is fine)."""
    assert re.search(rf"echo\s+\"?\$+[{{(]{SECRET}[}})]\"?(?![ \t]*\|)", MAKEFILE) is None


def test_gh_reads_the_token_on_stdin() -> None:
    """Verify ``gh auth login`` gets the token on stdin, expanded by the shell from the environment."""
    assert "printf '%s\\n' \"$${GITHUB_GH_TOKEN}\" | gh auth login" in MAKEFILE


def test_docker_never_gets_a_secret_value_on_its_argv() -> None:
    """Verify ``docker run`` forwards credentials by name only and ``docker build`` never takes one as a build arg."""
    assert re.search(rf"(?:-e|--env)[ \t=]+{SECRET}=", MAKEFILE) is None
    assert re.search(rf"--build-arg[ \t=]+{SECRET}", MAKEFILE) is None
    assert re.search(r"-e\s+PYPI_USERNAME\s", MAKEFILE) is not None
    assert re.search(r"-e\s+PYPI_PASSWORD\s", MAKEFILE) is not None
    assert re.search(r"-e\s+GITHUB_GH_TOKEN\s", MAKEFILE) is not None


def test_the_credentials_are_exported_to_the_recipes() -> None:
    """Verify the Makefile exports its variables, so ``$${NAME}`` and ``docker run -e NAME`` see the values."""
    assert re.search(r"^export\s*$", MAKEFILE, flags=re.MULTILINE) is not None


def test_no_sub_make_gets_a_secret_on_its_argv() -> None:
    """Verify no ``make`` / ``$(MAKE)`` call carries ``NAME=<value>`` or the old ``$(info)`` credential bundle."""
    make_calls: List[str] = [line for line in RECIPE_LINES if re.search(r"(?:\bmake\b|\$\(MAKE\))", line)]
    assert [line for line in make_calls if "$(info)" in line or re.search(rf"\b{SECRET}=", line)] == []


def test_the_devops_release_hands_the_credentials_over_the_environment() -> None:
    """Verify ``run_release_with_devops`` loads anchored ``^NAME=`` lines into the environment of the sub-make."""
    recipe: str = MAKEFILE.split("\nrun_release_with_devops:", 1)[1].split("\n\n", 1)[0]
    assert "$(info)" not in recipe
    assert "$(shell" not in recipe
    assert "set -a" in recipe
    assert "grep -h -E '^(GITHUB_GH_TOKEN|PYPI_USERNAME|PYPI_PASSWORD)='" in recipe
    assert re.search(r"\$\(MAKE\) release\s*$", recipe) is not None


def test_twine_never_gets_the_credentials_on_its_argv() -> None:
    """Verify twine reads the PyPI credentials from ``TWINE_USERNAME`` / ``TWINE_PASSWORD``, not ``-u`` / ``-p``."""
    twine_lines: List[str] = [line for line in RECIPE_LINES if "twine upload" in line]
    assert twine_lines
    assert [line for line in twine_lines if re.search(r"\s-[up]\s*\$", line)] == []
    assert 'TWINE_USERNAME="$${PYPI_USERNAME}" TWINE_PASSWORD="$${PYPI_PASSWORD}" twine upload' in MAKEFILE


def test_no_image_bakes_a_secret_from_a_build_arg() -> None:
    """Verify no Dockerfile declares a credential ``ARG`` or copies one into ``ENV`` (both stay in the image)."""
    for dockerfile in DOCKERFILES:
        text: str = dockerfile.read_text(encoding="utf-8")
        assert re.search(rf"^\s*ARG\s+{SECRET}\b", text, flags=re.MULTILINE) is None, dockerfile.name
        assert re.search(rf"^\s*ENV\s+{SECRET}[ \t=]+\S*\$", text, flags=re.MULTILINE) is None, dockerfile.name


def test_workflow_run_lines_never_interpolate_a_secret() -> None:
    """Verify ``${{ secrets.X }}`` only appears as an ``env:`` / ``with:`` value, never inside a ``run:`` command."""
    for workflow in WORKFLOWS:
        for line in workflow.read_text(encoding="utf-8").splitlines():
            if "secrets." in line:
                assert re.match(r"^\s*(?!run:)[\w-]+:\s*\$\{\{\s*secrets\.\w+\s*\}\}\s*$", line), workflow.name
