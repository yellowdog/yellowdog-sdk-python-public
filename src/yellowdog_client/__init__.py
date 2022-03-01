"""

Authenticating
--------------

To start using this SDK, you first need to create an ``Application`` in the YellowDog Platform
Portal. This provides you with an api ``key`` and ``secret`` to authenticate with the platform.

The PlatformClient provides access to all functionality and may be constructed as follows::

    from yellowdog_client import PlatformClient
    from yellowdog_client.model import ServicesSchema, ApiKey

    client = PlatformClient.create(
        ServicesSchema(defaultUrl="https://portal.yellowdog.co/api"),
        ApiKey("my_app_key",  "my_app_secret")
    )

The PlatformClient is split into several clients, each covering a specific area of functionality.
All clients are available as attributes of the PlatformClient.

Compute Client
--------------

The ComputeClient allows control of compute requirements, their instances and templates.

Finding data
============

To retrieve all currently active compute requirements::

    requirements = client.compute_client.find_all_compute_requirements()

To retrieve the details of a specific compute requirement::

    req_id = "ydid:compreq:000000:6c9343f5-ddd7-4903-bcbf-12c7a6bf1e1a"
    requirement = client.compute_client.find_compute_requirement_by_id(req_id)

To get latest status of a compute requirement::

    requirement = client.compute_client.get_compute_requirement(requirement)

To retrieve all available compute requirement templates::

    templates = client.compute_client.find_all_compute_requirement_templates()

Provisioning
============

One way to provision compute is to use a template that either you or somebody else has already
created in the `YellowDog Platform Portal`::

    from yellowdog_client.model import ComputeRequirementTemplateUsage

    request = ComputeRequirementTemplateUsage(
        templateId="ydid:crt:000000:f00646c4-38e6-4c9a-9a40-fdbcc30be0b1",
        requirementName="my requirement for 3 nodes",
        requirementNamespace="MY_PROJECT",
        requirementTag="tests",
        targetInstanceCount=3
    )

    compute_requirement = client.compute_client.provision_compute_requirement_template(request)

Alternatively, you can provision compute directly from a source, as follows:

.. code-block:: python

    from yellowdog_client.model import OciInstancesComputeSource
    from yellowdog_client.model import ComputeRequirement
    from yellowdog_client.model import SingleSourceProvisionStrategy

    requirement = ComputeRequirement(
        name="my OCI requirement for 3 nodes"
        namespace="MY_PROJECT"
        tag="tests"
        provisionStrategy=SingleSourceProvisionStrategy(
            sources=[
                OciInstancesComputeSource(
                    name="3 OCI instances",
                    limit=3,
                    credential="MY_KEYRING/OCI_CREDENTIAL",
                    region="eu-frankfurt-1",
                    availabilityDomain="hHlw:EU-FRANKFURT-1-AD-1",
                    compartmentId="ocid1.compartment.oc1..unique_compartment_identifier",
                    subnetId="ocid1.subnet.oc1.eu-frankfurt-1.unique_subnet_identifier",
                    imageId="ocid1.image.oc1.eu-frankfurt-1.unique_image_identifier"
                )
            ]
        )
    )

    requirement = client.compute_client.add_compute_requirement(requirement)

.. note::

    To grant access to a specific cloud provider, you need to have a keyring created in
    the `YellowDog Platform Portal` along with credentials for that provider.

    In this example, a keyring named `MY_KEYRING` is used, containing a credential
    named `OCI_CREDENTIAL`.

    To create a keyring, go to `YellowDog Platform Portal`, navigate to `ACCOUNT` -> `Keyrings` ->
    `Create Keyring`

Controlling
===========

With requirements up and running, you can stop, reprovision, or terminate compute requirements, or
control individual instances.

Stopping a compute requirement will stop all active instances in the compute requirement::

    client.compute_client.stop_compute_requirement(requirement)

.. warning::

    Not all cloud providers support stopping cloud instances.

Starting a compute requirement will start all stopped instances::

    client.compute_client.start_compute_requirement(requirement)

Terminating a compute requirement will terminate all active instances::

    client.compute_client.terminate_compute_requirement(requirement)

You can also terminate individual instances of a compute requirement.

Stopping individual instances of a compute requirement::

    instance1 = requirement.instances[0]
    instance2 = requirement.instances[1]
    client.compute_client.stop_instances(requirement, [instance1, instance2])

Starting individual instances of a compute requirement::

    client.compute_client.start_instances(requirement, [instance1, instance2])

Restarting individual instances of a compute requirement::

    client.compute_client.restart_instances(requirement, [instance1, instance2])

Terminating individual instances of a compute requirement::

    client.compute_client.terminate_instances(requirement, [instance1, instance2])

.. seealso::

    :class:`yellowdog_client.compute.ComputeClient`

Work Client & Worker Pool Client
--------------------------------

The WorkClient allows you to specify the work that you want the YellowDog Scheduler to perform.

The WorkerPoolClient allows to you create worker pools to execute this work.

Finding data
============

To retrieve all created work requirements::

    work_requirements = client.work_client.find_all_work_requirements()

To retrieve information about a work requirement by its id::

    req_id = "ydid:workreq:000000:UNIQUE_ID"
    work_requirement = client.work_client.get_work_requirement_by_id(req_id)

Provisioning
============

Provisioned worker pools are linked to compute requirements and created in a similar manner::

    from datetime import timedelta
    from yellowdog_client.model import ComputeRequirementTemplateUsage
    from yellowdog_client.model import AllWorkersReleasedShutdownCondition
    from yellowdog_client.model import ProvisionedWorkerPoolProperties

    worker_pool = client.work_client.provision_worker_pool(
        ComputeRequirementTemplateUsage(
            templateId="ydid:crt:000000:UNIQUE_ID",
            requirementNamespace="my_tests",
            requirementName="HelloWorldCompute",
            targetInstanceCount=1
        ),
        ProvisionedWorkerPoolProperties(
            autoShutdownConditions=[
                AllWorkersReleasedShutdownCondition(
                    delay=timedelta(seconds=30)
                )
            ],
            workerTag="HelloWorldTag"
        )
    )

To create a work requirement, utilizing the above worker pool (linked by tag "HelloWorldTag")::

    from yellowdog_client.model import RunSpecification
    from yellowdog_client.model import Task
    from yellowdog_client.model import TaskGroup
    from yellowdog_client.model import WorkRequirement

    task = Task(
        name="EchoHelloWorld",
        taskType="docker",
        taskData="hello-world"
    )

    work_requirement = WorkRequirement(
        namespace="my_tests",
        name="HelloWorldWork",
        tag="HelloWorldTag",
        taskGroups=[
            TaskGroup(
                name="HelloWorldGroup",
                tag="",
                runSpecification=RunSpecification(
                    taskTypes=["docker"],
                    minimumQueueConcurrency=1,
                    idealQueueConcurrency=1,
                    shareWorkers=False,
                    maximumTaskRetries=3,
                    workerTags=["HelloWorldTag"]
                ),
                priority=0
            )
        ],
        priority=0
    )

    work_requirement = client.work_client.add_work_requirement(work_requirement)
    tasks = client.work_client.add_tasks_to_task_group_by_name(work_requirement.namespace, work_requirement.name,
                                                               task_group.name, [task])

Controlling
===========

To shut down a worker pool::

    client.worker_pool_client.shutdown_worker_pool(compute_requirement.id)

To cancel a work requirement::

    client.work_client.cancel_work_requirement(work_requirement)
    # WorkRequirement

.. seealso::

    :class:`yellowdog_client.scheduler.WorkClient`
    :class:`yellowdog_client.scheduler.WorkerPoolClient`

Object Store Client
-------------------

The ObjectStoreClient allows uploading and downloading files across multiple cloud providers' storage.

Finding data
============

To retrieve all uploaded objects within a namespace::

    namespace_objects = client.object_store_client.get_namespace_object_paths(ObjectPathsRequest("MY_NAMESPACE"))
    # [ObjectPath, ObjectPath, ...]

To retrieve details about a stored file::

    object_details = client.object_store_client.get_object_detail("MY_NAMESPACE", "my_file.txt")
    # ObjectDetail

Transfer engine
===============

Both uploads and downloads rely on transfer engines, which run in background threads. Uploads and downloads can be
started/stopped any time by starting/stopping the engines.

To start the transfer engines::

    client.object_store_client.start_transfers()

To stop the transfer engines::

    client.object_store_client.stop_transfers()

Uploading
=========

Once the upload engine is started, any uploads in queue will be processed and transferred to the Object Store.
To create an upload session::

    session = client.object_store_client.create_upload_session("MY_NAMESPACE", "C:/my_file.txt")

Once the session is created, it can be started to proceed with file upload. To start a session::

    session.start()

If we want to cancel an upload, the session can be aborted::

    session.abort()

All file transfers are executed in the background. To block the thread until the upload is complete, use
:mod:`concurrent.futures`::

    from yellowdog_client.object_store.model import FileTransferStatus
    from concurrent import futures

    future = session.when_status_matches(lambda status: status == FileTransferStatus.Completed)
    futures.wait((future,))

Downloading
===========

To create a download session::

    session = client.object_store_client.create_download_session(
        "MY_NAMESPACE",
        "my_remote_file.txt",
        "C:/download_directory",
        "my_downloaded_file.txt"
    )

As with upload, download sessions can be started and stopped::

    session.start()
    # Session is now started

    session.abort()
    # Session is now aborted

To wait for file download to complete, use :mod:`concurrent.futures`::

    future = session.when_status_matches(lambda status: status == FileTransferStatus.Completed)
    futures.wait((future,))

Batch transfers
===============

Multiple files can be uploaded and downloaded in a single batch. The selection of files within the directory uses
:mod:`fnmatch` match syntax.

For example, to upload multiple .zip files found within a given directory::

    upload_batch_builder = client.object_store_client.build_upload_batch()
    upload_batch_builder.find_source_objects("C:/my_files_for_upload", "*.zip")
    upload_batch_builder.namespace = "MY_NAMESPACE"
    upload_batch = upload_batch_builder.get_batch_if_objects_found()
    upload_batch.start()

To wait for all file uploads to finish::

    future = upload_batch.when_status_matches(lambda status: status == FileTransferStatus.Completed)
    futures.wait((future,))

To create a batch download of all .txt files found within the namespace::

    download_batch_builder = client.object_store_client.build_download_batch()
    download_batch_builder.destination_folder = "C:/my_downloaded_files"
    download_batch_builder.find_source_objects("MY_NAMESPACE", "*.txt")
    download_batch = download_batch_builder.get_batch_if_objects_found()
    download_batch.start()

To wait for all file downloads to finish::

    future = download_batch.when_status_matches(lambda status: status == FileTransferStatus.Completed)
    futures.wait((future,))

.. seealso::

    :class:`yellowdog_client.object_store.ObjectStoreClient`

Keyring Client
--------------

The KeyringClient allows retrieval of YellowDog keyrings and the addition/removal of
credentials from those keyrings.

Finding data
============

To retrieve all available keyrings::

    keyrings = client.keyring_client.find_all_keyrings()

Creating and editing
====================

To create a new keyring::

    keyring = client.keyring_client.create_keyring("my_keyring", "My keyring holding all the credentials")

To add new credentials to the keyring::

    from yellowdog_client.model import AwsCredential
    from yellowdog_client.model import AzureInstanceCredential

    aws_credential = AwsCredential(
        name="My aws credential",
        accessKeyId="AWS_ACCESS",
        secretAccessKey="AWS_SECRET"
    )

    azure_credential = AzureInstanceCredential(
        name="My azure credential",
        adminUserName="my_azure_username",
        adminPassword="my_azure_password"
    )

    keyring = client.keyring_client.put_credential(keyring, aws_credential)
    keyring = client.keyring_client.put_credential(keyring, azure_credential)

.. seealso::

    :class:`yellowdog_client.account.KeyringClient`

Images Client
-------------

.. seealso::

    :class:`yellowdog_client.images.ImagesClient`

Usage Client
------------

.. seealso::

    :class:`yellowdog_client.usage.AllowancesClient`
"""

from ._version import __version__ as _version
from .platform_client import PlatformClient

__all__ = [
    "PlatformClient"
]

__version__ = _version
