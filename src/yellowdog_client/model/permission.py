from __future__ import annotations

from enum import Enum
from typing import Set


class Permission(Enum):
    ACCOUNT_APPLICATION_READ = "ACCOUNT_APPLICATION_READ", "Read Account Applications", None
    ACCOUNT_APPLICATION_WRITE = "ACCOUNT_APPLICATION_WRITE", "Write Account Applications", ACCOUNT_APPLICATION_READ
    ACCOUNT_AUTH_PROPERTIES_READ = "ACCOUNT_AUTH_PROPERTIES_READ", "Read Account Authentication Properties", None
    ACCOUNT_AUTH_PROPERTIES_WRITE = "ACCOUNT_AUTH_PROPERTIES_WRITE", "Write Account Authentication Properties", ACCOUNT_AUTH_PROPERTIES_READ
    ACCOUNT_GROUP_READ = "ACCOUNT_GROUP_READ", "Read Account Groups", None
    ACCOUNT_GROUP_WRITE = "ACCOUNT_GROUP_WRITE", "Write Account Groups", ACCOUNT_GROUP_READ
    ACCOUNT_ROLE_READ = "ACCOUNT_ROLE_READ", "Read Account Roles", None
    ACCOUNT_ROLE_WRITE = "ACCOUNT_ROLE_WRITE", "Write Account Roles", ACCOUNT_ROLE_READ
    ACCOUNT_USER_READ = "ACCOUNT_USER_READ", "Read Account Users", None
    ACCOUNT_USER_WRITE = "ACCOUNT_USER_WRITE", "Write Account Users", ACCOUNT_USER_READ
    COMPUTE_ALLOWANCE_READ = "COMPUTE_ALLOWANCE_READ", "Read Compute Allowances", None
    COMPUTE_ALLOWANCE_WRITE = "COMPUTE_ALLOWANCE_WRITE", "Write Compute Allowances", COMPUTE_ALLOWANCE_READ
    COMPUTE_READ = "COMPUTE_READ", "Read Compute", None
    COMPUTE_REQUIREMENT_TEMPLATE_WRITE = "COMPUTE_REQUIREMENT_TEMPLATE_WRITE", "Write Compute Requirement Templates", COMPUTE_READ
    COMPUTE_REQUIREMENT_WRITE = "COMPUTE_REQUIREMENT_WRITE", "Write Compute Requirements", COMPUTE_READ
    COMPUTE_SOURCE_TEMPLATE_WRITE = "COMPUTE_SOURCE_TEMPLATE_WRITE", "Write Compute Source Templates", COMPUTE_READ
    COMPUTE_USAGE_READ = "COMPUTE_USAGE_READ", "Read Compute Usage Data", None
    COMPUTE_USER_ATTRIBUTE_WRITE = "COMPUTE_USER_ATTRIBUTE_WRITE", "Write Compute User Attributes", COMPUTE_READ
    IMAGE_READ = "IMAGE_READ", "Read Images", None
    IMAGE_WRITE = "IMAGE_WRITE", "Write Images", IMAGE_READ
    KEYRING_READ = "KEYRING_READ", "Read Keyrings", None
    KEYRING_WRITE = "KEYRING_WRITE", "Write Keyrings", KEYRING_READ
    KEYRING_ACCESS_WRITE = "KEYRING_ACCESS_WRITE", "Write Keyring Access", KEYRING_READ
    LOG_READ = "LOG_READ", "Read Logs", None
    OBJECT_STORAGE_CONFIGURATION_READ = "OBJECT_STORAGE_CONFIGURATION_READ", "Read Object Storage Configurations", None
    OBJECT_STORAGE_CONFIGURATION_WRITE = "OBJECT_STORAGE_CONFIGURATION_WRITE", "Write Object Storage Configurations", OBJECT_STORAGE_CONFIGURATION_READ
    OBJECT_READ = "OBJECT_READ", "Read Objects", OBJECT_STORAGE_CONFIGURATION_READ
    OBJECT_WRITE = "OBJECT_WRITE", "Write Objects", OBJECT_READ
    WORK_REQUIREMENT_READ = "WORK_REQUIREMENT_READ", "Read Work Requirements", None
    WORK_REQUIREMENT_WRITE = "WORK_REQUIREMENT_WRITE", "Write Work Requirements", WORK_REQUIREMENT_READ
    WORKER_POOL_READ = "WORKER_POOL_READ", "Read Worker Pools", None
    WORKER_POOL_WRITE = "WORKER_POOL_WRITE", "Write Worker Pools", WORKER_POOL_READ
    WORKER_POOL_TOKEN_READ = "WORKER_POOL_TOKEN_READ", "Read Worker Pool Tokens", None
    WORKER_POOL_TOKEN_WRITE = "WORKER_POOL_TOKEN_WRITE", "Write Worker Pool Tokens", WORKER_POOL_READ

    def __new__(cls, value, title: str, includes: Set[Permission]):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.title = title
        obj.includes = includes
        return obj

    def __str__(self) -> str:
        return self.name
