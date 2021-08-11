from .test_utils import should_serde
from yellowdog_client.model import AzureInstancesComputeSource
from yellowdog_client.model import ComputeSourceStatus


def test_serialize__azure_instances_compute_source():
    obj_in_raw = AzureInstancesComputeSource(
        name="azure_instances_name",
        limit=5,
        region="azure_instances_region",
        credential="azure_instances_credential",
        imageId="azure_instances_imageId",
        assignPublicIp=True,
        userData="azure_instances_userData",
        environment="azure_instances_environment",
        networkResourceGroupName="azure_instances_networkResourceGroupName",
        networkName="azure_instances_networkName",
        adminUserCredential="azure_instances_adminUserCredential",
        sshKey="azure_instances_sshKey",
        subnetName="azure_instances_subnetName",
        vmSize="azure_instances_vmSize"
    )
    obj_in_raw.status = ComputeSourceStatus.ERRORED
    obj_in_raw.statusMessage = "azure_instances_statusMessage"
    obj_in_raw.id = "azure_instances_id"

    obj_in_dict = {
        "status": "ERRORED",
        "type": "co.yellowdog.platform.model.AzureInstancesComputeSource",
        "assignPublicIp": True,
        "name": "azure_instances_name",
        "limit": 5,
        "statusMessage": "azure_instances_statusMessage",
        "id": "azure_instances_id",
        "region": "azure_instances_region",
        "credential": "azure_instances_credential",
        "imageId": "azure_instances_imageId",
        "userData": "azure_instances_userData",
        "environment": "azure_instances_environment",
        "networkResourceGroupName": "azure_instances_networkResourceGroupName",
        "networkName": "azure_instances_networkName",
        "adminUserCredential": "azure_instances_adminUserCredential",
        "sshKey": "azure_instances_sshKey",
        "subnetName": "azure_instances_subnetName",
        "vmSize": "azure_instances_vmSize",
    }

    should_serde(obj_in_raw, obj_in_dict)
