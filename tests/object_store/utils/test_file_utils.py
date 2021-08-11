import pytest
from yellowdog_client.object_store.utils import FileUtils
from yellowdog_client.object_store.utils.file_utils import TimeoutException


class TestFileUtils(object):
    @pytest.fixture
    def env_mocks(self, mocker):
        self.os = mocker.patch("yellowdog_client.object_store.utils.file_utils.os")
        self.shutil = mocker.patch("yellowdog_client.object_store.utils.file_utils.shutil")
        self.time = mocker.patch("yellowdog_client.object_store.utils.file_utils.time")

    def test__rename__destination_already_exists__no_failures__destination_removed_expect_no_exception(self, env_mocks):
        self.os.path.isfile.return_value = True
        self.time.time.side_effect = [1, 2]

        FileUtils.rename_replace(source_file_path="C:/source.txt", destination_file_path="C:/destination.txt")

        self.os.remove.assert_called_once_with("C:/destination.txt")
        self.shutil.move.assert_called_once_with("C:/source.txt", "C:/destination.txt")

    def test__rename__one_failure__succeeds_on_second_try__expect_no_exception(self, env_mocks):
        self.os.path.isfile.return_value = False
        self.time.time.side_effect = [1, 2, 3]
        self.shutil.move.side_effect = [IOError("failing"), True]

        FileUtils.rename_replace(source_file_path="C:/source.txt", destination_file_path="C:/destination.txt")

        self.shutil.move.assert_any_call("C:/source.txt", "C:/destination.txt")

    def test__rename__all_failures__expect_timeout_exception(self, env_mocks):
        self.os.path.isfile.return_value = False
        self.time.time.side_effect = [1, 2, 3, 4, 5, 6, 7, 8]
        self.shutil.move.side_effect = IOError("failing")

        with pytest.raises(TimeoutException):
            FileUtils.rename_replace(source_file_path="C:/source.txt", destination_file_path="C:/destination.txt")

        self.shutil.move.assert_any_call("C:/source.txt", "C:/destination.txt")

