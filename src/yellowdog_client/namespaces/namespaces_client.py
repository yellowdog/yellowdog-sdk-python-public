from __future__ import annotations

from abc import ABC, abstractmethod

from yellowdog_client.common import Closeable, SearchClient
from yellowdog_client.model import NamespacePolicy, NamespacePolicySearch


class NamespacesClient(ABC, Closeable):
    """The API interface exposed by the YellowDog Namespaces Service"""

    @abstractmethod
    def save_namespace_policy(self, namespace_policy: NamespacePolicy) -> None:
        """
        Submits a namespace policy to either save or update.

        :param namespace_policy: the namespace policy to submit
        """

        pass

    @abstractmethod
    def get_namespace_policy(self, namespace: str) -> NamespacePolicy:
        """
        Requests the namespace policy for the specified namespace.

        :param namespace: the namespace
        :return: the namespace policy
        """

        pass

    @abstractmethod
    def delete_namespace_policy(self, namespace: str) -> None:
        """
        Deletes the namespace policy for the specified namespace if it exists.

        :param namespace: the namespace
        """

        pass

    @abstractmethod
    def get_namespace_policies(self, search: NamespacePolicySearch) -> SearchClient[NamespacePolicy]:
        """
        Returns a search client for searching namespace policies.

        :param search: the search criteria
        :return: a search client for searching namespace policies
        """

        pass
