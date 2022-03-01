from yellowdog_client.model import AlibabaInstanceChargeType
from yellowdog_client.model import AlibabaInstancesComputeSource
from yellowdog_client.model import AlibabaSpotStrategy
from yellowdog_client.model import ComputeSourceStatus
from .test_utils import should_serde


def test_serialize__alibaba_instances_compute_source():
    obj_in_raw = AlibabaInstancesComputeSource(
        name="alibaba_name",
        limit=5,
        region="alibaba_region",
        credential="alibaba_credential",
        availabilityZone="alibaba_availabilityZone",
        securityGroupId="alibaba_securityGroupId",
        instanceType="alibaba_instanceType",
        imageId="alibaba_imageId",
        specifyMinimum=True,
        assignPublicIp=True,
        keyName="alibaba_keyName",
        userData="alibaba_userData",
        instanceChargeType=AlibabaInstanceChargeType.POST_PAID,
        spotStrategy=AlibabaSpotStrategy.SPOT_AS_PRICE_GO,
        ramRoleName="alibaba_ramRoleName",
        vSwitchId="alibaba_vswitchId",
        spotPriceLimit=10.0
    )
    obj_in_raw.status = ComputeSourceStatus.UPDATING
    obj_in_raw.statusMessage = "alibaba_statusMessage"
    obj_in_raw.id = "alibaba_id"

    obj_in_dict = {
        "status": "UPDATING",
        "type": "co.yellowdog.platform.model.AlibabaInstancesComputeSource",
        "assignPublicIp": True,
        "name": "alibaba_name",
        "limit": 5,
        "statusMessage": "alibaba_statusMessage",
        "id": "alibaba_id",
        "region": "alibaba_region",
        "credential": "alibaba_credential",
        "availabilityZone": "alibaba_availabilityZone",
        "securityGroupId": "alibaba_securityGroupId",
        "instanceType": "alibaba_instanceType",
        "imageId": "alibaba_imageId",
        "specifyMinimum": True,
        "keyName": "alibaba_keyName",
        "userData": "alibaba_userData",
        "instanceChargeType": "POST_PAID",
        "spotStrategy": "SPOT_AS_PRICE_GO",
        "ramRoleName": "alibaba_ramRoleName",
        "vSwitchId": "alibaba_vswitchId",
        "spotPriceLimit": 10.0
    }

    should_serde(obj_in_raw, obj_in_dict)
