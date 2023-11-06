import traceback
from dataclasses import dataclass
from datetime import timedelta
from typing import List

from yellowdog_client.common import Proxy
from yellowdog_client.common.credentials import ApiKeyAuthenticationHeadersProvider
from yellowdog_client.common.server_sent_events import SubscriptionManager, SubscriptionEventListener
from yellowdog_client.model import ApiKey

from util.data import make
from util.sse.sse_server import SseServer
from util.waiter import wait_until


@dataclass
class Example:
    field: str


class ExampleSubscriptionEventListener(SubscriptionEventListener[Example]):
    def __init__(self):
        self.updates: List[Example] = []
        self.errors: List[Exception] = []
        self.cancelled: bool = False

    def updated(self, obj: Example) -> None:
        print(f"Received update: {obj}")
        self.updates.append(obj)

    def subscription_error(self, error: Exception) -> None:
        print(f"Received error: {type(error).__name__} {error}")
        traceback.print_tb(error.__traceback__)
        self.errors.append(error)

    def subscription_cancelled(self) -> None:
        self.cancelled = True


def test_can_stream_sse():
    with SseServer("/test") as sse_server:
        proxy = build_proxy(sse_server)

        with SubscriptionManager(
                update_events_provider=lambda id: proxy.stream(""),
                class_type=Example
        ) as subscription_manager:
            listener = ExampleSubscriptionEventListener()
            subscription_manager.add_listener("foo", listener)

            wait_until(lambda: sse_server.get_subscriber_count() == 1)

            sse_server.broadcast(id="foo1", type="entity_updated", data='{"field": "foo1"}')
            sse_server.broadcast(id="foo2", type="entity_updated", data='{"field": "foo2"}')

            wait_until(lambda: len(listener.updates) == 2)
            assert len(listener.errors) == 0


def build_proxy(sse_server) -> Proxy:
    return Proxy(
        authentication_headers_provider=ApiKeyAuthenticationHeadersProvider(make(ApiKey)),
        retry_count=0,
        initial_retry_interval=timedelta(seconds=0),
        base_url=sse_server.get_sse_url()
    )


def test_can_stream_chunked_sse():
    with SseServer("/test", chunked=True) as sse_server:
        proxy = build_proxy(sse_server)

        with SubscriptionManager(
                update_events_provider=lambda id: proxy.stream(""),
                class_type=Example
        ) as subscription_manager:
            listener = ExampleSubscriptionEventListener()
            subscription_manager.add_listener("foo", listener)

            wait_until(lambda: sse_server.get_subscriber_count() == 1)

            sse_server.broadcast_chunks(
                b'id: foo1\nevent: entity_updated\ndata:',
                b'{"field": "foo1"}',
                b'\n\n'
            )
            sse_server.broadcast_chunks(
                b'id:foo2\nevent:entity_updated\ndata:',
                b'{"field": "foo2"}',
                b'\n\n'
            )

            wait_until(lambda: len(listener.updates) == 2)
            assert len(listener.errors) == 0
