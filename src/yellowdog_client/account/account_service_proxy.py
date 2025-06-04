from typing import List

from yellowdog_client.common import Proxy
from yellowdog_client.model import UserSearch, SliceReference, Slice, GroupSummary, Application, \
    UpdateApplicationRequest, AddApplicationRequest, AddApplicationResponse, ApiKey, ApplicationSearch, \
    PermissionDetail, \
    Role, RoleSearch, Group, AddGroupRequest, UpdateGroupRequest, GroupSearch, User


class AccountServiceProxy:
    def __init__(self, proxy: Proxy) -> None:
        self.proxy: Proxy = proxy.append_base_url("/account/")

    def get_user(self, user_id: str) -> User:
        return self.proxy.get(User, "users/%s" % user_id)

    def search_users(self, search: UserSearch, slice_reference: SliceReference) -> Slice[User]:
        return self.proxy.get(
            Slice[User], "users",
            self.proxy.to_params(search, slice_reference)
        )

    def list_user_groups(self, user_id: str, slice_reference: SliceReference) -> Slice[GroupSummary]:
        return self.proxy.get(
            Slice[GroupSummary], "users/%s/groups" % user_id,
            self.proxy.to_params(slice_reference)
        )

    def get_application(self, application_id: str) -> Application:
        return self.proxy.get(Application, "applications/%s" % application_id)

    def update_application(self, application_id: str, request: UpdateApplicationRequest) -> Application:
        return self.proxy.put(Application, request, "applications/%s" % application_id)

    def add_application(self, request: AddApplicationRequest) -> AddApplicationResponse:
        return self.proxy.post(AddApplicationResponse, request, "applications")

    def regenerate_application_api_key(self, application_id: str) -> ApiKey:
        return self.proxy.post(ApiKey, url="applications/%s/key" % application_id)

    def search_applications(self, search: ApplicationSearch, slice_reference: SliceReference) -> Slice[Application]:
        return self.proxy.get(
            Slice[Application], "applications",
            self.proxy.to_params(search, slice_reference)
        )

    def list_application_groups(self, application_id: str, slice_reference: SliceReference) -> Slice[GroupSummary]:
        return self.proxy.get(
            Slice[GroupSummary], "applications/%s/groups" % application_id,
            self.proxy.to_params(slice_reference)
        )

    def delete_application(self, application_id: str) -> None:
        return self.proxy.delete("applications/%s" % application_id)

    def list_permissions(self) -> List[PermissionDetail]:
        return self.proxy.get(List[PermissionDetail], "permissions")

    def get_role(self, role_id: str) -> Role:
        return self.proxy.get(Role, "roles/%s" % role_id)

    def search_roles(self, search: RoleSearch, slice_reference: SliceReference) -> Slice[Role]:
        return self.proxy.get(
            Slice[Role], "roles",
            self.proxy.to_params(search, slice_reference)
        )

    def list_role_groups(self, role_id: str, slice_reference: SliceReference) -> Slice[GroupSummary]:
        return self.proxy.get(
            Slice[GroupSummary], "roles/%s/groups" % role_id,
            self.proxy.to_params(slice_reference)
        )

    def get_group(self, group_id: str) -> Group:
        return self.proxy.get(Group, "groups/%s" % group_id)

    def add_group(self, request: AddGroupRequest) -> Group:
        return self.proxy.post(Group, request, "groups")

    def update_group(self, group_id: str, request: UpdateGroupRequest) -> Group:
        return self.proxy.put(Group, request, "groups/%s" % group_id)

    def list_group_users(self, group_id: str, slice_reference: SliceReference) -> Slice[User]:
        return self.proxy.get(
            Slice[User], "groups/%s/users" % group_id,
            self.proxy.to_params(slice_reference)
        )

    def list_group_applications(self, group_id: str, slice_reference: SliceReference) -> Slice[Application]:
        return self.proxy.get(
            Slice[Application], "groups/%s/applications" % group_id,
            self.proxy.to_params(slice_reference)
        )

    def search_groups(self, search: GroupSearch, slice_reference: SliceReference) -> Slice[GroupSummary]:
        return self.proxy.get(
            Slice[GroupSummary], "groups",
            self.proxy.to_params(search, slice_reference)
        )

    def add_user_to_group(self, group_id: str, user_id: str) -> None:
        return self.proxy.put(url="groups/%s/users/%s" % (group_id, user_id))

    def add_application_to_group(self, group_id: str, application_id: str) -> None:
        return self.proxy.put(url="groups/%s/applications/%s" % (group_id, application_id))

    def add_role_to_group(self, group_id: str, role_id: str) -> None:
        return self.proxy.put(url="groups/%s/roles/%s" % (group_id, role_id))

    def remove_user_from_group(self, group_id: str, user_id: str) -> None:
        return self.proxy.delete("groups/%s/users/%s" % (group_id, user_id))

    def remove_application_from_group(self, group_id: str, application_id: str) -> None:
        return self.proxy.delete("groups/%s/applications/%s" % (group_id, application_id))

    def remove_role_from_group(self, group_id: str, role_id: str) -> None:
        return self.proxy.delete("groups/%s/roles/%s" % (group_id, role_id))

    def delete_group(self, group_id: str) -> None:
        return self.proxy.delete("groups/%s" % group_id)

