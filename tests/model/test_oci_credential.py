from .test_utils import should_serde
from yellowdog_client.model import OciCredential


class TestOciCredential(object):

    def test_serialize(self):
        obj_in_raw = OciCredential(
            name="OciCredential_name",
            userId="OciCredential_userId",
            passphrase="OciCredential_passphrase",
            tenantId="OciCredential_tenantId",
            fingerprint="OciCredential_fingerprint",
            privateKey="MY TEST DATA"
        )

        obj_in_dict = {
            "type": "co.yellowdog.platform.account.credentials.OciCredential",
            "privateKey": "MY TEST DATA",
            "name": "OciCredential_name",
            "userId": "OciCredential_userId",
            "passphrase": "OciCredential_passphrase",
            "tenantId": "OciCredential_tenantId",
            "fingerprint": "OciCredential_fingerprint",
        }

        should_serde(obj_in_raw, obj_in_dict)
