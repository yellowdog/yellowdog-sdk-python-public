from .test_utils import should_serde


def test_serialize__keyring_summary(keyring_summary, keyring_summary_dict):
    should_serde(keyring_summary, keyring_summary_dict)
