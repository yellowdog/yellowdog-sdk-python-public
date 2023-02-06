from typing import Dict

from requests.auth import AuthBase

from yellowdog_client.model import ApiKey

_AUTH_HEADER = "Authorization"
_AUTH_HEADER_API_KEY_TYPE = "yd-key"
_AUTH_HEADER_API_KEY_FIELD_SEPARATOR = ":"


class ApiKeyAuthenticationHeadersProvider(AuthBase):
    def __init__(self, key: ApiKey):
        if key is None:
            raise ValueError("ApiKey must not be None")
        self.__key = key

    def __call__(self, r):
        api_key_auth_headers = self._build_header()
        r.headers.update(api_key_auth_headers)
        return r

    def _build_header(self, ) -> Dict[str, str]:
        auth_header = "%s %s%s%s" % (
            _AUTH_HEADER_API_KEY_TYPE,
            self.__key.id,
            _AUTH_HEADER_API_KEY_FIELD_SEPARATOR,
            self.__key.secret
        )
        return {_AUTH_HEADER: auth_header}
