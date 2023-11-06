from .memory_mapped_file_reader import MemoryMappedFileReader


class MemoryMappedFileReaderFactory(object):
    @staticmethod
    def new_reader(file_path: str) -> MemoryMappedFileReader:
        return MemoryMappedFileReader(file_path=file_path)
