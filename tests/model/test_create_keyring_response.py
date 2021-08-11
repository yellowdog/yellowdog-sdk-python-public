from yellowdog_client.model import CreateKeyringResponse
from yellowdog_client.model import Keyring
from .test_utils import should_serde


def test_serialize_empty__create_keyring_response():
    obj_in_raw = CreateKeyringResponse()

    obj_in_dict = {}

    should_serde(obj_in_raw, obj_in_dict)


def test_serialize__create_keyring_response():
    obj_in_raw = CreateKeyringResponse()
    obj_in_raw.keyring = Keyring()
    obj_in_raw.keyring.id = "keyring_id"
    obj_in_raw.keyring.name = "keyring_name"
    obj_in_raw.keyring.description = "keyring_description"
    obj_in_raw.keyringPassword = "my_password"

    obj_in_dict = {
        'keyring': {
            "id": "keyring_id",
            "name": "keyring_name",
            "description": "keyring_description"
        },
        'keyringPassword': 'my_password'
    }

    should_serde(obj_in_raw, obj_in_dict)
