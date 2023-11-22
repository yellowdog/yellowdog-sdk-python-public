from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from yellowdog_client.common import Closeable
from yellowdog_client.model import Credential, Keyring, KeyringSummary


class KeyringClient(ABC, Closeable):

    @abstractmethod
    def create_keyring(self, name: str, description: str) -> Keyring:
        pass

    @abstractmethod
    def delete_keyring(self, keyring: Keyring) -> None:
        pass

    @abstractmethod
    def delete_keyring_by_name(self, keyring_name: str) -> None:
        pass

    @abstractmethod
    def find_all_keyrings(self) -> List[KeyringSummary]:
        pass

    @abstractmethod
    def put_credential(self, keyring: Keyring, credential: Credential) -> Keyring:
        pass

    @abstractmethod
    def put_credential_by_name(self, keyring_name: str, credential: Credential) -> Keyring:
        pass

    @abstractmethod
    def delete_credential(self, keyring: Keyring, credential_name: str) -> Keyring:
        pass

    @abstractmethod
    def delete_credential_by_name(self, keyring_name: str, credential_name: str) -> Keyring:
        pass
