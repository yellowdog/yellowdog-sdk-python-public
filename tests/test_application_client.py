import pytest

from util.api import MockApi, HttpMethod
from util.data import make
from yellowdog_client import PlatformClient
from yellowdog_client.account import ApplicationClient
from yellowdog_client.model import ServicesSchema, ApiKey, ApplicationDetails, Feature


@pytest.fixture
def application_client(mock_api: MockApi) -> ApplicationClient:
    platform_client = PlatformClient.create(
        ServicesSchema(defaultUrl=mock_api.url()),
        make(ApiKey)
    )
    return platform_client.application_client

def test_get_application_details(mock_api: MockApi, application_client: ApplicationClient):
    expected = ApplicationDetails(
        accountId="000000",
        accountName="test-name",
        id="test-id",
        name="test-name",
        allNamespacesReadable=True,
        readableNamespaces=["test-namespace"],
        features=[Feature.PLATFORM]
    )
    mock_api.mock(f"/application/", HttpMethod.GET, response=expected)

    actual = application_client.get_application_details()

    assert actual == expected
    mock_api.verify_all_requests_called()