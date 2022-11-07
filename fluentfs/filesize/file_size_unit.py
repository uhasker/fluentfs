from enum import Enum

from fluentfs.exceptions.exceptions import FluentFsException


class FileSizeUnit(Enum):
    AUTO = 0
    BYTE = 1
    KB = 2
    MB = 3
    GB = 4
    TB = 5
    KIB = 6
    MIB = 7
    GIB = 8
    TIB = 9

    def __repr__(self) -> str:
        if self == FileSizeUnit.AUTO:
            raise FluentFsException("FileSizeUnit.AUTO has no string representation")

        return {
            FileSizeUnit.BYTE: "B",
            FileSizeUnit.KB: "KB",
            FileSizeUnit.MB: "MB",
            FileSizeUnit.GB: "GB",
            FileSizeUnit.TB: "TB",
            FileSizeUnit.KIB: "KiB",
            FileSizeUnit.MIB: "MiB",
            FileSizeUnit.GIB: "GiB",
            FileSizeUnit.TIB: "TiB",
        }[self]

    def __str__(self) -> str:
        return repr(self)
