import os
from collections.abc import Iterator
from enum import Enum

from fluentfs.common.functional import FunctionalIterator
from fluentfs.exceptions.exceptions import FluentFsException
from fluentfs.filelike.file import File
from fluentfs.filelike.file_iterator import FileIterator
from fluentfs.filelike.file_like import FileLike
from fluentfs.paths.paths import dir_exists, file_exists


class _FileTreeWalkIteratorKind(Enum):
    FILE_LIKES = 0
    FILES_ONLY = 1
    DIRS_ONLY = 2


class _FileTreeWalkIterator(Iterator):
    def __init__(self, path: str, kind: _FileTreeWalkIteratorKind) -> None:
        self.walk_iterator = os.walk(path)
        self.path = path

        self.process_dirs = (
            kind == _FileTreeWalkIteratorKind.FILE_LIKES
            or kind == _FileTreeWalkIteratorKind.DIRS_ONLY
        )
        self.process_files = (
            kind == _FileTreeWalkIteratorKind.FILE_LIKES
            or kind == _FileTreeWalkIteratorKind.FILES_ONLY
        )

        self.sub_dir_path, _, file_names = next(self.walk_iterator)
        self.dir_processed = False
        self.current_file_names = sorted(file_names)

    def __next__(self) -> FileLike:
        if not self.dir_processed and self.process_dirs:
            self.dir_processed = True

            # We don't need to check if self.sub_dir_path is a symlink
            # since os.walk does not descend into symlink directories.

            # We don't expand user and vars since this will lead to incorrect paths
            # if we e.g. have a directory called "~" or "dir $SOME_VAR".
            return Dir(self.sub_dir_path, expand_user=False, expand_vars=False)

        if len(self.current_file_names) != 0 and self.process_files:
            file_name, *self.current_file_names = self.current_file_names
            file_path = os.path.join(self.sub_dir_path, file_name)

            if not file_exists(file_path):
                return next(self)

            # We don't expand user and vars since this will lead to incorrect paths
            # if we e.g. have a file called "~" or "dir $SOME_VAR".
            return File(file_path, expand_user=False, expand_vars=False)

        try:
            self.sub_dir_path, _, file_names = next(self.walk_iterator)
            self.current_file_names = sorted(file_names)
            self.dir_processed = False
            return next(self)
        except StopIteration:
            raise StopIteration


class Dir(FileLike):
    def __init__(
        self, path: str, expand_user: bool = True, expand_vars: bool = True
    ) -> None:
        super(Dir, self).__init__(
            path, expand_user=expand_user, expand_vars=expand_vars
        )

        if not dir_exists(self.path):
            raise FluentFsException(f"There is no directory at {path}")

    def file(self, file_name: str) -> "File":
        """
        The file with the given name located in this directory.

        :param file_name: The file name.
        :return: A File object representing the given file.
        """
        return File(os.path.join(self.path, file_name))

    def dir(self, subdir_name: str) -> "Dir":
        """
        The directory with the given name located in this directory.

        :param subdir_name: The name of the directory.
        :return: A Dir object representing the given directory.
        """
        return Dir(os.path.join(self.path, subdir_name))

    @property
    def file_likes(self) -> FunctionalIterator[FileLike]:
        """
        An iterator of file-like objects present in this directory and all subdirectories.

        :return: The iterator.
        """
        return FunctionalIterator(
            _FileTreeWalkIterator(self.path, _FileTreeWalkIteratorKind.FILE_LIKES)
        )

    @property
    def files(self) -> "FileIterator":
        """
        An iterator of (regular) files present in this directory and all subdirectories.

        :return: The iterator.
        """
        return FileIterator(
            _FileTreeWalkIterator(self.path, _FileTreeWalkIteratorKind.FILES_ONLY)
        )

    @property
    def dirs(self) -> FunctionalIterator["Dir"]:
        """
        An iterator of all directories present in this directory and all subdirectories.

        :return: The iterator.
        """
        return FunctionalIterator(
            _FileTreeWalkIterator(self.path, _FileTreeWalkIteratorKind.DIRS_ONLY)
        )

    def __repr__(self) -> str:
        return f'Dir("{self.path}")'
