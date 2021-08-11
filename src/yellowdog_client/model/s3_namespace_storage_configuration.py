from dataclasses import dataclass, field

from .namespace_storage_configuration import NamespaceStorageConfiguration


@dataclass
class S3NamespaceStorageConfiguration(NamespaceStorageConfiguration):
    type: str = field(default="co.yellowdog.platform.model.S3NamespaceStorageConfiguration", init=False)
    namespace: str
    bucketName: str
    region: str
    credential: str
