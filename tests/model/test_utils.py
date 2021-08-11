import json
from typing import Generic

from yellowdog_client.model import Identified, Named, Tagged
from yellowdog_client.common.json import Json


def should_serde(expected_object: object, expected_dict: dict, deserialize_cls: type = None):
    # Python has builtin serde via the json module but it doesn't support custom objects so we need to use our own
    # custom serde.
    #
    # expected_object is an object of a custom type. expected_dict is a representation of that same object but
    # only using builtin types.
    #
    # To test serialization, we serialize expected_object using our own serializer and then deserialize the
    # resulting JSON back into a dict using Python's deserialization. This dict is then compared against expected_dict.
    # This is done to ensure that the order of the keys are not considered and the test is able to call out which keys
    # are different making it easier to understand where problems are for large objects.

    actual_string = Json.dumps(expected_object)
    assert json.loads(actual_string) == expected_dict

    should_deserialize(expected_object, expected_dict, deserialize_cls)


def should_deserialize(obj: object, expected_dict: dict, deserialize_cls: type = None):
    if deserialize_cls is None:
        deserialize_cls = type(obj)
        if deserialize_cls.__base__ not in (object, Identified, Named, Tagged, Generic):
            deserialize_cls = deserialize_cls.__base__

    actual_object = Json.load(expected_dict, deserialize_cls)
    assert actual_object == obj
