import os
from test.test_fs_values import (
    A_TXT_PATH,
    BAD_F_TXT_PATH,
    BAD_OTHER_DIR_PATH,
    BASE_DIR_PATH,
    D_TXT_PATH,
    SUB_DIR_PATH,
    TEST_DIR_PATH,
)
from unittest import TestCase

import fluentfs as fs


class TestPath(TestCase):
    def test_file_exists_true_is_file(self) -> None:
        self.assertTrue(fs.file_like_exists(A_TXT_PATH))

    def test_file_exists_true_is_dir(self) -> None:
        self.assertTrue(fs.file_like_exists(A_TXT_PATH))

    def test_file_exists_false(self) -> None:
        self.assertFalse(fs.file_like_exists(BAD_F_TXT_PATH))

    def test_regular_file_exists_true(self) -> None:
        self.assertTrue(fs.file_exists(A_TXT_PATH))

    def test_regular_file_exists_false(self) -> None:
        self.assertFalse(fs.file_exists(BAD_F_TXT_PATH))

    def test_regular_file_exists_false_is_dir(self) -> None:
        self.assertFalse(fs.file_exists(SUB_DIR_PATH))

    def test_dir_exists(self) -> None:
        self.assertTrue(fs.dir_exists(SUB_DIR_PATH))

    def test_dir_exist_true(self) -> None:
        self.assertFalse(fs.dir_exists(BAD_OTHER_DIR_PATH))

    def test_dir_exist_false_is_file(self) -> None:
        self.assertFalse(fs.dir_exists(A_TXT_PATH))

    def test_path_is_absolute(self) -> None:
        self.assertTrue(fs.path_is_absolute(A_TXT_PATH))

    def test_path_is_relative(self) -> None:
        self.assertFalse(fs.path_is_relative(A_TXT_PATH))

    def test_file_like_name_file(self) -> None:
        self.assertEqual(fs.base_name(A_TXT_PATH), "a.txt")

    def test_file_like_name_dir(self) -> None:
        self.assertEqual(fs.base_name(SUB_DIR_PATH), "sub_dir")

    def test_relative_path(self) -> None:
        self.assertEqual(fs.relative_path(A_TXT_PATH, BASE_DIR_PATH), "a.txt")

    def test_relative_path2(self) -> None:
        self.assertEqual(fs.relative_path(D_TXT_PATH, SUB_DIR_PATH), "d.txt")

    def test_expand_path(self) -> None:
        normal_path = fs.expand_path("a.txt")
        expected_path = os.path.join(TEST_DIR_PATH, normal_path)
        self.assertEqual(normal_path, expected_path)
