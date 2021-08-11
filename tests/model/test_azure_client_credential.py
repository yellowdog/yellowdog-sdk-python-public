from .test_utils import should_serde

from yellowdog_client.model import AzureClientCredential


def test_serialize__azure_client_credential():
    obj_in_raw = AzureClientCredential(
        name="AzureClientCredential_name",
        clientId="AzureClientCredential_clientId",
        tenantId="AzureClientCredential_tenantId",
        subscriptionId="AzureClientCredential_subscriptionId",
        key="AzureClientCredential_key",
    )

    obj_in_dict = {
        "type": "co.yellowdog.platform.account.credentials.AzureClientCredential",
        "name": "AzureClientCredential_name",
        "clientId": "AzureClientCredential_clientId",
        "tenantId": "AzureClientCredential_tenantId",
        "subscriptionId": "AzureClientCredential_subscriptionId",
        "key": "AzureClientCredential_key"
    }

    should_serde(obj_in_raw, obj_in_dict)
