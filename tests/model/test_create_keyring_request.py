from yellowdog_client.model import CreateKeyringRequest
from .test_utils import should_serde


def test_serialize__create_keyring_request():
    obj_in_raw = CreateKeyringRequest(
        name="my_name",
        description="my_description",
        creatorSecret="my_creatorSecret",
    )

    obj_in_dict = {
        'name': 'my_name',
        'description': 'my_description',
        'creatorSecret': 'my_creatorSecret'
    }

    should_serde(obj_in_raw, obj_in_dict)
