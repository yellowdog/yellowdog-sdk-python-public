from datetime import datetime, timezone

import pytest

from yellowdog_client.common.json import Json
from yellowdog_client.common.iso_datetime import iso_format
from yellowdog_client.model import CloudProvider, KeyringSummary
from yellowdog_client.model import ComputeRequirement
from yellowdog_client.model import WaterfallProvisionStrategy
from yellowdog_client.model import GceInstanceGroupComputeSource
from yellowdog_client.model import SimulatorComputeSource
from yellowdog_client.model import ComputeSourceStatus
from yellowdog_client.model import ComputeRequirementStatus
from yellowdog_client.model import InstanceStatus
from yellowdog_client.model import AwsInstance
from yellowdog_client.model import AzureInstance


@pytest.fixture
def populated_compute_requirement_dict():
    obj_in_dict = {
        "tag": "req_tag",
        "namespace": "req_namespace",
        "name": "req_name",
        "provisionStrategy": {
            "sources": [
                {
                    "status": "ACTIVE",
                    "type": "co.yellowdog.platform.model.GceInstanceGroupComputeSource",
                    "assignPublicIp": True,
                    "id": "gce_id",
                    "name": "gce_name",
                    "limit": 10,
                    "statusMessage": "gce_statusMessage",
                    "credential": "gce_credential",
                    "userData": "gce_userData",
                    "sshKeys": "gce_sshKeys",
                    "project": "gce_project",
                    "region": "gce_region",
                    "zone": "gce_zone",
                    "machineType": "gce_machineType",
                    "image": "gce_image",
                    "network": "gce_network",
                    "subnetwork": "gce_subnetwork",
                    "preemptible": True,
                    "acceleratorCount": 0
                },
                {
                    "status": "ERRORED",
                    "type": "co.yellowdog.platform.model.SimulatorComputeSource",
                    "name": "simulator_name",
                    "limit": 20,
                    "instanceStartupTimeSeconds": 30,
                    "instanceStartupTimeVariance": 40.0,
                    "instanceShutdownTimeSeconds": 50,
                    "instanceShutdownTimeVariance": 60.0,
                    "unexpectedInstanceTerminationProbabilityPerSecond": 70.0,
                    "region": "sim-region",
                    "instanceType": "sim-instance",
                    "imageId": "sim-image",
                    "id": "simulator_id",
                    "statusMessage": "simulator_message",
                }
            ],
            "type": "co.yellowdog.platform.model.WaterfallProvisionStrategy"
        },
        "targetInstanceCount": 20,
        "status": "STOPPED",
        "id": "req_id",
        "createdTime": iso_format(datetime(2010, 12, 31, 18, 30, 45, 123456)),
        "instances": [
            {
                "type": "co.yellowdog.platform.model.AwsInstance",
                "instanceLifecycle": "aws_instanceLifecycle",
                "createdTime": iso_format(datetime(2011, 12, 31, 18, 30, 45, 123456)),
                "id": "aws_id",
                "imageId": "aws_imageId",
                "instanceType": "aws_instanceType",
                "provider": "AWS",
                "region": "aws_region",
                "status": "STOPPED",
                "subregion": "aws_subregion",
                "privateIpAddress": "aws_privateIpAddress",
                "publicIpAddress": "aws_publicIpAddress",
                "hostname": "aws_hostname"
            },
            {
                "type": "co.yellowdog.platform.model.AzureInstance",
                "createdTime": iso_format(datetime(2012, 12, 31, 18, 30, 45, 123456)),
                "id": "azure_id",
                "imageId": "azure_imageId",
                "instanceType": "azure_instanceType",
                "provider": "AZURE",
                "region": "azure_region",
                "status": "RUNNING",
                "subregion": "azure_subregion",
                "privateIpAddress": "azure_privateIpAddress",
                "publicIpAddress": "azure_publicIpAddress",
                "hostname": "azure_hostname"
            }
        ],
        "nextStatus": "TERMINATING",
        "autoReprovision": True,
        "statusChangedTime": iso_format(datetime(2013, 12, 31, 18, 30, 45, 123456)),
        "createdById": "123"
    }
    return obj_in_dict


