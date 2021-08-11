from enum import Enum


class FlattenPath(Enum):
    """Indicates which path flattening strategy should be applied when downloading task inputs."""
    FILE_NAME_ONLY = "FILE_NAME_ONLY"
    """Save the file to the working directory with just its file name."""
    REPLACE_PATH_SEPERATOR = "REPLACE_PATH_SEPERATOR"
    """Save the file to the working directory including directories in the output file name, separated by an underscore."""

    def __str__(self) -> str:
        return self.name
