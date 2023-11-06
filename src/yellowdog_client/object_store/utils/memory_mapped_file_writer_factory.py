from .memory_mapped_file_writter import MemoryMappedFileWriter


class MemoryMappedFileWriterFactory(object):
    @staticmethod
    def new_writer(file_path: str, file_size: int) -> MemoryMappedFileWriter:
        return MemoryMappedFileWriter(file_path=file_path, file_size=file_size)
