# Copyright 2021 ONDEWO GmbH
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


from typing import Pattern

from regex import regex


class TextHelper:
    FROM_CAMEL_TO_SNAKE_PATTERN: Pattern = regex.compile(r'((?<=[a-z])[A-Z]|(?!^)[A-Z](?=[a-z]))')

    @classmethod
    def from_camel_to_snake_case(cls, text: str) -> str:
        snaked: str = cls.FROM_CAMEL_TO_SNAKE_PATTERN.sub(r'_\1', text).lower()
        return snaked
