from __future__ import annotations

from abc import ABC, abstractmethod

from yellowdog_client.common import Closeable, SearchClient
from yellowdog_client.model import InstanceType, InstanceTypePrice, InstanceTypePriceSearch, InstanceTypeSearch, Region, RegionSearch, SubRegion, SubRegionSearch


class CloudInfoClient(ABC, Closeable):

    @abstractmethod
    def get_regions(self, region_search: RegionSearch) -> SearchClient[Region]:
        pass

    @abstractmethod
    def get_sub_regions(self, sub_region_search: SubRegionSearch) -> SearchClient[SubRegion]:
        pass

    @abstractmethod
    def get_instance_types(self, instance_type_search: InstanceTypeSearch) -> SearchClient[InstanceType]:
        pass

    @abstractmethod
    def get_instance_type_prices(self, instance_type_price_search: InstanceTypePriceSearch) -> SearchClient[InstanceTypePrice]:
        pass
