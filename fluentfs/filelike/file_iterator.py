from typing import Any, List, TypeVar, Union

from fluentfs.common import compile_regex
from fluentfs.common.functional import FunctionalIterator
from fluentfs.filelike.file import File
from fluentfs.paths.matches import (
    matches_base_path,
    matches_compiled_regex,
    matches_glob,
)

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
