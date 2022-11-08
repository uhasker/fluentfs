from abc import ABC, abstractmethod
from typing import Any

from fluentfs.paths.paths import base_name, expand_path, relative_path


class FileLike(ABC):
    def __init__(self, path: str) -> None:
        self._path = path

    @property
    def path(self) -> str:
        return expand_path(self._path)

    @property
    def relative_path(self) -> str:
        return relative_path(self.path)

    relpath = relative_path

    @property
    def name(self) -> str:
        return base_name(self.path)

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError  # pragma: no cover

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FileLike):
            return False
        return self.path == other.path
