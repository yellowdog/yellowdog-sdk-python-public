from .test_utils import should_serde
from yellowdog_client.model import KeyringCredential


def test_serialize__keyring_credential():
    obj_in_raw = KeyringCredential()
    obj_in_raw.name = "my_name"
    obj_in_raw.description = "my_description"
    obj_in_raw.type = "my_type"

    obj_in_dict = {
        'name': 'my_name',
        'description': 'my_description',
        'type': 'my_type'
    }

    should_serde(obj_in_raw, obj_in_dict)
