import fnmatch
import os
import re
from typing import List, Union

from fluentfs.common import compile_regex
from fluentfs.paths.paths import expand_path, expand_paths


def matches_base_path(path: str, base_paths: Union[str, List[str]]) -> bool:
    """
    Check whether a path matches one of the given base paths.

    A path matches a given base path if the maximally expanded version of the base path
    is a parent of the maximally expanded version of the path.

    For example if path="/home/username/somedir" and base_path="/home/username"
    then this function returns True because "/home/username" is a parent of
    "/home/username/somedir".

    The maximal expansion of the paths are needed to make this function work with relative
    paths and/or paths that contain ~ and/or environment variables.

    For example assume that ~ points to "/home/username" and there is a "somedir"
    directory inside "/home/username". Then if you call this function with
    path="somedir" and base_path="~" it will return True since "somedir" will be
    maximally expanded to "/home/username/somedir" and "~" will be maximally expanded
    to "/home/username".

    More examples with absolute paths:

    * matches_base_path("/home/username/somedir", "/home/username") returns True
    * matches_base_path("/home/username/somedir", "/home") returns True
    * matches_base_path("/home/username/somedir", "/") returns True
    * matches_base_path("/home/username/somedir", "/home/username/otherdir") returns False

    More examples with relative paths (assuming you are in the "/home/username" directory,
    there is a "/home/username/somedir" directory and ~ points to "/home/username"):

    * matches_base_path("somedir", "/home/username") returns True
    * matches_base_path("somedir", "~") returns True
    * matches_base_path(".", "~") returns True
    * matches_base_path("somedir", "otherdir") returns False

    :param path: The given path.
    :param base_paths: Either a single base path or a list of base paths.
    :return: True, if the path matches one of the base paths, False otherwise.
    """
    if isinstance(base_paths, str):
        base_paths = [base_paths]

    path = expand_path(path)
    base_paths = expand_paths(base_paths)

    for base_path in base_paths:
        if os.path.commonpath([path, base_path]) == base_path:
            return True
    return False


def matches_glob(path: str, patterns: Union[str, List[str]]) -> bool:
    """
    Check whether a path matches some glob pattern(s).

    Note that path is *NOT* maximally expanded to accommodate intuitive globbing
    of relative paths.

    :param path: The given path.
    :param patterns: Either a single glob pattern or a list of glob patterns.
    :return: True, if the path matches one of the glob patterns, False otherwise.
    """
    if isinstance(patterns, str):
        patterns = [patterns]

    for pattern in patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False


def matches_regex(path: str, regex: Union[str, List[str]]) -> bool:
    """
    Check whether a path matches one of the given regular expressions.

    :param path: The given path.
    :param regex: Either a single regular expression or a list of regular expressions.
    :return: True, if the path matches one of the regular expressions, False otherwise.
    """
    return matches_compiled_regex(path, compile_regex(regex))


def matches_compiled_regex(
    path: str, compiled_regexes: Union[re.Pattern, List[re.Pattern]]
) -> bool:
    """
    Check whether a path matches one of the given compiled regular expressions.

    :param path: The given path.
    :param compiled_regexes: Either a single compiled regular expression or a list
        of compiled regular expressions.
    :return: True, if the path matches one of the compiled regular expressions,
        False otherwise.
    """
    if isinstance(compiled_regexes, re.Pattern):
        compiled_regexes = [compiled_regexes]

    for compiled_regex in compiled_regexes:
        if compiled_regex.fullmatch(path):
            return True
    return False
