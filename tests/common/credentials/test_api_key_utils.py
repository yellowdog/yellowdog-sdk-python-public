from pytest_dictsdiff import check_objects as assert_dict

from yellowdog_client.common.credentials import ApiKeyUtils
from yellowdog_client.model import ApiKey


class TestBuildApiKeyAuthHeader(object):
    def test__composed_with_arguments_and_constants(self):
        expected_res = "yd-key aaa:bbb"
        res = ApiKeyUtils.build_api_key_auth_header(key_id="aaa", key_secret="bbb")

        assert expected_res == res


class TestBuildApiKeyAuthHeaderWithCredentials(object):
    def test__with_credentials__composed_from_api_key_and_constants(self):
        key = ApiKey("ccc", "ddd")

        expected_res = "yd-key ccc:ddd"
        res = ApiKeyUtils.build_api_key_auth_header_with_credentials(api_key_credential=key)

        assert expected_res == res


class TestBuildApiKeyAuthDict(object):
    def test__expected_return_dict_with_arguments_and_constant(self):
        expected_res = {"Authorization": "yd-key eee:fff"}
        res = ApiKeyUtils.build_api_key_auth_dict(key_id="eee", key_secret="fff")

        assert assert_dict(expected_res, res)


class TestBuildApiKeyAuthDictWithCredentials(object):
    def test__expected_return_dict_composed_from_api_key_and_constants(self):
        key = ApiKey("ggg", "hhh")

        expected_res = {"Authorization": "yd-key ggg:hhh"}
        res = ApiKeyUtils.build_api_key_auth_dict_with_credentials(api_key_credential=key)

        assert assert_dict(expected_res, res)
