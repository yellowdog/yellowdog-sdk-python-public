from .test_utils import should_serde
from yellowdog_client.model import AwsCredential


def test_serialize__aws_credential():
    obj_in_raw = AwsCredential(
        name="AwsCredential_name",
        accessKeyId="AwsCredential_accessKeyId",
        secretAccessKey="AwsCredential_secretAccessKey"
    )

    obj_in_dict = {
        "type": "co.yellowdog.platform.account.credentials.AwsCredential",
        "name": "AwsCredential_name",
        "accessKeyId": "AwsCredential_accessKeyId",
        "secretAccessKey": "AwsCredential_secretAccessKey"
    }

    should_serde(obj_in_raw, obj_in_dict)
