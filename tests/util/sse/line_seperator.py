from enum import Enum


class LineSeperator(Enum):
    CR = '\r'
    LF = '\n'
    CRLF = '\r\n'

    def __init__(self, value: str):
        self._string: str = value
        self._bytes: bytes = value.encode(encoding='utf-8')

    def as_bytes(self) -> bytes:
        return self._bytes

    def as_string(self) -> str:
        return self._string
