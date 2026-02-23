from typing import List

from .keyring_service_proxy import KeyringServiceProxy
from .keyring_client import KeyringClient
from yellowdog_client.model import Credential
from yellowdog_client.model import KeyringSummary
from yellowdog_client.model import Keyring
from ..common import check


class KeyringClientImpl(KeyringClient):
    def __init__(self, service_proxy: KeyringServiceProxy) -> None:
        self.__service_proxy: KeyringServiceProxy = service_proxy

    def create_keyring(self, name: str, description: str) -> Keyring:
        keyring = self.__service_proxy.create_keyring(name, description).keyring
        assert keyring is not None
        return keyring

    def delete_keyring(self, keyring: Keyring) -> None:
        name = check.not_none(keyring.name, "keyring.name")
        self.delete_keyring_by_name(name)

    def delete_keyring_by_name(self, keyring_name: str) -> None:
        self.__service_proxy.delete_keyring(keyring_name)

    def find_all_keyrings(self) -> List[KeyringSummary]:
        return self.__service_proxy.find_all_keyrings()

    def put_credential(self, keyring: Keyring, credential: Credential) -> Keyring:
        name = check.not_none(keyring.name, "keyring.name")
        return self.put_credential_by_name(name, credential)

    def put_credential_by_name(self, keyring_name: str, credential: Credential) -> Keyring:
        return self.__service_proxy.put_credential(keyring_name, credential)

    def delete_credential(self, keyring: Keyring, credential_name: str) -> Keyring:
        name = check.not_none(keyring.name, "keyring.name")
        return self.delete_credential_by_name(name, credential_name)

    def delete_credential_by_name(self, keyring_name: str, credential_name: str) -> Keyring:
        return self.__service_proxy.delete_credential(keyring_name, credential_name)

    def close(self) -> None:
        # Has no closing resources
        pass
