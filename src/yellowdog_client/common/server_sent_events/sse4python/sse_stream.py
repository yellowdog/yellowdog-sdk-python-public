from __future__ import annotations

import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import timedelta
from io import BufferedIOBase
from typing import Optional, Union, Tuple

import requests
from requests import HTTPError, Response
from requests.auth import AuthBase

from .server_sent_event import ServerSentEvent


@dataclass
class SseConnection:
    data: BufferedIOBase
    chunked: bool


class SseStream:
    # SSE Spec: Lines must be separated by either a U+000D CARRIAGE RETURN U+000A LINE FEED (CRLF) character pair,
    # a single U+000A LINE FEED (LF) character, or a single U+000D CARRIAGE RETURN (CR) character.
    _line_end_pattern: re.Pattern = re.compile(r'\r\n|\r|\n')
    _event_endings: Tuple[bytes] = (b'\r\n\r\n', b'\r\r', b'\n\n')
    _event_line_pattern: re.Pattern = re.compile('(?P<name>[^:]*):?( ?(?P<value>.*))?')

    def __init__(
            self,
            connection: SseConnection,
            connector: SseClient
    ) -> None:
        self._connection: SseConnection = connection
        self._connector: SseClient = connector

    def __iter__(self) -> SseStream:
        return self

    def __next__(self) -> ServerSentEvent:
        result = None
        # skip over results that consist only of comments
        while result is None:
            result = self._read_event()

        if isinstance(result, Exception):
            pass

        if result.retry is not None:
            self._connector.retry_interval = timedelta(milliseconds=result.retry)

        return result

    def _read_event(self) -> Union[ServerSentEvent, Exception]:
        event_bytes: bytes = b''
        while not event_bytes.endswith(self._event_endings):
            event_bytes += self._read_line()

        # SSE Spec: 'Streams must be decoded using the UTF-8 decode algorithm.'
        event_string = event_bytes.decode('utf-8')

        return self._parse_event(event_string)

    def _read_line(self) -> bytes:
        return self._connection.data.readline()

    # Will return None if the event is only blank lines or comments
    # Will return an Exception if the event cannot be parsed
    # Otherwise will return the event
    def _parse_event(self, event_string: str) -> Optional[ServerSentEvent, Exception]:
        event = ServerSentEvent()

        found_field = False
        for line in re.split(self._line_end_pattern, event_string):
            match = self._event_line_pattern.match(line)
            if match is None:
                return ValueError(f"Invalid server sent event line: {line}")

            name = match.group('name')
            if name == '':
                # If no name, ignore line as it is a comment e.g. :foo
                continue

            found_field = True
            value = match.group('value')

            if name == 'id':
                event.id = value
            elif name == 'event':
                event.type = value
            elif name == 'data':
                if event.data is None:
                    event.data = value
                else:
                    event.data += '\n' + value
            elif name == 'retry':
                try:
                    event.retry = int(value)
                except ValueError:
                    return ValueError(f"Invalid server sent event retry value: {value}")

        return event if found_field else None


class SseClient(ABC):
    def stream(self, initial_retry_interval: timedelta = timedelta(seconds=3)) -> SseStream:
        connection = self._connect(initial_retry_interval)
        return SseStream(connection, self)

    @abstractmethod
    def _connect(self, retry_interval: timedelta) -> SseConnection:
        pass


class RequestsSseClient(SseClient):
    def __init__(
            self,
            url: str,
            auth: Optional[AuthBase] = None
    ):
        self._url: str = url
        self._auth: Optional[AuthBase] = auth

    def _connect(self, retry_interval: timedelta) -> SseConnection:
        response = self._get(retry_interval)

        return SseConnection(
            data=response.raw,
            chunked=response.headers.get('Transfer-Encoding') == 'chunked'
        )

    def _get(self, retry_interval: timedelta) -> Response:
        while True:
            response = requests.get(
                self._url,
                stream=True,
                headers={
                    'Cache-Control': 'no-cache',
                    'Accept': 'text/event-stream'
                },
                auth=self._auth
            )

            try:
                response.raise_for_status()
                return response
            except HTTPError as ex:
                status_code = ex.response.status_code
                if status_code < 500:
                    raise ex
                time.sleep(retry_interval.total_seconds())
