from typing import List

from .cloud_info_client import CloudInfoClient
from .cloud_info_proxy import CloudInfoProxy
from yellowdog_client.common.pagination import paginate, with_slice_reference
from yellowdog_client.model import InstanceTypeSearch, Slice, InstanceType, SubRegionSearch, SubRegion, RegionSearch, Region


class CloudInfoClientImpl(CloudInfoClient):
    def __init__(self, service_proxy: CloudInfoProxy) -> None:
        self.__service_proxy: CloudInfoProxy = service_proxy

    def find_regions(self, search: RegionSearch) -> List[Region]:
        return paginate(lambda sr: self.slice_regions(with_slice_reference(search, sr)))

    def slice_regions(self, search: RegionSearch) -> Slice[Region]:
        return self.__service_proxy.slice_regions(search)

    def find_sub_regions(self, search: SubRegionSearch) -> List[SubRegion]:
        return paginate(lambda sr: self.slice_sub_regions(with_slice_reference(search, sr)))

    def slice_sub_regions(self, search: SubRegionSearch) -> Slice[SubRegion]:
        return self.__service_proxy.slice_sub_regions(search)

    def find_instance_types(self, search: InstanceTypeSearch) -> List[InstanceType]:
        return paginate(lambda sr: self.slice_instance_types(with_slice_reference(search, sr)))

    def slice_instance_types(self, search: InstanceTypeSearch) -> Slice[InstanceType]:
        return self.__service_proxy.slice_instance_types(search)

    def close(self):
        pass
