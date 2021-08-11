from yellowdog_client.common.json import Json


class ServerSentEvent(object):
    last_event_id: str = None
    event_type: str = None
    raw_data: str = None
    retry: bool = None

    def deserialize_data(self, class_type):
        return Json.loads(self.raw_data, class_type)
