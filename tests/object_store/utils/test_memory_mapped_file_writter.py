import pytest
from threading import Thread
from yellowdog_client.object_store.utils import MemoryMappedFileWriterFactory


class TestMemoryMappedFileWriter(object):
    @pytest.fixture
    def file_path(self, tmpdir):
        p = tmpdir.mkdir("sub").join("writter.txt")
        return str(p)

    def write(self, writer, offset, str_bytes):
        writer.write_bytes(offset=offset, str_bytes=str_bytes)

    def test_write_bytes(self, file_path):
        with MemoryMappedFileWriterFactory.new_writer(file_path=file_path, file_size=24) as writer:
            threads = [
                Thread(target=lambda: self.write(writer, 0, "111-")),
                Thread(target=lambda: self.write(writer, 4, "222-")),
                Thread(target=lambda: self.write(writer, 8, "333-")),
                Thread(target=lambda: self.write(writer, 12, "444-")),
                Thread(target=lambda: self.write(writer, 16, "555-")),
                Thread(target=lambda: self.write(writer, 20, "666-"))
            ]

            [x.start() for x in threads]
            [x.join() for x in threads]

        with open(file_path, "r") as f:
            text = f.read()
            assert text == "111-222-333-444-555-666-"
