from typing import List, Optional
from datetime import timedelta

from yellowdog_client.common.server_sent_events.sse4python import EventSource
from yellowdog_client.common import Proxy
from yellowdog_client.model import ProvisionedWorkerPool, ComputeRequirementTemplateUsage, \
    ProvisionedWorkerPoolProperties, WorkerPool, NodeSearch, Node, Slice, \
    SliceReference, WorkerPoolSummary, NodeActionGroup, NodeActionQueueSnapshot, AddNodeActionsRequest, \
    AddConfiguredWorkerPoolRequest, AddConfiguredWorkerPoolResponse, WorkerPoolToken


class WorkerPoolServiceProxy:
    def __init__(self, proxy: Proxy) -> None:
        self._proxy: Proxy = proxy.append_base_url("/workerPools/")

    def add_configured_worker_pool(self, request: AddConfiguredWorkerPoolRequest) -> AddConfiguredWorkerPoolResponse:
        return self._proxy.post(AddConfiguredWorkerPoolResponse, request, "configured")

    def refresh_configured_worker_pool_token(self, worker_pool_id: str, token_ttl: Optional[timedelta] = None) -> WorkerPoolToken:
        return self._proxy.post(WorkerPoolToken, token_ttl, "configured/%s/token/refresh" % worker_pool_id)

    def regenerate_configured_worker_pool_token(self, worker_pool_id: str, token_ttl: Optional[timedelta] = None) -> WorkerPoolToken:
        return self._proxy.post(WorkerPoolToken, token_ttl, "configured/%s/token/regenerate" % worker_pool_id)

    def get_configured_worker_pool_token_by_id(self, worker_pool_id: str) -> WorkerPoolToken:
        return self._proxy.get(WorkerPoolToken, "configured/%s/token" % worker_pool_id)

    def provision_worker_pool(
            self,
            template_usage: ComputeRequirementTemplateUsage,
            worker_pool_properties: ProvisionedWorkerPoolProperties
    ) -> ProvisionedWorkerPool:
        data = {
            "requirementTemplateUsage": template_usage,
            "provisionedProperties": worker_pool_properties
        }
        return self._proxy.post(ProvisionedWorkerPool, data, "provisioned/template")

    def resize_worker_pool(self, worker_pool_id: str, size: int) -> ProvisionedWorkerPool:
        return self._proxy.put(ProvisionedWorkerPool, url=f"provisioned/{worker_pool_id}?size={size}")

    def get_worker_pool_by_id(self, worker_pool_id: str) -> WorkerPool:
        return self._proxy.get(WorkerPool, worker_pool_id)

    def stream_worker_pool_updates(self, worker_pool_id: str) -> EventSource:
        return self._proxy.stream("%s/updates" % worker_pool_id)

    def search_nodes(self, search: NodeSearch, slice_reference: SliceReference) -> Slice[Node]:
        return self._proxy.get(Slice[Node], "nodes", self._proxy.to_params(search, slice_reference))

    def find_all_worker_pools(self):
        return self._proxy.get(List[WorkerPoolSummary])

    def shutdown_worker_pool(self, worker_pool_id: str) -> None:
        self._proxy.delete(worker_pool_id)

    def get_node_by_id(self, node_id: str) -> Node:
        return self._proxy.get(Node, "nodes/%s" % node_id)

    def shutdown_node(self, node_id: str) -> Node:
        return self._proxy.delete("nodes/%s" % node_id, Node)

    def add_node_actions_grouped(self, worker_pool_id: str, action_groups: List[NodeActionGroup], node_id_filter_list: Optional[List[str]] = None) -> None:
        return self._proxy.post(data=AddNodeActionsRequest(action_groups, node_id_filter_list), url="%s/actions" % worker_pool_id)

    def get_node_actions(self, node_id: str) -> NodeActionQueueSnapshot:
        return self._proxy.get(NodeActionQueueSnapshot, "nodes/%s/actions" % node_id)
