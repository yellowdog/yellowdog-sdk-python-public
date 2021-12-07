from yellowdog_client.model import OciInstancesComputeSource
from yellowdog_client.model import ComputeSourceStatus
from .test_utils import should_serde


def test_serialize__oci_instances_compute_source():
    obj_in_raw = OciInstancesComputeSource(
        name="oci_instances_name",
        limit=5,
        credential="oci_instances_credential",
        sshKey="oci_instances_sshKey",
        region="oci_instances_region",
        availabilityDomain="oci_instances_availabilityDomain",
        compartmentId="oci_instances_compartmentId",
        imageId="oci_instances_imageId",
        shape="oci_instances_shape",
        subnetId="oci_instances_subnetId",
        assignPublicIp=True,
        userData="oci_instances_userData"
    )
    obj_in_raw.status = ComputeSourceStatus.NEW
    obj_in_raw.statusMessage = "oci_instances_statusMessage"
    obj_in_raw.id = "oci_instances_id"

    obj_in_dict = {
        "status": "NEW",
        "type": "co.yellowdog.platform.model.OciInstancesComputeSource",
        "assignPublicIp": True,
        "name": "oci_instances_name",
        "limit": 5,
        "statusMessage": "oci_instances_statusMessage",
        "id": "oci_instances_id",
        "credential": "oci_instances_credential",
        "sshKey": "oci_instances_sshKey",
        "region": "oci_instances_region",
        "availabilityDomain": "oci_instances_availabilityDomain",
        "compartmentId": "oci_instances_compartmentId",
        "imageId": "oci_instances_imageId",
        "shape": "oci_instances_shape",
        "subnetId": "oci_instances_subnetId",
        "userData": "oci_instances_userData",
        "preemptible": False,
    }

    should_serde(obj_in_raw, obj_in_dict)
