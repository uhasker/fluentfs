from abc import ABC, abstractmethod
from typing import Any

from fluentfs.paths.paths import base_name, expand_path, relative_path


class FileLike(ABC):
    def __init__(
        self, path: str, expand_user: bool = True, expand_vars: bool = True
    ) -> None:
        self._path = path

        self.expand_user = expand_user
        self.expand_vars = expand_vars

    @property
    def path(self) -> str:
        """
        The maximally expanded path of the file-like object.
        """
        return expand_path(
            self._path, expand_user=self.expand_user, expand_vars=self.expand_vars
        )

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
