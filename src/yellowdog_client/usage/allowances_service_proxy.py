from typing import List

from yellowdog_client.model import Allowance, ComputeRequirement, AllowanceExhaustedNotification
from yellowdog_client.common import Proxy


class AllowancesServiceProxy:
    def __init__(self, proxy: Proxy) -> None:
        self._proxy: Proxy = proxy.append_base_url("/allowances/")

    def add_allowance(self, allowance: Allowance) -> Allowance:
        return self._proxy.post(Allowance, allowance)

    def delete_allowance_by_id(self, allowance_id: str) -> None:
        self._proxy.delete(allowance_id)

    def get_allowance_by_id(self, allowance_id: str) -> Allowance:
        return self._proxy.get(Allowance, allowance_id)

    def boost_allowance_by_id(self, allowance_id: str, boost_hours: int) -> Allowance:
        return self._proxy.post(Allowance, url="%s/boost/%s" % (allowance_id, boost_hours))

    def find_all_allowances(self) -> List[Allowance]:
        return self._proxy.get(List[Allowance])

    def check_compute_requirement_exhaustion(self, compute_requirement: ComputeRequirement) -> List[AllowanceExhaustedNotification]:
        return self._proxy.put(List[AllowanceExhaustedNotification], compute_requirement, "requirement")
