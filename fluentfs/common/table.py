from collections.abc import Mapping, Sequence
from typing import Any, Dict, Iterable, List, Union, cast

from fluentfs.exceptions.exceptions import FluentFsException


class Table:
    def __init__(self, cols: Union[Sequence[str], Mapping[str, Sequence[Any]]]) -> None:
        """
        Initialize an empty table with the given column names.

        :param cols: A sequence of column names. Each column name should be a string.
            Note that the order of the column names matters since columns can be accessed
            by index.
        """
        if not cols:
            raise FluentFsException("table must have at least one column")

        if isinstance(cols, Sequence):
            self._cols: Dict[str, List[str]] = {col_name: [] for col_name in cols}
        elif isinstance(cols, Mapping):
            self._cols = {col_name: list(col) for col_name, col in cols.items()}
        else:
            raise FluentFsException(
                "cols must be a sequence or a mapping, received "
                f"a {type(cols)} instead"
            )

    def col_name(self, idx: int) -> str:
        """
        Get the name of a column from its index.

        >>> table = Table({
        ...     "Country": ["Germany", "France"],
        ...     "Capital": ["Berlin", "Paris"],
        ...     "Language": ["German", "French"]
        ... })
        >>> table.col_name(0)
        'Country'
        >>> table.col_name(1)
        'Capital'
        >>> table.col_name(2)
        'Language'

        :param idx: The column index.
        :return: The column name.
        """
        return self.col_names[idx]

    @property
    def col_names(self) -> List[str]:
        """Dict[str, str]
        The names of the table columns.

        Note that the names are returned in the order of the columns.

        >>> table = Table({
        ...     "Country": ["Germany", "France"],
        ...     "Capital": ["Berlin", "Paris"],
        ...     "Language": ["German", "French"]
        ... })
        >>> table.col_names
        ['Country', 'Capital', 'Language']
        """
        return list(self._cols.keys())

    def col(self, col_id: Union[str, int]) -> List[Any]:
        """
        Get (the values of) a column by its name or index.

        >>> table = Table({
        ...     "Country": ["Germany", "France"],
        ...     "Capital": ["Berlin", "Paris"],
        ...     "Language": ["German", "French"]
        ... })
        >>> table.col(0)
        ['Germany', 'France']
        >>> table.col("Country")
        ['Germany', 'France']
        >>> table.col(1)
        ['Berlin', 'Paris']
        >>> table.col("Capital")
        ['Berlin', 'Paris']
        >>> table.col(2)
        ['German', 'French']
        >>> table.col("Language")
        ['German', 'French']

        :param col_id: The column identifier. If this is a string, then col_id is assumed
            to be the name of the column. If this is an integer, then col_id is assumed
            to be the index of the column.
        :return: A list containing the values of the column.
        """
        if isinstance(col_id, str):
            return self._cols[col_id]
        elif isinstance(col_id, int):
            return self._cols[self.col_name(col_id)]
        else:
            raise FluentFsException(
                f"col_id must be str or int, received " f"{type(col_id)} instead"
            )

    def value(self, row_idx: int, col_id: Union[str, int]) -> Any:
        """
        Get a value from the table by row and column.

        >>> table = Table({
        ...     "Country": ["Germany", "France"],
        ...     "Capital": ["Berlin", "Paris"],
        ...     "Language": ["German", "French"]
        ... })
        >>> table.value(row_idx=1, col_id=2)
        'French'
        >>> table.value(row_idx=1, col_id="Language")
        'French'

        :param row_idx: The index of the row.
        :param col_id: The column identifier. If this is a string, then col_id is assumed
            to be the name of the column. If this is an integer, then col_id is assumed
            to be the index of the column.
        :return: The value residing at row with index row_idx and column with
            identifier col_id.
        """
        return self.col(col_id)[row_idx]

    def row(
        self, idx: int, return_mapping: bool = False
    ) -> Union[List[str], Dict[str, Any]]:
        """
        Get a row.

        Note that values of the row will be ordered according to the order of the columns.

        >>> table = Table({
        ...     "Country": ["Germany", "France"],
        ...     "Capital": ["Berlin", "Paris"],
        ...     "Language": ["German", "French"]
        ... })
        >>> table.row(idx=0)
        ['Germany', 'Berlin', 'German']
        >>> table.row(idx=1)
        ['France', 'Paris', 'French']
        >>> table.row(idx=0, return_mapping=True)
        {'Country': 'Germany', 'Capital': 'Berlin', 'Language': 'German'}
        >>> table.row(idx=1, return_mapping=True)
        {'Country': 'France', 'Capital': 'Paris', 'Language': 'French'}

        :param idx: The row index.
        :param return_mapping: If this is True, return a list of row values. If this is
            False, return a dictionary mapping column values to row values. Note that the
            dictionary is ordered according to the order of the columns.
        :return: A list containing the row values.
        """
        row_dict = {col_name: self.value(idx, col_name) for col_name in self.col_names}

        return row_dict if return_mapping else list(row_dict.values())

    @property
    def n_rows(self) -> int:
        """
        The number of rows.

        >>> table = Table({
        ...     "Country": ["Germany", "France"],
        ...     "Capital": ["Berlin", "Paris"],
        ...     "Language": ["German", "French"]
        ... })
        >>> table.n_rows
        2
        """
        assert self.n_cols != 0

        first_col = self.col(0)
        return len(first_col)

    @property
    def n_cols(self) -> int:
        """
        The number of columns.

        >>> table = Table({
        ...     "Country": ["Germany", "France"],
        ...     "Capital": ["Berlin", "Paris"],
        ...     "Language": ["German", "French"]
        ... })
        >>> table.n_cols
        3
        """
        return len(self.col_names)

    def add_row(self, row: Union[Mapping[str, Any], Sequence[Any]]) -> None:
        """
        Add a row to the table.

        >>> table = Table(["Country", "Capital", "Language"])
        >>> table.add_row(["Germany", "Berlin", "German"])
        >>> table.add_row({"Language": "French", "Capital": "Paris", "Country": "France"})
        >>> table
        | Country  | Capital  | Language |
        | ________ | ________ | _________|
        | Germany  | Berlin   | German   |
        | ________ | ________ | _________|
        | France   | Paris    | French   |

        :param row: The row. It must be either a sequence of values or a mapping
            of column names to values. If the row is a sequence of values, each value
            will be inserted into the column with the corresponding index.
        """
        if isinstance(row, Sequence):
            if len(row) != self.n_cols:
                raise FluentFsException(
                    "the number of row values must be equal to the number of columns"
                )

            row_dict = {
                col_name: row[row_idx]
                for row_idx, col_name in enumerate(self.col_names)
            }
        elif isinstance(row, Mapping):
            row_dict = dict(row)
        else:
            raise FluentFsException(
                f"row must be either a dictionary or a list, but was {type(row)} instead"
            )

        cols_diff = row_dict.keys() ^ self._cols.keys()
        if len(cols_diff) != 0:
            raise FluentFsException(
                f"the row keys must be equal to the column names, "
                f"but the following keys differed: {cols_diff!r}"
            )

        for k, v in row_dict.items():
            self._cols[k].append(v)

    def add_rows(
        self, rows: Union[Iterable[Mapping[str, Any]], Iterable[Sequence[Any]]]
    ) -> None:
        for row in rows:
            self.add_row(row)

    def __getitem__(self, i: int) -> Dict[str, Any]:
        row = self.row(i, return_mapping=True)
        return cast(Dict[str, str], row)

    def __len__(self) -> int:
        return self.n_rows

    def __header(self, col_ljust_vals: Dict[str, int]) -> str:
        justified_col_names = [
            col_name.ljust(col_ljust_vals[col_name]) for col_name in self.col_names
        ]
        return " | ".join(justified_col_names)

    def __sep_str(self, col_ljust_vals: Dict[str, int], row_idx: int) -> str:
        separators = [
            "_" * col_ljust_vals[col_name] for col_name, _ in self[row_idx].items()
        ]
        return " | ".join(separators)

    def __col_str(self, col_ljust_vals: Dict[str, int], row_idx: int) -> str:
        justified_cols = [
            str(col).ljust(col_ljust_vals[col_name])
            for col_name, col in self[row_idx].items()
        ]
        return " | ".join(justified_cols)

    def __repr__(self) -> str:
        col_ljust_vals = {}
        for col_name, col in self._cols.items():
            cols_str = [str(val) for val in self.col(col_name)] + [col_name]
            col_ljust_vals[col_name] = len(max(cols_str, key=len)) + 1

        s = "| " + self.__header(col_ljust_vals) + "|\n"
        for row_idx in range(len(self)):
            s += "| " + self.__sep_str(col_ljust_vals, row_idx) + "|\n"
            s += "| " + self.__col_str(col_ljust_vals, row_idx) + "|\n"
        return s[:-1]  # remove last newline

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Table):  # pragma: no cover
            return False  # pragma: no cover
        return self._cols == other._cols


if __name__ == "__main__":  # pragma: no cover
    import doctest  # pragma: no cover

    doctest.testmod()  # pragma: no cover
