from abc import ABC, abstractmethod
from typing import List

from yellowdog_client.common import Closeable
from yellowdog_client.model import InstanceType, InstanceTypePrice, InstanceTypePriceSearch, InstanceTypeSearch, Region, RegionSearch, Slice, SubRegion, SubRegionSearch


class CloudInfoClient(ABC, Closeable):

    @abstractmethod
    def find_regions(self, search: RegionSearch) -> List[Region]:
        """
        Find a list of regions matching the specified search.

        Warning: This method will automatically iterate over all response slices. See the stream and slice methods for
        more control.

        :param search: tbe search filters
        :return: a list of matching regions
        """

        pass

    @abstractmethod
    def slice_regions(self, search: RegionSearch) -> Slice[Region]:
        """
        Retrieve a slice of regions matching the specified search.

        :param search: tbe search filters
        :return: a slice of matching regions
        """

        pass

    @abstractmethod
    def find_sub_regions(self, search: SubRegionSearch) -> List[SubRegion]:
        """
        Find a list of subregions matching the specified search.

        Warning: This method will automatically iterate over all response slices. See the stream and slice methods for
        more control.

        :param search: tbe search filters
        :return: a list of matching subregions
        """

        pass

    @abstractmethod
    def slice_sub_regions(self, search: SubRegionSearch) -> Slice[SubRegion]:
        """
        Retrieve a slice of subregions matching the specified search.

        :param search: tbe search filters
        :return: a slice of matching subregions
        """

        pass

    @abstractmethod
    def find_instance_types(self, search: InstanceTypeSearch) -> List[InstanceType]:
        """
        Find a list of instance types matching the specified search.

        Warning: This method will automatically iterate over all response slices. See the stream and slice methods for
        more control.

        :param search: tbe search filters
        :return: a list of matching instance types
        """

        pass

    @abstractmethod
    def slice_instance_types(self, search: InstanceTypeSearch) -> Slice[InstanceType]:
        """
        Retrieve a slice of instance types matching the specified search.

        :param search: tbe search filters
        :return: a slice of matching instance types
        """

        pass

    @abstractmethod
    def find_instance_type_prices(self, search: InstanceTypePriceSearch) -> List[InstanceTypePrice]:
        """
        Find a list of instance type prices matching the specified search.

        Warning: This method will automatically iterate over all response slices. See the stream and slice methods for
        more control.

        :param search: tbe search filters
        :return: a list of matching instance type prices
        """

        pass

    @abstractmethod
    def slice_instance_type_prices(self, search: InstanceTypePriceSearch) -> Slice[InstanceTypePrice]:
        pass
