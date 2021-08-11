from .test_utils import should_serde
from yellowdog_client.model import GoogleCloudCredential


class TestGoogleCloudCredential(object):

    def test_serialize__google_cloud_credential(self):
        obj_in_raw = GoogleCloudCredential("GoogleCloudCredential_name", "MY TEST DATA")

        obj_in_dict = {
            "name": "GoogleCloudCredential_name",
            "type": "co.yellowdog.platform.account.credentials.GoogleCloudCredential",
            "serviceAccountKeyJson": "MY TEST DATA"
        }

        should_serde(obj_in_raw, obj_in_dict)
