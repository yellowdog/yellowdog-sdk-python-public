from datetime import datetime, timezone

from yellowdog_client.common.iso_datetime import iso_format
from yellowdog_client.model import OciInstance
from yellowdog_client.model import CloudProvider
from yellowdog_client.model import InstanceStatus
from .test_utils import should_serde


def test_serialize__oci_instance():
    obj_in_raw = OciInstance()
    obj_in_raw.createdTime = datetime(2010, 12, 31, 18, 30, 45, 123000, timezone.utc)
    obj_in_raw.id = "oci_id"
    obj_in_raw.imageId = "oci_imageId"
    obj_in_raw.instanceType = "oci_instanceType"
    obj_in_raw.provider = CloudProvider.OCI
    obj_in_raw.region = "oci_region"
    obj_in_raw.status = InstanceStatus.UNKNOWN
    obj_in_raw.subregion = "oci_subregion"
    obj_in_raw.privateIpAddress = "oci_privateIpAddress"
    obj_in_raw.publicIpAddress = "oci_publicIpAddress"
    obj_in_raw.hostname = "oci_hostname"
    obj_in_raw.compartmentId = "oci_compartmentId"

    obj_in_dict = {
        "type": "co.yellowdog.platform.model.OciInstance",
        "createdTime": iso_format(datetime(2010, 12, 31, 18, 30, 45, 123456)),
        "id": "oci_id",
        "imageId": "oci_imageId",
        "instanceType": "oci_instanceType",
        "provider": "OCI",
        "region": "oci_region",
        "status": "UNKNOWN",
        "subregion": "oci_subregion",
        "privateIpAddress": "oci_privateIpAddress",
        "publicIpAddress": "oci_publicIpAddress",
        "hostname": "oci_hostname",
        "compartmentId": "oci_compartmentId"
    }

    should_serde(obj_in_raw, obj_in_dict)
