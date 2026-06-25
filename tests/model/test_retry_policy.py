from yellowdog_client.model import TaskErrorSelector
from yellowdog_client.model.retry_policy import retry
from yellowdog_client.model.selection import includes


def test_retry_policy_factory_function():
    retry_policy = retry(max=1)
    assert retry_policy.maxRetries == 1
    assert retry_policy.retryErrors is None

def test_retry_policy_factory_function_given_retry_errors():
    when = includes([TaskErrorSelector()])
    retry_policy = retry(max=1, when=when)
    assert retry_policy.maxRetries == 1
    assert retry_policy.retryErrors == when
