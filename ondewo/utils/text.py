from typing import Pattern

from regex import regex


class TextHelper:
    FROM_CAMEL_TO_SNAKE_PATTERN: Pattern = regex.compile(r'((?<=[a-z])[A-Z]|(?!^)[A-Z](?=[a-z]))')

    @classmethod
    def from_camel_to_snake_case(cls, text: str) -> str:
        snaked: str = cls.FROM_CAMEL_TO_SNAKE_PATTERN.sub(r'_\1', text).lower()
        return snaked
