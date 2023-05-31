from datetime import timedelta
from typing import TypeVar, List, Optional, Callable

from .worker_pool_helper import WorkerPoolHelper
from .worker_pool_service_proxy import WorkerPoolServiceProxy
from .worker_pool_client import WorkerPoolClient
from yellowdog_client.common.server_sent_events import SubscriptionManager, SubscriptionEventListener
from yellowdog_client.model import Identified, ProvisionedWorkerPool, ProvisionedWorkerPoolProperties, \
    ComputeRequirementTemplateUsage, WorkerPool, WorkerPoolSummary, NodeSearch, Node, \
    SliceReference, Slice, NodeActionQueueSnapshot, NodeActionGroup, NodeAction, NodeIdFilter, \
    WorkerPoolToken, AddConfiguredWorkerPoolRequest, AddConfiguredWorkerPoolResponse, ConfiguredWorkerPool
from yellowdog_client.common import SearchClient
from ..common.pagination import paginate

T = TypeVar('T', bound=WorkerPool)


class WorkerPoolClientImpl(WorkerPoolClient):
    def __init__(self, service_proxy: WorkerPoolServiceProxy) -> None:
        self.__service_proxy = service_proxy
        self.__requirement_subscriptions = SubscriptionManager(
            update_events_provider=self.__service_proxy.stream_worker_pool_updates,
            class_type=WorkerPool
        )

    @staticmethod
    def _check_has_id(identified: Optional[Identified]) -> None:
        if not identified:
            raise ValueError("Provided entity may not be None")

        if not identified.id:
            raise ValueError(
                "Provided %s has not yet been submitted to YellowDog Scheduler" % identified.__class__.__name__
            )

    def add_configured_worker_pool(self, request: AddConfiguredWorkerPoolRequest) -> AddConfiguredWorkerPoolResponse:
        return self.__service_proxy.add_configured_worker_pool(request)

    def refresh_configured_worker_pool_token(self, worker_pool: ConfiguredWorkerPool, token_ttl: Optional[timedelta] = None) -> WorkerPoolToken:
        return self.refresh_configured_worker_pool_token_by_id(worker_pool.id, token_ttl)

    def refresh_configured_worker_pool_token_by_id(self, worker_pool_id: str, token_ttl: Optional[timedelta] = None) -> WorkerPoolToken:
        return self.__service_proxy.refresh_configured_worker_pool_token(worker_pool_id, token_ttl)

    def regenerate_configured_worker_pool_token(self, worker_pool: ConfiguredWorkerPool, token_ttl: Optional[timedelta] = None) -> WorkerPoolToken:
        return self.regenerate_configured_worker_pool_token_by_id(worker_pool.id, token_ttl)

    def regenerate_configured_worker_pool_token_by_id(self, worker_pool_id: str, token_ttl: Optional[timedelta] = None) -> WorkerPoolToken:
        return self.__service_proxy.regenerate_configured_worker_pool_token(worker_pool_id, token_ttl)

    def get_configured_worker_pool_token(self, worker_pool: ConfiguredWorkerPool) -> WorkerPoolToken:
        return self.get_configured_worker_pool_token_by_id(worker_pool.id)

    def get_configured_worker_pool_token_by_id(self, worker_pool_id: str) -> WorkerPoolToken:
        return self.__service_proxy.get_configured_worker_pool_token_by_id(worker_pool_id)

    def provision_worker_pool(
            self,
            requirement_template_usage: ComputeRequirementTemplateUsage,
            provisioned_properties: Optional[ProvisionedWorkerPoolProperties] = None
    ) -> ProvisionedWorkerPool:
        return self.__service_proxy.provision_worker_pool(requirement_template_usage, provisioned_properties)

    def resize_worker_pool(self, worker_pool: ProvisionedWorkerPool, size: int) -> ProvisionedWorkerPool:
        return self.resize_worker_pool_by_id(worker_pool.id, size)

    def resize_worker_pool_by_id(self, worker_pool_id: str, size: int) -> ProvisionedWorkerPool:
        return self.__service_proxy.resize_worker_pool(worker_pool_id, size)

    def shutdown_worker_pool(self, worker_pool: WorkerPool) -> None:
        return self.shutdown_worker_pool_by_id(worker_pool.id)

    def shutdown_worker_pool_by_id(self, worker_pool_id: str) -> None:
        return self.__service_proxy.shutdown_worker_pool(worker_pool_id)

    def get_worker_pool(self, worker_pool: T) -> T:
        self._check_has_id(worker_pool)
        return self.get_worker_pool_by_id(worker_pool.id)

    def get_worker_pool_by_id(self, worker_pool_id: str) -> WorkerPool:
        return self.__service_proxy.get_worker_pool_by_id(worker_pool_id)

    def add_worker_pool_listener(self, worker_pool: WorkerPool, listener: SubscriptionEventListener[WorkerPool]) -> None:
        self._check_has_id(worker_pool)
        self.add_worker_pool_listener_by_id(worker_pool.id, listener)

    def add_worker_pool_listener_by_id(self, worker_pool_id: str, listener: SubscriptionEventListener[WorkerPool]) -> None:
        self.__requirement_subscriptions.add_listener(worker_pool_id, listener)

    def remove_worker_pool_listener(self, listener: SubscriptionEventListener[WorkerPool]) -> None:
        self.__requirement_subscriptions.remove_listener(listener)

    def get_worker_pool_helper(self, worker_pool: WorkerPool) -> WorkerPoolHelper:
        return WorkerPoolHelper(worker_pool, self)

    def get_worker_pool_helper_by_id(self, worker_pool_id: str) -> WorkerPoolHelper:
        worker_pool = self.get_worker_pool_by_id(worker_pool_id)
        return self.get_worker_pool_helper(worker_pool)

    def find_all_worker_pools(self) -> List[WorkerPoolSummary]:
        return self.__service_proxy.find_all_worker_pools()

    def find_nodes(self, search: NodeSearch) -> List[Node]:
        return paginate(lambda sr: self.find_nodes_slice(search, sr))

    def find_nodes_slice(self, search: NodeSearch, slice_reference: SliceReference) -> Slice[Node]:
        return self.__service_proxy.search_nodes(search, slice_reference)

    def get_node(self, node: Node) -> Node:
        return self.get_node_by_id(node.id)

    def get_node_by_id(self, node_id: str) -> Node:
        return self.__service_proxy.get_node_by_id(node_id)

    def shutdown_node(self, node: Node) -> Node:
        return self.shutdown_node_by_id(node.id)

    def shutdown_node_by_id(self, node_id: str) -> Node:
        return self.__service_proxy.shutdown_node(node_id)

    def add_node_actions_for_node(self, node: Node, *actions: NodeAction) -> None:
        self.add_node_actions_for_node_by_id(node.workerPoolId, node.id, *actions)

    def add_node_actions_for_node_by_id(self, worker_pool_id: str, node_id: str, *actions: NodeAction) -> None:
        for action in actions:
            action.nodeIdFilter = NodeIdFilter.LIST
            action.nodeTypes = None

        self.add_node_actions_grouped_by_id(worker_pool_id, [NodeActionGroup(list(actions))], [node_id])

    def add_node_actions(self, worker_pool: WorkerPool, *actions: NodeAction) -> None:
        self.add_node_actions_by_id(worker_pool.id, *actions)

    def add_node_actions_by_id(self, worker_pool_id: str, *actions: NodeAction) -> None:
        self.add_node_actions_grouped_by_id(worker_pool_id, [NodeActionGroup(list(actions))])

    def add_node_actions_grouped(self, worker_pool: WorkerPool, action_groups: Optional[List[NodeActionGroup]] = None, node_id_filter_list: Optional[List[str]] = None) -> None:
        self.add_node_actions_grouped_by_id(worker_pool.id, action_groups, node_id_filter_list)

    def add_node_actions_grouped_by_id(self, worker_pool_id: str, action_groups: Optional[List[NodeActionGroup]] = None, node_id_filter_list: Optional[List[str]] = None) -> None:
        self.__service_proxy.add_node_actions_grouped(worker_pool_id, action_groups, node_id_filter_list)

    def get_node_actions(self, node: Node) -> NodeActionQueueSnapshot:
        return self.get_node_actions_by_id(node.id)

    def get_node_actions_by_id(self, node_id: str) -> NodeActionQueueSnapshot:
        return self.__service_proxy.get_node_actions(node_id)

    def get_nodes(self, search: NodeSearch) -> SearchClient[Node]:
        get_next_slice_function: Callable[[SliceReference], Slice[Node]] = \
            lambda slice_reference: self.__service_proxy.search_nodes(search, slice_reference)

        return SearchClient(get_next_slice_function)

    def close(self) -> None:
        self.__requirement_subscriptions.close()
