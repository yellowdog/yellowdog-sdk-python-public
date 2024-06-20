from yellowdog_client.common import Proxy, SearchClient
from yellowdog_client.model import NamespacePolicy, NamespacePolicySearch, Node, SliceReference


class NamespacesServiceProxy:
    def __init__(self, proxy: Proxy) -> None:
        self._proxy: Proxy = proxy.append_base_url("/namespaces/")

    def save_namespace_policy(self, namespace_policy: NamespacePolicy) -> None:
        return self._proxy.put(url=f"{namespace_policy.namespace}/policy", data=namespace_policy)

    def get_namespace_policy(self, namespace: str) -> NamespacePolicy:
        return self._proxy.get(f"{namespace}/policy")

    def delete_namespace_policy(self, namespace: str) -> None:
        self._proxy.delete(f"{namespace}/policy")

    def get_namespace_policies(self, search: NamespacePolicySearch,  slice_reference: SliceReference) -> SearchClient[NamespacePolicy]:
        return self._proxy.get(NamespacePolicy[Node], "policies", self._proxy.to_params(search, slice_reference))
