from yellowdog_client.model import ServicesSchema, ApiKey
from yellowdog_client import PlatformClient


def test__platform_client():
    PlatformClient.create(
        ServicesSchema(defaultUrl="test"),
        ApiKey()
    )
