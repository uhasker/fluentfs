import datetime
import os
from typing import Any

from fluentfs.exceptions.exceptions import FluentFsException
from fluentfs.filelike.file_like import FileLike
from fluentfs.filesize.file_size import FileSize
from fluentfs.paths.paths import file_exists


class File(FileLike):
    def __init__(
        self, path: str, expand_user: bool = True, expand_vars: bool = True
    ) -> None:
        super(File, self).__init__(
            path, expand_user=expand_user, expand_vars=expand_vars
        )

        if not file_exists(self.path):
            raise FluentFsException(f"There is no (regular) file at {path}")

    @property
    def bytes(self) -> bytes:
        """
        The content of the file.

        :return: The content bytes.
        """
        with open(self.path, "rb") as file:
            return file.read()

    @property
    def byte_count(self) -> int:
        """
        The number of bytes of this file.

        This is similar to `wc -c $FILENAME`.

        :return: The number of bytes.
        """
        return os.path.getsize(self.path)

    dir: Any

    @property
    def extension(self) -> str:
        """
        The extension of this file.

        :return: The extension. If the file has no extension, an empty string will be
            returned. Otherwise, the extension *without* the preceding dot will be returned
            (e.g. "txt", *not* ".txt").
        """
        _, ext = os.path.splitext(self.path)
        return ext[1:] if len(ext) > 0 else ext

    ext = extension

    @property
    def size(self) -> FileSize:
        """
        The size of this file.

        :return: A FileSize object representing the size of this file (in bytes).
        """
        return FileSize(self.byte_count)

    @property
    def access_time(self) -> datetime.datetime:
        """
        The last access time of this file.

        :return: A datetime object representing the last access time.
        """
        atime = os.path.getatime(self.path)
        return datetime.datetime.fromtimestamp(atime)

    atime = access_time

    @property
    def mod_time(self) -> datetime.datetime:
        """
        The last modification time of this file.

        :return: A datetime object representing the last modification time.
        """
        mtime = os.path.getmtime(self.path)
        return datetime.datetime.fromtimestamp(mtime)

    mtime = mod_time

    def __lt__(self, other: "File") -> bool:
        return self.size < other.size

    def __repr__(self) -> str:
        return f'File("{self.path}")'

    # these attributes are created in the TextFile class
    t: Any
    text_file: Any
