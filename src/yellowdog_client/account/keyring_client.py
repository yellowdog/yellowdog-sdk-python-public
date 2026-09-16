from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from yellowdog_client.common import Closeable, SearchClient
from yellowdog_client.model import ApiKey, CreateKeyringResponse, Credential, Keyring, KeyringSearch, KeyringSummary, UpdateKeyringRequest


class KeyringClient(ABC, Closeable):

    @abstractmethod
    def create_keyring(self, name: str, description: str) -> Keyring:
        """
        .. deprecated:: (unknown)
        """

        pass

    @abstractmethod
    def add_keyring(self, name: str, description: str) -> CreateKeyringResponse:
        pass

    @abstractmethod
    def get_keyring(self, keyring_id: str) -> Keyring:
        pass

    @abstractmethod
    def update_keyring(self, keyring_id: str, request: UpdateKeyringRequest) -> Keyring:
        pass

    @abstractmethod
    def delete_keyring(self, keyring: Keyring) -> None:
        pass

    @abstractmethod
    def delete_keyring_by_name(self, keyring_name: str) -> None:
        pass

    @abstractmethod
    def find_all_keyrings(self) -> List[KeyringSummary]:
        """
        .. deprecated:: (unknown)
            use :meth:`get_keyrings(keyring_search)` instead to search keyrings.
        """

        pass

    @abstractmethod
    def get_keyrings(self, search: KeyringSearch) -> SearchClient[KeyringSummary]:
        pass

    @abstractmethod
    def grant_application_access_to_keyring(self, keyring_name: str, application_id: str, application_api_key: ApiKey) -> Keyring:
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
