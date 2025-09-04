from __future__ import annotations

from enum import Enum
from typing import List

from .permission_scope import PermissionScope


class Permission(Enum):
    NAMESPACE_READ = "NAMESPACE_READ", "Read Namespaces", PermissionScope.NAMESPACED_OR_GLOBAL, None
    COMPUTE_READ = "COMPUTE_READ", "Read Compute", PermissionScope.NAMESPACED_OR_GLOBAL, NAMESPACE_READ
    COMPUTE_REQUIREMENT_TEMPLATE_WRITE = "COMPUTE_REQUIREMENT_TEMPLATE_WRITE", "Write Compute Requirement Templates", PermissionScope.NAMESPACED_OR_GLOBAL, COMPUTE_READ
    COMPUTE_REQUIREMENT_WRITE = "COMPUTE_REQUIREMENT_WRITE", "Write Compute Requirements", PermissionScope.NAMESPACED_OR_GLOBAL, COMPUTE_READ
    COMPUTE_SOURCE_TEMPLATE_WRITE = "COMPUTE_SOURCE_TEMPLATE_WRITE", "Write Compute Source Templates", PermissionScope.NAMESPACED_OR_GLOBAL, COMPUTE_READ
    IMAGE_READ = "IMAGE_READ", "Read Images", PermissionScope.NAMESPACED_OR_GLOBAL, NAMESPACE_READ
    IMAGE_WRITE = "IMAGE_WRITE", "Write Images", PermissionScope.NAMESPACED_OR_GLOBAL, IMAGE_READ
    NAMESPACE_POLICY_READ = "NAMESPACE_POLICY_READ", "Read Namespace Policies", PermissionScope.NAMESPACED_OR_GLOBAL, NAMESPACE_READ
    NAMESPACE_POLICY_WRITE = "NAMESPACE_POLICY_WRITE", "Write Namespace Policies", PermissionScope.NAMESPACED_OR_GLOBAL, NAMESPACE_POLICY_READ
    WORK_REQUIREMENT_READ = "WORK_REQUIREMENT_READ", "Read Work Requirements", PermissionScope.NAMESPACED_OR_GLOBAL, NAMESPACE_READ
    WORK_REQUIREMENT_WRITE = "WORK_REQUIREMENT_WRITE", "Write Work Requirements", PermissionScope.NAMESPACED_OR_GLOBAL, WORK_REQUIREMENT_READ
    WORKER_POOL_READ = "WORKER_POOL_READ", "Read Worker Pools", PermissionScope.NAMESPACED_OR_GLOBAL, NAMESPACE_READ
    WORKER_POOL_WRITE = "WORKER_POOL_WRITE", "Write Worker Pools", PermissionScope.NAMESPACED_OR_GLOBAL, WORKER_POOL_READ
    WORKER_POOL_TOKEN_READ = "WORKER_POOL_TOKEN_READ", "Read Worker Pool Tokens", PermissionScope.NAMESPACED_OR_GLOBAL, WORKER_POOL_READ
    WORKER_POOL_TOKEN_WRITE = "WORKER_POOL_TOKEN_WRITE", "Write Worker Pool Tokens", PermissionScope.NAMESPACED_OR_GLOBAL, WORKER_POOL_TOKEN_READ
    WORKER_POOL_WORKER_WRITE = "WORKER_POOL_WORKER_WRITE", "Write Worker Pool Workers", PermissionScope.NAMESPACED_OR_GLOBAL, WORKER_POOL_READ
    ACCOUNT_APPLICATION_READ = "ACCOUNT_APPLICATION_READ", "Read Account Applications", PermissionScope.GLOBAL_ONLY, None
    ACCOUNT_APPLICATION_WRITE = "ACCOUNT_APPLICATION_WRITE", "Write Account Applications", PermissionScope.GLOBAL_ONLY, ACCOUNT_APPLICATION_READ
    ACCOUNT_AUTH_PROPERTIES_READ = "ACCOUNT_AUTH_PROPERTIES_READ", "Read Account Authentication Properties", PermissionScope.GLOBAL_ONLY, None
    ACCOUNT_AUTH_PROPERTIES_WRITE = "ACCOUNT_AUTH_PROPERTIES_WRITE", "Write Account Authentication Properties", PermissionScope.GLOBAL_ONLY, ACCOUNT_AUTH_PROPERTIES_READ
    ACCOUNT_GROUP_READ = "ACCOUNT_GROUP_READ", "Read Account Groups", PermissionScope.GLOBAL_ONLY, None
    ACCOUNT_GROUP_WRITE = "ACCOUNT_GROUP_WRITE", "Write Account Groups", PermissionScope.GLOBAL_ONLY, ACCOUNT_GROUP_READ
    ACCOUNT_POLICY_READ = "ACCOUNT_POLICY_READ", "Read Account Policy", PermissionScope.GLOBAL_ONLY, None
    ACCOUNT_POLICY_WRITE = "ACCOUNT_POLICY_WRITE", "Write Account Policy", PermissionScope.GLOBAL_ONLY, ACCOUNT_POLICY_READ
    ACCOUNT_ROLE_READ = "ACCOUNT_ROLE_READ", "Read Account Roles", PermissionScope.GLOBAL_ONLY, None
    ACCOUNT_ROLE_WRITE = "ACCOUNT_ROLE_WRITE", "Write Account Roles", PermissionScope.GLOBAL_ONLY, ACCOUNT_ROLE_READ
    ACCOUNT_USER_READ = "ACCOUNT_USER_READ", "Read Account Users", PermissionScope.GLOBAL_ONLY, None
    ACCOUNT_USER_WRITE = "ACCOUNT_USER_WRITE", "Write Account Users", PermissionScope.GLOBAL_ONLY, ACCOUNT_USER_READ
    ACCOUNT_NAMESPACE_WRITE = "ACCOUNT_NAMESPACE_WRITE", "Write Account Namespaces", PermissionScope.GLOBAL_ONLY, NAMESPACE_READ
    COMPUTE_ALLOWANCE_READ = "COMPUTE_ALLOWANCE_READ", "Read Compute Allowances", PermissionScope.GLOBAL_ONLY, None
    COMPUTE_ALLOWANCE_WRITE = "COMPUTE_ALLOWANCE_WRITE", "Write Compute Allowances", PermissionScope.GLOBAL_ONLY, COMPUTE_ALLOWANCE_READ
    COMPUTE_USER_ATTRIBUTE_READ = "COMPUTE_USER_ATTRIBUTE_READ", "Read Compute User Attributes", PermissionScope.GLOBAL_ONLY, None
    COMPUTE_USER_ATTRIBUTE_WRITE = "COMPUTE_USER_ATTRIBUTE_WRITE", "Write Compute User Attributes", PermissionScope.GLOBAL_ONLY, COMPUTE_USER_ATTRIBUTE_READ
    KEYRING_READ = "KEYRING_READ", "Read Keyrings", PermissionScope.GLOBAL_ONLY, None
    KEYRING_WRITE = "KEYRING_WRITE", "Write Keyrings", PermissionScope.GLOBAL_ONLY, KEYRING_READ
    KEYRING_ACCESS_WRITE = "KEYRING_ACCESS_WRITE", "Write Keyring Access", PermissionScope.GLOBAL_ONLY, KEYRING_READ
    OBJECT_STORAGE_CONFIGURATION_READ = "OBJECT_STORAGE_CONFIGURATION_READ", "Read Object Storage Configurations", PermissionScope.GLOBAL_ONLY, None
    OBJECT_STORAGE_CONFIGURATION_WRITE = "OBJECT_STORAGE_CONFIGURATION_WRITE", "Write Object Storage Configurations", PermissionScope.GLOBAL_ONLY, OBJECT_STORAGE_CONFIGURATION_READ
    OBJECT_READ = "OBJECT_READ", "Read Objects", PermissionScope.GLOBAL_ONLY, OBJECT_STORAGE_CONFIGURATION_READ
    OBJECT_WRITE = "OBJECT_WRITE", "Write Objects", PermissionScope.GLOBAL_ONLY, OBJECT_READ
    METRICS_READ = "METRICS_READ", "Read Metrics", PermissionScope.GLOBAL_ONLY, None
    METRICS_WRITE = "METRICS_WRITE", "Write Metrics", PermissionScope.GLOBAL_ONLY, METRICS_READ
    LOG_READ = "LOG_READ", "Read Logs", PermissionScope.GLOBAL_ONLY, None
    COMPUTE_USAGE_READ = "COMPUTE_USAGE_READ", "Read Compute Usage Data", PermissionScope.GLOBAL_ONLY, None

    def __new__(cls, value, title: str, scope: PermissionScope, includes: List[Permission]):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.title = title
        obj.scope = scope
        obj.includes = includes
        return obj

    def __str__(self) -> str:
        return self.name
