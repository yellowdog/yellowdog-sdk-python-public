from http.server import BaseHTTPRequestHandler
from typing import List, Optional, BinaryIO

from .event_stream_writer import EventStreamWriter
from .event_subscriber import EventSubscriber
from .line_seperator import LineSeperator

_HTTP_STATUS_OK = 200
_HTTP_HEADER_CONTENT_TYPE = 'Content-Type'
_MEDIA_TYPE_TEXT_EVENT_STREAM = 'text/event-stream'


class EventBroadcaster:
    def __init__(
            self,
            line_seperator: LineSeperator = LineSeperator.LF,
            chunked_transfer_encoding: bool = False
    ):
        self._line_separator: LineSeperator = line_seperator
        self._subscribers: List[EventSubscriber] = []
        self._chunked_transfer_encoding: bool = chunked_transfer_encoding

    def subscribe(self, request_handler: BaseHTTPRequestHandler) -> None:
        request_handler.send_response(_HTTP_STATUS_OK)
        request_handler.send_header(_HTTP_HEADER_CONTENT_TYPE, _MEDIA_TYPE_TEXT_EVENT_STREAM)

        if self._chunked_transfer_encoding:
            request_handler.send_header('Transfer-Encoding', 'chunked')

        request_handler.end_headers()

        self.subscribe_stream(request_handler.wfile)

    def subscribe_stream(self, output_stream: BinaryIO):
        writer = EventStreamWriter(output_stream, self._line_separator)
        self._subscribers.append(EventSubscriber(writer))

    def broadcast(
            self,
            type: Optional[str] = None,
            id: Optional[str] = None,
            data: Optional[str] = None,
            retry: Optional[int] = None
    ) -> None:
        for subscriber in self._subscribers:
            subscriber.emit_event(type, id, data, retry)

    def broadcast_chunks(self, *data: bytes) -> None:
        for subscriber in self._subscribers:
            for chunk in data:
                subscriber.emit_raw(self._to_chunk(chunk))

    def get_subscriber_count(self) -> int:
        return len(self._subscribers)

    @staticmethod
    def _to_chunk(data: bytes) -> bytes:
        return b'%x\r\n%s\r\n' % (len(data), data)
