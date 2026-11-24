import pytest
import time
import warnings
from datetime import timedelta
from http import HTTPStatus
from requests.exceptions import ConnectionError
from typing import Optional
from unittest import mock
from werkzeug.wrappers import Response
from yellowdog_client import PlatformClient
from yellowdog_client.model import ServicesSchema, ApiKey, RetryProperties

from util.api import MockApi
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
