from datetime import datetime, timezone

from yellowdog_client.common.iso_datetime import iso_format
from yellowdog_client.model import AlibabaInstance
from yellowdog_client.model import CloudProvider
from yellowdog_client.model import InstanceStatus
from .test_utils import should_serde


def test_serialize_empty__alibaba_instance():
    obj_in_raw = AlibabaInstance()

    obj_in_dict = {"type": "co.yellowdog.platform.model.AlibabaInstance"}
    should_serde(obj_in_raw, obj_in_dict)


def test_serialize__alibaba_instance():
    obj_in_raw = AlibabaInstance()
    obj_in_raw.createdTime = datetime(2010, 12, 31, 18, 30, 45, 123000, timezone.utc)
    obj_in_raw.id = "alibaba_id"
    obj_in_raw.imageId = "alibaba_imageId"
    obj_in_raw.instanceType = "alibaba_instanceType"
    obj_in_raw.provider = CloudProvider.ALIBABA
    obj_in_raw.region = "alibaba_region"
    obj_in_raw.status = InstanceStatus.STOPPING
    obj_in_raw.subregion = "alibaba_subregion"
    obj_in_raw.privateIpAddress = "alibaba_privateIpAddress"
    obj_in_raw.publicIpAddress = "alibaba_publicIpAddress"
    obj_in_raw.hostname = "alibaba_hostname"

    obj_in_dict = {
        "type": "co.yellowdog.platform.model.AlibabaInstance",
        "createdTime": iso_format(datetime(2010, 12, 31, 18, 30, 45, 123456, timezone.utc)),
        "id": "alibaba_id",
        "imageId": "alibaba_imageId",
        "instanceType": "alibaba_instanceType",
        "provider": "ALIBABA",
        "region": "alibaba_region",
        "status": "STOPPING",
        "subregion": "alibaba_subregion",
        "privateIpAddress": "alibaba_privateIpAddress",
        "publicIpAddress": "alibaba_publicIpAddress",
        "hostname": "alibaba_hostname"
    }

    should_serde(obj_in_raw, obj_in_dict)
