from dataclasses import dataclass, field

from .namespace_storage_configuration import NamespaceStorageConfiguration


@dataclass
class AlibabaNamespaceStorageConfiguration(NamespaceStorageConfiguration):
    type: str = field(default="co.yellowdog.platform.model.AlibabaNamespaceStorageConfiguration", init=False)
    namespace: str
    endpoint: str
    bucketName: str
    credential: str
