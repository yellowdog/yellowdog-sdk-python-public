from .account import KeyringClient, KeyringClientImpl, KeyringServiceProxy
from .client_collection import ClientCollection
from .cloud_info import CloudInfoClient, CloudInfoClientImpl, CloudInfoProxy
from .common import Proxy, Closeable
from .common.credentials import ApiKeyAuthenticationHeadersProvider
from .compute import ComputeClient, ComputeClientImpl, ComputeServiceProxy
from .images import ImagesClient, ImagesClientImpl, ImagesServiceProxy
from .model import ServicesSchema, ApiKey
from .object_store import ObjectStoreClient, ObjectStoreServiceProxy
from .scheduler import WorkClient, WorkClientImpl, WorkServiceProxy, WorkerPoolClient, WorkerPoolClientImpl, \
    WorkerPoolServiceProxy
from .usage import AllowancesClient, AllowancesClientImpl, AllowancesServiceProxy


class PlatformClient(Closeable):
    """
    Main class for accessing YellowDog services. Must be created with valid YellowDog Service Platform url
    and credentials.

    To construct, use static :meth:`create` method.
    """

    def __init__(
            self,
            keyring_client: KeyringClient,
            compute_client: ComputeClient,
            images_client: ImagesClient,
            work_client: WorkClient,
            worker_pool_client: WorkerPoolClient,
            object_store_client: ObjectStoreClient,
            allowances_client: AllowancesClient,
            cloud_info_client: CloudInfoClient
    ) -> None:
        self.__clients = ClientCollection()
        self.compute_client: ComputeClient = self.__clients.add(compute_client)
        """Compute service client. Used for controlling compute requirements and instances"""
        self.keyring_client: KeyringClient = self.__clients.add(keyring_client)
        """Account/Keyring client. Used for controlling users keyrings"""
        self.images_client: ImagesClient = self.__clients.add(images_client)
        """Images client. Used for controlling machine images"""
        self.work_client: WorkClient = self.__clients.add(work_client)
        """Work client. Used for controlling work requirements"""
        self.worker_pool_client: WorkerPoolClient = self.__clients.add(worker_pool_client)
        """Worker Pool client. Used for controlling worker pools"""
        self.object_store_client: ObjectStoreClient = self.__clients.add(object_store_client)
        """Object store client. Used for file upload and download"""
        self.allowances_client: AllowancesClient = self.__clients.add(allowances_client)
        """Allowances client. User to constrain how much compute can be used"""
        self.cloud_info_client: CloudInfoClient = self.__clients.add(cloud_info_client)
        """Allowances client. User to constrain how much compute can be used"""

    @staticmethod
    def create(services_schema: ServicesSchema, api_key: ApiKey) -> "PlatformClient":
        """
        Construct :class:`PlatformClient` object.

        :param services_schema: configuration for platform client. Includes url for YellowDog platform service
        :param api_key: the api key to use for authenticating with the YellowDog platform
        :returns: created YellowDog Platform client
        """
        api_key_authentication_headers_provider = ApiKeyAuthenticationHeadersProvider(api_key)

        proxy = Proxy(
            authentication_headers_provider=api_key_authentication_headers_provider,
            retry_count=services_schema.retry.maxAttempts,
            max_retry_interval_seconds=int(services_schema.retry.maxInterval.total_seconds())
        )

        compute_url = services_schema.defaultUrl if services_schema.computeServiceUrl is None else services_schema.computeServiceUrl
        account_url = services_schema.defaultUrl if services_schema.accountServiceUrl is None else services_schema.accountServiceUrl
        images_url = services_schema.defaultUrl if services_schema.imagesServiceUrl is None else services_schema.imagesServiceUrl
        scheduler_url = services_schema.defaultUrl if services_schema.schedulerServiceUrl is None else services_schema.schedulerServiceUrl
        object_store_url = services_schema.defaultUrl if services_schema.objectStoreServiceUrl is None else services_schema.objectStoreServiceUrl
        usage_url = services_schema.defaultUrl if services_schema.usageServiceUrl is None else services_schema.usageServiceUrl
        cloud_info_url = services_schema.defaultUrl if services_schema.cloudInfoServiceUrl is None else services_schema.cloudInfoServiceUrl

        compute_client = ComputeClientImpl(ComputeServiceProxy(proxy.append_base_url(compute_url)))
        keyring_client = KeyringClientImpl(KeyringServiceProxy(proxy.append_base_url(account_url)))
        images_client = ImagesClientImpl(ImagesServiceProxy(proxy.append_base_url(images_url)))
        work_client = WorkClientImpl(WorkServiceProxy(proxy.append_base_url(scheduler_url)))
        worker_pool_client = WorkerPoolClientImpl(WorkerPoolServiceProxy(proxy.append_base_url(scheduler_url)))
        object_store_client = ObjectStoreClient(ObjectStoreServiceProxy(proxy.append_base_url(object_store_url)))
        allowances_client = AllowancesClientImpl(AllowancesServiceProxy(proxy.append_base_url(usage_url)))
        cloud_info_client = CloudInfoClientImpl(CloudInfoProxy(proxy.append_base_url(cloud_info_url)))

        return PlatformClient(
            keyring_client=keyring_client,
            compute_client=compute_client,
            images_client=images_client,
            work_client=work_client,
            worker_pool_client=worker_pool_client,
            object_store_client=object_store_client,
            allowances_client=allowances_client,
            cloud_info_client=cloud_info_client
        )

    def close(self) -> None:
        """
        Closes all ongoing connections in :class:`PlatformClient`

        .. note::

            Client also supports ``with`` keyword. When executing :meth:`__exit__`, method :meth:`close` is invoked

            .. code-block:: python

                with PlatformClient.create(services_schema, api_key) as client:
                    helper = client.compute_client.get_compute_requirement_helper(compute_requirement)
                    # Stuff goes here...
        """
        self.__clients.close()
