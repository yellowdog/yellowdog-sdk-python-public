from yellowdog_client.model import AzureScaleSetComputeSource
from yellowdog_client.model import ComputeSourceStatus
from .test_utils import should_serde


def test_serialize__azure_scale_set_compute_source():
    obj_in_raw = AzureScaleSetComputeSource(
        name="azure_scale_set_name",
        limit=5,
        region="azure_scale_set_region",
        credential="azure_scale_set_credential",
        imageId="azure_scale_set_imageId",
        userData="azure_scale_set_userData",
        environment="azure_scale_set_environment",
        networkResourceGroupName="azure_scale_set_networkResourceGroupName",
        networkName="azure_scale_set_networkName",
        adminUserCredential="azure_scale_set_adminUserCredential",
        sshKey="azure_scale_set_sshKey",
        subnetName="azure_scale_set_subnetName",
        vmSize="azure_scale_set_vmSize"
    )
    obj_in_raw.status = ComputeSourceStatus.INACTIVE
    obj_in_raw.statusMessage = "azure_scale_set_statusMessage"
    obj_in_raw.id = "azure_scale_set_id"

    obj_in_dict = {
        "status": "INACTIVE",
        "type": "co.yellowdog.platform.model.AzureScaleSetComputeSource",
        "name": "azure_scale_set_name",
        "limit": 5,
        "statusMessage": "azure_scale_set_statusMessage",
        "id": "azure_scale_set_id",
        "region": "azure_scale_set_region",
        "credential": "azure_scale_set_credential",
        "imageId": "azure_scale_set_imageId",
        "userData": "azure_scale_set_userData",
        "environment": "azure_scale_set_environment",
        "networkResourceGroupName": "azure_scale_set_networkResourceGroupName",
        "networkName": "azure_scale_set_networkName",
        "adminUserCredential": "azure_scale_set_adminUserCredential",
        "sshKey": "azure_scale_set_sshKey",
        "subnetName": "azure_scale_set_subnetName",
        "vmSize": "azure_scale_set_vmSize",
    }

    should_serde(obj_in_raw, obj_in_dict)
