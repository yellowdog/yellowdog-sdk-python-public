import pytest
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
