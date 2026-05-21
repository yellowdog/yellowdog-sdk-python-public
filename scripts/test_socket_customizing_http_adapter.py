#!/usr/bin/env python3
"""
Reproducer for stale-connection hangs (YEL-14759).

Runs a local HTTP CONNECT proxy.  After idle_timeout seconds it inserts an
iptables DROP rule targeting only the existing connection's ephemeral port,
simulating a network device that silently drops idle connections without RST.
New connections use a different ephemeral port and are not blocked.

Without TCP keepalive:
  - urllib3 reuses the stale socket → TCP retransmits for ~924 s

With TCP keepalive (KEEPIDLE=2, KEEPINTVL=1, KEEPCNT=1 → 3 s detection):
  - keepalive detects the dead socket → urllib3 retries on a new ephemeral
    port (not blocked) → completes in < 1 s

Run as root (iptables requires it):
    sudo ./.venv/bin/python scripts/test_socket_customizing_http_adapter.py
"""

import http.server
import logging
import os
import select
import socket
import socketserver
import subprocess
import threading
import time
from typing import List, Tuple

import requests
from urllib.parse import urlparse

from urllib3.connection import HTTPConnection

from yellowdog_client.platform_client import _SocketCustomizingHTTPAdapter, _build_socket_options

# Toggle to test with and without keepalive.
KEEPALIVE_ENABLED = True

# Tuned low so detection completes in 3s: KEEPIDLE + KEEPCNT * KEEPINTVL = 2 + 1*1 = 3s.
# KEEPIDLE must be > idle_timeout (1s) so the DROP rule is in place before the first probe.
SOCKET_OPTIONS = (
    _build_socket_options(keepalive_idle=2, keepalive_interval=1, keepalive_count=1)
    if KEEPALIVE_ENABLED
    else list(HTTPConnection.default_socket_options)
)


def _build_session(socket_options: List[Tuple[int, int, int]]) -> requests.Session:
    session = requests.Session()
    adapter = _SocketCustomizingHTTPAdapter(socket_options=socket_options)
    session.mount("http://", adapter)
    return session


class _LocalServer:
    """Minimal HTTP server that responds 200 OK to any request."""

    def __init__(self):
        self._server = None
        self._thread = None

    def __enter__(self):
        class Handler(http.server.BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_GET(self):
                body = b'{"status":"ok"}'
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_):
                pass

        self._server = socketserver.ThreadingTCPServer(('127.0.0.1', 0), Handler)
        self._server.allow_reuse_address = True
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, *_):
        if self._server:
            self._server.shutdown()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self._server.server_address[1]}"


