from .api_key_constants import ApiKeyConstants
from yellowdog_client.model import ApiKey


class ApiKeyUtils(object):
    @staticmethod
    def build_api_key_auth_header(key_id, key_secret):
        # type: (str, str) -> str
        return "%s %s%s%s" % (
            ApiKeyConstants.AUTH_HEADER_API_KEY_TYPE,
            key_id,
            ApiKeyConstants.AUTH_HEADER_API_KEY_FIELD_SEPARATOR,
            key_secret
        )

    @staticmethod
    def build_api_key_auth_header_with_credentials(api_key_credential):
        # type: (ApiKey) -> str
        return ApiKeyUtils.build_api_key_auth_header(api_key_credential.id, api_key_credential.secret)

    @staticmethod
    def build_api_key_auth_dict(key_id, key_secret):
        # type: (str, str) -> {str: str}
        auth_header = ApiKeyUtils.build_api_key_auth_header(key_id=key_id, key_secret=key_secret)
        return {ApiKeyConstants.AUTH_HEADER: auth_header}

    @staticmethod
    def build_api_key_auth_dict_with_credentials(api_key_credential):
        # type: (ApiKey) -> {str: str}
        return ApiKeyUtils.build_api_key_auth_dict(api_key_credential.id, api_key_credential.secret)
