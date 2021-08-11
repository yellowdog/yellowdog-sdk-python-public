from dataclasses import dataclass, field

from .namespace_storage_configuration import NamespaceStorageConfiguration


@dataclass
class GcsNamespaceStorageConfiguration(NamespaceStorageConfiguration):
    type: str = field(default="co.yellowdog.platform.model.GcsNamespaceStorageConfiguration", init=False)
    namespace: str
    bucketName: str
    credential: str
