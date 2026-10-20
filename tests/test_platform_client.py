import time
from datetime import timedelta
from http import HTTPStatus

import pytest
from unittest import mock
from requests.exceptions import ConnectionError
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


def test_services_schema_read_timeout_fails_stalled_requests(mock_api: MockApi):

    def stall(_request: object) -> Response:
        time.sleep(1.5)
        return Response(status=HTTPStatus.OK)

    mock_api.httpserver.expect_oneshot_request("/work/requirements/foo").respond_with_handler(stall)
    schema = ServicesSchema(
        defaultUrl=mock_api.url(),
        readTimeout=timedelta(seconds=1),
        retry=RetryProperties(maxAttempts=0)
    )

    with PlatformClient.create(schema, make(ApiKey)) as client:
        with pytest.raises(ConnectionError, match="Read timed out"):
            client.work_client.get_work_requirement_by_id("foo")


def test_services_schema_read_timeout_can_be_disabled(mock_api: MockApi):

    schema = ServicesSchema(defaultUrl=mock_api.url(), readTimeout=None)
    client = PlatformClient.create(schema, make(ApiKey))
    client.close()
