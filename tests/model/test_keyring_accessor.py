from .test_utils import should_serde

from yellowdog_client.model import KeyringAccessor


def test_serialize__keyring_accessor():
    obj_in_raw = KeyringAccessor()
    obj_in_raw.accessorId = "my_accessorId"
    obj_in_raw.accessorType = "my_accessorType"
    obj_in_raw.accessorName = "my_accessorName"

    obj_in_dict = {
        'accessorId': 'my_accessorId',
        'accessorType': 'my_accessorType',
        'accessorName': 'my_accessorName'
    }

    should_serde(obj_in_raw, obj_in_dict)
