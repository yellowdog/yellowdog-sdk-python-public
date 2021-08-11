from yellowdog_client.common.server_sent_events.sse4python import ServerSentEvent
from yellowdog_client.model import ComputeRequirement


class TestDeserializeData(object):
    def test_obj_in_raw__expect__json_parsed(self, populated_compute_requirement_str, populated_compute_requirement):
        event = ServerSentEvent()
        event.raw_data = populated_compute_requirement_str

        obj = event.deserialize_data(class_type=ComputeRequirement)

        assert obj == populated_compute_requirement
