from typing import Optional, BinaryIO

from .line_seperator import LineSeperator

_COMMENT_PREFIX = b':'
_FIELD_SEPARATOR = b': '
_FIELD_NAME_RETRY = b'retry'
_FIELD_NAME_ID = b'id'
_FIELD_NAME_EVENT = b'event'
_FIELD_NAME_DATA = b'data'


class EventStreamWriter:
    def __init__(
            self,
            output_stream: BinaryIO,
            line_seperator: LineSeperator,
    ):
        self._output_stream = output_stream
        self._line_seperator = line_seperator

    def write_line(self):
        self.write(self._line_seperator.as_bytes())

    def write_type(self, type: str):
        if self._line_seperator.as_string() in type:
            raise ValueError("type must not contain newlines")
        self.write_field(_FIELD_NAME_EVENT, type)

    def write_data(self, data: str):
        if data is None:
            self.write_field(_FIELD_NAME_DATA)
        else:
            for line in data.splitlines():
                self.write_field(_FIELD_NAME_DATA, line)

    def write_id(self, id: str):
        if self._line_seperator.as_string() in id:
            raise ValueError("id must not contain newlines")
        self.write_field(_FIELD_NAME_ID, id)

    def write_retry(self, value_in_millis: Optional[int] = None):
        if value_in_millis < 0:
            raise ValueError("retry must be greater than or equal to 0")

        self.write_field(_FIELD_NAME_RETRY, None if value_in_millis is None else str(value_in_millis))

    def write_comment(self, comment: str):
        if comment is None:
            raise ValueError("comment must not be None")
        if self._line_seperator.as_string() in comment:
            raise ValueError("comment must not contain newlines")

        for line in comment.splitlines():
            self.write(_COMMENT_PREFIX)
            self.write_string(line)
            self.write_line()

    def flush(self):
        self._output_stream.flush()

    def write_field(self, name: bytes, value: Optional[str] = None):
        self.write(name)
        if value is not None:
            self.write(_FIELD_SEPARATOR)
            self.write_string(value)
        self.write_line()

    def write_string(self, value: str):
        self.write(value.encode(encoding='utf-8'))

    def write(self, value: bytes):
        self._output_stream.write(value)
