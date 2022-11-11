from unittest import TestCase

import fluentfs as fs


class TestTable(TestCase):
    def setUp(self) -> None:
        self.table = fs.Table(cols=["Col1", "Col2", "Col3"])
        self.table.add_row({"Col1": "A", "Col2": "B", "Col3": "C"})
        self.table.add_row({"Col1": "D", "Col2": "E", "Col3": "F"})

    def test_dict_table(self) -> None:
        table = fs.Table(
            cols={"Col1": ["A", "D"], "Col2": ["B", "E"], "Col3": ["C", "F"]}
        )
        self.assertEqual(table, self.table)

    def test_table_exception(self) -> None:
        self.assertRaises(fs.FluentFsException, fs.Table, 1)

    def test_table_zero_cols_exception(self) -> None:
        self.assertRaises(fs.FluentFsException, fs.Table, [])

    def test_col_name(self) -> None:
        self.assertEqual(self.table.col_name(1), "Col2")

    def test_col_names(self) -> None:
        self.assertEqual(self.table.col_names, ["Col1", "Col2", "Col3"])

    def test_col(self) -> None:
        self.assertEqual(self.table.col("Col3"), ["C", "F"])

    def test_col2(self) -> None:
        self.assertEqual(self.table.col(2), ["C", "F"])

    def test_col_exception(self) -> None:
        self.assertRaises(fs.FluentFsException, self.table.col, [0, 1])

    def test_col_by_name(self) -> None:
        self.assertEqual(self.table.col("Col1"), ["A", "D"])

    def test_value(self) -> None:
        self.assertEqual(self.table.value(1, 2), "F")

    def test_value_by_name(self) -> None:
        self.assertEqual(self.table.value(1, "Col3"), "F")

    def test_row(self) -> None:
        self.assertEqual(self.table.row(1), ["D", "E", "F"])

    def test_row_dict(self) -> None:
        self.assertEqual(
            self.table.row(0, return_mapping=True),
            {"Col1": "A", "Col2": "B", "Col3": "C"},
        )

    def test_n_rows(self) -> None:
        self.assertEqual(self.table.n_rows, 2)

    def test_n_cols(self) -> None:
        self.assertEqual(self.table.n_cols, 3)

    def test_add_row_wrong_len_exception(self) -> None:
        self.assertRaises(fs.FluentFsException, self.table.add_row, ["G", "H"])

    def test_add_row_wrong_type_exception(self) -> None:
        self.assertRaises(fs.FluentFsException, self.table.add_row, 3)

    def test_add_row_keys_diff_exception(self) -> None:
        self.assertRaises(fs.FluentFsException, self.table.add_row, {"Col1": "G"})

    def test_add_row_list(self) -> None:
        self.table.add_row(["G", "H", "I"])
        self.assertEqual(self.table.row(2), ["G", "H", "I"])

    def test_add_row_dict(self) -> None:
        self.table.add_row({"Col1": "G", "Col2": "H", "Col3": "I"})
        self.assertEqual(self.table.row(2), ["G", "H", "I"])

    def test_add_rows(self) -> None:
        self.table.add_rows(
            [
                {"Col1": "G", "Col2": "H", "Col3": "I"},
                {"Col1": "J", "Col2": "K", "Col3": "L"},
            ]
        )
        self.assertEqual(self.table.row(3), ["J", "K", "L"])

    def test_add_row_dict_other_order(self) -> None:
        self.table.add_row({"Col2": "H", "Col3": "I", "Col1": "G"})
        self.assertEqual(self.table.row(2), ["G", "H", "I"])

    def test_getitem(self) -> None:
        self.assertEqual(self.table[1], {"Col1": "D", "Col2": "E", "Col3": "F"})

    def test_len(self) -> None:
        self.assertEqual(len(self.table), 2)

    def test_str(self) -> None:
        self.assertEqual(
            str(self.table),
            "| Col1  | Col2  | Col3 |\n"
            "| _____ | _____ | _____|\n"
            "| A     | B     | C    |\n"
            "| _____ | _____ | _____|\n"
            "| D     | E     | F    |",
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(self.table),
            "| Col1  | Col2  | Col3 |\n"
            "| _____ | _____ | _____|\n"
            "| A     | B     | C    |\n"
            "| _____ | _____ | _____|\n"
            "| D     | E     | F    |",
        )

    def test_table_from_rows(self) -> None:
        table = fs.Table(
            cols={"Col1": ["A", "D"], "Col2": ["B", "E"], "Col3": ["C", "F"]}
        )
        self.assertEqual(
            str(table),
            "| Col1  | Col2  | Col3 |\n"
            "| _____ | _____ | _____|\n"
            "| A     | B     | C    |\n"
            "| _____ | _____ | _____|\n"
            "| D     | E     | F    |",
        )
