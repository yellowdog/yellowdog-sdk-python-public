from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from yellowdog_client.common import Closeable, SearchClient
from yellowdog_client.model import AddApplicationRequest, AddApplicationResponse, AddGroupRequest, ApiKey, Application, ApplicationSearch, Group, GroupSearch, GroupSummary, PermissionDetail, Role, RoleSearch, UpdateApplicationRequest, UpdateGroupRequest, User, UserSearch


class AccountClient(ABC, Closeable):
    """The API interface exposed by the YellowDog Account Service"""

    @abstractmethod
    def get_user(self, user_id: str) -> User:
        pass

    @abstractmethod
    def get_users(self, search: UserSearch) -> SearchClient[User]:
        pass

    @abstractmethod
    def get_user_groups(self, user_id: str) -> SearchClient[GroupSummary]:
        pass

    @abstractmethod
    def get_application(self, application_id: str) -> Application:
        pass

    @abstractmethod
    def update_application(self, application_id: str, request: UpdateApplicationRequest) -> Application:
        pass

    @abstractmethod
    def add_application(self, request: AddApplicationRequest) -> AddApplicationResponse:
        pass

    @abstractmethod
    def regenerate_application_api_key(self, application_id: str) -> ApiKey:
        pass

    @abstractmethod
    def get_applications(self, search: ApplicationSearch) -> SearchClient[Application]:
        pass

    @abstractmethod
    def get_application_groups(self, application_id: str) -> SearchClient[GroupSummary]:
        pass

    @abstractmethod
    def delete_application(self, application_id: str) -> None:
        pass

    @abstractmethod
    def list_permissions(self) -> List[PermissionDetail]:
        pass

    @abstractmethod
    def get_role(self, role_id: str) -> Role:
        pass

    @abstractmethod
    def get_roles(self, search: RoleSearch) -> SearchClient[Role]:
        pass

    @abstractmethod
    def get_role_groups(self, role_id: str) -> SearchClient[GroupSummary]:
        pass

    @abstractmethod
    def get_group(self, group_id: str) -> Group:
        pass

    @abstractmethod
    def add_group(self, request: AddGroupRequest) -> Group:
        pass

    @abstractmethod
    def update_group(self, group_id: str, request: UpdateGroupRequest) -> Group:
        pass

    @abstractmethod
    def get_group_users(self, group_id: str) -> SearchClient[User]:
        pass

    @abstractmethod
    def get_group_applications(self, group_id: str) -> SearchClient[Application]:
        pass

    @abstractmethod
    def get_groups(self, search: GroupSearch) -> SearchClient[GroupSummary]:
        pass

    @abstractmethod
    def add_user_to_group(self, group_id: str, user_id: str) -> None:
        pass

    @abstractmethod
    def add_application_to_group(self, group_id: str, application_id: str) -> None:
        pass

    @abstractmethod
    def add_role_to_group(self, group_id: str, role_id: str) -> None:
        pass

    @abstractmethod
    def remove_user_from_group(self, group_id: str, user_id: str) -> None:
        pass

    @abstractmethod
    def remove_application_from_group(self, group_id: str, application_id: str) -> None:
        pass

    @abstractmethod
    def remove_role_from_group(self, group_id: str, role_id: str) -> None:
        pass

    @abstractmethod
    def delete_group(self, group_id: str) -> None:
        pass
