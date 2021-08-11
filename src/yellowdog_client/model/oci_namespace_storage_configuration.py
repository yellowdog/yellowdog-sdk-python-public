from dataclasses import dataclass, field

from .namespace_storage_configuration import NamespaceStorageConfiguration


@dataclass
class OciNamespaceStorageConfiguration(NamespaceStorageConfiguration):
    type: str = field(default="co.yellowdog.platform.model.OciNamespaceStorageConfiguration", init=False)
    namespace: str
    ociNamespaceName: str
    bucketName: str
    region: str
    credential: str
