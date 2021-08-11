from yellowdog_client.model import GceInstanceGroupComputeSource
from yellowdog_client.model import ComputeSourceStatus
from .test_utils import should_serde


def test_serialize__gce_instance_group_compute_source():
    obj_in_raw = GceInstanceGroupComputeSource(
        name="gce_name",
        limit=5,
        credential="gce_credential",
        assignPublicIp=True,
        userData="gce_userData",
        sshKeys="gce_sshKeys",
        project="gce_project",
        region="gce_region",
        zone="gce_zone",
        machineType="gce_machineType",
        image="gce_image",
        network="gce_network",
        subnetwork="gce_subnetwork",
        preemptible=True,
        acceleratorType="ACCELERATOR",
        acceleratorCount=100
    )
    obj_in_raw.status = ComputeSourceStatus.UPDATING
    obj_in_raw.statusMessage = "gce_statusMessage"
    obj_in_raw.id = "gce_id"

    obj_in_dict = {
        "status": "UPDATING",
        "type": "co.yellowdog.platform.model.GceInstanceGroupComputeSource",
        "assignPublicIp": True,
        "name": "gce_name",
        "limit": 5,
        "statusMessage": "gce_statusMessage",
        "id": "gce_id",
        "credential": "gce_credential",
        "userData": "gce_userData",
        "sshKeys": "gce_sshKeys",
        "project": "gce_project",
        "region": "gce_region",
        "zone": "gce_zone",
        "machineType": "gce_machineType",
        "image": "gce_image",
        "network": "gce_network",
        "subnetwork": "gce_subnetwork",
        "preemptible": True,
        "acceleratorType": "ACCELERATOR",
        "acceleratorCount": 100
    }

    should_serde(obj_in_raw, obj_in_dict)
