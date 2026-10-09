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
The GitHub release body is sliced out of RELEASE.md by the Makefile's ``CURRENT_RELEASE_NOTES``.

The slice starts at ``Release ONDEWO NLU Python Client <version>`` and ends at the next ``*****`` line. A heading
spelled any other way gives an empty slice, and ``gh release create -n ""`` then publishes a release without notes and
without an error (ondewo-vtsi-client-python 4.0.0 to 8.7.0 shipped like that).
"""

import re
from pathlib import Path
from typing import List

REPO_ROOT: Path = Path(__file__).resolve().parents[2]
RELEASE_NOTES: str = (REPO_ROOT / "RELEASE.md").read_text(encoding="utf-8")
MAKEFILE: str = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
HEADING_PREFIX: str = "## Release ONDEWO NLU Python Client "


def _release_notes_slice(version: str) -> List[str]:
    """Reproduce the Makefile's perl range ``/Release ONDEWO NLU Python Client <v>/../^\\*{5}/``."""
    lines: List[str] = RELEASE_NOTES.splitlines()
    start: int = next(i for i, line in enumerate(lines) if f"Release ONDEWO NLU Python Client {version}" in line)
    # Like perl's range operator, an unterminated last section runs to the end of the file.
    end: int = next((i for i in range(start + 1, len(lines)) if re.match(r"^\*{5}", lines[i])), len(lines))
    return lines[start : end + 1]


def test_the_makefile_slices_the_heading_this_test_checks() -> None:
    """The perl range in the Makefile still matches the heading spelling pinned here."""
    assert "/Release ONDEWO NLU Python Client ${ONDEWO_NLU_VERSION}/../^\\*{5}/" in MAKEFILE


def test_every_release_heading_uses_the_spelling_the_makefile_slices() -> None:
    """No ``## Release ONDEWO`` heading may use another spelling."""
    headings: List[str] = [line for line in RELEASE_NOTES.splitlines() if line.startswith("## Release ONDEWO")]
    assert headings
    assert [heading for heading in headings if not heading.startswith(HEADING_PREFIX)] == []


def test_every_release_section_ends_before_the_next_heading() -> None:
    """Each slice holds exactly one release: a missing ``*****`` separator would pull in the next section."""
    versions: List[str] = [
        line[len(HEADING_PREFIX) :].strip() for line in RELEASE_NOTES.splitlines() if line.startswith(HEADING_PREFIX)
    ]
    assert versions
    assert [v for v in versions if sum(line.startswith(HEADING_PREFIX) for line in _release_notes_slice(v)) != 1] == []


def test_the_current_version_has_non_empty_release_notes() -> None:
    """The version the Makefile releases has a section with content between its heading and the separator."""
    version_match = re.search(r"^ONDEWO_NLU_VERSION=(\S+)$", MAKEFILE, re.MULTILINE)
    assert version_match is not None
    body: List[str] = [line for line in _release_notes_slice(version_match.group(1))[1:-1] if line.strip()]
    assert len(body) > 1
