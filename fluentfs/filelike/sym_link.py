import os
from typing import Union, cast

from fluentfs.exceptions.exceptions import FluentFsException
from fluentfs.filelike.dir import Dir
from fluentfs.filelike.file import File
from fluentfs.filelike.file_like import FileLike
from fluentfs.paths.paths import FileLikeKind, file_like_kind, symlink_exists


def _file_like_from_path(path: str) -> FileLike:
    """
    Get the respective file-like object from the given path.

    If no file-like object is present at the given path, a FluentFsException is raised.

    :param path: The given path.
    :return: A Dir object if a directory is present, a File object if a (regular) file
        is present and a SymLink object if a symbolic link is present.
    """
    kind = file_like_kind(path)
    if kind == FileLikeKind.DIR:
        return Dir(path)
    if kind == FileLikeKind.FILE:
        return File(path)
    if kind == FileLikeKind.SYMLINK:
        return SymLink(path)

    raise FluentFsException(
        f"no file-like object present at path {path}"
    )  # pragma: no cover


class SymLink(FileLike):
    def __init__(
        self, path: str, expand_user: bool = True, expand_vars: bool = True
    ) -> None:
        super().__init__(path, expand_user=expand_user, expand_vars=expand_vars)

        if not symlink_exists(self.path):
            raise FluentFsException(f"There is no symbolic link at {path}")

    @property
    def target(self) -> FileLike:
        """
        The immediate target of this symbolic link.

        For example if you have a symbolic link c.txt pointing to b.txt, which in turn
        points to a.txt, then this property will return b.txt and *NOT* a.txt.
        """
        target_path = os.readlink(self.path)
        return _file_like_from_path(target_path)

    @property
    def final_target(self) -> Union[File, Dir]:
        """
        The final target of this symbolic link.

        For example if you have a symbolic link c.txt pointing to b.txt, which in turn
        points to a.txt, then this property will return a.txt and *NOT* b.txt.
        """
        target_path = os.readlink(self.path)
        while symlink_exists(target_path):
            target_path = os.readlink(target_path)
        return cast(Union[File, Dir], _file_like_from_path(target_path))

    def __repr__(self) -> str:
        return f'SymLink("{self.path}")'
