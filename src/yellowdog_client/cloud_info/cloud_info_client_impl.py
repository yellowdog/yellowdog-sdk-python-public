from typing import Callable

from yellowdog_client.model import InstanceTypeSearch, Slice, InstanceType, SubRegionSearch, SubRegion, RegionSearch, \
    Region, SliceReference

from .cloud_info_client import CloudInfoClient
from .cloud_info_proxy import CloudInfoProxy
from yellowdog_client.common.search_client import SearchClient
from ..model import InstanceTypePriceSearch, InstanceTypePrice


class CloudInfoClientImpl(CloudInfoClient):

    def __init__(self, service_proxy: CloudInfoProxy) -> None:
        self.__service_proxy: CloudInfoProxy = service_proxy

    def get_regions(self, region_search: RegionSearch) -> SearchClient[Region]:
        def get_next_slice(slice_reference: SliceReference) -> Slice[Region]:
            return self.__service_proxy.slice_regions(region_search, slice_reference)

        return SearchClient(get_next_slice)

    def get_sub_regions(self, sub_region_search: SubRegionSearch) -> SearchClient[SubRegion]:
        def get_next_slice(slice_reference: SliceReference) -> Slice[SubRegion]:
            return self.__service_proxy.slice_sub_regions(sub_region_search, slice_reference)

        return SearchClient(get_next_slice)

    def get_instance_types(self, instance_type_search: InstanceTypeSearch) -> SearchClient[InstanceType]:
        def get_next_slice(slice_reference: SliceReference) -> Slice[InstanceType]:
            return self.__service_proxy.slice_instance_types(instance_type_search, slice_reference)

        return SearchClient(get_next_slice)

    def get_instance_type_prices(self, instance_type_price_search: InstanceTypePriceSearch) -> SearchClient[InstanceTypePrice]:
        def get_next_slice(slice_reference: SliceReference) -> Slice[InstanceTypePrice]:
            return self.__service_proxy.slice_instance_type_prices(instance_type_price_search, slice_reference)

        return SearchClient(get_next_slice)

    def close(self):
        pass
