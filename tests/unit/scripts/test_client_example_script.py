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
import importlib
import importlib.util
from pathlib import Path


_SCRIPT_PATH = Path(__file__).parents[4] / 'ondewo' / 'nlu' / 'scripts' / 'client_example_script.py'


class TestClientExampleScript:
    def test_script_file_exists(self) -> None:
        assert _SCRIPT_PATH.exists(), f'Script not found at {_SCRIPT_PATH}'

    def test_script_is_valid_python(self) -> None:
        source = _SCRIPT_PATH.read_text()
        # Raises SyntaxError if the file cannot be compiled
        compile(source, str(_SCRIPT_PATH), 'exec')

    def test_module_can_be_imported(self) -> None:
        spec = importlib.util.spec_from_file_location('client_example_script', _SCRIPT_PATH)
        assert spec is not None
        module = importlib.util.module_from_spec(spec)
        # Loading executes module-level code but not the if __name__ == '__main__' block,
        # so no network connection or file I/O is triggered.
        assert spec.loader is not None
        spec.loader.exec_module(module)  # type: ignore[union-attr]

    def test_main_block_is_guarded(self) -> None:
        # All executable logic must be inside `if __name__ == '__main__':` so that
        # importing the module never triggers network calls or file reads.
        source = _SCRIPT_PATH.read_text()
        lines = source.splitlines()
        guarded_start = next(
            (i for i, l in enumerate(lines) if l.strip().startswith("if __name__")),
            None,
        )
        assert guarded_start is not None, "No 'if __name__ == \"__main__\":' block found"
        # No top-level statements that perform I/O should appear before the guard.
        top_level_io = [
            line.strip() for line in lines[:guarded_start]
            if line.strip().startswith(('open(', 'Client(', 'client.services'))
        ]
        assert top_level_io == [], f'Unguarded I/O statements found: {top_level_io}'
