from datetime import datetime, timezone, timedelta

import pytest

from yellowdog_client.common.iso_datetime import iso_format
from yellowdog_client.model import RunSpecification
from yellowdog_client.model import CloudProvider
from yellowdog_client.model import Task
from yellowdog_client.model import FlattenPath
from yellowdog_client.model import TaskInput
from yellowdog_client.model import TaskInputSource
from yellowdog_client.model import TaskOutput
from yellowdog_client.model import TaskOutputSource
from yellowdog_client.model import TaskStatus
from yellowdog_client.model import TaskGroup
from yellowdog_client.model import TaskGroupStatus
from yellowdog_client.model import WorkRequirement
from yellowdog_client.model import WorkRequirementStatus
from yellowdog_client.model import AllWorkersReleasedShutdownCondition
from yellowdog_client.model import NoRegisteredWorkersShutdownCondition
from yellowdog_client.model import ProvisionedWorkerPoolProperties
from yellowdog_client.model import ComputeRequirementTemplateUsage
from yellowdog_client.model import DoubleRange


@pytest.fixture
def run_specification_raw():
    return RunSpecification(
        instanceTypes=["instance_type1", "instance_type2"],
        taskTypes=["type1", "type2", "type3"],
        maximumTaskRetries=5,
        providers=[CloudProvider.OCI, CloudProvider.GOOGLE],
        regions=["region1", "region2"],
        workerTags=["tag1", "tag2"],
        vcpus=DoubleRange(min=3.0)
    )


@pytest.fixture
def run_specification_dict():
    return {
        "instanceTypes": ["instance_type1", "instance_type2"],
        "taskTypes": ["type1", "type2", "type3"],
        "maximumTaskRetries": 5,
        "providers": ["OCI", "GOOGLE"],
        "regions": ["region1", "region2"],
        "workerTags": ["tag1", "tag2"],
        "vcpus": {"min": 3.0}
    }


@pytest.fixture
def task_raw():
    obj_in_raw = Task(
        name="my_name",
        tag="my_tag",
        taskType="my_task_type",
        taskData="my_data",
        environment={"ENV1": "VAL1", "ENV2": "VAL2", "ENV3": "VAL3"},
        inputs=[
            TaskInput(
                source=TaskInputSource.OTHER_NAMESPACE,
                namespace="input1_namespace",
                objectNamePattern="input1_objectNamePattern"
            ),
            TaskInput(
                source=TaskInputSource.OTHER_NAMESPACE,
                namespace="input2_namespace",
                objectNamePattern="input2_objectNamePattern"
            ),
            TaskInput(
                source=TaskInputSource.TASK_NAMESPACE,
                namespace="input3_namespace",
                objectNamePattern="input3_objectNamePattern"
            )
        ],
        flattenInputPaths=FlattenPath.REPLACE_PATH_SEPERATOR,
        outputs=[
            TaskOutput(
                source=TaskOutputSource.WORKER_DIRECTORY,
                directoryName="output1_directoryName",
                filePattern="output1_filePattern",
                uploadOnFailed=True
            ),
            TaskOutput(
                source=TaskOutputSource.PROCESS_OUTPUT,
                directoryName="output2_directoryName",
                filePattern="output2_filePattern",
                uploadOnFailed=False
            ),
            TaskOutput(
                source=TaskOutputSource.OTHER_DIRECTORY,
                directoryName="output3_directoryName",
                filePattern="output3_filePattern",
                uploadOnFailed=True
            )
        ]
    )
    obj_in_raw.id = "my_id"
    obj_in_raw.fullyQualifiedName = "my_fullyQualifiedName"
    obj_in_raw.status = TaskStatus.COMPLETED
    obj_in_raw.retryCount = 100
    obj_in_raw.startedTime = datetime(2011, 12, 31, 18, 30, 45, 123000, timezone.utc)
    obj_in_raw.finishedTime = datetime(2012, 12, 31, 18, 30, 45, 123000, timezone.utc)
    obj_in_raw.taskGroupId = "my_taskGroupId"
    obj_in_raw.workerId = "my_workerId"
    return obj_in_raw


@pytest.fixture
def task_dict():
    return {
        "name": "my_name",
        "tag": "my_tag",
        "taskType": "my_task_type",
        "taskData": "my_data",
        "environment": {"ENV1": "VAL1", "ENV2": "VAL2", "ENV3": "VAL3"},
        "inputs": [
            {
                "source": "OTHER_NAMESPACE",
                "namespace": "input1_namespace",
                "objectNamePattern": "input1_objectNamePattern",
                "required": False
            },
            {
                "source": "OTHER_NAMESPACE",
                "namespace": "input2_namespace",
                "objectNamePattern": "input2_objectNamePattern",
                "required": False
            },
            {
                "source": "TASK_NAMESPACE",
                "namespace": "input3_namespace",
                "objectNamePattern": "input3_objectNamePattern",
                "required": False
            }
        ],
        "flattenInputPaths": "REPLACE_PATH_SEPERATOR",
        "outputs": [
            {
                "source": "WORKER_DIRECTORY",
                "directoryName": "output1_directoryName",
                "filePattern": "output1_filePattern",
                "uploadOnFailed": True,
                "required": False
            },
            {
                "source": "PROCESS_OUTPUT",
                "directoryName": "output2_directoryName",
                "filePattern": "output2_filePattern",
                "uploadOnFailed": False,
                "required": False
            },
            {
                "source": "OTHER_DIRECTORY",
                "directoryName": "output3_directoryName",
                "filePattern": "output3_filePattern",
                "uploadOnFailed": True,
                "required": False
            }
        ],
        "status": "COMPLETED",
        "id": "my_id",
        "fullyQualifiedName": "my_fullyQualifiedName",
        "retryCount": 100,
        "startedTime": iso_format(datetime(2011, 12, 31, 18, 30, 45, 123456)),
        "finishedTime": iso_format(datetime(2012, 12, 31, 18, 30, 45, 123456)),
        "taskGroupId": "my_taskGroupId",
        "workerId": "my_workerId"
    }


