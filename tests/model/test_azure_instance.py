from datetime import datetime, timezone

from yellowdog_client.common.iso_datetime import iso_format
from yellowdog_client.model import AzureInstance
from yellowdog_client.model import CloudProvider
from yellowdog_client.model import InstanceStatus
from .test_utils import should_serde


def test_serialize_empty__azure_instance():
    obj_in_raw = AzureInstance()

    obj_in_dict = {"type": "co.yellowdog.platform.model.AzureInstance"}

    should_serde(obj_in_raw, obj_in_dict)


def test_serialize__azure_instance():
    obj_in_raw = AzureInstance()
    obj_in_raw.createdTime = datetime(2010, 12, 31, 18, 30, 45, 123000, timezone.utc)
    obj_in_raw.id = "azure_id"
    obj_in_raw.imageId = "azure_imageId"
    obj_in_raw.instanceType = "azure_instanceType"
    obj_in_raw.provider = CloudProvider.AZURE
    obj_in_raw.region = "azure_region"
    obj_in_raw.status = InstanceStatus.STOPPED
    obj_in_raw.subregion = "azure_subregion"
    obj_in_raw.privateIpAddress = "azure_privateIpAddress"
    obj_in_raw.publicIpAddress = "azure_publicIpAddress"
    obj_in_raw.hostname = "azure_hostname"

    obj_in_dict = {
        "type": "co.yellowdog.platform.model.AzureInstance",
        "createdTime": iso_format(datetime(2010, 12, 31, 18, 30, 45, 123456)),
        "id": "azure_id",
        "imageId": "azure_imageId",
        "instanceType": "azure_instanceType",
        "provider": "AZURE",
        "region": "azure_region",
        "status": "STOPPED",
        "subregion": "azure_subregion",
        "privateIpAddress": "azure_privateIpAddress",
        "publicIpAddress": "azure_publicIpAddress",
        "hostname": "azure_hostname",
    }

    should_serde(obj_in_raw, obj_in_dict)
