from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from yellowdog_client.common import Closeable, SearchClient
from yellowdog_client.model import Allowance, AllowanceExhaustedNotification, AllowanceSearch, ComputeRequirement


class AllowancesClient(ABC, Closeable):

    @abstractmethod
    def add_allowance(self, allowance: Allowance) -> Allowance:
        pass

    @abstractmethod
    def delete_allowance(self, allowance: Allowance) -> None:
        pass

    @abstractmethod
    def delete_allowance_by_id(self, allowance_id: str) -> None:
        pass

    @abstractmethod
    def get_allowance(self, allowance: Allowance) -> Allowance:
        pass

    @abstractmethod
    def get_allowance_by_id(self, allowance_id: str) -> Allowance:
        pass

    @abstractmethod
    def boost_allowance(self, allowance: Allowance, boost_hours: int) -> Allowance:
        pass

    @abstractmethod
    def boost_allowance_by_id(self, allowance_id: str, boost_hours: int) -> Allowance:
        pass

    @abstractmethod
    def get_allowances(self, allowance_search: AllowanceSearch) -> SearchClient[Allowance]:
        pass

    @abstractmethod
    def check_compute_requirement_exhaustion(self, compute_requirement: ComputeRequirement) -> List[AllowanceExhaustedNotification]:
        pass
