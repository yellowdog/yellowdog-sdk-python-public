from .test_utils import should_serde
from yellowdog_client.model import AlibabaCredential


class TestAlibabaCredential(object):

    def test_serialize_populated(self):
        obj_in_raw = AlibabaCredential(
            name="AlibabaCredential_name",
            accessKeyId="AlibabaCredential_accessKeyId",
            secretAccessKey="AlibabaCredential_secretAccessKey"
        )

        obj_in_dict = {
            "type": "co.yellowdog.platform.account.credentials.AlibabaCredential",
            "name": "AlibabaCredential_name",
            "accessKeyId": "AlibabaCredential_accessKeyId",
            "secretAccessKey": "AlibabaCredential_secretAccessKey"
        }
        should_serde(obj_in_raw, obj_in_dict)
