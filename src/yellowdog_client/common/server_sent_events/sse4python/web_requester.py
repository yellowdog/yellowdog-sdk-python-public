import codecs
import http.client
import re
import time
from typing import Callable

import sseclient
import requests
from requests.auth import AuthBase
from sseclient import SSEClient

from .chained_thread import ChainedThread
from .server_response import ServerResponse


def _readall_chunked_patched(self):
    assert self.chunked != http.client._UNKNOWN
    value = []
    try:
        while True:
            chunk_left = self._get_chunk_left()
            if chunk_left is None:
                break
            value.append(self._safe_read(chunk_left))
            self.chunk_left = 0
            return b''.join(value)
        return b''.join(value)
    except http.client.IncompleteRead:
        raise http.client.IncompleteRead(b''.join(value))


def connect(self):
    if self.last_id:
        self.requests_kwargs['headers']['Last-Event-ID'] = self.last_id

    # Use session if set.  Otherwise fall back to requests module.
    requester = self.session or requests
    self.resp = requester.get(self.url, stream=True, **self.requests_kwargs)

    if hasattr(self.resp.raw, '_fp'):
        self.resp.raw._fp._readall_chunked = lambda: _readall_chunked_patched(self.resp.raw._fp)

    self.resp_iterator = self.iter_content()

    if self.resp.encoding:
        self.decoder = codecs.getincrementaldecoder(  # throws on non-200
            self.resp.encoding)(errors='replace')

    # TODO: Ensure we're handling redirects.  Might also stick the 'origin'
    # attribute on Events like the Javascript spec requires.
    self.resp.raise_for_status()


def next_patched(self):
    while not self._event_complete():
        try:
            next_chunk = next(self.resp_iterator)
            if not next_chunk:
                raise EOFError()
            self.buf += self.decoder.decode(next_chunk)
        except StopIteration:
            return
        except (requests.RequestException, EOFError, http.client.IncompleteRead) as e:
            print(e)
            time.sleep(self.retry / 1000.0)
            self._connect()

            # The SSE spec only supports resuming from a whole message, so
            # if we have half a message we should throw it out.
            head, sep, tail = self.buf.rpartition('\n')
            self.buf = head + sep
            continue

    # Split the complete event (up to the end_of_field) into event_string,
    # and retain anything after the current complete event in self.buf
    # for next time.
    (event_string, self.buf) = re.split(sseclient.end_of_field, self.buf, maxsplit=1)
    msg = sseclient.Event.parse(event_string)

    # If the server requests a specific retry delay, we need to honor it.
    if msg.retry:
        self.retry = msg.retry

    # last_id should only be set if included in the message.  It's not
    # forgotten if a message omits it.
    if msg.id:
        self.last_id = msg.id

    return msg


def iter_content(self):
    def generate():
        while True:
            chunk = self.resp.raw.read(self.chunk_size)
            if not chunk:
                break
            if chunk is None:
                chunk = ""
            yield chunk

    return generate()


sseclient.SSEClient._connect = connect
sseclient.SSEClient.iter_content = iter_content
sseclient.SSEClient.__next__ = next_patched


class WebRequester(object):
    # chunk size None will force sse client to read whole chunk, received from the stream
    __chunk_size = None

    def __init__(self, auth_base: AuthBase) -> None:
        self.__auth_base = auth_base

    def get(self, url: str, callback: Callable[[ServerResponse], ChainedThread]) -> ChainedThread:
        thread = ChainedThread(callback=callback, target=lambda: self.__get(url=url))
        thread.start()
        return thread

    def __get(self, url: str) -> ServerResponse:
        sse_session = SSEClient(
            url=url,
            auth=self.__auth_base,
            chunk_size=self.__chunk_size
        )
        return ServerResponse(sse_session=sse_session)
