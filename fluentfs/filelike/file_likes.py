import datetime
import os
from enum import Enum
from typing import Any, Iterator, List, TypeVar, Union

from fluentfs.common import compile_regex
from fluentfs.common.functional import FunctionalIterator
from fluentfs.exceptions.exceptions import FluentFsException
from fluentfs.filelike.file_like import FileLike
from fluentfs.filesize.file_size import FileSize
from fluentfs.paths.matches import (
    matches_base_path,
    matches_compiled_regex,
    matches_glob,
)
from fluentfs.paths.paths import dir_exists, file_exists


class File(FileLike):
    def __init__(self, path: str) -> None:
        super(File, self).__init__(path)

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

    @property
    def dir(self) -> "Dir":
        """
        The directory containing this file.

        :return: A Dir object representing the directory.
        """
        return Dir(os.path.dirname(self.path))

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


class _FileTreeWalkIteratorKind(Enum):
    FILE_LIKES = 0
    FILES_ONLY = 1
    DIRS_ONLY = 2


class _FileTreeWalkIterator(Iterator):
    def __init__(self, path: str, kind: _FileTreeWalkIteratorKind) -> None:
        self.it = os.walk(path)
        self.path = path

        self.process_dirs = (
            kind == _FileTreeWalkIteratorKind.FILE_LIKES
            or kind == _FileTreeWalkIteratorKind.DIRS_ONLY
        )
        self.process_files = (
            kind == _FileTreeWalkIteratorKind.FILE_LIKES
            or kind == _FileTreeWalkIteratorKind.FILES_ONLY
        )

        self.sub_dir_path, _, file_names = next(self.it)
        self.sub_dir_processed = False
        self.file_names = sorted(file_names)

    def __next__(self) -> FileLike:
        if not self.sub_dir_processed and self.process_dirs:
            self.sub_dir_processed = True
            return Dir(self.sub_dir_path)

        if len(self.file_names) != 0 and self.process_files:
            file_name, *self.file_names = self.file_names
            return File(os.path.join(self.sub_dir_path, file_name))

        try:
            self.sub_dir_path, _, file_names = next(self.it)
            self.file_names = sorted(file_names)
            self.sub_dir_processed = False
            return next(self)
        except StopIteration:
            raise StopIteration


class Dir(FileLike):
    def __init__(self, path: str) -> None:
        super(Dir, self).__init__(path)

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


T = TypeVar("T", bound=File)
TFileIterator = TypeVar("TFileIterator", bound="FileIterator")


