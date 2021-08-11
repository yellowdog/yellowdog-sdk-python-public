from typing import TypeVar, List, Optional

from .worker_pool_helper import WorkerPoolHelper
from .worker_pool_service_proxy import WorkerPoolServiceProxy
from .worker_pool_client import WorkerPoolClient
from yellowdog_client.common.server_sent_events import SubscriptionManager, SubscriptionEventListener
from yellowdog_client.model import Identified, ProvisionedWorkerPool, ProvisionedWorkerPoolProperties, \
    ComputeRequirementTemplateUsage, WorkerPool, WorkerPoolSummary, NodeSearch, Node, \
    SliceReference, Slice, NodeActionQueueSnapshot, NodeActionGroup, NodeAction, NodeIdFilter

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

    def provision_worker_pool(
            self,
            requirement_template_usage: ComputeRequirementTemplateUsage,
            provisioned_properties: Optional[ProvisionedWorkerPoolProperties] = None
    ) -> ProvisionedWorkerPool:
        return self.__service_proxy.provision_worker_pool(requirement_template_usage, provisioned_properties)

    def get_worker_pool(self, worker_pool: T) -> T:
        self._check_has_id(worker_pool)
        return self.get_worker_pool_by_id(worker_pool.id)

    def get_worker_pool_by_id(self, worker_pool_id: str) -> WorkerPool:
        return self.__service_proxy.get_worker_pool_by_id(worker_pool_id)

    def add_worker_pool_listener(self, worker_pool: WorkerPool, listener: SubscriptionEventListener[WorkerPool]) -> None:
        self._check_has_id(worker_pool)
        self.__requirement_subscriptions.add_listener(worker_pool, listener)

    def remove_worker_pool_listener(self, listener: SubscriptionEventListener[WorkerPool]) -> None:
        self.__requirement_subscriptions.remove_listener(listener)

    def get_worker_pool_helper(self, worker_pool: WorkerPool) -> WorkerPoolHelper:
        return WorkerPoolHelper(worker_pool, self)

    def find_all_worker_pools(self) -> List[WorkerPoolSummary]:
        return self.__service_proxy.find_all_worker_pools()

    def shutdown_worker_pool(self, worker_pool_id: str) -> None:
        self.__service_proxy.shutdown_worker_pool(worker_pool_id)

    def find_nodes(self, search: NodeSearch) -> List[Node]:
        slice = self.find_nodes_slice(search, SliceReference())
        items = slice.items

        while slice.nextSliceId is not None:
            slice = self.find_nodes_slice(search, SliceReference(slice.nextSliceId))
            items += slice.items

        return items

    def find_nodes_slice(self, search: NodeSearch, slice_reference: SliceReference) -> Slice[Node]:
        return self.__service_proxy.find_nodes_slice(search, slice_reference)

    def get_node_by_id(self, node_id: str) -> Node:
        return self.__service_proxy.get_node_by_id(node_id)

    def add_node_actions_for_node(self, worker_pool_id: str, node_id: str, *actions: NodeAction) -> None:
        for action in actions:
            action.nodeIdFilter = NodeIdFilter.LIST
            action.nodeTypes = None

        self.add_node_actions_grouped(
            worker_pool_id,
            [NodeActionGroup(list(actions))],
            [node_id]
        )

    def add_node_actions(self, worker_pool_id: str, *actions: NodeAction) -> None:
        self.add_node_actions_grouped(
            worker_pool_id,
            [NodeActionGroup(list(actions))]
        )

    def add_node_actions_grouped(self, worker_pool_id: str, action_groups: List[NodeActionGroup], node_id_filter_list: Optional[List[str]] = None) -> None:
        self.__service_proxy.add_node_actions_grouped(worker_pool_id, action_groups, node_id_filter_list)

    def get_node_actions(self, node_id: str) -> NodeActionQueueSnapshot:
        return self.__service_proxy.get_node_actions(node_id)

    def close(self) -> None:
        self.__requirement_subscriptions.close()
