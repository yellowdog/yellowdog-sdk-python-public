from .test_utils import should_serde

from yellowdog_client.model import AzureInstanceCredential


def test_serialize__azure_instance_credential():
    obj_in_raw = AzureInstanceCredential(
        name="AzureInstanceCredential_name",
        adminUsername="AzureInstanceCredential_adminUserName",
        adminPassword="AzureInstanceCredential_adminPassword",
    )

    obj_in_dict = {
        "type": "co.yellowdog.platform.account.credentials.AzureInstanceCredential",
        "name": "AzureInstanceCredential_name",
        "adminUsername": "AzureInstanceCredential_adminUserName",
        "adminPassword": "AzureInstanceCredential_adminPassword"
    }

    should_serde(obj_in_raw, obj_in_dict)
