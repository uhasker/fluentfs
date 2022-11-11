from test.test_fs_values import BASE_DIR_PATH
from unittest import TestCase

import fluentfs as fs


class TestReadme(TestCase):
    def test_readme_short_example(self) -> None:
        total_size = fs.Dir(BASE_DIR_PATH).files.filter_ext("txt").t().map_lc().sum()
        self.assertEqual(total_size, 15)

    def test_readme_long_example(self) -> None:
        total_size = (
            fs.Dir(BASE_DIR_PATH)
            .files.filter_extension("txt")
            .text_file_iterator()
            .map_line_count()
            .sum()
        )
        self.assertEqual(total_size, 15)

    def test_readme_explicit_long_example(self) -> None:
        total_size = (
            fs.Dir(BASE_DIR_PATH)
            .files.filter(lambda f: f.extension == "txt")
            .text_file_iterator()
            .map_self(lambda f: f.line_count)
            .reduce(lambda x, y: x + y, 0)
        )
        self.assertEqual(total_size, 15)
