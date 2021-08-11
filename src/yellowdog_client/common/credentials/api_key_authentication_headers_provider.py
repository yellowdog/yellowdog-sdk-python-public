from typing import Optional, Tuple

from requests.auth import AuthBase

from .api_key_constants import ApiKeyConstants
from .api_key_utils import ApiKeyUtils
from yellowdog_client.model import ApiKey
from .requests_api_key_authentication import RequestsApiKeyAuthentication


class ApiKeyAuthenticationHeadersProvider(object):
    def __init__(self):
        self.key = None     # type: Optional[ApiKey]

    def build_header(self):
        # type: () -> Tuple[str, str]
        if not self.key:
            raise ValueError("Please set API KEY")
        return ApiKeyConstants.AUTH_HEADER, ApiKeyUtils.build_api_key_auth_header_with_credentials(self.key)

    def get_requests_authentication_base(self):
        # type: () -> AuthBase
        if not self.key:
            raise ValueError("Please set API KEY")
        return RequestsApiKeyAuthentication(self.key)
