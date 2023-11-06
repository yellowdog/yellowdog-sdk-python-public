from typing import Optional

from .event_stream_writer import EventStreamWriter


class EventSubscriber:
    def __init__(
            self,
            event_stream_writer: EventStreamWriter
    ):
        self._event_stream_writer = event_stream_writer

    def emit_raw(
            self,
            data: bytes
    ):
        self._event_stream_writer.write(data)
        self._event_stream_writer.flush()

    def emit_event(
            self,
            type: Optional[str] = None,
            id: Optional[str] = None,
            data: Optional[str] = None,
            retry: Optional[int] = None
    ):
        if id is not None:
            self._event_stream_writer.write_id(id)
        if type is not None:
            self._event_stream_writer.write_type(type)
        if retry is not None:
            self._event_stream_writer.write_retry(retry)
        if data is not None:
            self._event_stream_writer.write_data(data)

        self._event_stream_writer.write_line()
        self._event_stream_writer.flush()

    def emit_comment(self, value: str):
        self._event_stream_writer.write_comment(value)
        self._event_stream_writer.write_line()
        self._event_stream_writer.flush()
