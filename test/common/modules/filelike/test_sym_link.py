import os
from test.test_fs_values import (
    A2_SYMLINK_PATH,
    A_SYMLINK_PATH,
    A_TXT_PATH,
    BASE_DIR_PATH,
    BASE_DIR_SYMLINK2_PATH,
    BASE_DIR_SYMLINK_PATH,
    BROKEN_SYMLINK_PATH,
    NO_PATH,
)
from unittest import TestCase

import fluentfs as fs


class SymLinkExceptionTest(TestCase):
    def test_exception(self) -> None:
        self.assertRaises(fs.FluentFsException, fs.SymLink, A_TXT_PATH)


class FileSymLinkTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not os.path.islink(A_SYMLINK_PATH):
            os.symlink(A_TXT_PATH, A_SYMLINK_PATH)
        if not os.path.islink(A2_SYMLINK_PATH):
            os.symlink(A_SYMLINK_PATH, A2_SYMLINK_PATH)

    def test_target(self) -> None:
        target = fs.SymLink(A2_SYMLINK_PATH).target
        self.assertEqual(target.path, A_SYMLINK_PATH)

    def test_final_target(self) -> None:
        final_target = fs.SymLink(A2_SYMLINK_PATH).final_target
        self.assertEqual(final_target.path, A_TXT_PATH)

    def test_repr(self) -> None:
        self.assertEqual(
            repr(fs.SymLink(A_SYMLINK_PATH)), f'SymLink("{A_SYMLINK_PATH}")'
        )

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.islink(A_SYMLINK_PATH):
            os.remove(A_SYMLINK_PATH)
        if os.path.islink(A2_SYMLINK_PATH):
            os.remove(A2_SYMLINK_PATH)


class DirSymLinkTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not os.path.islink(BASE_DIR_SYMLINK_PATH):
            os.symlink(BASE_DIR_PATH, BASE_DIR_SYMLINK_PATH)
        if not os.path.islink(BASE_DIR_SYMLINK2_PATH):
            os.symlink(BASE_DIR_SYMLINK_PATH, BASE_DIR_SYMLINK2_PATH)

    def test_target(self) -> None:
        target = fs.SymLink(BASE_DIR_SYMLINK2_PATH).target
        self.assertEqual(target.path, BASE_DIR_SYMLINK_PATH)

    def test_final_target(self) -> None:
        final_target = fs.SymLink(BASE_DIR_SYMLINK2_PATH).final_target
        self.assertEqual(final_target.path, BASE_DIR_PATH)

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.islink(BASE_DIR_SYMLINK_PATH):
            os.remove(BASE_DIR_SYMLINK_PATH)
        if os.path.islink(BASE_DIR_SYMLINK2_PATH):
            os.remove(BASE_DIR_SYMLINK2_PATH)


class BrokenSymLinkTest(TestCase):
    def test_target(self) -> None:
        if not os.path.islink(BROKEN_SYMLINK_PATH):
            os.symlink(NO_PATH, BROKEN_SYMLINK_PATH)

        sym_link = fs.SymLink(BROKEN_SYMLINK_PATH)
        with self.assertRaises(fs.FluentFsException):
            sym_link.target

        if os.path.islink(BROKEN_SYMLINK_PATH):
            os.remove(BROKEN_SYMLINK_PATH)
