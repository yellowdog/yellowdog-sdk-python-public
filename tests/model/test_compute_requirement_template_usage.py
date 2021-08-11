from yellowdog_client.model import ComputeRequirementTemplateUsage
from .test_utils import should_serde


def test_serialize__compute_requirement_summary():
    obj_in_raw = ComputeRequirementTemplateUsage(
        templateId="request_templateId",
        requirementName="request_requirementName",
        requirementNamespace="request_requirementNamespace",
        requirementTag="request_requirementTag",
        targetInstanceCount=10,
        autoReprovision=True
    )

    obj_in_dict = {
        "templateId": "request_templateId",
        "requirementName": "request_requirementName",
        "requirementNamespace": "request_requirementNamespace",
        "requirementTag": "request_requirementTag",
        "targetInstanceCount": 10,
        "autoReprovision": True
    }

    should_serde(obj_in_raw, obj_in_dict)
