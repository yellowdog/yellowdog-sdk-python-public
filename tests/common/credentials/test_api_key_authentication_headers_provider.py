from yellowdog_client.common.credentials import ApiKeyAuthenticationHeadersProvider
import pytest
from requests.auth import AuthBase
from yellowdog_client.common.credentials import RequestsApiKeyAuthentication


class TestBuildHeader(object):
    def test___no_key__expect_exception(self):
        provider = ApiKeyAuthenticationHeadersProvider()

        with pytest.raises(ValueError):
            provider.build_header()

    def test___with_key__expect_tuple_with_header_and_cred(self, mocker):
        build_mock = mocker.patch(
            "yellowdog_client.common.credentials.api_key_utils.ApiKeyUtils.build_api_key_auth_header_with_credentials"
        )
        build_mock.return_value = "mock_value"

        provider = ApiKeyAuthenticationHeadersProvider()
        provider.key = "some_key"

        res = provider.build_header()
        expected_res = ("Authorization", "mock_value")

        assert expected_res == res
        build_mock.assert_called_once_with("some_key")


class TestGetRequestsAuthenticationBase(object):
    def test___no_key__expect_exception(self):
        provider = ApiKeyAuthenticationHeadersProvider()

        with pytest.raises(ValueError):
            provider.get_requests_authentication_base()

    def test___with_key__expect_custom_auth_base(self):
        provider = ApiKeyAuthenticationHeadersProvider()
        provider.key = "some_key"

        res = provider.get_requests_authentication_base()
        assert type(res) == RequestsApiKeyAuthentication
        assert issubclass(type(res), AuthBase)