class FileIterator(FunctionalIterator[T]):
    def filter_extension(
        self: TFileIterator, extension: Union[str, List[str]]
    ) -> TFileIterator:
        """
        Filter the files by extension.

        :param extension: Either a single extension or a list of extensions.
            Note that extensions must be given without the preceding dot, e.g. "txt"
            instead of ".txt".
        :return: A file iterator containing the files that have the given extension.
        """
        if isinstance(extension, str):
            extension = [extension]
        return self.filter(lambda file: file.extension in extension)

    filter_ext = filter_extension
    include_extension = filter_extension
    include_ext = filter_extension

    def filter_base_path(
        self: TFileIterator, base_paths: Union[str, List[str]]
    ) -> TFileIterator:
        """
        Filter the files by whether their paths match some base path(s).

        See the documentation of matches_base_path for more information.

        :param base_paths: Either a single base path or a list of base paths.
        :return: A file iterator containing the files that match the given base path(s).
        """
        return self.filter(lambda file: matches_base_path(file.path, base_paths))

    include_base_path = filter_base_path
    filter_base = filter_base_path
    include_base = filter_base_path

    def filter_not_base_path(
        self: TFileIterator, base_paths: Union[str, List[str]]
    ) -> TFileIterator:
        """
        Filter the files by whether their paths don't match some base path(s).

        See the documentation of matches_base_path for more information.

        :param base_paths: Either a single base path or a list of base paths.
        :return: A file iterator containing the files that don't match the given base path(s).
        """
        return self.filter(lambda file: not matches_base_path(file.path, base_paths))

    exclude_base_path = filter_not_base_path
    filter_not_base = filter_not_base_path
    exclude_base = filter_not_base_path

    def include_or_exclude_base_path(
        self: TFileIterator, base_paths: Union[str, List[str]], include: bool
    ) -> TFileIterator:
        """
        Include or exclude all files whose paths match some base path(s).

        This is useful e.g. if you have a scenario where you are given a bunch of
        directories along with a flag specifying whether they should be excluded or
        included. Without this function you would potentially have to construct two
        different function chains for each case.

        :param base_paths: Either a single base path or a list of base paths.
        :param include: True, to include the matching files, False to exclude them.
        :return: A file iterator containing the non-excluded files.
        """
        return (
            self.filter_base_path(base_paths)
            if include
            else self.filter_not_base_path(base_paths)
        )

    def filter_glob(
        self: TFileIterator, pattern: Union[str, List[str]]
    ) -> TFileIterator:
        """
        Filter the files by whether their paths match some glob(s).

        See the documentation of matches_glob for more information.

        :param pattern: Either a single glob pattern or a list of glob patterns.
        :return: A file iterator containing the files that match the given glob(s).
        """
        return self.filter(lambda file: matches_glob(file.path, pattern))

    include_glob = filter_glob

    def filter_not_glob(
        self: TFileIterator, pattern: Union[str, List[str]]
    ) -> TFileIterator:
        """
        Filter the files by whether their paths don't match some glob(s).

        See the documentation of matches_glob for more information.

        :param pattern: Either a single glob pattern or a list of glob patterns.
        :return: A file iterator containing the files that don't match the given glob(s).
        """
        return self.filter(lambda file: not matches_glob(file.path, pattern))

    exclude_glob = filter_not_glob

    def include_or_exclude_glob(
        self: TFileIterator, patterns: Union[str, List[str]], include: bool
    ) -> TFileIterator:
        """
        Include or exclude files that match some glob pattern(s).

        :param patterns: Either a single glob pattern or a list of glob patterns.
        :param include: True, to include the matching files, False to exclude them.
        :return: A file iterator containing the non-excluded files.
        """
        return self.filter_glob(patterns) if include else self.filter_not_glob(patterns)

    def filter_name_regex(
        self: TFileIterator, regex: Union[str, List[str]]
    ) -> TFileIterator:
        """
        Filter the files by whether their *names* match some regex(es).

        :param regex: Either a single regular expression or a list of regular expressions.
        :return: A file iterator containing the files whose names match the regex(es).
        """
        compiled_regex = compile_regex(regex)
        return self.filter(
            lambda file: matches_compiled_regex(file.name, compiled_regex)
        )

    include_name_regex = filter_name_regex

    def filter_not_name_regex(
        self: TFileIterator, regex: Union[str, List[str]]
    ) -> TFileIterator:
        """
        Filter the files by whether their *names* don't match some regex(es).

        :param regex: Either a single regular expression or a list of regular expressions.
        :return: A file iterator containing the files whose names don't match the regex(es).
        """
        compiled_regex = compile_regex(regex)
        return self.filter(
            lambda file: not matches_compiled_regex(file.name, compiled_regex)
        )

    exclude_name_regex = filter_not_name_regex

    def filter_path_regex(
        self: TFileIterator, regex: Union[str, List[str]]
    ) -> TFileIterator:
        """
        Filter the files by whether their *paths* match some regex(es).

        :param regex: Either a single regular expression or a list of regular expressions.
        :return: A file iterator containing the files whose paths match the regex(es).
        """
        compiled_regex = compile_regex(regex)
        return self.filter(
            lambda file: matches_compiled_regex(file.path, compiled_regex)
        )

    include_path_regex = filter_path_regex

    def filter_not_path_regex(
        self: TFileIterator, regex: Union[str, List[str]]
    ) -> TFileIterator:
        """
        Filter the files by whether their *paths* don't match some regex(es).

        :param regex: Either a single regular expression or a list of regular expressions.
        :return: A file iterator containing the files whose paths don't match the regex(es).
        """
        compiled_regex = compile_regex(regex)
        return self.filter(
            lambda file: not matches_compiled_regex(file.path, compiled_regex)
        )

    exclude_path_regex = filter_not_path_regex

    def include_or_exclude_path_regex(
        self: TFileIterator, regex: Union[str, List[str]], include: bool
    ) -> TFileIterator:
        """
        Include or exclude all files match one of the given regexes.

        :param regex: Either a single regular expression or a list of regular expressions.
        :param include: True, if regexes should be included, False otherwise.
        :return: A file iterator containing the non-excluded files.
        """
        return (
            self.filter_path_regex(regex)
            if include
            else self.filter_not_path_regex(regex)
        )

    def map_path(self) -> FunctionalIterator[str]:
        """
        Map the files to their paths.

        :return: A functional iterator containing the file path.
        """
        return self.map(lambda file: file.path)

    def map_name(self) -> FunctionalIterator[str]:
        """
        Map the files to their names.

        :return: A functional iterator containing the file name.
        """
        return self.map(lambda file: file.name)

    def map_byte_count(self) -> FunctionalIterator[int]:
        """
        Map the files to their byte counts.

        :return: A functional iterator containing the byte counts.
        """
        return self.map(lambda file: file.byte_count)

    # These attributes are created in the TextFileIterator class
    text_file_iterator: Any
    t: Any
