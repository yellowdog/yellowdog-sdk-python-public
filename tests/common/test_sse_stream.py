from concurrent.futures import ThreadPoolExecutor
from typing import List

from yellowdog_client.common.server_sent_events.sse4python import ServerSentEvent
from yellowdog_client.common.server_sent_events.sse4python.sse_stream import RequestsSseClient, \
    SseStream

from util.sse.sse_server import SseServer
from util.waiter import wait_until


def connect_client(server: SseServer) -> SseStream:
    stream = RequestsSseClient(server.get_sse_url(), None).stream()
    wait_until(lambda: server.get_subscriber_count() == 1)
    return stream


def stream_events(sse_stream: SseStream, event_count: int) -> List[ServerSentEvent]:
    events: List[ServerSentEvent] = []

    for event in sse_stream:
        print(f"Received event: {event}")
        events.append(event)
        if len(events) >= event_count:
            break

    return events


def wait_until_events(sse_stream: SseStream, event_count: int) -> List[ServerSentEvent]:
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(stream_events, sse_stream, event_count)
        return future.result(timeout=2)


def test_can_stream_events():
    with SseServer("/test") as server:
        sse_stream = connect_client(server)

        server.broadcast(id="foo", type="bar", data="baz")

        events = wait_until_events(sse_stream, 1)
        assert events[0] == ServerSentEvent(id="foo", type="bar", data="baz")


def test_can_stream_chunked_events():
    with SseServer("/test", chunked=True) as server:
        sse_stream = connect_client(server)

        server.broadcast_chunks(
            b'id: foo1\nevent: bar1\ndata:',
            b'{"field": "foo1"}',
            b'\n\n'
        )
        server.broadcast_chunks(
            b'id:foo2\nevent:bar2\ndata:',
            b'{"field": "foo2"}',
            b'\n\n'
        )

        events = wait_until_events(sse_stream, 2)
        assert events[0] == ServerSentEvent(id="foo1", type="bar1", data='{"field": "foo1"}')
        assert events[1] == ServerSentEvent(id="foo2", type="bar2", data='{"field": "foo2"}')
