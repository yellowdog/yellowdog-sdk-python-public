from threading import Thread

import pytest

from yellowdog_client.object_store.utils import MemoryMappedFileReaderFactory


class TestMemoryMappedFileReader(object):
    @pytest.fixture
    def populated_file(self, tmpdir):
        p = tmpdir.mkdir("sub").join("reader.txt")
        p.write("111-222-333-444-555-666-")
        return str(p)

    def read1(self, reader):
        self.res1 = reader.read_bytes(offset=0, size=4)

    def read2(self, reader):
        self.res2 = reader.read_bytes(offset=4, size=4)

    def read3(self, reader):
        self.res3 = reader.read_bytes(offset=8, size=4)

    def read4(self, reader):
        self.res4 = reader.read_bytes(offset=12, size=4)

    def read5(self, reader):
        self.res5 = reader.read_bytes(offset=16, size=4)

    def read6(self, reader):
        self.res6 = reader.read_bytes(offset=20, size=4)

    def test_read(self, populated_file):
        with MemoryMappedFileReaderFactory.new_reader(file_path=populated_file) as reader:
            threads = [
                Thread(target=lambda: self.read1(reader)),
                Thread(target=lambda: self.read2(reader)),
                Thread(target=lambda: self.read3(reader)),
                Thread(target=lambda: self.read4(reader)),
                Thread(target=lambda: self.read5(reader)),
                Thread(target=lambda: self.read6(reader))
            ]

            [x.start() for x in threads]
            [x.join() for x in threads]

        assert self.res1 == b"111-"
        assert self.res2 == b"222-"
        assert self.res3 == b"333-"
        assert self.res4 == b"444-"
        assert self.res5 == b"555-"
        assert self.res6 == b"666-"