class SilentDropProxy:
    """
    HTTP proxy that silently drops an established connection after idle_timeout
    seconds by blocking only that connection's ephemeral port via iptables.

    urllib3's retry opens a fresh socket with a different ephemeral port which
    is not blocked, so it succeeds immediately — but only if keepalive has
    already detected the stale socket before the retry is attempted.
    """

    def __init__(self, idle_timeout: int = 5):
        self._idle_timeout = idle_timeout
        self._port = None
        self._server = None
        self._thread = None
        self._blocked_ports: set = set()

    def __enter__(self):
        self._start()
        os.environ['HTTP_PROXY'] = f'http://127.0.0.1:{self._port}'
        print(f"[proxy] listening on 127.0.0.1:{self._port}  idle_timeout={self._idle_timeout}s")
        return self

    def __exit__(self, *_):
        os.environ.pop('HTTP_PROXY', None)
        for port in list(self._blocked_ports):
            self._remove_drop(port)
        if self._server:
            self._server.shutdown()
        print("[proxy] stopped")

    def _insert_drop(self, client_port: int):
        if client_port in self._blocked_ports:
            return
        self._blocked_ports.add(client_port)
        self._iptables("I", "1", client_port)
        print(f"\n[proxy] idle timeout — SILENT DROP on ephemeral port {client_port}"
              f" (new connections on other ports are unaffected)\n")

    def _remove_drop(self, client_port: int):
        if client_port not in self._blocked_ports:
            return
        self._blocked_ports.discard(client_port)
        self._iptables("D", "", client_port)

    def _iptables(self, action: str, position: str, client_port: int):
        cmd = ["iptables", f"-{action}", "INPUT"]
        if position:
            cmd.append(position)
        cmd += ["-i", "lo", "-p", "tcp", "--dport", str(client_port), "-j", "DROP"]
        if os.geteuid() != 0:
            cmd = ["sudo"] + cmd
        subprocess.run(cmd, check=True)

    def _start(self):
        proxy = self

        class Handler(socketserver.BaseRequestHandler):
            def handle(self):
                buf = b""
                while b"\r\n\r\n" not in buf:
                    chunk = self.request.recv(4096)
                    if not chunk:
                        return
                    buf += chunk

                first_line = buf.split(b"\r\n")[0].decode()
                method, uri, _ = first_line.split()

                # Parse host and port from the request URI or Host header.
                if uri.startswith("http://"):
                    parsed = urlparse(uri)
                    host = parsed.hostname
                    port = parsed.port or 80
                    # Rewrite URI to path-only for the upstream server.
                    path = parsed.path or "/"
                    if parsed.query:
                        path += "?" + parsed.query
                    buf = buf.replace(uri.encode(), path.encode(), 1)
                else:
                    host, port = uri.rsplit(":", 1)
                    port = int(port)

                try:
                    remote = socket.create_connection((host, port), timeout=10)
                except Exception:
                    self.request.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
                    return

                client_port = self.request.getpeername()[1]
                timer = [None]

                def reset_idle_timer():
                    if timer[0]:
                        timer[0].cancel()
                    t = threading.Timer(
                        proxy._idle_timeout,
                        lambda: proxy._insert_drop(client_port)
                    )
                    t.daemon = True
                    t.start()
                    timer[0] = t

                # For plain HTTP, forward the buffered request immediately.
                remote.sendall(buf)
                reset_idle_timer()
                self.request.setblocking(False)
                remote.setblocking(False)

                try:
                    while True:
                        r, _, e = select.select(
                            [self.request, remote], [], [self.request, remote], 0.5
                        )
                        if e:
                            break
                        for src in r:
                            dst = remote if src is self.request else self.request
                            try:
                                data = src.recv(65536)
                                if not data:
                                    return
                                dst.sendall(data)
                                reset_idle_timer()
                            except (BlockingIOError, ConnectionResetError,
                                    BrokenPipeError, OSError):
                                return
                finally:
                    if timer[0]:
                        timer[0].cancel()
                    try:
                        remote.close()
                    except Exception:
                        pass

        class Server(socketserver.ThreadingTCPServer):
            allow_reuse_address = True
            daemon_threads = True

        self._server = Server(('127.0.0.1', 0), Handler)
        self._port = self._server.server_address[1]
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )
    logging.getLogger("urllib3").setLevel(logging.DEBUG)


def _get(session: requests.Session, url: str, label: str) -> None:
    print(f"--- {label} --- [{time.strftime('%H:%M:%S')}]")

    start = time.monotonic()
    stop_event = threading.Event()

    def _tick():
        while not stop_event.wait(60):
            print(f"  ... still waiting ({time.monotonic() - start:.0f}s elapsed)")

    ticker = threading.Thread(target=_tick, daemon=True)
    ticker.start()

    try:
        response = session.get(url)
        status = response.status_code
    finally:
        stop_event.set()

    elapsed = time.monotonic() - start
    print(f"Done in {elapsed:.3f}s  HTTP {status}\n")


def main() -> None:
    _setup_logging()

    with _LocalServer() as server, SilentDropProxy(idle_timeout=1):
        session = _build_session(SOCKET_OPTIONS)
        try:
            _get(session, server.url, "request 1 (opens connection through proxy)")

            # Sleep long enough for the proxy to drop (1s) and for keepalive to
            # exhaust the stale socket (KEEPIDLE=2 + KEEPCNT*KEEPINTVL=1*1=1 → 3s).
            # Keepalive only fires on an idle socket — if request 2 starts before
            # ETIMEDOUT is set, TCP enters retransmission mode instead.
            print("Sleeping 5s — proxy drops at 1s, keepalive exhausts at 3s…")
            time.sleep(5)

            _get(session, server.url, "request 2 — instant with keepalive, ~924s without")
        finally:
            session.close()


if __name__ == "__main__":
    main()
