from yellowdog_client.model import AwsSpotComputeSource
from yellowdog_client.model import ComputeSourceStatus
from .test_utils import should_serde


def test_serialize__aws_spot_compute_source():
    obj_in_raw = AwsSpotComputeSource(
        name="aws_spot_name",
        limit=5,
        region="aws_spot_region",
        credential="aws_spot_credential",
        availabilityZone="aws_spot_availabilityZone",
        securityGroupId="aws_spot_securityGroupId",
        instanceType="aws_spot_instanceType",
        imageId="aws_spot_imageId",
        assignPublicIp=True,
        keyName="aws_spot_keyName",
        iamRoleArn="aws_spot_iamRoleName",
        subnetId="aws_spot_subnetId",
        userData="aws_spot_userData",
        spotPriceMax=50.0
    )
    obj_in_raw.status = ComputeSourceStatus.ACTIVE
    obj_in_raw.statusMessage = "aws_spot_statusMessage"
    obj_in_raw.id = "aws_spot_id"

    obj_in_dict = {
        "status": "ACTIVE",
        "type": "co.yellowdog.platform.model.AwsSpotComputeSource",
        "assignPublicIp": True,
        "name": "aws_spot_name",
        "limit": 5,
        "statusMessage": "aws_spot_statusMessage",
        "id": "aws_spot_id",
        "region": "aws_spot_region",
        "credential": "aws_spot_credential",
        "availabilityZone": "aws_spot_availabilityZone",
        "securityGroupId": "aws_spot_securityGroupId",
        "instanceType": "aws_spot_instanceType",
        "imageId": "aws_spot_imageId",
        "keyName": "aws_spot_keyName",
        "iamRoleArn": "aws_spot_iamRoleName",
        "subnetId": "aws_spot_subnetId",
        "userData": "aws_spot_userData",
        "spotPriceMax": 50.0
    }

    should_serde(obj_in_raw, obj_in_dict)
