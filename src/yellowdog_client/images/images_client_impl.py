from typing import List

from .images_client import ImagesClient
from .images_service_proxy import ImagesServiceProxy
from .page import Page
from .pageable import Pageable
from yellowdog_client.model import MachineImageFamilySearch, MachineImageFamilySummary, MachineImage, MachineImageGroup, MachineImageFamily


class ImagesClientImpl(ImagesClient):
    def __init__(self, service_proxy: ImagesServiceProxy) -> None:
        self.__service_proxy: ImagesServiceProxy = service_proxy

    def add_image_family(self, family: MachineImageFamily) -> MachineImageFamily:
        return self.__service_proxy.add_image_family(family)

    def add_image_group(self, family: MachineImageFamily, group: MachineImageGroup) -> MachineImageGroup:
        return self.__service_proxy.add_image_group(family, group)

    def add_image(self, group: MachineImageGroup, image: MachineImage) -> MachineImage:
        return self.__service_proxy.add_image(group, image)

    def update_image_family(self, family: MachineImageFamily) -> MachineImageFamily:
        return self.__service_proxy.update_image_family(family)

    def update_image_group(self, group: MachineImageGroup) -> MachineImageGroup:
        return self.__service_proxy.update_image_group(group)

    def update_image(self, image: MachineImage) -> MachineImage:
        return self.__service_proxy.update_image(image)

    def delete_image_family(self, family: MachineImageFamily) -> None:
        self.__service_proxy.delete_image_family(family)

    def delete_image_group(self, group: MachineImageGroup) -> None:
        self.__service_proxy.delete_image_group(group)

    def delete_image(self, image: MachineImage) -> None:
        self.__service_proxy.delete_image(image)

    def get_image_family_by_id(self, family_id: str) -> MachineImageFamily:
        return self.__service_proxy.get_image_family_by_id(family_id)

    def get_image_family_by_name(self, namespace: str, family_name: str) -> MachineImageFamily:
        return self.__service_proxy.get_image_family_by_name(namespace, family_name)

    def get_latest_image_group_by_family_id(self, family_id: str) -> MachineImageGroup:
        return self.__service_proxy.get_latest_image_group_by_family_id(family_id)

    def get_latest_image_group_by_family_name(self, namespace: str, family_name: str) -> MachineImageGroup:
        return self.__service_proxy.get_latest_image_group_by_family_name(namespace, family_name)

    def get_image_group_by_id(self, group_id: str) -> MachineImageGroup:
        return self.__service_proxy.get_image_group_by_id(group_id)

    def get_image_group_by_name(self, namespace: str, family_name: str, group_name: str) -> MachineImageGroup:
        return self.__service_proxy.get_image_group_by_name(namespace, family_name, group_name)

    def get_image(self, image_id: str) -> MachineImage:
        return self.__service_proxy.get_image_by_id(image_id)

    def get_all_image_families(self) -> List[MachineImageFamilySummary]:
        return self.__service_proxy.get_all_image_families()

    def search_image_families(self, search: MachineImageFamilySearch) -> List[MachineImageFamilySummary]:
        return self.search_image_families_paged(search, Pageable()).content

    def search_image_families_paged(self, search: MachineImageFamilySearch, pageable: Pageable) -> Page[MachineImageFamilySummary]:
        return self.__service_proxy.search_image_families_paged(search, pageable)

    def close(self):
        pass
