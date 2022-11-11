from unittest import TestCase

import fluentfs as fs


class TestFunctional(TestCase):
    def test_list(self) -> None:
        result = fs.FunctionalIterator([1, 2, 3, 4]).list()
        self.assertEqual(result, [1, 2, 3, 4])

    def test_filter(self) -> None:
        result = fs.FunctionalIterator([1, 2, 3, 4]).filter(lambda x: x % 2 == 0).list()
        self.assertEqual(result, [2, 4])

    def test_map(self) -> None:
        result = fs.FunctionalIterator([1, 2, 3, 4]).map_self(lambda x: x * 2).list()
        self.assertEqual(result, [2, 4, 6, 8])

    def test_reduce(self) -> None:
        result = fs.FunctionalIterator([1, 2, 3, 4]).reduce(lambda x, y: x + y, 0)
        self.assertEqual(result, 10)

    def test_len(self) -> None:
        result = fs.FunctionalIterator([1, 2, 3, 4]).len()
        self.assertEqual(result, 4)

    def test_sum(self) -> None:
        result = fs.FunctionalIterator([1, 2, 3, 4]).sum()
        self.assertEqual(result, 10)

    def test_min(self) -> None:
        result = fs.FunctionalIterator([2, 1, 4, 3]).max()
        self.assertEqual(result, 4)

    def test_max(self) -> None:
        result = fs.FunctionalIterator([2, 1, 4, 3]).min()
        self.assertEqual(result, 1)

    def test_sort_asc(self) -> None:
        result = fs.FunctionalIterator([2, 1, 4, 3]).sort_asc().list()
        self.assertEqual(result, [1, 2, 3, 4])

    def test_sort_asc_key(self) -> None:
        result = (
            fs.FunctionalIterator(["ab", "a", "abcd", "abc"])
            .sort_asc(key=lambda s: len(s))
            .list()
        )
        self.assertEqual(result, ["a", "ab", "abc", "abcd"])

    def test_sort(self) -> None:
        result = fs.FunctionalIterator([2, 1, 4, 3]).sort().list()
        self.assertEqual(result, [1, 2, 3, 4])

    def test_sort_desc(self) -> None:
        result = fs.FunctionalIterator([2, 1, 4, 3]).sort_desc().list()
        self.assertEqual(result, [4, 3, 2, 1])

    def test_sort_desc_key(self) -> None:
        result = (
            fs.FunctionalIterator(["ab", "a", "abcd", "abc"])
            .sort_desc(key=lambda s: len(s))
            .list()
        )
        self.assertEqual(result, ["abcd", "abc", "ab", "a"])

    def test_top_0(self) -> None:
        result = fs.FunctionalIterator([2, 1, 4, 3]).top_n(0).list()
        self.assertEqual(result, [])

    def test_top_n(self) -> None:
        result = fs.FunctionalIterator([2, 1, 4, 3]).top_n(2).list()
        self.assertEqual(result, [4, 3])

    def test_for_each(self) -> None:
        values = []
        fs.FunctionalIterator([2, 1, 4, 3]).for_each(lambda x: values.append(x * 2))
        self.assertEqual(values, [4, 2, 8, 6])

    def test_table(self) -> None:
        table = fs.FunctionalIterator([1, 2, 3, 4]).table(
            col_names=["val", "sq", "cube"], row_fun=lambda v: (v, v**2, v**3)
        )
        self.assertEqual(
            table,
            fs.Table(
                cols={"val": [1, 2, 3, 4], "sq": [1, 4, 9, 16], "cube": [1, 8, 27, 64]}
            ),
        )
