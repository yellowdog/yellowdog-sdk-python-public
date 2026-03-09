from typing import List

from yellowdog_client.common import Proxy
from yellowdog_client.model import KeyringSummary
from yellowdog_client.model import Keyring
from yellowdog_client.model import CreateKeyringRequest
from yellowdog_client.model import CreateKeyringResponse
from yellowdog_client.model import Credential
from yellowdog_client.model import GrantApplicationAccessRequest
from yellowdog_client.model import ApiKey


class KeyringServiceProxy:
    def __init__(self, proxy: Proxy) -> None:
        self._proxy: Proxy = proxy.append_base_url("/keyrings/")

    def find_all_keyrings(self) -> List[KeyringSummary]:
        return self._proxy.get(List[KeyringSummary])

    def create_keyring(self, name: str, description: str) -> CreateKeyringResponse:
        return self._proxy.post(CreateKeyringResponse, CreateKeyringRequest(
            name=name,
            description=description
        ))

    def delete_keyring(self, keyring_name: str) -> None:
        self._proxy.delete(keyring_name)

    def grant_application_access_to_keyring(self, keyring_name: str, application_id: str, application_api_key: ApiKey) -> Keyring:
        request = GrantApplicationAccessRequest(applicationApiKey=application_api_key)
        return self._proxy.put(Keyring, request, "%s/access/applications/%s" % (keyring_name, application_id))

    def put_credential(self, keyring_name: str, credential: Credential) -> Keyring:
        return self._proxy.put(Keyring, credential, "%s/credentials" % keyring_name)

    def delete_credential(self, keyring_name: str, credential_name: str) -> Keyring:
        return self._proxy.delete("%s/credentials/%s" % (keyring_name, credential_name), Keyring)
