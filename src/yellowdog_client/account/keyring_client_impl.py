from typing import List

from .keyring_service_proxy import KeyringServiceProxy
from .keyring_client import KeyringClient
from yellowdog_client.model import Credential
from yellowdog_client.model import KeyringSummary
from yellowdog_client.model import Keyring


class KeyringClientImpl(KeyringClient):
    def __init__(self, service_proxy: KeyringServiceProxy) -> None:
        self.__service_proxy: KeyringServiceProxy = service_proxy

    def create_keyring(self, name: str, description: str) -> Keyring:
        return self.__service_proxy.create_keyring(name, description).keyring

    def delete_keyring(self, keyring: Keyring) -> None:
        self.delete_keyring_by_name(keyring.name)

    def delete_keyring_by_name(self, keyring_name: str) -> None:
        self.__service_proxy.delete_keyring(keyring_name)

    def find_all_keyrings(self) -> List[KeyringSummary]:
        return self.__service_proxy.find_all_keyrings()

    def put_credential(self, keyring: Keyring, credential: Credential) -> Keyring:
        return self.put_credential_by_name(keyring.name, credential)

    def put_credential_by_name(self, keyring_name: str, credential: Credential) -> Keyring:
        return self.__service_proxy.put_credential(keyring_name, credential)

    def delete_credential(self, keyring: Keyring, credential_name: str) -> Keyring:
        return self.delete_credential_by_name(keyring.name, credential_name)

    def delete_credential_by_name(self, keyring_name: str, credential_name: str) -> Keyring:
        return self.__service_proxy.delete_credential(keyring_name, credential_name)

    def close(self):
        # Has no closing resources
        pass
