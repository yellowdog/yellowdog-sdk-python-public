from yellowdog_client.model import ProvisionedWorkerPoolProperties
from .test_utils import should_serde


def test_serialize_empty():
    obj_in_raw = ProvisionedWorkerPoolProperties()

    obj_in_dict = {
        'type': 'co.yellowdog.platform.model.ProvisionedWorkerPoolProperties'
    }

    should_serde(obj_in_raw, obj_in_dict)


def test_serialize_populated(provisioned_worker_pool_properties_raw, provisioned_worker_pool_properties_dict):
    should_serde(provisioned_worker_pool_properties_raw, provisioned_worker_pool_properties_dict)
