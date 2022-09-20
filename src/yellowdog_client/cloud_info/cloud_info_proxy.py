from yellowdog_client.common import Proxy
from yellowdog_client.model import RegionSearch, Slice, Region, SubRegion, SubRegionSearch, InstanceTypeSearch, \
    InstanceType, InstanceTypePrice, InstanceTypePriceSearch


class CloudInfoProxy:
    def __init__(self, proxy: Proxy) -> None:
        self._proxy: Proxy = proxy.append_base_url("/cloudInfo/")

    def slice_regions(self, search: RegionSearch) -> Slice[Region]:
        return self._proxy.get(Slice[Region], "regions", self._proxy.to_params(search))

    def slice_sub_regions(self, search: SubRegionSearch) -> Slice[SubRegion]:
        return self._proxy.get(Slice[SubRegion], "subRegions", self._proxy.to_params(search))

    def slice_instance_types(self, search: InstanceTypeSearch) -> Slice[InstanceType]:
        return self._proxy.get(Slice[InstanceType], "instanceTypes", self._proxy.to_params(search))

    def slice_instance_type_prices(self, search: InstanceTypePriceSearch) -> Slice[InstanceTypePrice]:
        return self._proxy.get(Slice[InstanceTypePrice], "instanceTypePrices", self._proxy.to_params(search))