@pytest.fixture
def machine_configuration_dict():
    return {
        'instanceType': 'my_instanceType',
        'imageId': 'my_imageId'
    }


@pytest.fixture
def task_group_raw(task_raw, run_specification_raw):
    obj_in_raw = TaskGroup(
        name="my_name",
        tag="my_tag",
        runSpecification=run_specification_raw,
        priority=5,
        dependentOn="my_dependent_on"
    )
    obj_in_raw.id = "my_id"
    obj_in_raw.status = TaskGroupStatus.STARVED
    obj_in_raw.statusChangedTime = datetime(2015, 12, 31, 18, 30, 45, 123000, timezone.utc)
    return obj_in_raw


@pytest.fixture
def task_group_dict(task_dict, run_specification_dict):
    return {
        "name": "my_name",
        "tag": "my_tag",
        "runSpecification": run_specification_dict,
        "priority": 5,
        "dependentOn": "my_dependent_on",
        "status": "STARVED",
        "id": "my_id",
        "statusChangedTime": iso_format(datetime(2015, 12, 31, 18, 30, 45, 123456)),
        "autoComplete": True,
        "autoFail": True
    }


@pytest.fixture
def work_requirement_raw(task_group_raw):
    obj_in_raw = WorkRequirement(
        namespace="my_namespace",
        name="my_name",
        tag="my_tag",
        taskGroups=[task_group_raw, task_group_raw, task_group_raw],
        priority=50,
        fulfilOnSubmit=True
    )
    obj_in_raw.id = "my_id"
    obj_in_raw.createdTime = datetime(2014, 12, 31, 18, 30, 45, 123000, timezone.utc)
    obj_in_raw.statusChangedTime = datetime(2015, 12, 31, 18, 30, 45, 123000, timezone.utc)
    obj_in_raw.status = WorkRequirementStatus.UNFULFILLED
    return obj_in_raw


@pytest.fixture
def work_requirement_dict(task_group_dict):
    return {
        "namespace": "my_namespace",
        "name": "my_name",
        "tag": "my_tag",
        "taskGroups": [task_group_dict, task_group_dict, task_group_dict],
        "priority": 50,
        "fulfilOnSubmit": True,
        "status": "UNFULFILLED",
        "id": "my_id",
        "createdTime": iso_format(datetime(2014, 12, 31, 18, 30, 45, 123456)),
        "statusChangedTime": iso_format(datetime(2015, 12, 31, 18, 30, 45, 123456))
    }


@pytest.fixture
def provisioned_worker_pool_properties_raw():
    return ProvisionedWorkerPoolProperties(
        nodeBootTimeLimit=timedelta(minutes=30, seconds=15),
        autoShutdownConditions=[
            AllWorkersReleasedShutdownCondition(delay=timedelta(minutes=3)),
            NoRegisteredWorkersShutdownCondition()
        ]
    )


@pytest.fixture
def provisioned_worker_pool_properties_dict():
    return {
        "nodeBootTimeLimit": "PT30M15S",
        "autoShutdownConditions": [
            {
                "delay": "PT3M",
                "type": "co.yellowdog.platform.model.AllWorkersReleasedShutdownCondition"
            },
            {
                "type": "co.yellowdog.platform.model.NoRegisteredWorkersShutdownCondition"
            }
        ]
    }


@pytest.fixture
def compute_requirement_template_dict():
    return {
        "id": "template_id",
        "name": "template_name",
        "description": "template_description",
        "provisionStrategy": {
            "type": "co.yellowdog.platform.model.SplitProvisionStrategy",
            "sources": [
                {
                    "id": "simulator_id",
                    "type": "co.yellowdog.platform.model.SimulatorComputeSource",
                    "name": "simulator_name",
                    "limit": 20,
                    "instanceStartupTimeSeconds": 30,
                    "instanceStartupTimeVariance": 40.0,
                    "instanceShutdownTimeSeconds": 50,
                    "instanceShutdownTimeVariance": 60.0,
                    "unexpectedInstanceTerminationProbabilityPerSecond": 70.0,
                    "maximumInstancesAvailable": 80,
                    "status": "ERRORED",
                    "statusMessage": "simulator_message"
                }
            ]
        }
    }


@pytest.fixture
def compute_requirement_template_usage_raw():
    return ComputeRequirementTemplateUsage(
        templateId="request_templateId",
        requirementName="request_requirementName",
        requirementNamespace="request_requirementNamespace",
        requirementTag="request_requirementTag",
        targetInstanceCount=10
    )


@pytest.fixture
def compute_requirement_template_usage_dict():
    return {
        "templateId": "request_templateId",
        "requirementName": "request_requirementName",
        "requirementNamespace": "request_requirementNamespace",
        "requirementTag": "request_requirementTag",
        "targetInstanceCount": 10
    }
