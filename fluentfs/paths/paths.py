import os
from enum import Enum
from typing import List, Optional

from fluentfs.exceptions.exceptions import FluentFsException


def file_like_exists(path: str) -> bool:
    """
    Check whether a file-like object (i.e. a file, directory or symlink) with the given path exists.

    :param path: The given path.
    :return: True, if a file-like object is present at the given path, False otherwise.
    """
    return os.path.exists(path)


def file_exists(path: str) -> bool:
    """
    Check whether a (regular) file is present at the given path.

    Note that the behaviour of file_exists is different from os.path.isfile since
    file_exists returns False if path represents a symbol link (unlike os.path.isfile
    which will return True in this case).

    :param path: The given path.
    :return: True, if a file is present. False if no file-like object is present at
        the given path at all or if the path represents a directory.
    """
    return os.path.isfile(path) and not os.path.islink(path)


def dir_exists(path: str) -> bool:
    """
    Check whether a directory is present at the given path.

    Note that the behaviour of dir_exists is different from os.path.isdir since
    dir_exists returns False if path represents a symbol link (unlike os.path.isdir
    which will return True in this case).

    :param path: The given path.
    :return: True, if a directory is present. False if no file-like object is present at
        the given path at all or if the path represents a (regular) file.
    """
    return os.path.isdir(path) and not os.path.islink(path)


def symlink_exists(path: str) -> bool:
    """
    Check whether a symbolic link is present at the given path.

    :param path: The given path.
    :return: True, if a symbolic link is present. False if no file-like object is present at
        the given path at all or if the path does not represent a symbolic like (but e.g. a
        (regular) file or a directory instead).
    """
    return os.path.islink(path)


class FileLikeKind(Enum):
    DIR = 0
    FILE = 1
    SYMLINK = 2


def file_like_kind(path: str) -> FileLikeKind:
    """
    Get the kind of file-like object present at the given path.

    If no file-like object is present at the given path, a FluentFsException is raised.

    :param path: The given path.
    :return: FileKind.DIR if a directory is present, FileKind.FILE if a (regular) file
        is present and FileKind.SYMLINK if a symbolic link is present.
    """
    if dir_exists(path):
        return FileLikeKind.DIR
    if file_exists(path):
        return FileLikeKind.FILE
    if symlink_exists(path):
        return FileLikeKind.SYMLINK

    raise FluentFsException(f"no file-like object present at path {path}")


def path_is_absolute(path: str) -> bool:
    """
    Check whether a given path is absolute.

    :param path: The given path.
    :return: True, if the path is absolute, False otherwise.
    """
    return os.path.isabs(path)


def path_is_relative(path: str) -> bool:
    """
    Check whether a given path is relative.

    :param path: The given path.
    :return: True, if the path is relative, False otherwise.
    """
    return not path_is_absolute(path)


def base_name(path: str) -> str:
    """
    Get the base name of a file-like object (i.e. a file or directory).

    Examples:
    * base_name("/home/username/somedir/a.txt") returns "a.txt"
    * base_name("/home/username/somedir/subdir") returns "subdir"

    :param path: The path of the file-like object.
    :return: The base name of the file-like object.
    """
    return os.path.basename(path)


def relative_path(path: str, base_path: Optional[str] = None) -> str:
    """
    Get the path relative to a base path.

    Examples:
    * relative_path("/home/username/somedir/a.txt", "/home/username/somedir") returns "a.txt"
    * relative_path("/home/username/somedir/a.txt", "/home/username") returns "somedir/a.txt"

    :param path: The given path.
    :param base_path: The base path.
    :return: The relative path.
    """
    if base_path is None:
        base_path = current_path()
    return os.path.relpath(path, base_path)


def expand_path(path: str, expand_user: bool = True, expand_vars: bool = True) -> str:
    """
    Maximally expand a path.

    The maximally expanded path is the absolute path corresponding to the given path with:
    * special characters (like ~) expanded
    * environment variables expanded

    :param path: The given path.
    :return: The maximally expanded path.
    """
    if expand_user:
        path = os.path.expanduser(path)
    if expand_vars:
        path = os.path.expandvars(path)
    return os.path.abspath(path)


def expand_paths(
    paths: List[str], expand_user: bool = True, expand_vars: bool = True
) -> List[str]:
    """
    Maximally expand a list of paths.

    See the documentation of expand_path for more information.

    :param paths: The list of paths.
    :return: The maximally expanded paths.
    """
    return [
        expand_path(path, expand_user=expand_user, expand_vars=expand_vars)
        for path in paths
    ]


def current_path() -> str:
    """
    Get the path representing the current working directory.

    :return: The path.
    """
    return os.getcwd()
