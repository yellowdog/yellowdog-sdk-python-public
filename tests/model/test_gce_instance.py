from datetime import datetime, timezone

from yellowdog_client.common.iso_datetime import iso_format
from yellowdog_client.model import GceInstance
from yellowdog_client.model import CloudProvider
from yellowdog_client.model import InstanceStatus
from .test_utils import should_serde


def test_serialize_empty__gce_instance():
    obj_in_raw = GceInstance()

    obj_in_dict = {"type": "co.yellowdog.platform.model.GceInstance", "preemptible": False}

    should_serde(obj_in_raw, obj_in_dict)


def test_serialize__gce_instance():
    obj_in_raw = GceInstance()
    obj_in_raw.createdTime = datetime(2010, 12, 31, 18, 30, 45, 123000, timezone.utc)
    obj_in_raw.id = "gce_id"
    obj_in_raw.imageId = "gce_imageId"
    obj_in_raw.instanceType = "gce_instanceType"
    obj_in_raw.provider = CloudProvider.ON_PREMISE
    obj_in_raw.region = "gce_region"
    obj_in_raw.status = InstanceStatus.RUNNING
    obj_in_raw.subregion = "gce_subregion"
    obj_in_raw.privateIpAddress = "gce_privateIpAddress"
    obj_in_raw.publicIpAddress = "gce_publicIpAddress"
    obj_in_raw.hostname = "gce_hostname"
    obj_in_raw.preemptible = True

    obj_in_dict = {
        "type": "co.yellowdog.platform.model.GceInstance",
        "preemptible": True,
        "createdTime": iso_format(datetime(2010, 12, 31, 18, 30, 45, 123456)),
        "id": "gce_id",
        "imageId": "gce_imageId",
        "instanceType": "gce_instanceType",
        "provider": "ON_PREMISE",
        "region": "gce_region",
        "status": "RUNNING",
        "subregion": "gce_subregion",
        "privateIpAddress": "gce_privateIpAddress",
        "publicIpAddress": "gce_publicIpAddress",
        "hostname": "gce_hostname",
    }

    should_serde(obj_in_raw, obj_in_dict)
