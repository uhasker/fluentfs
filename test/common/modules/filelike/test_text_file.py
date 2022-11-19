import os.path
from test.test_fs_values import (
    A_TXT_PATH,
    B_TXT_PATH,
    BAD_ENCODING_PATH,
    EMPTY_TXT_PATH,
    EMPTYLINES_TXT_PATH,
)
from unittest import TestCase

import fluentfs as fs


class TextFileContentTest(TestCase):
    def test_content_empty(self) -> None:
        self.assertEqual(fs.TextFile(EMPTY_TXT_PATH).content, "")

    def test_content(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).content, "line 2\nline 3")

    def test_content_bad_encoding_raise(self) -> None:
        if not os.path.exists(BAD_ENCODING_PATH):
            with open(BAD_ENCODING_PATH, "w", encoding="cp1252") as f:
                f.write("äöu")

        with self.assertRaises(fs.FluentFsException):
            fs.TextFile(BAD_ENCODING_PATH).content

        os.remove(BAD_ENCODING_PATH)

    def test_content_bad_encoding_no_raise(self) -> None:
        if not os.path.exists(BAD_ENCODING_PATH):
            with open(BAD_ENCODING_PATH, "w", encoding="cp1252") as f:
                f.write("äöu")

        self.assertEqual(
            fs.TextFile(BAD_ENCODING_PATH, raise_on_decode_error=False).content, ""
        )

        os.remove(BAD_ENCODING_PATH)


class TextFileLinesTest(TestCase):
    def test_lines_empty(self) -> None:
        self.assertEqual(fs.TextFile(EMPTY_TXT_PATH).lines.list(), [])

    def test_lines(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).lines.list(), ["line 2", "line 3"])

    def test_line_lens_empty(self) -> None:
        self.assertEqual(fs.TextFile(EMPTY_TXT_PATH).line_lens.list(), [])

    def test_line_lens(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).line_lens.list(), [6, 6])

    def test_max_line_len(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).max_line_len, 6)

    def test_empty_lines(self) -> None:
        self.assertEqual(fs.TextFile(EMPTYLINES_TXT_PATH).empty_lines.list(), ["", ""])

    def test_empty_line_count(self) -> None:
        self.assertEqual(fs.TextFile(EMPTYLINES_TXT_PATH).empty_line_count, 2)

    def test_non_empty_lines(self) -> None:
        self.assertEqual(
            fs.TextFile(EMPTYLINES_TXT_PATH).non_empty_lines.list(),
            ["line 1", "line 3", "line 5"],
        )

    def test_non_empty_line_count(self) -> None:
        self.assertEqual(fs.TextFile(EMPTYLINES_TXT_PATH).non_empty_line_count, 3)

    def test_lines_bad_encoding_raise(self) -> None:
        if not os.path.exists(BAD_ENCODING_PATH):
            with open(BAD_ENCODING_PATH, "w", encoding="cp1252") as f:
                f.write("äöu")

        with self.assertRaises(fs.FluentFsException):
            fs.TextFile(BAD_ENCODING_PATH).lines

        os.remove(BAD_ENCODING_PATH)

    def test_lines_bad_encoding_no_raise(self) -> None:
        if not os.path.exists(BAD_ENCODING_PATH):
            with open(BAD_ENCODING_PATH, "w", encoding="cp1252") as f:
                f.write("äöu")

        self.assertEqual(
            fs.TextFile(BAD_ENCODING_PATH, raise_on_decode_error=False).lines.list(), []
        )

        os.remove(BAD_ENCODING_PATH)


class TextFileWordsTest(TestCase):
    def test_words_empty(self) -> None:
        self.assertEqual(fs.TextFile(EMPTY_TXT_PATH).words.list(), [])

    def test_words(self) -> None:
        self.assertEqual(
            fs.TextFile(B_TXT_PATH).words.list(), ["line", "2", "line", "3"]
        )


class TextFileCharCountTest(TestCase):
    def test_char_count_empty(self) -> None:
        self.assertEqual(fs.TextFile(EMPTY_TXT_PATH).char_count, 0)

    def test_char_count(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).char_count, 13)

    def test_cc(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).cc, 13)


class TextFileWordCountTest(TestCase):
    def test_word_count_empty(self) -> None:
        self.assertEqual(fs.TextFile(EMPTY_TXT_PATH).word_count, 0)

    def test_word_count(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).word_count, 4)

    def test_wc(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).wc, 4)


class TextFileLineCountTest(TestCase):
    def test_line_count_empty(self) -> None:
        self.assertEqual(fs.TextFile(EMPTY_TXT_PATH).line_count, 0)

    def test_line_count(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).line_count, 2)

    def test_lc(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).lc, 2)


class TextFileStrTest(TestCase):
    def test_str(self) -> None:
        self.assertEqual(str(fs.TextFile(A_TXT_PATH)), f"TextFile({A_TXT_PATH})")

    def test_repr(self) -> None:
        self.assertEqual(repr(fs.TextFile(A_TXT_PATH)), f"TextFile({A_TXT_PATH})")
