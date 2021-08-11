from typing import List

from yellowdog_client.model import ComputeRequirement, AllowanceExhaustedNotification, Allowance
from .allowances_client import AllowancesClient
from .allowances_service_proxy import AllowancesServiceProxy


class AllowancesClientImpl(AllowancesClient):
    def __init__(self, service_proxy: AllowancesServiceProxy) -> None:
        self.__service_proxy: AllowancesServiceProxy = service_proxy

    def add_allowance(self, allowance: Allowance) -> Allowance:
        return self.__service_proxy.add_allowance(allowance)

    def delete_allowance_by_id(self, allowance_id: str) -> None:
        self.__service_proxy.delete_allowance_by_id(allowance_id)

    def get_allowance_by_id(self, allowance_id: str) -> Allowance:
        return self.__service_proxy.get_allowance_by_id(allowance_id)

    def boost_allowance_by_id(self, allowance_id: str, boost_hours: int) -> Allowance:
        return self.__service_proxy.boost_allowance_by_id(allowance_id, boost_hours)

    def find_all_allowances(self) -> List[Allowance]:
        return self.__service_proxy.find_all_allowances()

    def check_compute_requirement_exhaustion(self, compute_requirement: ComputeRequirement) -> List[AllowanceExhaustedNotification]:
        return self.__service_proxy.check_compute_requirement_exhaustion(compute_requirement)

    def close(self):
        pass
