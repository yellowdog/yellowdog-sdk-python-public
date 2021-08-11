from .test_utils import should_serde
from yellowdog_client.model import AwsOnDemandComputeSource
from yellowdog_client.model import ComputeSourceStatus


def test_serialize__aws_on_demand_compute_source():
    obj_in_raw = AwsOnDemandComputeSource(
        name="aws_on_demand_name",
        limit=5,
        region="aws_on_demand_region",
        credential="aws_on_demand_credential",
        availabilityZone="aws_on_demand_availabilityZone",
        securityGroupId="aws_on_demand_securityGroupId",
        instanceType="aws_on_demand_instanceType",
        imageId="aws_on_demand_imageId",
        specifyMinimum=True,
        assignPublicIp=True,
        keyName="aws_on_demand_keyName",
        iamRoleArn="aws_on_demand_iamRoleName",
        subnetId="aws_on_demand_subnetId",
        userData="aws_on_demand_userData"
    )
    obj_in_raw.status = ComputeSourceStatus.ACTIVE
    obj_in_raw.statusMessage = "aws_on_demand_statusMessage"
    obj_in_raw.id = "aws_on_demand_id"

    obj_in_dict = {
        "status": "ACTIVE",
        "type": "co.yellowdog.platform.model.AwsOnDemandComputeSource",
        "assignPublicIp": True,
        "name": "aws_on_demand_name",
        "limit": 5,
        "statusMessage": "aws_on_demand_statusMessage",
        "id": "aws_on_demand_id",
        "region": "aws_on_demand_region",
        "credential": "aws_on_demand_credential",
        "availabilityZone": "aws_on_demand_availabilityZone",
        "securityGroupId": "aws_on_demand_securityGroupId",
        "instanceType": "aws_on_demand_instanceType",
        "imageId": "aws_on_demand_imageId",
        "specifyMinimum": True,
        "keyName": "aws_on_demand_keyName",
        "iamRoleArn": "aws_on_demand_iamRoleName",
        "subnetId": "aws_on_demand_subnetId",
        "userData": "aws_on_demand_userData"
    }

    should_serde(obj_in_raw, obj_in_dict)
