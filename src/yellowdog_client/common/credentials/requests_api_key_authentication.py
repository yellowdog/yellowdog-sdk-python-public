from requests.auth import AuthBase

from .api_key_utils import ApiKeyUtils


class RequestsApiKeyAuthentication(AuthBase):
    def __init__(self, key):
        self.__key = key

    def __call__(self, r):
        api_key_auth_headers = ApiKeyUtils.build_api_key_auth_dict_with_credentials(api_key_credential=self.__key)
        r.headers.update(api_key_auth_headers)
        return r
