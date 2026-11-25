import pytest
import sys
import time
import warnings
from datetime import timedelta
from http import HTTPStatus
from requests.exceptions import ConnectionError
from typing import Optional
from unittest import mock
from werkzeug.wrappers import Response
from yellowdog_client import PlatformClient, __version__
from yellowdog_client.common import Product
from yellowdog_client.model import ServicesSchema, ApiKey, RetryProperties, NamespacePolicy

from util.api import MockApi, HttpMethod
from util.data import make


@pytest.fixture
def platform_client(mock_api: MockApi) -> PlatformClient:
    return PlatformClient.create(
        ServicesSchema(defaultUrl=mock_api.url()),
        make(ApiKey)
    )


# This test ensures that a NotImplementedError is not raised when the close method is called on the PlatformClient
# This will happen if a new client is added that forgets to implement close.
def test_can_close(mock_api: MockApi, platform_client: PlatformClient):
    platform_client.close()


def test_close_closes_session(mock_api: MockApi, platform_client: PlatformClient):
    session = platform_client._PlatformClient__session

    with mock.patch.object(session, "close") as mock_session_close:
        platform_client.close()

    mock_session_close.assert_called_once()


def test_default_services_schema_applies_90s_connection_timeout(mock_api: MockApi):

    schema = ServicesSchema(defaultUrl=mock_api.url())
    assert schema.connectionTimeout == timedelta(seconds=90)


def test_services_schema_connection_timeout_can_be_overridden(mock_api: MockApi):

    schema = ServicesSchema(defaultUrl=mock_api.url(), connectionTimeout=timedelta(seconds=60))
    client = PlatformClient.create(schema, make(ApiKey))
    client.close()


def test_services_schema_connection_timeout_can_be_disabled(mock_api: MockApi):

    schema = ServicesSchema(defaultUrl=mock_api.url(), connectionTimeout=None)
    client = PlatformClient.create(schema, make(ApiKey))
    client.close()


def test_default_services_schema_applies_90s_read_timeout(mock_api: MockApi):

    schema = ServicesSchema(defaultUrl=mock_api.url())
    assert schema.readTimeout == timedelta(seconds=90)


def test_default_services_schema_applies_90s_request_timeout(mock_api: MockApi):

    schema = ServicesSchema(defaultUrl=mock_api.url())
    assert schema.requestTimeout == timedelta(seconds=90)


def stall_get_work_requirement(mock_api: MockApi) -> None:
    def stall(_request: object) -> Response:
        time.sleep(1.5)
        return Response(status=HTTPStatus.OK)

    mock_api.httpserver.expect_oneshot_request("/work/requirements/foo").respond_with_handler(stall)


def test_services_schema_request_timeout_fails_stalled_requests(mock_api: MockApi):

    stall_get_work_requirement(mock_api)
    schema = ServicesSchema(
        defaultUrl=mock_api.url(),
        requestTimeout=timedelta(seconds=1),
        retry=RetryProperties(maxAttempts=0)
    )

    with PlatformClient.create(schema, make(ApiKey)) as client:
        with pytest.raises(ConnectionError, match="Read timed out"):
            client.work_client.get_work_requirement_by_id("foo")


def test_services_schema_read_timeout_fails_stalled_requests(mock_api: MockApi):

    stall_get_work_requirement(mock_api)
    with pytest.warns(DeprecationWarning):
        schema = ServicesSchema(
            defaultUrl=mock_api.url(),
            readTimeout=timedelta(seconds=1),
            retry=RetryProperties(maxAttempts=0)
        )

    with PlatformClient.create(schema, make(ApiKey)) as client:
        with pytest.raises(ConnectionError, match="Read timed out"):
            client.work_client.get_work_requirement_by_id("foo")


@pytest.mark.parametrize("schema_args, expected", [
    ({}, timedelta(seconds=90)),
    ({"requestTimeout": timedelta(seconds=30)}, timedelta(seconds=30)),
    ({"requestTimeout": None}, None),
    ({"readTimeout": timedelta(seconds=30)}, timedelta(seconds=30)),
    ({"readTimeout": None}, None),
    ({"requestTimeout": timedelta(seconds=30), "readTimeout": timedelta(seconds=60)}, timedelta(seconds=30)),
    ({"requestTimeout": None, "readTimeout": timedelta(seconds=60)}, None),
])
@pytest.mark.filterwarnings("ignore:ServicesSchema.readTimeout is deprecated:DeprecationWarning")
def test_resolves_request_timeout(schema_args: dict[str, Optional[timedelta]], expected: Optional[timedelta]):
    assert PlatformClient._resolve_request_timeout(ServicesSchema(**schema_args)) == expected


def test_setting_read_timeout_warns_it_is_deprecated():
    with pytest.warns(DeprecationWarning, match="readTimeout is deprecated"):
        ServicesSchema(readTimeout=timedelta(seconds=30))


def test_default_read_timeout_does_not_warn():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        ServicesSchema(requestTimeout=timedelta(seconds=30))


def test_services_schema_read_timeout_can_be_disabled(mock_api: MockApi):

    with pytest.warns(DeprecationWarning):
        schema = ServicesSchema(defaultUrl=mock_api.url(), readTimeout=None)
    client = PlatformClient.create(schema, make(ApiKey))
    client.close()


def _sent_user_agent(mock_api: MockApi, *products: Product) -> str:
    mock_api.mock("/namespaces/foo/policy", HttpMethod.GET, response=NamespacePolicy(namespace="foo"))
    with PlatformClient.create(ServicesSchema(defaultUrl=mock_api.url()), make(ApiKey), *products) as client:
        client.namespaces_client.get_namespace_policy("foo")
    request, _ = mock_api.httpserver.log[-1]
    return request.headers["User-Agent"]


def test_user_agent_names_sdk_and_python(mock_api: MockApi):
    python = f"{sys.version_info.major}.{sys.version_info.minor}"

    assert _sent_user_agent(mock_api) == f"yd/1.1.0 yellowdog-sdk-python/{__version__} python/{python}"


def test_user_agent_appends_products_in_order(mock_api: MockApi):
    python = f"{sys.version_info.major}.{sys.version_info.minor}"

    user_agent = _sent_user_agent(mock_api, Product("my-framework", "3.0"), Product("my-app", "1.2.0"))

    assert user_agent == f"yd/1.1.0 yellowdog-sdk-python/{__version__} python/{python} my-framework/3.0 my-app/1.2.0"


def test_product_accepts_every_token_character():
    token = "!#$%&'*+-.^_`|~09AZaz"

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        product = Product(token, token)

    assert product.name == token
    assert product.version == token


@pytest.mark.parametrize("value, sent", [
    ("my app", "my_app"),
    (" my-app\t", "my-app"),
    ("1/0", "1#0"),
    ("my\x00app", "myapp"),
    ("my-äpp", "my-_pp"),
    ("(1.0)", "_1.0_"),
    ("", "unknown"),
    ("\x00", "unknown"),
    ("my\x85app", "myapp"),
    ("\xa0my\u2007app\u202f", "_my_app_"),
    ("\u3000my\u2028app\u3000", "my_app"),
])
def test_product_sends_token_in_place_of_value_that_is_not_one(value: str, sent: str):
    with pytest.warns(UserWarning, match="is not an RFC 9110 token") as warnings_issued:
        product = Product(value, value)

    assert product == Product(sent, sent)
    assert len(warnings_issued) == 2
    assert warnings_issued[0].filename == __file__


def test_product_rejects_none():
    with pytest.raises(TypeError):
        Product(None, "1.0")
