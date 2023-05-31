from typing import List, Callable

from yellowdog_client.model import ComputeRequirement, AllowanceExhaustedNotification, Allowance, AllowanceSearch, \
    SliceReference, Slice
from .allowances_client import AllowancesClient
from .allowances_service_proxy import AllowancesServiceProxy
from yellowdog_client.common import SearchClient


class AllowancesClientImpl(AllowancesClient):
    def __init__(self, service_proxy: AllowancesServiceProxy) -> None:
        self.__service_proxy: AllowancesServiceProxy = service_proxy

    def add_allowance(self, allowance: Allowance) -> Allowance:
        return self.__service_proxy.add_allowance(allowance)

    def delete_allowance(self, allowance: Allowance) -> None:
        self.delete_allowance_by_id(allowance.id)

    def delete_allowance_by_id(self, allowance_id: str) -> None:
        self.__service_proxy.delete_allowance_by_id(allowance_id)

    def get_allowance(self, allowance: Allowance) -> Allowance:
        return self.get_allowance_by_id(allowance.id)

    def get_allowance_by_id(self, allowance_id: str) -> Allowance:
        return self.__service_proxy.get_allowance_by_id(allowance_id)

    def boost_allowance(self, allowance: Allowance, boost_hours: int) -> Allowance:
        return self.boost_allowance_by_id(allowance.id, boost_hours)

    def boost_allowance_by_id(self, allowance_id: str, boost_hours: int) -> Allowance:
        return self.__service_proxy.boost_allowance_by_id(allowance_id, boost_hours)

    def get_allowances(self, search: AllowanceSearch) -> SearchClient[Allowance]:
        get_next_slice_function: Callable[[SliceReference], Slice[Allowance]] = \
            lambda slice_reference: self.__service_proxy.search_allowances(search, slice_reference)

        return SearchClient(get_next_slice_function)

    def check_compute_requirement_exhaustion(self, compute_requirement: ComputeRequirement) -> List[AllowanceExhaustedNotification]:
        return self.__service_proxy.check_compute_requirement_exhaustion(compute_requirement)

    def close(self):
        pass
