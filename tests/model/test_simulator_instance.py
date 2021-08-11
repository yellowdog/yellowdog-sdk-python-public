from datetime import datetime, timezone

from yellowdog_client.common.iso_datetime import iso_format
from yellowdog_client.model import SimulatorInstance
from yellowdog_client.model import CloudProvider
from yellowdog_client.model import InstanceStatus
from .test_utils import should_serde


def test_serialize__simulator_instance():
    obj_in_raw = SimulatorInstance()
    obj_in_raw.createdTime = datetime(2010, 12, 31, 18, 30, 45, 123000, timezone.utc)
    obj_in_raw.id = "simulator_id"
    obj_in_raw.imageId = "simulator_imageId"
    obj_in_raw.instanceType = "simulator_instanceType"
    obj_in_raw.provider = CloudProvider.ON_PREMISE
    obj_in_raw.region = "simulator_region"
    obj_in_raw.status = InstanceStatus.RUNNING
    obj_in_raw.subregion = "simulator_subregion"
    obj_in_raw.privateIpAddress = "simulator_privateIpAddress"
    obj_in_raw.publicIpAddress = "simulator_publicIpAddress"
    obj_in_raw.hostname = "simulator_hostname"
    obj_in_raw.updateTime = datetime(2011, 12, 31, 18, 30, 45, 123000, timezone.utc)
    obj_in_raw.refreshTime = datetime(2012, 12, 31, 18, 30, 45, 123000, timezone.utc)

    obj_in_dict = {
        "type": "co.yellowdog.platform.model.SimulatorInstance",
        "createdTime": iso_format(datetime(2010, 12, 31, 18, 30, 45, 123456)),
        "id": "simulator_id",
        "imageId": "simulator_imageId",
        "instanceType": "simulator_instanceType",
        "provider": "ON_PREMISE",
        "region": "simulator_region",
        "status": "RUNNING",
        "subregion": "simulator_subregion",
        "privateIpAddress": "simulator_privateIpAddress",
        "publicIpAddress": "simulator_publicIpAddress",
        "hostname": "simulator_hostname",
        "updateTime": iso_format(datetime(2011, 12, 31, 18, 30, 45, 123456)),
        "refreshTime": iso_format(datetime(2012, 12, 31, 18, 30, 45, 123456))
    }

    should_serde(obj_in_raw, obj_in_dict)
