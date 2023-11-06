from __future__ import annotations

import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from types import TracebackType
from typing import Optional, Dict

from .event_broadcaster import EventBroadcaster


class SseServer:

    def __init__(self, path: str, chunked: bool = False):
        self._http_server: Optional[ThreadingHTTPServer] = None
        self._event_broadcaster: EventBroadcaster = EventBroadcaster(chunked_transfer_encoding=chunked)
        self._path: str = path
        self._running: bool = False
        self._forwards: Dict[str, str] = {}

    def __enter__(self) -> 'SseServer':
        class SseRequestHandler(BaseHTTPRequestHandler):
            def do_GET(inner_self):
                if inner_self.path in self._forwards:
                    print(f"Received request for {inner_self.path} forwarding to {self._forwards[inner_self.path]}")
                    inner_self.send_response(302)
                    inner_self.send_header('Location', self._forwards[inner_self.path] + inner_self.path)
                    inner_self.end_headers()
                    return

                if inner_self.path != self._path:
                    print(f"Received unexpected request for {inner_self.path}")
                    inner_self.send_error(404, "Not found")
                    return

                self._event_broadcaster.subscribe(inner_self)
                while self._running:
                    time.sleep(1)

        self._http_server = ThreadingHTTPServer(('localhost', 0), SseRequestHandler)
        self._http_server.daemon_threads = True
        Thread(target=self._http_server.serve_forever, daemon=True).start()
        self._running = True
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[TracebackType]):
        self._running = False
        self._http_server.shutdown()

    def forward(self, local_path: str, remote_url: str) -> SseServer:
        self._forwards[local_path] = remote_url
        return self

    def get_root_url(self) -> str:
        return f'http://{self._http_server.server_name}:{self._http_server.server_port}'

    def get_sse_url(self) -> str:
        return f'{self.get_root_url()}{self._path}'

    def get_subscriber_count(self) -> int:
        return self._event_broadcaster.get_subscriber_count()

    def broadcast(
            self,
            type: Optional[str] = None,
            id: Optional[str] = None,
            data: Optional[str] = None,
            retry: Optional[int] = None
    ):
        self._event_broadcaster.broadcast(type, id, data, retry)

    def broadcast_chunks(self, *data: bytes):
        self._event_broadcaster.broadcast_chunks(*data)
