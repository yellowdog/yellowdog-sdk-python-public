from yellowdog_client.model import Keyring
from yellowdog_client.model import KeyringCredential
from yellowdog_client.model import KeyringAccessor
from .test_utils import should_serde


def test_serialize__keyring():
    cr1 = KeyringCredential()
    cr1.name = "cr1_name"
    cr1.description = "cr1_description"
    cr1.type = "cr1_type"

    cr2 = KeyringCredential()
    cr2.name = "cr2_name"
    cr2.description = "cr2_description"
    cr2.type = "cr2_type"

    cr3 = KeyringCredential()
    cr3.name = "cr3_name"
    cr3.description = "cr3_description"
    cr3.type = "cr3_type"

    acc1 = KeyringAccessor()
    acc1.accessorId = "acc1_accessorId"
    acc1.accessorType = "cr1_accessorType"
    acc1.accessorName = "cr1_accessorName"

    acc2 = KeyringAccessor()
    acc2.accessorId = "acc2_accessorId"
    acc2.accessorType = "cr2_accessorType"
    acc2.accessorName = "cr2_accessorName"

    acc3 = KeyringAccessor()
    acc3.accessorId = "acc3_accessorId"
    acc3.accessorType = "cr3_accessorType"
    acc3.accessorName = "cr3_accessorName"

    obj_in_raw = Keyring()
    obj_in_raw.id = "my_id"
    obj_in_raw.name = "my_name"
    obj_in_raw.description = "my_description"
    obj_in_raw.credentials = [cr1, cr2, cr3]
    obj_in_raw.accessors = [acc1, acc2, acc3]

    obj_in_dict = {
        'id': 'my_id',
        'name': 'my_name',
        'description': 'my_description',
        'credentials': [
            {
                'name': 'cr1_name',
                'description': 'cr1_description',
                'type': 'cr1_type'
            },
            {
                'name': 'cr2_name',
                'description': 'cr2_description',
                'type': 'cr2_type'
            },
            {
                'name': 'cr3_name',
                'description': 'cr3_description',
                'type': 'cr3_type'
            }
        ],
        'accessors': [
            {
                'accessorId': 'acc1_accessorId',
                'accessorType': 'cr1_accessorType',
                'accessorName': 'cr1_accessorName'
            },
            {
                'accessorId': 'acc2_accessorId',
                'accessorType': 'cr2_accessorType',
                'accessorName': 'cr2_accessorName'
            },
            {
                'accessorId': 'acc3_accessorId',
                'accessorType': 'cr3_accessorType',
                'accessorName': 'cr3_accessorName'
            }
        ]
    }
    should_serde(obj_in_raw, obj_in_dict)
