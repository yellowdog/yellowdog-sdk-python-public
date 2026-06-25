from yellowdog_client.model.failure_policy import failure
from yellowdog_client.model.resubmission_destination import destination


def test_failure_policy_factory_function():
    destinations = [destination(toTaskGroup="some-task-group")]
    failure_policy = failure(destinations)
    assert failure_policy.resubmissionDestinations == destinations
