from yellowdog_client.model import ApiKey
from .test_utils import should_serde


def test_serialize__api_key():
    obj_in_raw = ApiKey("foo", "bar")
    obj_in_dict = {'id': 'foo', 'secret': 'bar'}

    should_serde(obj_in_raw, obj_in_dict)
