from typing import List

from yellowdog_client.account.account_client import AccountClient
from yellowdog_client.account.account_service_proxy import AccountServiceProxy
from yellowdog_client.common import SearchClient
from yellowdog_client.model import User, SliceReference, UserSearch, Slice, GroupSummary, Application, \
    ApplicationSearch, UpdateApplicationRequest, AddApplicationResponse, AddApplicationRequest, ApiKey, \
    PermissionDetail, Role, Group, AddGroupRequest, UpdateGroupRequest, GroupSearch, RoleSearch


class AccountClientImpl(AccountClient):
    def __init__(self, service_proxy: AccountServiceProxy) -> None:
        self.__service_proxy = service_proxy

    def get_user(self, user_id: str) -> User:
        return self.__service_proxy.get_user(user_id)

    def get_users(self, search: UserSearch) -> SearchClient[User]:
        def get_next_slice_function(slice_reference: SliceReference) -> Slice[User]:
            return self.__service_proxy.search_users(search, slice_reference)

        return SearchClient(get_next_slice_function)

    def get_user_groups(self, user_id: str) -> SearchClient[GroupSummary]:
        def get_next_slice_function(slice_reference: SliceReference) -> Slice[GroupSummary]:
            return self.__service_proxy.list_user_groups(user_id, slice_reference)

        return SearchClient(get_next_slice_function)

    def get_application(self, application_id: str) -> Application:
        return self.__service_proxy.get_application(application_id)

    def update_application(self, application_id: str, request: UpdateApplicationRequest) -> Application:
        return self.__service_proxy.update_application(application_id, request)

    def add_application(self, request: AddApplicationRequest) -> AddApplicationResponse:
        return self.__service_proxy.add_application(request)

    def regenerate_application_api_key(self, application_id: str) -> ApiKey:
        return self.__service_proxy.regenerate_application_api_key(application_id)

    def get_applications(self, search: ApplicationSearch) -> SearchClient[Application]:
        def get_next_slice_function(slice_reference: SliceReference) -> Slice[Application]:
            return self.__service_proxy.search_applications(search, slice_reference)

        return SearchClient(get_next_slice_function)

    def get_application_groups(self, application_id: str) -> SearchClient[GroupSummary]:
        def get_next_slice_function(slice_reference: SliceReference) -> Slice[GroupSummary]:
            return self.__service_proxy.list_application_groups(application_id, slice_reference)

        return SearchClient(get_next_slice_function)

    def delete_application(self, application_id: str) -> None:
        return self.__service_proxy.delete_application(application_id)

    def list_permissions(self) -> List[PermissionDetail]:
        return self.__service_proxy.list_permissions()

    def get_role(self, role_id: str) -> Role:
        return self.__service_proxy.get_role(role_id)

    def get_roles(self, search: RoleSearch) -> SearchClient[Role]:
        def get_next_slice_function(slice_reference: SliceReference) -> Slice[Role]:
            return self.__service_proxy.search_roles(search, slice_reference)

        return SearchClient(get_next_slice_function)

    def get_role_groups(self, role_id: str) -> SearchClient[GroupSummary]:
        def get_next_slice_function(slice_reference: SliceReference) -> Slice[GroupSummary]:
            return self.__service_proxy.list_role_groups(role_id, slice_reference)

        return SearchClient(get_next_slice_function)

    def get_group(self, group_id: str) -> Group:
        return self.__service_proxy.get_group(group_id)

    def add_group(self, request: AddGroupRequest) -> Group:
        return self.__service_proxy.add_group(request)

    def update_group(self, group_id: str, request: UpdateGroupRequest) -> Group:
        return self.__service_proxy.update_group(group_id, request)

    def get_group_users(self, group_id: str) -> SearchClient[User]:
        def get_next_slice_function(slice_reference: SliceReference) -> Slice[User]:
            return self.__service_proxy.list_group_users(group_id, slice_reference)

        return SearchClient(get_next_slice_function)

    def get_group_applications(self, group_id: str) -> SearchClient[Application]:
        def get_next_slice_function(slice_reference: SliceReference) -> Slice[Application]:
            return self.__service_proxy.list_group_applications(group_id, slice_reference)

        return SearchClient(get_next_slice_function)

    def get_groups(self, search: GroupSearch) -> SearchClient[GroupSummary]:
        def get_next_slice_function(slice_reference: SliceReference) -> Slice[GroupSummary]:
            return self.__service_proxy.search_groups(search, slice_reference)

        return SearchClient(get_next_slice_function)

    def add_user_to_group(self, group_id: str, user_id: str) -> None:
        return self.__service_proxy.add_user_to_group(group_id, user_id)

    def add_application_to_group(self, group_id: str, application_id: str) -> None:
        return self.__service_proxy.add_application_to_group(group_id, application_id)

    def add_role_to_group(self, group_id: str, role_id: str) -> None:
        return self.__service_proxy.add_role_to_group(group_id, role_id)

    def remove_user_from_group(self, group_id: str, user_id: str) -> None:
        return self.__service_proxy.remove_user_from_group(group_id, user_id)

    def remove_application_from_group(self, group_id: str, application_id: str) -> None:
        return self.__service_proxy.remove_application_from_group(group_id, application_id)

    def remove_role_from_group(self, group_id: str, role_id: str) -> None:
        return self.__service_proxy.remove_role_from_group(group_id, role_id)

    def delete_group(self, group_id: str) -> None:
        return self.__service_proxy.delete_group(group_id)

    def close(self):
        # Has no closing resources
        pass
