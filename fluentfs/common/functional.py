import heapq
from collections.abc import Iterator
from functools import reduce
from typing import Callable, Iterable, List, TypeVar

T = TypeVar("T")
S = TypeVar("S")


class FunctionalIterator(Iterator[T]):
    def __init__(self, iterable: Iterable[T]) -> None:
        super().__init__()
        self.it = iter(iterable)

    def __next__(self) -> T:
        return next(self.it)

    def list(self) -> List[T]:
        return list(self)

    def filter(self, fun: Callable[[T], bool]) -> "FunctionalIterator[T]":
        return FunctionalIterator(filter(fun, self))

    def map(self, fun: Callable[[T], S]) -> "FunctionalIterator[S]":
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

    def sort_asc(self) -> List[T]:
        return sorted(self)  # type: ignore

    sort = sort_asc

    def sort_desc(self) -> List[T]:
        return sorted(self, reverse=True)  # type: ignore

    def top_n(self, n: int) -> List[T]:
        return heapq.nlargest(n, self)

    def sum(self) -> T:
        return self.reduce(lambda acc, val: acc + val, 0)  # type: ignore
