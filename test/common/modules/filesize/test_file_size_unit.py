from unittest import TestCase

import fluentfs as fs
from fluentfs import FileSizeUnit


class FileSizeUnitTest(TestCase):
    def test_exception(self) -> None:
        self.assertRaises(fs.FluentFsException, repr, fs.FileSizeUnit.AUTO)

    def test_file_size_unit(self) -> None:
        self.assertEqual(str(FileSizeUnit.KB), "KB")