@pytest.fixture
def populated_compute_requirement_str(populated_compute_requirement_dict):
    return Json.dumps(populated_compute_requirement_dict)


@pytest.fixture
def populated_compute_requirement():
    instance_aws = AwsInstance()
    instance_aws.instanceLifecycle = "aws_instanceLifecycle"
    instance_aws.createdTime = datetime(2011, 12, 31, 18, 30, 45, 123000, timezone.utc)
    instance_aws.id = "aws_id"
    instance_aws.imageId = "aws_imageId"
    instance_aws.instanceType = "aws_instanceType"
    instance_aws.provider = CloudProvider.AWS
    instance_aws.region = "aws_region"
    instance_aws.status = InstanceStatus.STOPPED
    instance_aws.subregion = "aws_subregion"
    instance_aws.privateIpAddress = "aws_privateIpAddress"
    instance_aws.publicIpAddress = "aws_publicIpAddress"
    instance_aws.hostname = "aws_hostname"

    instance_azure = AzureInstance()
    instance_azure.createdTime = datetime(2012, 12, 31, 18, 30, 45, 123000, timezone.utc)
    instance_azure.id = "azure_id"
    instance_azure.imageId = "azure_imageId"
    instance_azure.instanceType = "azure_instanceType"
    instance_azure.provider = CloudProvider.AZURE
    instance_azure.region = "azure_region"
    instance_azure.status = InstanceStatus.RUNNING
    instance_azure.subregion = "azure_subregion"
    instance_azure.privateIpAddress = "azure_privateIpAddress"
    instance_azure.publicIpAddress = "azure_publicIpAddress"
    instance_azure.hostname = "azure_hostname"

    compute_source_gce = GceInstanceGroupComputeSource(
        name="gce_name",
        limit=10,
        credential="gce_credential",
        assignPublicIp=True,
        userData="gce_userData",
        sshKeys="gce_sshKeys",
        project="gce_project",
        region="gce_region",
        zone="gce_zone",
        machineType="gce_machineType",
        image="gce_image",
        network="gce_network",
        subnetwork="gce_subnetwork",
        preemptible=True
    )
    compute_source_gce.id = "gce_id"
    compute_source_gce.status = ComputeSourceStatus.ACTIVE
    compute_source_gce.statusMessage = "gce_statusMessage"

    compute_source_simulator = SimulatorComputeSource(
        name="simulator_name",
        limit=20,
        instanceStartupTimeSeconds=30,
        instanceStartupTimeVariance=40.0,
        instanceShutdownTimeSeconds=50,
        instanceShutdownTimeVariance=60.0,
        unexpectedInstanceTerminationProbabilityPerSecond=70.0
    )
    compute_source_simulator.id = "simulator_id"
    compute_source_simulator.status = ComputeSourceStatus.ERRORED
    compute_source_simulator.statusMessage = "simulator_message"

    obj_in_raw = ComputeRequirement(
        namespace="req_namespace",
        name="req_name",
        provisionStrategy=WaterfallProvisionStrategy(
            sources=[compute_source_gce, compute_source_simulator]
        )
    )
    obj_in_raw.id = "req_id"
    obj_in_raw.tag = "req_tag"
    obj_in_raw.createdTime = datetime(2010, 12, 31, 18, 30, 45, 123000, timezone.utc)
    obj_in_raw.targetInstanceCount = 20
    obj_in_raw.instances = [instance_aws, instance_azure]
    obj_in_raw.status = ComputeRequirementStatus.STOPPED
    obj_in_raw.nextStatus = ComputeRequirementStatus.TERMINATING
    obj_in_raw.autoReprovision = True
    obj_in_raw.statusChangedTime = datetime(2013, 12, 31, 18, 30, 45, 123000, timezone.utc)
    obj_in_raw.createdById = "123"

    return obj_in_raw


@pytest.fixture
def keyring_summary_dict():
    return {
        'id': 'my_id',
        'name': 'my_name',
        'description': 'my_description'
    }


@pytest.fixture
def keyring_summary():
    return KeyringSummary(
        id="my_id",
        name="my_name",
        description="my_description"
    )
