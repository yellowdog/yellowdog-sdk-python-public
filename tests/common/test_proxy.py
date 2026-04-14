import datetime
import gzip
import json
import traceback
from dataclasses import dataclass
from http import HTTPStatus
from typing import List, Optional
from unittest import mock

import pytest
from requests import HTTPError
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectTimeout
from urllib3.util.retry import Retry
from werkzeug.wrappers import Response as WerkzeugResponse

from util.api import MockApi, HttpMethod
from util.data import make
from util.sse.sse_server import SseServer
from util.waiter import wait_until
from yellowdog_client.common import Proxy, UserAgent
from yellowdog_client.common.credentials import ApiKeyAuthenticationHeadersProvider
from yellowdog_client.common.json import Json
from yellowdog_client.common.server_sent_events import SubscriptionManager, SubscriptionEventListener
from yellowdog_client.model import ApiKey, ServicesSchema
from yellowdog_client.platform_client import PlatformClient

TEST_ENDPOINT = "/test"


def build_proxy(base_url: str, retry_count: int = 0, compress_requests: bool = False,
                connection_timeout: Optional[float] = 90.0) -> Proxy:
    session = Session()
    adapter = HTTPAdapter(max_retries=Retry(
        total=retry_count,
        connect=retry_count,
        read=retry_count,
        backoff_factor=2,
        allowed_methods=frozenset(['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'TRACE']),
        status_forcelist=[429, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511],
        raise_on_status=False
    ))
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return Proxy(
        authentication_headers_provider=ApiKeyAuthenticationHeadersProvider(make(ApiKey)),
        session=session,
        base_url=base_url,
        user_agent=UserAgent("test", "1.0", "3.8"),
        compress_requests=compress_requests,
        connection_timeout=connection_timeout
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


def test_serializes_date_params_in_iso_format(mock_api: MockApi):
    proxy = build_proxy(mock_api.url())

    mock_api.mock(TEST_ENDPOINT, HttpMethod.GET, params={"foo": "2018-10-02T14%3A38%3A09.023Z"})

    proxy.get(None, TEST_ENDPOINT, params={"foo": datetime.datetime(
        year=2018,
        month=10,
        day=2,
        hour=14,
        minute=38,
        second=9,
        microsecond=23000,
        tzinfo=datetime.timezone.utc
    )})

    mock_api.verify_all_requests_called()


def test_serializes_duration_params_in_iso_format(mock_api: MockApi):
    proxy = build_proxy(mock_api.url())

    mock_api.mock(TEST_ENDPOINT, HttpMethod.GET, params={"foo": "P1DT2H30S"})

    proxy.get(None, TEST_ENDPOINT, params={"foo": datetime.timedelta(days=1, hours=2, seconds=30)})

    mock_api.verify_all_requests_called()


def test_large_request_body_is_gzip_compressed(mock_api: MockApi):
    proxy = build_proxy(mock_api.url(), compress_requests=True)
    data = Example(field="x" * Proxy.GZIP_THRESHOLD_BYTES)  # Exceeds threshold

    captured = {}

    def handler(request):
        captured["content_encoding"] = request.headers.get("Content-Encoding")
        captured["body"] = request.data
        return WerkzeugResponse(Json.dumps(data), content_type="application/json", status=200)

    mock_api.httpserver.expect_oneshot_request(TEST_ENDPOINT, method="POST").respond_with_handler(handler)

    proxy.post(Example, data, TEST_ENDPOINT)

    assert captured["content_encoding"] == "gzip"
    actual = Json.load(json.loads(gzip.decompress(captured["body"])), Example)
    assert actual == data
    mock_api.verify_all_requests_called()


def test_small_request_body_is_not_compressed(mock_api: MockApi):
    proxy = build_proxy(mock_api.url(), compress_requests=True)
    data = Example(field="small")

    captured = {}

    def handler(request):
        captured["content_encoding"] = request.headers.get("Content-Encoding")
        captured["body"] = request.data
        return WerkzeugResponse(Json.dumps(data), content_type="application/json", status=200)

    mock_api.httpserver.expect_oneshot_request(TEST_ENDPOINT, method="POST").respond_with_handler(handler)

    proxy.post(Example, data, TEST_ENDPOINT)

    assert captured["content_encoding"] is None
    actual = Json.load(json.loads(captured["body"]), Example)
    assert actual == data
    mock_api.verify_all_requests_called()


def test_session_is_reused_across_requests(mock_api: MockApi):
    proxy = build_proxy(mock_api.url())

    mock_api.mock(TEST_ENDPOINT, HttpMethod.GET, response=Example(field="first"))
    mock_api.mock(TEST_ENDPOINT, HttpMethod.GET, response=Example(field="second"))

    initial_session = proxy._session
    proxy.get(Example, TEST_ENDPOINT)
    proxy.get(Example, TEST_ENDPOINT)

    assert proxy._session is initial_session


def test_sub_proxy_shares_session_with_parent():
    proxy = build_proxy("http://example.com")
    sub_proxy = proxy.append_base_url("/api")

    assert sub_proxy._session is proxy._session


def test_connect_timeout_passed_as_connect_only_tuple(mock_api: MockApi):
    """The connect timeout must be sent as (connect, None) so only the connect phase is applied."""
    proxy = build_proxy(mock_api.url(), connection_timeout=5.0)

    mock_api.mock(TEST_ENDPOINT, HttpMethod.GET, response=Example(field="foo"))

    with mock.patch.object(proxy._session, "send", wraps=proxy._session.send) as mock_send:
        proxy.get(Example, TEST_ENDPOINT)

    assert mock_send.call_args[1]["timeout"] == (5.0, None)


def test_connection_timeout_is_propagated_to_sub_proxy():
    proxy = build_proxy("http://example.com", connection_timeout=10.0)
    sub_proxy = proxy.append_base_url("/api")

    assert sub_proxy._connection_timeout == 10.0


def test_request_raises_connect_timeout(mock_api: MockApi):

    proxy = build_proxy(mock_api.url(), connection_timeout=0.0001)

    with mock.patch.object(
        proxy._session, "send", side_effect=ConnectTimeout("Connection timed out")
    ):
        with pytest.raises(ConnectTimeout):
            proxy.get(Example, TEST_ENDPOINT)