import re
from test.test_fs_values import A_TXT_PATH, BASE_DIR_PATH, SUB_DIR_PATH
from unittest import TestCase

import fluentfs.paths.matches


class TestMatches(TestCase):
    def test_path_matches_base_str(self) -> None:
        self.assertTrue(
            fluentfs.paths.matches.matches_base_path(SUB_DIR_PATH, BASE_DIR_PATH)
        )

    def test_path_matches_base(self) -> None:
        self.assertTrue(
            fluentfs.paths.matches.matches_base_path(SUB_DIR_PATH, [BASE_DIR_PATH])
        )

    def test_path_matches_regex_str(self) -> None:
        self.assertTrue(fluentfs.paths.matches.matches_regex(A_TXT_PATH, r".*a\.txt"))

    def test_path_matches_regex(self) -> None:
        self.assertTrue(fluentfs.paths.matches.matches_regex(A_TXT_PATH, [r".*a\.txt"]))

    def test_path_matches_compiled_regex_pattern(self) -> None:
        self.assertTrue(
            fluentfs.paths.matches.matches_compiled_regex(
                A_TXT_PATH, re.compile(r".*a\.txt")
            )
        )

    def test_path_matches_compiled_regex(self) -> None:
        self.assertTrue(
            fluentfs.paths.matches.matches_compiled_regex(
                A_TXT_PATH, [re.compile(r".*a\.txt")]
            )
        )

    def test_path_matches_glob_pattern(self) -> None:
        self.assertTrue(fluentfs.paths.matches.matches_glob(A_TXT_PATH, "*/a.txt"))

    def test_path_matches_glob(self) -> None:
        self.assertTrue(fluentfs.paths.matches.matches_glob(A_TXT_PATH, ["*/a.txt"]))
