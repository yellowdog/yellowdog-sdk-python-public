from abc import ABC, abstractmethod
from typing import List

from yellowdog_client.common import Closeable
from yellowdog_client.model import InstanceType, InstanceTypeSearch, Region, RegionSearch, Slice, SubRegion, SubRegionSearch


class CloudInfoClient(ABC, Closeable):

    @abstractmethod
    def find_regions(self, search: RegionSearch) -> List[Region]:
        pass

    @abstractmethod
    def slice_regions(self, search: RegionSearch) -> Slice[Region]:
        pass

    @abstractmethod
    def find_sub_regions(self, search: SubRegionSearch) -> List[SubRegion]:
        pass

    @abstractmethod
    def slice_sub_regions(self, search: SubRegionSearch) -> Slice[SubRegion]:
        pass

    @abstractmethod
    def find_instance_types(self, search: InstanceTypeSearch) -> List[InstanceType]:
        pass

    @abstractmethod
    def slice_instance_types(self, search: InstanceTypeSearch) -> Slice[InstanceType]:
        pass
