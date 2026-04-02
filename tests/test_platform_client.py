import pytest
from unittest import mock
from yellowdog_client import PlatformClient
from yellowdog_client.model import ServicesSchema, ApiKey

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
