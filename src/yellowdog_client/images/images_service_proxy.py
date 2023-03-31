from typing import List

from yellowdog_client.common import Proxy
from yellowdog_client.model import MachineImageFamily, MachineImageGroup, MachineImage, MachineImageFamilySummary, \
    MachineImageFamilySearch, SliceReference, Slice


class ImagesServiceProxy:
    def __init__(self, proxy: Proxy) -> None:
        self._proxy: Proxy = proxy.append_base_url("/images/")

    def add_image_family(self, family: MachineImageFamily) -> MachineImageFamily:
        return self._proxy.post(MachineImageFamily, family, "families")

    def add_image_group(self, family: MachineImageFamily, group: MachineImageGroup) -> MachineImageGroup:
        return self._proxy.post(MachineImageGroup, group, "families/%s/groups" % family.id)

    def add_image(self, group: MachineImageGroup, image: MachineImage) -> MachineImage:
        return self._proxy.post(MachineImage, image, "groups/%s/images" % group.id)

    def update_image_family(self, family: MachineImageFamily) -> MachineImageFamily:
        return self._proxy.put(MachineImageFamily, family, "families")

    def update_image_group(self, group: MachineImageGroup) -> MachineImageGroup:
        return self._proxy.put(MachineImageGroup, group, "groups")

    def update_image(self, image: MachineImage) -> MachineImage:
        return self._proxy.put(MachineImage, image, "images")

    def delete_image_family(self, family: MachineImageFamily) -> None:
        self._proxy.delete("families/%s" % family.id)

    def delete_image_group(self, group: MachineImageGroup) -> None:
        self._proxy.delete("groups/%s" % group.id)

    def delete_image(self, image: MachineImage) -> None:
        self._proxy.delete("images/%s" % image.id)

    def get_image_family_by_id(self, family_id: str) -> MachineImageFamily:
        return self._proxy.get(MachineImageFamily, "families/%s" % family_id)

    def get_image_group_by_id(self, group_id: str) -> MachineImageGroup:
        return self._proxy.get(MachineImageGroup, "groups/%s" % group_id)

    def get_image_by_id(self, image_id: str) -> MachineImage:
        return self._proxy.get(MachineImage, "images/%s" % image_id)

    def get_image_family_by_name(self, namespace: str, family_name: str) -> MachineImageFamily:
        return self._proxy.get(MachineImageFamily, "namespaces/%s/families/%s" % (namespace, family_name))

    def get_image_group_by_name(self, namespace: str, family_name: str, group_name: str) -> MachineImageGroup:
        return self._proxy.get(MachineImageGroup, "namespaces/%s/families/%s/groups/%s" % (namespace, family_name, group_name))

    def get_latest_image_group_by_family_name(self, namespace: str, family_name: str) -> MachineImageGroup:
        return self._proxy.get(MachineImageGroup, "namespaces/%s/families/%s/groups/latest" % (namespace, family_name))

    def get_latest_image_group_by_family_id(self, family_id: str) -> MachineImageGroup:
        return self._proxy.get(MachineImageGroup, "families/%s/groups/latest" % family_id)

    def get_all_image_families(self) -> List[MachineImageFamilySummary]:
        return self._proxy.get(List[MachineImageFamilySummary], "families")

    def search_image_families(self, search: MachineImageFamilySearch, slice_reference: SliceReference) -> Slice[MachineImageFamilySummary]:
        return self._proxy.get(Slice[MachineImageFamilySummary], "families", self._proxy.to_params(search, slice_reference))
