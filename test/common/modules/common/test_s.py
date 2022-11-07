from unittest import TestCase

from fluentfs.common import chomp


class TestS(TestCase):
    def test_chomp1(self) -> None:
        self.assertEqual(chomp("test\n"), "test")

    def test_chomp2(self) -> None:
        self.assertEqual(chomp("test\r\n"), "test")

    def test_chomp3(self) -> None:
        self.assertEqual(chomp("test"), "test")

    def test_chomp4(self) -> None:
        self.assertEqual(chomp("test\n\n"), "test\n")
