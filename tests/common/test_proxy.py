import traceback
from dataclasses import dataclass
from http import HTTPStatus
from typing import List

import pytest
from requests import HTTPError
from yellowdog_client.common import Proxy, UserAgent
from yellowdog_client.common.credentials import ApiKeyAuthenticationHeadersProvider
from yellowdog_client.common.server_sent_events import SubscriptionManager, SubscriptionEventListener
from yellowdog_client.model import ApiKey

from util.api import MockApi, HttpMethod
from util.data import make
from util.sse.sse_server import SseServer
from util.waiter import wait_until

TEST_ENDPOINT = "/test"


def build_proxy(base_url: str, retry_count: int = 0, max_retry_interval_seconds: int = 0) -> Proxy:
    return Proxy(
        authentication_headers_provider=ApiKeyAuthenticationHeadersProvider(make(ApiKey)),
        retry_count=retry_count,
        max_retry_interval_seconds=max_retry_interval_seconds,
        base_url=base_url,
        user_agent=UserAgent("test", "1.0", "3.8")
    )


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
    with SseServer(TEST_ENDPOINT) as sse_server:
        proxy = build_proxy(sse_server.get_sse_url())

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


def test_can_stream_chunked_sse():
    with SseServer(TEST_ENDPOINT, chunked=True) as sse_server:
        proxy = build_proxy(sse_server.get_sse_url())

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


def test_retry_on_5xx_status(mock_api: MockApi):
    proxy = build_proxy(mock_api.url(), retry_count=1)

    expected = Example(field="foo")

    mock_api.mock_error(TEST_ENDPOINT, HttpMethod.GET, status=HTTPStatus.SERVICE_UNAVAILABLE)
    mock_api.mock(TEST_ENDPOINT, HttpMethod.GET, response=expected)

    actual = proxy.get(Example, TEST_ENDPOINT)

    assert actual == expected


def test_does_not_retry_more_than_max(mock_api: MockApi):
    proxy = build_proxy(mock_api.url(), retry_count=1)

    mock_api.mock_error(TEST_ENDPOINT, HttpMethod.GET, status=HTTPStatus.SERVICE_UNAVAILABLE)
    mock_api.mock_error(TEST_ENDPOINT, HttpMethod.GET, status=HTTPStatus.SERVICE_UNAVAILABLE)
    mock_api.mock(TEST_ENDPOINT, HttpMethod.GET, response=Example(field="foo"))

    with pytest.raises(HTTPError) as ex_info:
        proxy.get(Example, TEST_ENDPOINT)

    assert ex_info.value.response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
