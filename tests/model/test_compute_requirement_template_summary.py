from yellowdog_client.model import ComputeRequirementTemplateSummary
from .test_utils import should_serde


def test_serialize__compute_requirement_summary():
    obj_in_raw = ComputeRequirementTemplateSummary()
    obj_in_raw.id = "summary_id"
    obj_in_raw.name = "summary_name"
    obj_in_raw.description = "summary_description"

    obj_in_dict = {
        "id": "summary_id",
        "name": "summary_name",
        "description": "summary_description"
    }

    should_serde(obj_in_raw, obj_in_dict)
