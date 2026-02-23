from datetime import timedelta
from typing import TypeVar, List, Optional, Callable, cast

from yellowdog_client.common import SearchClient, check
from yellowdog_client.common.server_sent_events import SubscriptionManager, SubscriptionEventListener
from yellowdog_client.model import ProvisionedWorkerPool, ProvisionedWorkerPoolProperties, \
    ComputeRequirementTemplateUsage, WorkerPool, WorkerPoolSummary, NodeSearch, Node, \
    SliceReference, Slice, NodeActionQueueSnapshot, NodeActionGroup, NodeAction, NodeIdFilter, \
    WorkerPoolToken, AddConfiguredWorkerPoolRequest, AddConfiguredWorkerPoolResponse, \
    ConfiguredWorkerPool, WorkerPoolSearch
from .worker_pool_client import WorkerPoolClient
from .worker_pool_helper import WorkerPoolHelper
from .worker_pool_service_proxy import WorkerPoolServiceProxy
from ..common.pagination import paginate

T = TypeVar('T', bound=WorkerPool)


class WorkerPoolClientImpl(WorkerPoolClient):
    def __init__(self, service_proxy: WorkerPoolServiceProxy) -> None:
        self.__service_proxy = service_proxy
        self.__requirement_subscriptions = SubscriptionManager(
            update_events_provider=self.__service_proxy.stream_worker_pool_updates,
            class_type=WorkerPool
        )

    def add_configured_worker_pool(self, request: AddConfiguredWorkerPoolRequest) -> AddConfiguredWorkerPoolResponse:
        return self.__service_proxy.add_configured_worker_pool(request)

    def refresh_configured_worker_pool_token(self, worker_pool: ConfiguredWorkerPool, token_ttl: Optional[timedelta] = None) -> WorkerPoolToken:
        id_ = check.not_none(worker_pool.id, "worker_pool.id")
        return self.refresh_configured_worker_pool_token_by_id(id_, token_ttl)

    def refresh_configured_worker_pool_token_by_id(self, worker_pool_id: str, token_ttl: Optional[timedelta] = None) -> WorkerPoolToken:
        return self.__service_proxy.refresh_configured_worker_pool_token(worker_pool_id, token_ttl)

    def regenerate_configured_worker_pool_token(self, worker_pool: ConfiguredWorkerPool, token_ttl: Optional[timedelta] = None) -> WorkerPoolToken:
        id_ = check.not_none(worker_pool.id, "worker_pool.id")
        return self.regenerate_configured_worker_pool_token_by_id(id_, token_ttl)

    def regenerate_configured_worker_pool_token_by_id(self, worker_pool_id: str, token_ttl: Optional[timedelta] = None) -> WorkerPoolToken:
        return self.__service_proxy.regenerate_configured_worker_pool_token(worker_pool_id, token_ttl)

    def get_configured_worker_pool_token(self, worker_pool: ConfiguredWorkerPool) -> WorkerPoolToken:
        id_ = check.not_none(worker_pool.id, "worker_pool.id")
        return self.get_configured_worker_pool_token_by_id(id_)

    def get_configured_worker_pool_token_by_id(self, worker_pool_id: str) -> WorkerPoolToken:
        return self.__service_proxy.get_configured_worker_pool_token_by_id(worker_pool_id)

    def provision_worker_pool(
            self,
            requirement_template_usage: ComputeRequirementTemplateUsage,
            provisioned_properties: Optional[ProvisionedWorkerPoolProperties] = None
    ) -> ProvisionedWorkerPool:
        return self.__service_proxy.provision_worker_pool(requirement_template_usage, provisioned_properties)

    def resize_worker_pool(self, worker_pool: ProvisionedWorkerPool, size: int) -> ProvisionedWorkerPool:
        id_ = check.not_none(worker_pool.id, "worker_pool.id")
        return self.resize_worker_pool_by_id(id_, size)

    def resize_worker_pool_by_id(self, worker_pool_id: str, size: int) -> ProvisionedWorkerPool:
        return self.__service_proxy.resize_worker_pool(worker_pool_id, size)

    def shutdown_worker_pool(self, worker_pool: WorkerPool) -> None:
        id_ = check.not_none(worker_pool.id, "worker_pool.id")
        return self.shutdown_worker_pool_by_id(id_)

    def shutdown_worker_pool_by_id(self, worker_pool_id: str) -> None:
        return self.__service_proxy.shutdown_worker_pool(worker_pool_id)

    # noinspection PyUnnecessaryCast. Suppressed because mypy correctly requires a cast is needed but Pycharm does not.
    def get_worker_pool(self, worker_pool: T) -> T:
        id_ = check.not_none(worker_pool.id, "worker_pool.id")
        return cast(T, self.get_worker_pool_by_id(id_))

    def get_worker_pool_by_id(self, worker_pool_id: str) -> WorkerPool:
        return self.__service_proxy.get_worker_pool_by_id(worker_pool_id)

    def get_worker_pool_by_name(self, namespace: str, name: str) -> WorkerPool:
        return self.__service_proxy.get_worker_pool_by_name(namespace, name)

    def add_worker_pool_listener(self, worker_pool: WorkerPool, listener: SubscriptionEventListener[WorkerPool]) -> None:
        id_ = check.not_none(worker_pool.id, "worker_pool.id")
        self.add_worker_pool_listener_by_id(id_, listener)

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
        search = WorkerPoolSearch()
        return paginate(lambda sr: self._get_worker_pools_slice(search, sr))

    def get_worker_pools(self, search: WorkerPoolSearch) -> SearchClient[WorkerPoolSummary]:
        get_next_slice_function = lambda slice_reference: self._get_worker_pools_slice(search, slice_reference)
        return SearchClient(get_next_slice_function)

    def _get_worker_pools_slice(self, search: WorkerPoolSearch, slice_reference: SliceReference) -> Slice[WorkerPoolSummary]:
        return self.__service_proxy.find_worker_pools(search, slice_reference)

    def find_nodes(self, search: NodeSearch) -> List[Node]:
        return paginate(lambda sr: self.find_nodes_slice(search, sr))

    def find_nodes_slice(self, search: NodeSearch, slice_reference: SliceReference) -> Slice[Node]:
        return self.__service_proxy.search_nodes(search, slice_reference)

    def get_node(self, node: Node) -> Node:
        id_ = check.not_none(node.id, "node.id")
        return self.get_node_by_id(id_)

    def get_node_by_id(self, node_id: str) -> Node:
        return self.__service_proxy.get_node_by_id(node_id)

    def get_node_by_worker_id(self, worker_id: str) -> Node:
        return self.__service_proxy.get_node_by_worker_id(worker_id)

    def shutdown_node(self, node: Node) -> Node:
        if node.id is None:
            raise ValueError("node.id must not be None")
        return self.shutdown_node_by_id(node.id)

    def shutdown_node_by_id(self, node_id: str) -> Node:
        return self.__service_proxy.shutdown_node(node_id)

    def add_node_actions_for_node(self, node: Node, *actions: NodeAction) -> None:
        if node.id is None:
            raise ValueError("node.id must not be None")
        assert node.workerPoolId is not None
        self.add_node_actions_for_node_by_id(node.workerPoolId, node.id, *actions)

    def add_node_actions_for_node_by_id(self, worker_pool_id: str, node_id: str, *actions: NodeAction) -> None:
        for action in actions:
            action.nodeIdFilter = NodeIdFilter.LIST
            action.nodeTypes = None

        self.add_node_actions_grouped_by_id(worker_pool_id, [NodeActionGroup(list(actions))], [node_id])

    def add_node_actions(self, worker_pool: WorkerPool, *actions: NodeAction) -> None:
        id_ = check.not_none(worker_pool.id, "worker_pool.id")
        self.add_node_actions_by_id(id_, *actions)

    def add_node_actions_by_id(self, worker_pool_id: str, *actions: NodeAction) -> None:
        self.add_node_actions_grouped_by_id(worker_pool_id, [NodeActionGroup(list(actions))])

    def add_node_actions_grouped(self, worker_pool: WorkerPool, action_groups: Optional[List[NodeActionGroup]] = None, node_id_filter_list: Optional[List[str]] = None) -> None:
        id_ = check.not_none(worker_pool.id, "worker_pool.id")
        self.add_node_actions_grouped_by_id(id_, action_groups, node_id_filter_list)

    def add_node_actions_grouped_by_id(self, worker_pool_id: str, action_groups: Optional[List[NodeActionGroup]] = None, node_id_filter_list: Optional[List[str]] = None) -> None:
        if action_groups is None:
            raise ValueError("action_groups must not be None")

        self.__service_proxy.add_node_actions_grouped(worker_pool_id, action_groups, node_id_filter_list)

    def get_node_actions(self, node: Node) -> NodeActionQueueSnapshot:
        _id = check.not_none(node.id, "node.id")
        return self.get_node_actions_by_id(_id)

    def get_node_actions_by_id(self, node_id: str) -> NodeActionQueueSnapshot:
        return self.__service_proxy.get_node_actions(node_id)

    def get_nodes(self, search: NodeSearch) -> SearchClient[Node]:
        get_next_slice_function: Callable[[SliceReference], Slice[Node]] = \
            lambda slice_reference: self.__service_proxy.search_nodes(search, slice_reference)

        return SearchClient(get_next_slice_function)

    def close(self) -> None:
        self.__requirement_subscriptions.close()
