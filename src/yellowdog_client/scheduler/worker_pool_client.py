from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar

from .worker_pool_helper import WorkerPoolHelper
from yellowdog_client.common import Closeable
from yellowdog_client.common.server_sent_events import SubscriptionEventListener
from yellowdog_client.model import ComputeRequirementTemplateUsage, Node, NodeAction, NodeActionGroup, NodeActionQueueSnapshot, NodeSearch, ProvisionedWorkerPool, ProvisionedWorkerPoolProperties, Slice, SliceReference, WorkerPool, WorkerPoolSummary

T = TypeVar('T', bound=WorkerPool)


class WorkerPoolClient(ABC, Closeable):
    """Client interface containing methods for accessing YellowDog Scheduler functions."""

    @abstractmethod
    def provision_worker_pool(self, requirement_template_usage: ComputeRequirementTemplateUsage, provisioned_properties: Optional[ProvisionedWorkerPoolProperties] = None) -> ProvisionedWorkerPool:
        """
        Requests that the supplied compute requirement template request is used to provision a worker pool.

        :param requirement_template_usage: the compute requirement template usage from which to provision a worker pool
        :param provisioned_properties:    the properties used to determine behaviour when managing the worker pool
        :return: the provisioned worker pool
        """

        pass

    @abstractmethod
    def get_worker_pool(self, worker_pool: T) -> T:
        """
        Gets the latest state of the supplied worker pool.

        :param worker_pool: the worker pool for which to get the latest state
        :return: the latest state of the worker pool
        """

        pass

    @abstractmethod
    def get_worker_pool_by_id(self, worker_pool_id: str) -> WorkerPool:
        """
        Gets the latest state of the worker pool with the specified ID.

        :param worker_pool_id: the ID of the worker pool
        :return: the latest state of the worker pool
        """

        pass

    @abstractmethod
    def add_worker_pool_listener(self, worker_pool: WorkerPool, listener: SubscriptionEventListener[WorkerPool]) -> None:
        """
        Adds an event listener to receive notifications of changes for the specified worker pool.
        The client manages subscriptions to YellowDog Scheduler such that the first listener created for a worker pool will cause a Server-Sent Events subscription to be initiated; additional listeners for the same worker pool share that subscription.

        :param worker_pool: the worker pool for which to receive notifications
        :param listener:   the event listener that will be invoked for notifications
        """

        pass

    @abstractmethod
    def remove_worker_pool_listener(self, listener: SubscriptionEventListener[WorkerPool]) -> None:
        """
        Removes the specified event listener.
        The client manages subscriptions to YellowDog Scheduler such that when the last listener for a worker pool is removed, the associated Server-Sent Events subscription is cancelled.

        :param listener: the event listener that will no longer be invoked for notifications
        """

        pass

    @abstractmethod
    def get_worker_pool_helper(self, worker_pool: WorkerPool) -> WorkerPoolHelper:
        """
        Constructs a new worker pool helper for the specified worker pool.

        :param worker_pool: the worker pool for which the helper will be constructed
        :return: a new worker pool helper
        """

        pass

    @abstractmethod
    def find_all_worker_pools(self) -> List[WorkerPoolSummary]:
        """
        Returns summaries of all existing worker pools within the system for the requesting user.

        :return: a list of worker pool summaries
        """

        pass

    @abstractmethod
    def shutdown_worker_pool(self, worker_pool_id: str) -> None:
        """
        Shuts down the worker pool with the specified ID.

        :param worker_pool_id: the ID of the worker pool to shutdown
        """

        pass

    @abstractmethod
    def find_nodes(self, search: NodeSearch) -> List[Node]:
        """
        Returns worker pool nodes within the system that match the specified search.
        WARNING: If your search matches too many workers to fit into your application's memory limits, consider using
        #streamNodes(NodeSearch) or #findNodes(NodeSearch, SliceReference).

        :param search: the search
        :return: a list of nodes
        """

        pass

    @abstractmethod
    def find_nodes_slice(self, search: NodeSearch, slice_reference: SliceReference) -> Slice[Node]:
        """
        Returns a slice of nodes that match the specified search and slice reference.

        :param search:         the search
        :param slice_reference: the slice reference
        :return: a slice of nodes
        """

        pass

    @abstractmethod
    def get_node_by_id(self, node_id: str) -> Node:
        """
        Gets the latest state of the node with the specified ID.

        :param node_id: the ID of the node
        :return: the latest state of the node
        """

        pass

    @abstractmethod
    def add_node_actions_for_node(self, worker_pool_id: str, node_id: str, *actions: NodeAction) -> None:
        """
        Adds node actions to be performed for the specified node. Sets the nodeIdFilter and nodeTypes properties of any actions to apply to the specified node.

        :param worker_pool_id: the ID of the worker pool containing the node
        :param node_id:       the ID of the node
        :param actions:      the node actions
        """

        pass

    @abstractmethod
    def add_node_actions(self, worker_pool_id: str, *actions: NodeAction) -> None:
        """
        Adds the specified node actions to be performed for the specified worker pool.

        :param worker_pool_id: the ID of the worker pool
        :param actions:      the node actions
        """

        pass

    @abstractmethod
    def add_node_actions_grouped(self, worker_pool_id: str, action_groups: List[NodeActionGroup], node_id_filter_list: Optional[List[str]] = None) -> None:
        """
        Adds the specified groups of node actions to be performed for the specified worker pool.

        :param worker_pool_id:     the ID of the worker pool
        :param action_groups:     the node action groups
        :param node_id_filter_list: a list of node IDs that can be used to filter recipients of node actions
        """

        pass

    @abstractmethod
    def get_node_actions(self, node_id: str) -> NodeActionQueueSnapshot:
        """
        Gets the current state of the specified node's action queue.

        :param node_id: the ID of the node
        :return: the current state of the action queue
        """

        pass
