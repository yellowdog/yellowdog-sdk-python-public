from yellowdog_client.model import OciInstancePoolComputeSource
from yellowdog_client.model import ComputeSourceStatus
from .test_utils import should_serde


def test_serialize__oci_instance_pool_compute_source():
    obj_in_raw = OciInstancePoolComputeSource(
        name="oci_instance_pool_name",
        limit=5,

        credential="oci_instance_pool_credential",
        sshKey="oci_instance_pool_sshKey",
        region="oci_instance_pool_region",
        availabilityDomain="oci_instance_pool_availabilityDomain",
        compartmentId="oci_instance_pool_compartmentId",
        imageId="oci_instance_pool_imageId",
        shape="oci_instance_pool_shape",
        subnetId="oci_instance_pool_subnetId",
        assignPublicIp=True,
        userData="oci_instance_pool_userData",

    )
    obj_in_raw.status = ComputeSourceStatus.INACTIVE
    obj_in_raw.statusMessage = "oci_instance_pool_statusMessage"
    obj_in_raw.id = "oci_instance_pool_id"
    obj_in_raw.clusterNetworkId = "oci_instance_pool_instanceConfigurationId"
    obj_in_raw.instancePoolId = "oci_instance_pool_instancePoolId"

    obj_in_dict = {
        "status": "INACTIVE",
        "type": "co.yellowdog.platform.model.OciInstancePoolComputeSource",
        "assignPublicIp": True,
        "name": "oci_instance_pool_name",
        "limit": 5,
        "statusMessage": "oci_instance_pool_statusMessage",
        "id": "oci_instance_pool_id",
        "credential": "oci_instance_pool_credential",
        "sshKey": "oci_instance_pool_sshKey",
        "region": "oci_instance_pool_region",
        "availabilityDomain": "oci_instance_pool_availabilityDomain",
        "compartmentId": "oci_instance_pool_compartmentId",
        "imageId": "oci_instance_pool_imageId",
        "shape": "oci_instance_pool_shape",
        "subnetId": "oci_instance_pool_subnetId",
        "userData": "oci_instance_pool_userData",
        "clusterNetworkId": "oci_instance_pool_instanceConfigurationId",
        "instancePoolId": "oci_instance_pool_instancePoolId"
    }

    should_serde(obj_in_raw, obj_in_dict)
