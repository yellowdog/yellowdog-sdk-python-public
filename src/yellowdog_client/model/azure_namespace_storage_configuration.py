from dataclasses import dataclass, field

from .namespace_storage_configuration import NamespaceStorageConfiguration


@dataclass
class AzureNamespaceStorageConfiguration(NamespaceStorageConfiguration):
    type: str = field(default="co.yellowdog.platform.model.AzureNamespaceStorageConfiguration", init=False)
    namespace: str
    containerName: str
    credential: str
