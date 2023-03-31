from yellowdog_client.common import Proxy
from yellowdog_client.model import RegionSearch, Slice, Region, SubRegion, SubRegionSearch, InstanceTypeSearch, \
    InstanceType, InstanceTypePrice, InstanceTypePriceSearch, SliceReference


class CloudInfoProxy:
    def __init__(self, proxy: Proxy) -> None:
        self._proxy: Proxy = proxy.append_base_url("/cloudInfo/")

    def slice_regions(self, search: RegionSearch, slice_reference: SliceReference) -> Slice[Region]:
        return self._proxy.get(Slice[Region], "regions", self._proxy.to_params(search, slice_reference))

    def slice_sub_regions(self, search: SubRegionSearch, slice_reference: SliceReference) -> Slice[SubRegion]:
        return self._proxy.get(Slice[SubRegion], "subRegions", self._proxy.to_params(search, slice_reference))

    def slice_instance_types(self, search: InstanceTypeSearch, slice_reference: SliceReference) -> Slice[InstanceType]:
        return self._proxy.get(Slice[InstanceType], "instanceTypes", self._proxy.to_params(search, slice_reference))

    def slice_instance_type_prices(self, search: InstanceTypePriceSearch, slice_reference: SliceReference) -> Slice[InstanceTypePrice]:
        return self._proxy.get(Slice[InstanceTypePrice], "instanceTypePrices", self._proxy.to_params(search, slice_reference))
