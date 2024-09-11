from typing import Callable

from .namespaces_client import NamespacesClient
from .namespaces_service_proxy import NamespacesServiceProxy
from yellowdog_client.common import SearchClient
from yellowdog_client.model import NamespacePolicy, NamespacePolicySearch, Slice, SliceReference


class NamespacesClientImpl(NamespacesClient):
    def __init__(self, service_proxy: NamespacesServiceProxy) -> None:
        self.__service_proxy = service_proxy

    def save_namespace_policy(self, namespace_policy: NamespacePolicy) -> None:
        self.__service_proxy.save_namespace_policy(namespace_policy)

    def get_namespace_policy(self, namespace: str) -> NamespacePolicy:
        return self.__service_proxy.get_namespace_policy(namespace)

    def delete_namespace_policy(self, namespace: str) -> None:
        self.__service_proxy.delete_namespace_policy(namespace)

    def get_namespace_policies(self, search: NamespacePolicySearch) -> SearchClient[NamespacePolicy]:
        get_next_slice_function: Callable[[SliceReference], Slice[NamespacePolicy]] = \
            lambda slice_reference: self.__service_proxy.get_namespace_policies(search, slice_reference)

        return SearchClient(get_next_slice_function)

    def close(self) -> None:
        pass
