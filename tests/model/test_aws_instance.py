from datetime import datetime, timezone

from .test_utils import should_serde
from yellowdog_client.common.iso_datetime import iso_format
from yellowdog_client.model import AwsInstance
from yellowdog_client.model import CloudProvider
from yellowdog_client.model import InstanceStatus


def test_serialize_empty__aws_instance():
    obj_in_raw = AwsInstance()

    obj_in_dict = {"type": "co.yellowdog.platform.model.AwsInstance"}

    should_serde(obj_in_raw, obj_in_dict)


def test_serialize__aws_instance():
    obj_in_raw = AwsInstance()
    obj_in_raw.createdTime = datetime(2010, 12, 31, 18, 30, 45, 123000, timezone.utc)
    obj_in_raw.id = "aws_id"
    obj_in_raw.imageId = "aws_imageId"
    obj_in_raw.instanceType = "aws_instanceType"
    obj_in_raw.provider = CloudProvider.AWS
    obj_in_raw.region = "aws_region"
    obj_in_raw.status = InstanceStatus.STOPPED
    obj_in_raw.subregion = "aws_subregion"
    obj_in_raw.privateIpAddress = "aws_privateIpAddress"
    obj_in_raw.publicIpAddress = "aws_publicIpAddress"
    obj_in_raw.hostname = "aws_hostname"
    obj_in_raw.instanceLifecycle = "aws_instanceLifecycle"

    obj_in_dict = {
        "type": "co.yellowdog.platform.model.AwsInstance",
        "createdTime": iso_format(datetime(2010, 12, 31, 18, 30, 45, 123456)),
        "id": "aws_id",
        "imageId": "aws_imageId",
        "instanceType": "aws_instanceType",
        "provider": "AWS",
        "region": "aws_region",
        "status": "STOPPED",
        "subregion": "aws_subregion",
        "privateIpAddress": "aws_privateIpAddress",
        "publicIpAddress": "aws_publicIpAddress",
        "hostname": "aws_hostname",
        "instanceLifecycle": "aws_instanceLifecycle"
    }

    should_serde(obj_in_raw, obj_in_dict)
