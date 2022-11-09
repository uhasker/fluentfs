import heapq
from collections.abc import Iterator
from functools import reduce
from typing import Any, Callable, Iterable, List, Sequence, TypeVar

from fluentfs.common.table import Table

T = TypeVar("T")
S = TypeVar("S")
TFunctionalIterator = TypeVar("TFunctionalIterator", bound="FunctionalIterator")


class FunctionalIterator(Iterator[T]):
    def __init__(self, iterable: Iterable[T]) -> None:
        super().__init__()
        self.it = iter(iterable)

    def __next__(self) -> T:
        return next(self.it)

    def list(self) -> List[T]:
        return list(self)

    def filter(
        self: TFunctionalIterator, fun: Callable[[T], bool]
    ) -> TFunctionalIterator:
        return type(self)(filter(fun, self))

    def map(self: TFunctionalIterator, fun: Callable[[T], S]) -> TFunctionalIterator:
        return type(self)(map(fun, self))  # type

    def map_not_self(
        self: TFunctionalIterator, fun: Callable[[T], S]
    ) -> "FunctionalIterator":
        return FunctionalIterator(map(fun, self))

    def reduce(self, fun: Callable[[S, T], S], start: S) -> S:
        return reduce(fun, self, start)

    def len(self) -> int:
        return self.reduce(lambda acc, val: acc + 1, 0)

    def for_each(self, fun: Callable[[T], None]) -> None:
        for val in self:
            fun(val)

    def min(self) -> T:
        return min(self)  # type: ignore

    def max(self) -> T:
        return max(self)  # type: ignore

    def sort_asc(
        self: TFunctionalIterator, key: Callable = None
    ) -> TFunctionalIterator:
        if key:
            return type(self)(sorted(self, key=key))  # type: ignore
        else:
            return type(self)(sorted(self))  # type: ignore

    sort = sort_asc

    def sort_desc(
        self: TFunctionalIterator, key: Callable = None
    ) -> TFunctionalIterator:
        if key:
            return type(self)(sorted(self, key=key, reverse=True))  # type: ignore
        else:
            return type(self)(sorted(self, reverse=True))  # type: ignore

    def top_n(self: TFunctionalIterator, n: int) -> TFunctionalIterator:
        return type(self)(heapq.nlargest(n, self))

    def sum(self) -> T:
        return self.reduce(lambda acc, val: acc + val, 0)  # type: ignore

    def table(
        self, col_names: List[str], row_fun: Callable[[T], Sequence[Any]]
    ) -> Table:
        table = Table(cols=col_names)
        rows = self.map(row_fun)
        table.add_rows(rows)  # type: ignore
        return table
