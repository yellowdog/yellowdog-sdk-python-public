import pytest

from yellowdog_client.object_store.utils import FnmatchUtils


@pytest.mark.parametrize("input,expected", [
    ("some/path/to/a/file", False),
    ("some/path/*/files", True),
    ("a/long/but/not/interesting/folder/path/", False),
    ("some/path/to??fu.txt", True),
    ("normal_file_name.txt", False),
    ("some/path/[a-z]/test.txt", True),
    ("some/path/[!a-z]/test.txt", True)
])
def test_should_detect_ant_patterns(input: str, expected: bool):
    assert FnmatchUtils.uses_path_pattern(input) == expected


@pytest.mark.parametrize("input,expected", [
    ("some/path/to/a/file", "some/path/to/a/"),
    ("some/path/*/files", "some/path/"),
    ("a/long/but/not/interesting/folder/path/", "a/long/but/not/interesting/folder/path/"),
    ("some/path/to??fu.txt", "some/path/"),
    ("normal_file_name.txt", None),
    ("some/path/[a-z]/test.txt", "some/path/"),
    ("some/path/[!a-z]/test.txt", "some/path/")
])
def test_should_extract_path_prefix(input: str, expected: str):
    assert FnmatchUtils.get_prefix_before_path_patterns(input) == expected
