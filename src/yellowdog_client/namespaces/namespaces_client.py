from __future__ import annotations

from abc import ABC, abstractmethod

from yellowdog_client.common import Closeable, SearchClient
from yellowdog_client.model import CreateNamespaceRequest, Namespace, NamespacePolicy, NamespacePolicySearch, NamespaceSearch


class NamespacesClient(ABC, Closeable):
    """The API interface exposed by the YellowDog Namespaces Service"""

    @abstractmethod
    def get_namespace(self, namespace_id: str) -> Namespace:
        """
        Gets the namespace with a matching ID.

        :param namespace_id: the namespace ID
        :return: the namespace
        """

        pass

    @abstractmethod
    def get_namespaces(self, search: NamespaceSearch) -> SearchClient[Namespace]:
        """
        Returns a search client for namespaces that match the NamespaceSearch parameter.

        :param search: the search object to filter and sort results
        :return: a search client for matching namespaces
        """

        pass

    @abstractmethod
    def create_namespace(self, request: CreateNamespaceRequest) -> str:
        """
        Creates a namespace.

        :param request: the request containing the data to create the namespace
        :return: the namespace ID
        """

        pass

    @abstractmethod
    def delete_namespace(self, namespace_id: str) -> None:
        """
        Deletes a namespace.

        :param namespace_id: the ID of the namespace to delete
        """

        pass

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
