from __future__ import annotations

from abc import ABC, abstractmethod

from yellowdog_client.common import Closeable, SearchClient
from yellowdog_client.model import MachineImage, MachineImageFamily, MachineImageFamilySearch, MachineImageFamilySummary, MachineImageGroup


class ImagesClient(ABC, Closeable):

    @abstractmethod
    def add_image_family(self, family: MachineImageFamily) -> MachineImageFamily:
        pass

    @abstractmethod
    def add_image_group(self, family: MachineImageFamily, group: MachineImageGroup) -> MachineImageGroup:
        pass

    @abstractmethod
    def add_image(self, group: MachineImageGroup, image: MachineImage) -> MachineImage:
        pass

    @abstractmethod
    def update_image_family(self, family: MachineImageFamily) -> MachineImageFamily:
        pass

    @abstractmethod
    def update_image_group(self, group: MachineImageGroup) -> MachineImageGroup:
        pass

    @abstractmethod
    def update_image(self, image: MachineImage) -> MachineImage:
        pass

    @abstractmethod
    def delete_image_family(self, family: MachineImageFamily) -> None:
        pass

    @abstractmethod
    def delete_image_group(self, group: MachineImageGroup) -> None:
        pass

    @abstractmethod
    def delete_image(self, image: MachineImage) -> None:
        pass

    @abstractmethod
    def get_image_family_by_id(self, family_id: str) -> MachineImageFamily:
        pass

    @abstractmethod
    def get_image_family_by_name(self, namespace: str, family_name: str) -> MachineImageFamily:
        pass

    @abstractmethod
    def get_latest_image_group_by_family_id(self, family_id: str) -> MachineImageGroup:
        pass

    @abstractmethod
    def get_latest_image_group_by_family_name(self, namespace: str, family_name: str) -> MachineImageGroup:
        pass

    @abstractmethod
    def get_image_group_by_id(self, group_id: str) -> MachineImageGroup:
        pass

    @abstractmethod
    def get_image_group_by_name(self, namespace: str, family_name: str, group_name: str) -> MachineImageGroup:
        pass

    @abstractmethod
    def get_image(self, image_id: str) -> MachineImage:
        pass

    @abstractmethod
    def get_image_families(self, search: MachineImageFamilySearch) -> SearchClient[MachineImageFamilySummary]:
        pass
