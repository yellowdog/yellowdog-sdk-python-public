from mock import MagicMock
from yellowdog_client.common.credentials import RequestsApiKeyAuthentication
from pytest_dictsdiff import check_objects as assert_dict


class TestRequestsApiKeyAuthentication(object):
    def test__called__expect_request_updated_with_headers(self, mocker):
        build_dict = mocker.patch(
            "yellowdog_client.common.credentials.api_key_utils.ApiKeyUtils.build_api_key_auth_dict_with_credentials"
        )
        build_dict.return_value = {"return_key": "return_value"}
        auth_base = RequestsApiKeyAuthentication(key="custom_key")

        r = MagicMock()
        r.headers = {}

        auth_base.__call__(r)

        assert assert_dict({"return_key": "return_value"}, r.headers)
        build_dict.assert_called_once_with(api_key_credential="custom_key")
